import subprocess, re, json


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


device_id = 1
powershell_cmd = f"Set-AudioDevice -Index {device_id}"
print(powershell_cmd)

subprocess.run(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", powershell_cmd], check=True)