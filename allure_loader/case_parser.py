import os
import json
import pandas as pd

def load_allure_result_cases(folder):
    """
    Парсит все файлы *-result.json в заданной папке.
    Каждый файл — один тест-кейс.
    """
    result_files = [f for f in os.listdir(folder) if f.endswith('-result.json')]
    cases = []
    for filename in result_files:
        filepath = os.path.join(folder, filename)
        with open(filepath, encoding='utf-8') as f:
            case = json.load(f)
            labels = {l['name']: l['value'] for l in case.get('labels', []) if isinstance(l, dict) and 'name' in l and 'value' in l}
            cases.append({
                'uuid': case.get('uuid'),
                'name': case.get('name'),
                'fullName': case.get('fullName'),
                'status': case.get('status'),
                'start': case.get('start'),
                'stop': case.get('stop'),
                'duration': (case.get('stop') or 0) - (case.get('start') or 0),
                'description': case.get('description'),
                'message': case.get('statusMessage'),
                'trace': case.get('statusTrace'),
                'feature': labels.get('feature'),
                'suite': labels.get('suite'),
                'parentSuite': labels.get('parentSuite'),
                'subSuite': labels.get('subSuite'),
                'severity': labels.get('severity'),
                'tag': labels.get('tag'),
                'owner': labels.get('owner'),
            })
    return pd.DataFrame(cases)
