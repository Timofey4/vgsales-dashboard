"""Тесты веб-интерфейса (Flask test client, без запуска сервера)."""
import pandas as pd
import pytest

from app import create_app


@pytest.fixture
def client():
    df = pd.DataFrame({
        'Platform': ['PS2', 'PS2', 'X360', 'X360', 'Wii'],
        'Year': [2000, 2001, 2005, 2006, 2008],
        'Global_Sales': [10.0, 20.0, 5.0, 15.0, 30.0],
    })
    return create_app(df).test_client()


def test_index_default(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "data:image/png;base64" in resp.get_data(as_text=True)


def test_index_mean_metric(client):
    resp = client.get("/?metric=mean&top_n=5&year_from=2000&year_to=2008")
    assert resp.status_code == 200
    assert "Средние продажи на игру" in resp.get_data(as_text=True)


def test_empty_range_shows_notice(client):
    resp = client.get("/?year_from=2002&year_to=2004")
    assert "Нет данных" in resp.get_data(as_text=True)


def test_invalid_params_do_not_crash(client):
    resp = client.get("/?year_from=abc&year_to=&metric=hack&top_n=9999")
    assert resp.status_code == 200


def test_swapped_years_are_fixed(client):
    resp = client.get("/?year_from=2008&year_to=2000")
    assert resp.status_code == 200
    assert "data:image/png;base64" in resp.get_data(as_text=True)
