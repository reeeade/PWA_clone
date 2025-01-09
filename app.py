import json
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DEVICE_DATA_FILE = "device_data.json"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save-device-info", methods=["POST"])
def save_device_info():
    device_info = request.json
    if not device_info:
        return jsonify({"error": "No data to save"}), 400

    # Читаем существующие данные, если файл уже есть
    all_data = []
    if os.path.exists(DEVICE_DATA_FILE):
        with open(DEVICE_DATA_FILE, "r", encoding="utf-8") as file:
            try:
                all_data = json.load(file)
            except json.JSONDecodeError:
                all_data = []

    # Определяем новый ID
    if all_data:
        new_id = max(item["id"] for item in all_data) + 1
    else:
        new_id = 1

    # Добавляем данные в новый формат
    new_entry = {
        "id": new_id,
        "data": device_info  # Оставляем объект JSON вместо строки
    }
    all_data.append(new_entry)

    # Сохраняем данные обратно в файл
    try:
        with open(DEVICE_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(all_data, file, indent=4, ensure_ascii=False)
    except Exception as error:
        return jsonify({"error": str(error)}), 500

    return jsonify({"message": "Data saved successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
