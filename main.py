import os
from allure_loader.loader import extract_allure_archive
from allure_loader.case_parser import load_allure_result_cases
from allure_loader.parser import find_and_load_csv

def main():
    # Путь к архиву
    zip_path = os.path.join('reports', 'Allure_20Report.zip')
    folder = extract_allure_archive(zip_path)
    print(f"Архив распакован: {folder}")

    # ищем директорию Allure_20Report внутри архива
    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isdir(path) and 'allure' in item.lower():
            allure_folder = path
            break

    # Парсим тест-кейсы из большого JSON в test-cases
#    allure_data_folder = None
#    for root, dirs, files in os.walk(folder):
#        if 'test-cases' in dirs:
#            allure_data_folder = root
#            break

#    if allure_data_folder:
#        df_cases = load_allure_test_cases_big_json(allure_data_folder)
#    else:
#        print("Папка test-cases не найдена!")
    df_cases = load_allure_result_cases(allure_folder)
    print(f"Всего тестов: {len(df_cases)}")
    print(df_cases.head())
    print("\nСтатистика по статусам:")
    print(df_cases['status'].value_counts())

    # Пример: читаем suites.csv (если нужен быстрый срез)
    try:
        df = find_and_load_csv(folder, "suites.csv")
        print(f"\nСтрок в suites.csv: {len(df)}")
        print(df.head())
    except FileNotFoundError:
        print("Файл suites.csv не найден, работаем только с JSON.")

if __name__ == "__main__":
    main()