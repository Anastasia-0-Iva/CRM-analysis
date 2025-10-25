from datetime import datetime, timedelta, date
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd
from tqdm import tqdm
from config.main_config import API_KEY, GET_USER_URL, GET_CHANGE_URL
from utils.get_signatures_for_api import get_signature


#Список водителей (из API)
def get_parking_drivers_with_fio():
    payload = {'timestamp': int(datetime.now().timestamp())}
    signature = get_signature(payload, API_KEY)

    try:
        resp = requests.post(GET_USER_URL, json=payload,
                             headers={'Authorization': signature}, timeout=120)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Ошибка получения пользователей:", e)
        return []

    if not data.get('success'):
        print("API ошибка:", data.get('error'))
        return []

    users_list = data.get('users_list', {})
    result = []
    for uid, u in users_list.items():
        if u.get('user_role_name') != 'Водители Парковые':
            continue
        try:
            created_dt = datetime.fromisoformat(u['created_at'][:10]).date()
        except Exception:
            continue
        if not (date(2025, 9, 1) <= created_dt <= date(2025, 10, 1)):
            continue

        last, first, mid = (u.get('last_name', ''), u.get('first_name', ''), u.get('middle_name', ''))
        fio = ' '.join(filter(None, [last, first, mid])) or 'Без имени'
        phone = u.get('phone', '')
        #АТП из API
        atp = u.get('branch', 'Нет АТП')
        result.append((uid, fio, phone, atp, u['created_at']))
    return result


#Смены за период для одного водителя
def get_shifts_period(driver_id: str):
    body = {
        "timestamp": int(datetime.now().timestamp()),
        "filters": {
            "users_id": [driver_id],
            "date_start": "2025-09-01",
            "date_end": "2025-10-01"
        }
    }
    signature = get_signature(body, API_KEY)

    try:
        resp = requests.post(GET_CHANGE_URL, json=body,
                             headers={"Authorization": signature}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return [], None, None

    if not data.get('success'):
        return [], None, None

    shifts_raw = data.get("shifts_list") or data.get("data") or []
    if isinstance(shifts_raw, dict):
        shifts_all = list(shifts_raw.values())
    else:
        shifts_all = shifts_raw if isinstance(shifts_raw, list) else []

    shifts = [s for s in shifts_all if str(s.get("user_id")) == str(driver_id)]
    if not shifts:
        return [], None, None

    sorted_shifts = sorted(shifts, key=lambda x: x.get("start", ""))
    return (shifts,
            sorted_shifts[0].get("start"),
            sorted_shifts[-1].get("start"))


#Параллельный обход
drivers = get_parking_drivers_with_fio()
print("Всего водителей:", len(drivers))

def process_one(driver_tuple):
    uid, fio, phone, atp, created_at = driver_tuple
    shifts, first, last = get_shifts_period(uid)
    total = len(shifts)

    otkok = "Нет оттока"
    if last:
        last_dt = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        if last_dt < datetime.now() - timedelta(days=14):
            otkok = "Отток"

    return {
        "ФИО": fio,
        "Телефон": phone,
        "АТП": atp,
        "Дата регистрации": created_at,
        "Первая смена": first,
        "Последняя смена": last,
        "Кол-во смен": total,
        "Отток": otkok
    }

rows = []
with ThreadPoolExecutor(max_workers=20) as pool:
    futures = [pool.submit(process_one, d) for d in drivers]
    for fut in tqdm(as_completed(futures), total=len(drivers), desc="Обработка"):
        rows.append(fut.result())

df_final = pd.DataFrame(rows)
df_final.to_csv('itog.csv', index=False, encoding='utf-8-sig')

print("\nГотово! Файл itog.csv сохранён на рабочий стол.")
print(df_final.head())