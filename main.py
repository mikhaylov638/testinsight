import os

# --- 1. Поиск нужного файла отчета в папках проекта ---
def find_report(filename, search_dirs=["reports", "."]):
    """
    Ищет указанный файл (например, 'allure_test_results_enhanced.csv' или 'allure-report.zip')
    сначала в папке reports/, потом в корне проекта.
    Возвращает полный путь, если файл найден, иначе None.
    """
    for folder in search_dirs:
        candidate = os.path.join(folder, filename)
        if os.path.exists(candidate):
            return candidate
    return None

# --- 2. Обработка "золотого" отчета (CSV) ---
def analyze_golden_report(csv_path):
    """
    Импортирует и запускает функцию анализа для "золотого" CSV-отчета.
    Функция main() берется из твоего golden_report_analysis.py (или аналога).
    """
    from csv_xlsx_analysis.golden_report_analysis import main as golden_main
    print(f"\n[INFO] Найден 'золотой' отчет: {csv_path}")
    golden_main(csv_path)

# --- 3. Обработка стандартного отчета (zip) ---
def analyze_allure_zip(zip_path):
    """
    Импортирует и запускает функцию анализа для архива allure-report.zip.
    Функция main() берется из твоего модуля zip_analysis.main_analysis.py (или аналога).
    """
    from zip_analysis.loader import extract_allure_archive as allure_main
    print(f"\n[INFO] Используем стандартный архивный анализ: {zip_path}")
    allure_main(zip_path)

# --- 4. Точка входа: выбирает анализ в зависимости от найденного файла ---
def main():
    # Сначала ищем "золотой" CSV-отчет
    golden_csv = find_report("allure_test_results_enhanced.csv")
    golden_xlsx = find_report("allure_test_results_enhanced.xlsx")
    if golden_csv or golden_xlsx:
        analyze_golden_report(golden_csv or golden_xlsx)
        return

    # Если не найден — ищем zip-отчет Allure
    allure_zip = find_report("allure-report.zip")
    if allure_zip:
        analyze_allure_zip(allure_zip)
        return

    # Если не найден ни один файл — сообщаем об ошибке
    print("\n[ERROR] Не найден ни 'золотой' CSV-отчет, ни архив allure-report.zip.\n"
          "Положите нужный файл в корень проекта или в папку reports/!")

# --- 5. Запуск по cli ---
if __name__ == "__main__":
    main()
