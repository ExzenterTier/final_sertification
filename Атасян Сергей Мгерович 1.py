#Атасян Сергей Мгерович


import requests
import multiprocessing

# Модель данных
class DroneModel:
    """
    Класс DroneModel отвечает за хранение данных о состоянии БПЛА.
    """

    def __init__(self):
        """
        Инициализация данных о состоянии БПЛА.
        """
        self.altitude = 0  # Высота в метрах
        self.speed = 0  # Скорость в м/с
        self.coords = (0, 0)  # Координаты
        self.battery_level = 100  # Уровень заряда батареи в процентах

    def update_coords(self, new_coords):
        """
        Обновляет координаты БПЛА.
        :param new_coords: Новые координаты (x, y)
        """
        self.coords = new_coords

    def update_altitude(self, new_altitude):
        """
        Обновляет высоту БПЛА.
        :param new_altitude: Новая высота
        """
        self.altitude = new_altitude

    def update_speed(self, new_speed):
        """
        Обновляет скорость БПЛА.
        :param new_speed: Новая скорость
        """
        self.speed = new_speed

    def update_battery_level(self, expenditure):
        """
        Обновляет уровень заряда батареи.
        :param expenditure: Расход батареи в процентах
        """
        self.battery_level -= expenditure

# Представление
class DroneView:
    """
    Класс DroneView отвечает за визуализацию данных о состоянии БПЛА.
    """

    @staticmethod
    def display_status(model):
        """
        Выводит на экран информацию о текущем состоянии БПЛА.
        :param model: Экземпляр DroneModel с данными о состоянии
        """
        print(f"Altitude: {model.altitude} meters, Speed: {model.speed} m/s, "
              f"Position: {model.coords}, Battery: {model.battery_level}%")

    @staticmethod
    def alert(message):
        """
        Выводит предупреждающее сообщение.
        :param message: Текст предупреждения
        """
        print(f"ALERT: {message}")

# Контроллер
class DroneController:
    """
    Класс DroneController отвечает за управление логикой работы БПЛА.
    """

    def __init__(self, model, view):
        """
        Инициализация контроллера.
        :param model: Экземпляр DroneModel
        :param view: Экземпляр DroneView
        """
        self.model = model
        self.view = view

    def change_coords(self, new_coords):
        """
        Обновляет координаты БПЛА.
        :param new_coords: Новые координаты (x, y)
        """
        self.model.update_coords(new_coords)
        self.view.display_status(self.model)

    def change_altitude(self, new_altitude):
        """
        Обновляет высоту БПЛА.
        :param new_altitude: Новая высота
        """
        self.model.update_altitude(new_altitude)
        self.view.display_status(self.model)

    def change_speed(self, new_speed):
        """
        Обновляет скорость БПЛА.
        :param new_speed: Новая скорость
        """
        self.model.update_speed(new_speed)
        self.view.display_status(self.model)

    def monitor_battery(self):
        """
        Проверяет уровень заряда батареи и выполняет возвращение на базу при низком заряде.
        """
        if self.model.battery_level < 20:
            self.view.alert("Низкий заряд батареи! Возвращение на базу!")
            self.return_to_base()

    def return_to_base(self):
        """
        Возвращает БПЛА на базу (в начальную точку).
        """
        self.model.update_coords((0, 0))
        self.model.update_altitude(0)
        self.model.update_speed(0)
        self.view.display_status(self.model)
        self.view.alert("Беспилотник вернулся на базу!")

# Наблюдатель и сенсор препятствий
class SensorObserver:
    """
    Базовый класс наблюдателя за данными сенсоров.
    """

    def update(self, data):
        """
        Метод обновления данных сенсора. Должен быть реализован в подклассах.
        """
        raise NotImplementedError("Метод update должен быть реализован")

class ObstacleSensor(SensorObserver):
    """
    Класс ObstacleSensor отвечает за обработку данных о препятствиях и управление БПЛА.
    """

    def __init__(self, controller):
        """
        Инициализация сенсора препятствий.
        :param controller: Экземпляр DroneController для управления БПЛА
        """
        self.controller = controller

    def update(self, data):
        """
        Обрабатывает данные о препятствиях и изменяет курс или останавливает БПЛА.
        :param data: Данные сенсора (например, дистанция до препятствия)
        """
        if data['distance'] < 7:
            print("Препятствие слишком близко! Изменение курса...")
            # Логика изменения курса: смещение на 7 единиц по оси x
            new_coords = (self.controller.model.coords[0] + 7, self.controller.model.coords[1])
            self.controller.change_coords(new_coords)
        elif data['distance'] < 3:
            print("Опасное расстояние! Остановка БПЛА.")
            self.controller.change_speed(0)  # Остановка

