import pandas as pd
import os

def main(excel_path=None):
    """
    Анализирует Excel-отчёт (XLSX или CSV) с результатами тестов и формирует отчёт с аналитикой по трём листам:
    1. Частота багов по разделам (feature)
    2. Типы багов (failure_type)
    3. Топ-50 самых долгих тестов по времени выполнения
    """

    # --- Автоопределение файла, если путь не передали ---
    if not excel_path:
        # Ищем по умолчанию
        default_xlsx = "reports/allure_test_results_enhanced.xlsx"
        default_csv  = "reports/allure_test_results_enhanced.csv"
        for path in [default_xlsx, default_csv]:
            if os.path.exists(path):
                excel_path = path
                break
        else:
            print("❌ Не найден файл отчёта!")
            return

    # --- Читаем Excel или CSV ---
    try:
        if excel_path.endswith('.csv'):
            # Попробуем несколько популярных кодировок
            tried = False
            for encoding in ['utf-8', 'utf-16', 'cp1251', 'utf-8-sig']:
                try:
                    df = pd.read_csv(excel_path, sep=',', encoding=encoding)
                    tried = True
                    break
                except Exception:
                    continue
            if not tried:
                print(f"Ошибка чтения CSV: не удалось подобрать кодировку для {excel_path}")
                return
        else:
            df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Ошибка при чтении файла {excel_path}: {e}")
        return

    # ------ 1. Частота багов по разделам ------
    fail_status = ['failed', 'broken']
    if 'feature' in df.columns and 'status' in df.columns:
        bugs_by_section = (
            df[df['status'].isin(fail_status)]
            .groupby('feature')
            .size()
            .reset_index(name='fail_count')
            .sort_values('fail_count', ascending=False)
        )
    else:
        bugs_by_section = pd.DataFrame({'feature': [], 'fail_count': []})

    # ------ 2. Типы багов ------
    if 'failure_type' in df.columns and 'status' in df.columns:
        types = (
            df[df['status'].isin(fail_status)]
            .groupby('failure_type')
            .size()
            .reset_index(name='count')
            .sort_values('count', ascending=False)
        )
    elif 'failure_message' in df.columns and 'status' in df.columns:
        types = (
            df[df['status'].isin(fail_status)]
            .groupby('failure_message')
            .size()
            .reset_index(name='count')
            .sort_values('count', ascending=False)
        )
    else:
        types = pd.DataFrame({'type': [], 'count': []})

    # ------ 3. Топ по времени ------
    if 'duration_sec' in df.columns:
        # duration_sec может быть строкой с запятой — приводим к float
        df['duration_sec'] = df['duration_sec'].astype(str).str.replace(',', '.')
        df['duration_sec'] = pd.to_numeric(df['duration_sec'], errors='coerce')
        slowest = (
            df[['test_name', 'status', 'duration_sec', 'feature', 'failure_type', 'failure_message']]
            .sort_values('duration_sec', ascending=False)
            .head(50)
        )
    else:
        slowest = pd.DataFrame()

    # --- Сохраняем в централизованный каталог ---
    out_dir = os.path.join(os.getcwd(), "C:/Projects/testinsight_reports")
    os.makedirs(out_dir, exist_ok=True)
    out_name = os.path.join(out_dir, "golden_report_analysis.xlsx")

    with pd.ExcelWriter(out_name, engine='openpyxl') as writer:
        bugs_by_section.to_excel(writer, sheet_name='Баги по разделам', index=False)
        types.to_excel(writer, sheet_name='Типы багов', index=False)
        slowest.to_excel(writer, sheet_name='Топ по времени', index=False)

    print(f"✅ Отчёт успешно сохранён: {out_name}")

if __name__ == "__main__":
    main()
