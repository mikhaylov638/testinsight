import os
import pandas as pd

def find_and_load_csv(folder, csv_name="suites.csv"):
    """
    Ищет и читает CSV (suites.csv, behaviors.csv...) в папке (и подпапках).
    Возвращает DataFrame.
    """
    for root, dirs, files in os.walk(folder):
        if csv_name in files:
            csv_path = os.path.join(root, csv_name)
            return pd.read_csv(csv_path)
    raise FileNotFoundError(f"{csv_name} не найден в {folder}")
