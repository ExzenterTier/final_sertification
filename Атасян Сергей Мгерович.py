# Атасян Сергей Мгерович

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Модель данных
class DroneModel:
    def __init__(self):
        self.altitude = 0  # Высота
        self.speed = 0  # Скорость
        self.coords = (0, 0)  # Координаты
        self.battery_level = 100  # Заряд батареи

    def update_coords(self, new_coords):
        self.coords = new_coords

    def update_altitude(self, new_altitude):
        self.altitude = new_altitude

    def update_speed(self, new_speed):
        self.speed = new_speed

    def update_battery_level(self, consumption):
        # Уменьшение заряда батареи с защитой от отрицательных значений
        self.battery_level = max(0, self.battery_level - consumption)

# Представление
class DroneView:
    @staticmethod
    def display_status(model):
        return {
            "altitude": model.altitude,
            "speed": model.speed,
            "position": model.coords,
            "battery_level": model.battery_level
        }

    @staticmethod
    def alert(message):
        return {"alert": message}

# Контроллер
class DroneController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def change_coords(self, new_coords):
        self.model.update_coords(new_coords)
        return self.view.display_status(self.model)

    def change_altitude(self, new_altitude):
        self.model.update_altitude(new_altitude)
        return self.view.display_status(self.model)

    def change_speed(self, new_speed):
        self.model.update_speed(new_speed)
        return self.view.display_status(self.model)

    def monitor_battery(self):
        if self.model.battery_level < 20:
            return self.view.alert("Низкий заряд батареи! Возвращение на базу!")
        return {"battery_level": self.model.battery_level}

    def return_to_base(self):
        self.model.update_coords((0, 0))
        self.model.update_altitude(0)
        self.model.update_speed(0)
        return self.view.alert("Беспилотник вернулся на базу!")

# Создание экземпляров модели и контроллера
drone_model = DroneModel()
drone_view = DroneView()
drone_controller = DroneController(drone_model, drone_view)

# API для управления дроном
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(drone_view.display_status(drone_model))

@app.route('/position', methods=['POST'])
def update_position():
    data = request.get_json()
    if 'coords' not in data or not isinstance(data['coords'], (list, tuple)) or len(data['coords']) != 2:
        return jsonify({"error": "Некорректный формат координат"}), 400
    new_coords = data['coords']
    return jsonify(drone_controller.change_coords(new_coords))

@app.route('/altitude', methods=['POST'])
def update_altitude():
    data = request.get_json()
    if 'altitude' not in data or not isinstance(data['altitude'], (int, float)):
        return jsonify({"error": "Некорректный формат высоты"}), 400
    new_altitude = data['altitude']
    return jsonify(drone_controller.change_altitude(new_altitude))

@app.route('/speed', methods=['POST'])
def update_speed():
    data = request.get_json()
    if 'speed' not in data or not isinstance(data['speed'], (int, float)):
        return jsonify({"error": "Некорректный формат скорости"}), 400
    new_speed = data['speed']
    return jsonify(drone_controller.change_speed(new_speed))

@app.route('/battery', methods=['GET'])
def check_battery():
    return jsonify(drone_controller.monitor_battery())

@app.route('/return_to_base', methods=['POST'])
def initiate_return_to_base():
    return jsonify(drone_controller.return_to_base())
@app.route('/', methods=['GET'])
def home():
    return Response("Система управления дроном запущена")


if __name__ == '__main__':
    app.run(debug=True)
