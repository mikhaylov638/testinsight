import os
import zipfile
import tempfile
from dotenv import load_dotenv

load_dotenv()
REPORTS_DIR = os.getenv('ALLURE_REPORTS_DIR', 'reports')

def extract_allure_archive(zip_path, extract_to=None):
    """
    Распаковывает архив Allure в указанный каталог (или во временный).
    Возвращает путь к распакованной папке.
    """
    if extract_to is None:
        extract_to = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to