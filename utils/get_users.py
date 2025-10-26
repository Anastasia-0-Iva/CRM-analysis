import datetime
import requests
from config.main_config import API_KEY, GET_USER_URL
from utils.get_signatures_for_api import get_signature

def get_parking_drivers_with_fio():
    data = {'timestamp': datetime.datetime.now().timestamp()}
    signature = get_signature(data, API_KEY)

    START_DATE = datetime.date(2025, 9, 1)
    END_DATE   = datetime.date(2025, 10, 1)

    try:
        resp = requests.post(
            GET_USER_URL,
            json=data,
            headers={'Authorization': signature},
            timeout=60
        )
        resp.raise_for_status()
        response_data = resp.json()

        if response_data.get('success'):
            users_list = response_data.get('users_list', {})

            result = []  # будем складывать кортежи (user_id, ФИО)
            for user_id, user_data in users_list.items():
                # фильтр по роли
                if user_data.get('user_role_name') != 'Водители Парковые':
                    continue

                # фильтр по дате регистрации
                created_raw = user_data.get('created_at')
                if not created_raw:
                    continue
                try:
                    created_date = datetime.datetime.fromisoformat(created_raw[:10]).date()
                except Exception:
                    continue
                if not (START_DATE <= created_date <= END_DATE):
                    continue

                # Формируем ФИО
                last = (user_data.get('last_name') or '').strip()
                first = (user_data.get('first_name') or '').strip()
                mid = (user_data.get('middle_name') or '').strip()
                fio = ' '.join(filter(None, [last, first, mid])) or 'Без имени'

                phone = user_data.get('phone', '')
                created_at = user_data.get('created_at', '')
                branch = user_data.get('branch', '')

                result.append((user_id, fio, phone, branch, created_at))

            return result

        else:
            print(f"Ошибка в ответе API: {response_data.get('error')}")
            return []


    except Exception as e:
        print(f"Ошибка: {e}")
        return []

if __name__ == '__main__':
    drivers = get_parking_drivers_with_fio()
    for uid, fio, phone, branch, created_at in drivers:
        print(uid, fio, phone, branch, created_at)