"""Логика анализа продаж видеоигр"""
import pandas as pd
def load_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Удаляет строки без года и приводит Year к int."""
    cleaned = df.dropna(subset=['Year']).copy()
    cleaned['Year'] = cleaned['Year'].astype(int)
    return cleaned


def platform_average_sales(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """Средние продажи на игру по платформам, топ-N по убыванию."""
    return (
        df.groupby('Platform')['Global_Sales']
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )


def platform_total_sales(df: pd.DataFrame, top_n: int = 10) -> pd.Series:
    """Суммарные продажи по платформам, топ-N по убыванию."""
    return (
        df.groupby('Platform')['Global_Sales']
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )


def filter_by_year_range(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    """Фильтрует датасет по диапазону лет включительно."""
    return df[(df['Year'] >= start) & (df['Year'] <= end)]
