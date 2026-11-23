"""Загрузка датасета vgsales.

Порядок:
1. Если есть локальный файл data/vgsales.csv — читаем его.
2. Иначе скачиваем через kagglehub и сохраняем копию в data/.
"""
import shutil
from pathlib import Path

import pandas as pd

from analysis import load_and_clean

DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_PATH = DATA_DIR / "vgsales.csv"
KAGGLE_DATASET = "kedokedokedo/vgsales"


def _download_from_kaggle() -> None:
    """Скачивает датасет с Kaggle и кладёт vgsales.csv в папку data/."""
    import kagglehub  # импорт здесь, чтобы он нужен был только при первом запуске

    print("Локальный файл не найден, скачиваю датасет с Kaggle...")
    path = Path(kagglehub.dataset_download(KAGGLE_DATASET))
    DATA_DIR.mkdir(exist_ok=True)
    shutil.copy(path / "vgsales.csv", CSV_PATH)


def get_dataframe() -> pd.DataFrame:
    """Возвращает очищенный датафрейм с продажами."""
    if not CSV_PATH.exists():
        try:
            _download_from_kaggle()
        except Exception as exc:
            raise FileNotFoundError(
                f"Не удалось получить датасет. Скачайте vgsales.csv вручную "
                f"({KAGGLE_DATASET}) и положите в {CSV_PATH}. Причина: {exc}"
            ) from exc
    return load_and_clean(pd.read_csv(CSV_PATH))
