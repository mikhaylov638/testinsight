import json

with open(r'C:\Users\Евгений\AppData\Local\Temp\Tmp_view\allure-report\data\test-cases\e5fecdda12899559.json', encoding='utf-8') as f:
    data = json.load(f)
    print(type(data))
    if isinstance(data, dict):
        print('Keys:', data.keys())
        for k in data:
            print(f"Ключ: {k} — Тип: {type(data[k])}")
    elif isinstance(data, list):
        print('В списке элементов:', len(data))
        print('Первый элемент:', type(data[0]))
