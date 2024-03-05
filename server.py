import subprocess
import re
import json
from flask import Flask, render_template, request

app = Flask(__name__)


# Функція для отримання списку всіх аудіопристроїв
def get_all_audio_devices():
    powershell_cmd = "Get-AudioDevice -List"
    result = subprocess.run(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", powershell_cmd],
                            capture_output=True, text=True, check=True)
    return result.stdout


def split_text_to_json(text):
    # Визначте регулярний вираз для знаходження блоків
    pattern = re.compile(
        r'Index\s+:\s+(\d+)\s+Default\s+:\s+(\S+)\s+DefaultCommunication\s+:\s+(\S+)\s+Type\s+:\s+(\S+)\s+Name\s+:\s+(.+?)\s+ID\s+:\s+(.+?)\s+Device\s+:\s+(.+?)(?=(Index\s+:\s+\d+|$))',
        re.DOTALL)

    # Знайдіть всі блоки у тексті
    blocks = pattern.findall(text)

    # Перетворіть кожен блок у словник та збережіть їх у список
    result = []
    for block in blocks:
        result.append({
            'Index': int(block[0]),
            'Default': block[1] == 'True',
            'DefaultCommunication': block[2] == 'True',
            'Type': block[3],
            'Name': block[4],
            'ID': block[5],
            'Device': block[6]
        })

    # Перетворіть список у JSON-рядок
    json_result = json.loads(json.dumps(result, indent=2))
    return json_result


# Роут для головної сторінки
@app.route('/')
def index():
    devices = split_text_to_json(get_all_audio_devices())

    print(devices)
    return render_template('index.html', devices=devices, all_devices=devices)


# Роут для зміни пристрою виводу
@app.route('/set_output_device', methods=['POST'])
def set_output_device_route():
    device_id = request.form['device']

    # Використання PowerShell для зміни пристрою виводу
    powershell_cmd = f"Set-AudioDevice -Index {device_id}"
    print(powershell_cmd)
    try:
        subprocess.run(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", powershell_cmd], check=True)
        message = 'Success'
    except subprocess.CalledProcessError as e:
        message = f'Error: {e}', 500

    # Поверніть шаблон разом із змінною message
    devices = split_text_to_json(get_all_audio_devices())
    return render_template('index.html', devices=devices, all_devices=devices, message=message)


if __name__ == '__main__':
    app.run(debug=True)
