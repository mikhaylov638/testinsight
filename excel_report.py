import os
import pandas as pd

def export_failures_to_excel(df, out_dir='../testinsight_reports', filename='allure_broken_failed.xlsx'):
    """
    Экспортирует broken и failed тесты в Excel-отчёт.
    На первом листе — все broken, на втором — все failed.
    В каждом листе: имя теста, статус, message, trace, statusMessage, statusTrace (по максимуму).
    """
    # Фильтруем broken и failed
    broken_df = df[df['status'] == 'broken'].copy()
    failed_df = df[df['status'] == 'failed'].copy()

    # Сохраняем только важные поля (или всё, что есть)
    cols = ['name', 'status', 'message', 'trace', 'statusMessage', 'statusTrace', 'feature', 'suite', 'owner']
    broken_df = broken_df[[c for c in cols if c in broken_df.columns]]
    failed_df = failed_df[[c for c in cols if c in failed_df.columns]]

    # Делаем папку для отчётов, если её нет
    os.makedirs(out_dir, exist_ok=True)
    file_path = os.path.join(out_dir, filename)

    # Пишем в Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        broken_df.to_excel(writer, index=False, sheet_name='Broken')
        failed_df.to_excel(writer, index=False, sheet_name='Failed')

    print(f'Excel-отчёт по сломанным/упавшим тестам сохранён: {file_path}')

# Пример вызова:
# export_failures_to_excel(df_cases)
