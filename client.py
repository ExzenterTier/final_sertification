import requests

# URL сервера
BASE_URL = 'http://127.0.0.1:5000'

# Проверка статуса дрона
def get_status():
    response = requests.get(f"{BASE_URL}/status")
    print("Статус дрона:", response.json())

# Обновление координат
def update_position(coords):
    response = requests.post(f"{BASE_URL}/position", json={"coords": coords})
    print("Обновление позиции:", response.json())

# Обновление высоты
def update_altitude(altitude):
    response = requests.post(f"{BASE_URL}/altitude", json={"altitude": altitude})
    print("Обновление высоты:", response.json())

# Обновление скорости
def update_speed(speed):
    response = requests.post(f"{BASE_URL}/speed", json={"speed": speed})
    print("Обновление скорости:", response.json())

# Проверка уровня заряда батареи
def check_battery():
    response = requests.get(f"{BASE_URL}/battery")
    print("Проверка батареи:", response.json())

# Возвращение на базу
def return_to_base():
    response = requests.post(f"{BASE_URL}/return_to_base")
    print("Возвращение на базу:", response.json())

# Тесты клиента
if __name__ == "__main__":
    print("=== Тестирование API дрона ===")

    # Проверка начального статуса
    get_status()

    # Изменение координат
    update_position((10, 20))

    # Установка высоты
    update_altitude(15)

    # Установка скорости
    update_speed(5)

    # Проверка уровня батареи
    check_battery()

    # Возвращение на базу
    return_to_base()

    # Финальная проверка статуса
    get_status()
