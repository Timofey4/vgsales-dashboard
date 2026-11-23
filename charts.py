"""Построение графиков для веб-интерфейса."""
import base64
import io

import matplotlib
matplotlib.use("Agg")  # без GUI — обязательно для работы внутри Flask
import matplotlib.pyplot as plt
import pandas as pd


def bar_chart_base64(data: pd.Series, title: str, color: str) -> str:
    """Рисует столбчатую диаграмму и возвращает PNG в виде base64-строки."""
    fig, ax = plt.subplots(figsize=(10, 4.5))
    data.plot(kind="bar", color=color, ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Продажи (млн копий)")
    ax.set_xlabel("Платформа")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)  # освобождаем память
    return base64.b64encode(buf.getvalue()).decode("ascii")
