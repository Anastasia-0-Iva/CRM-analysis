from datetime import datetime, timedelta
import requests
from config.main_config import API_KEY, GET_CHANGE_URL
from utils.get_signatures_for_api import get_signature
import get_users

driver_ids = get_users.get_parking_drivers_with_fio()
print("Всего водителей:", len(driver_ids))

sample = driver_ids
results = {}

for driver_id, fio, phone, branch, created_at in sample:
    date_end = "2025-10-01"
    date_start = "2025-09-01"

    body = {
        "timestamp": int(datetime.now().timestamp()),
        "filters": {
            "users_id": [driver_id],
            "date_start": date_start,
            "date_end": date_end
        }
    }
    signature = get_signature(body, API_KEY)

    try:
        resp = requests.post(
            GET_CHANGE_URL,
            headers={"Authorization": signature},
            json=body,
            timeout=30
        )

        if resp.status_code == 200:
            data = resp.json()

            shifts_raw = data.get("shifts_list") or data.get("data") or []

            if isinstance(shifts_raw, dict):
                shifts_all = list(shifts_raw.values())
            else:
                shifts_all = shifts_raw if isinstance(shifts_raw, list) else []

            shifts = [s for s in shifts_all if str(s.get("user_id")) == str(driver_id)]

            first_shift_date = None
            last_shift_date = None
            otk_msg = "Нет оттока"

            if shifts:
                sorted_shifts = sorted(shifts, key=lambda x: x.get("start", ""))
                first_shift_date = sorted_shifts[0].get("start")
                last_shift_date = sorted_shifts[-1].get("start")

                if last_shift_date:
                    last_dt = datetime.strptime(last_shift_date, "%Y-%m-%d %H:%M:%S")
                    otk_msg = "Отток" if last_dt >= datetime.now() - timedelta(days=14) else "Нет оттока"

            results[driver_id] = {
                "first_shift_date": first_shift_date,
                "total_shifts": len(shifts),
                "last_shift_date": last_shift_date,
                "отток": otk_msg
            }

            print(f"Водитель {fio}: {len(shifts)} смен, "
                  f"первая: {first_shift_date}, последняя: {last_shift_date} -> {otk_msg}")

    except Exception as e:
        print(f"Ошибка для водителя {fio}: {e}")
