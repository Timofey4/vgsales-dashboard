import pandas as pd
import pytest

from analysis import (
    load_and_clean,
    platform_average_sales,
    platform_total_sales,
    filter_by_year_range,
)


@pytest.fixture
def sample_df():
    """Минимальный тестовый датафрейм с известными значениями."""
    return pd.DataFrame({
        'Platform': ['PS2', 'PS2', 'X360', 'X360', 'Wii', None],
        'Year': [2000, 2001, 2005, 2006, 2008, None],
        'Global_Sales': [10.0, 20.0, 5.0, 15.0, 30.0, 99.0],
    })


def test_load_and_clean_removes_nan_years(sample_df):
    result = load_and_clean(sample_df)
    assert len(result) == 5
    assert result['Year'].isna().sum() == 0


def test_load_and_clean_year_is_int(sample_df):
    result = load_and_clean(sample_df)
    assert pd.api.types.is_integer_dtype(result['Year'])


def test_platform_average_sales_values(sample_df):
    df = load_and_clean(sample_df)
    result = platform_average_sales(df, top_n=3)
    assert result['PS2'] == pytest.approx(15.0)
    assert result['X360'] == pytest.approx(10.0)
    assert result['Wii'] == pytest.approx(30.0)


def test_platform_average_sales_sorted_desc(sample_df):
    df = load_and_clean(sample_df)
    result = platform_average_sales(df, top_n=3)
    assert list(result.values) == sorted(result.values, reverse=True)


def test_platform_average_sales_top_n(sample_df):
    df = load_and_clean(sample_df)
    assert len(platform_average_sales(df, top_n=2)) == 2


def test_platform_total_sales_values(sample_df):
    df = load_and_clean(sample_df)
    result = platform_total_sales(df, top_n=3)
    assert result['PS2'] == pytest.approx(30.0)
    assert result['X360'] == pytest.approx(20.0)
    assert result['Wii'] == pytest.approx(30.0)


def test_platform_total_sales_sorted_desc(sample_df):
    df = load_and_clean(sample_df)
    result = platform_total_sales(df, top_n=3)
    assert list(result.values) == sorted(result.values, reverse=True)


def test_filter_by_year_range_keeps_correct_years(sample_df):
    df = load_and_clean(sample_df)
    result = filter_by_year_range(df, 2001, 2006)
    assert set(result['Year'].unique()) == {2001, 2005, 2006}


def test_filter_by_year_range_empty(sample_df):
    df = load_and_clean(sample_df)
    assert filter_by_year_range(df, 1990, 1995).empty


def test_filter_by_year_range_inclusive(sample_df):
    df = load_and_clean(sample_df)
    result = filter_by_year_range(df, 2000, 2000)
    assert len(result) == 1
    assert result.iloc[0]['Year'] == 2000