# Состояния полета
class DroneState:
    """
    Базовый класс для различных состояний полета.
    """

    def handle(self, drone):
        """
        Метод обработки состояния. Должен быть реализован в подклассах.
        """
        raise NotImplementedError("Метод handle должен быть реализован")

class Takeoff(DroneState):
    """
    Класс Takeoff отвечает за состояние взлета БПЛА.
    """

    def handle(self, drone):
        """
        Реализует логику взлета БПЛА.
        :param drone: Экземпляр StatefulDrone
        """
        print("Взлет...")
        drone.model.update_altitude(10)

class Landing(DroneState):
    """
    Класс Landing отвечает за состояние посадки БПЛА.
    """

    def handle(self, drone):
        """
        Реализует логику посадки БПЛА.
        :param drone: Экземпляр StatefulDrone
        """
        print("Посадка...")
        drone.model.update_altitude(0)
        drone.model.update_speed(0)

# Дрон с поддержкой состояний
class StatefulDrone:
    """
    Класс StatefulDrone управляет состояниями и действиями БПЛА.
    """

    def __init__(self, state, model, view):
        """
        Инициализация дрона с состояниями.
        :param state: Начальное состояние полета
        :param model: Экземпляр DroneModel
        :param view: Экземпляр DroneView
        """
        self.state = state
        self.model = model
        self.view = view

    def change_state(self, state):
        """
        Изменяет текущее состояние БПЛА.
        :param state: Новое состояние полета
        """
        self.state = state

    def perform_action(self):
        """
        Выполняет действие в соответствии с текущим состоянием БПЛА.
        """
        self.state.handle(self)
        self.view.display_status(self.model)

# Интеграция с внешним API
class WeatherAPI:
    """
    Класс WeatherAPI отвечает за взаимодействие с API для получения данных о погоде.
    """

    def __init__(self, api_key):
        """
        Инициализация API с ключом доступа.
        :param api_key: Ключ доступа к API
        """
        self.api_key = api_key

    def get_weather(self, location):
        """
        Получает данные о погоде для указанного местоположения.
        :param location: Название местоположения (город, страна)
        :return: Погодные условия и скорость ветра
        """
        url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={location}"
        response = requests.get(url)
        data = response.json()
        return data['current']['condition']['text'], data['current']['wind_mph']

# Пример использования WeatherAPI
# weather_api = WeatherAPI(api_key='МОЙ-АПИ-КЛЮЧ')
# weather_conditions, wind_speed = weather_api.get_weather('New York')
# print(f"Current weather: {weather_conditions}, Wind speed: {wind_speed} mph")

# Параллельная обработка данных с сенсоров
def process_sensor_data(data):
    """
    Обрабатывает данные с сенсора в параллельном процессе.
    :param data: Данные сенсора
    :return: Обработанные данные
    """
    processed_data = data * 2  # Пример обработки
    return processed_data

if __name__ == '__main__':
    sensor_data = [1, 2, 3, 4, 5]
    pool = multiprocessing.Pool()
    results = pool.map(process_sensor_data, sensor_data)
    print(f"Обработанные данные датчиков: {results}")

# Юнит-тесты
import unittest

class TestDroneNavigation(unittest.TestCase):
    """
    Класс TestDroneNavigation тестирует основные функции управления БПЛА.
    """

    def test_update_position(self):
        """
        Тестирует обновление позиции БПЛА.
        """
        drone_model = DroneModel()
        controller = DroneController(drone_model, DroneView())
        controller.change_coords((10, 20))
        self.assertEqual(drone_model.coords, (10, 20))

    def test_battery_monitoring(self):
        """
        Тестирует мониторинг уровня заряда батареи и возвращение на базу.
        """
        drone_model = DroneModel()
        drone_model.update_battery_level(80)  # Понижаем заряд батареи
        controller = DroneController(drone_model, DroneView())
        controller.monitor_battery()
        self.assertEqual(drone_model.coords, (0, 0))  # Дрон должен вернуться на базу

if __name__ == '__main__':
    unittest.main()
