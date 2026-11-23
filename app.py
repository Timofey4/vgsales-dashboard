"""Flask-интерфейс для анализа продаж видеоигр по платформам."""
from flask import Flask, render_template, request

from analysis import (
    filter_by_year_range,
    platform_average_sales,
    platform_total_sales,
)
from charts import bar_chart_base64
from data_loader import get_dataframe

METRICS = {
    "sum": "Суммарные продажи",
    "mean": "Средние продажи на игру",
}
TOP_N_MIN, TOP_N_MAX = 5, 20


def _to_int(value, default):
    """Безопасно превращает значение формы в int."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def create_app(df=None) -> Flask:
    """Фабрика приложения. df можно передать в тестах."""
    app = Flask(__name__)
    data = df if df is not None else get_dataframe()

    year_min, year_max = int(data["Year"].min()), int(data["Year"].max())

    @app.route("/")
    def index():
        # 1. Вход: параметры из формы
        start = _to_int(request.args.get("year_from"), year_min)
        end = _to_int(request.args.get("year_to"), year_max)
        if start > end:
            start, end = end, start
        start, end = max(start, year_min), min(end, year_max)

        metric = request.args.get("metric", "sum")
        if metric not in METRICS:
            metric = "sum"
        top_n = min(max(_to_int(request.args.get("top_n"), 10), TOP_N_MIN), TOP_N_MAX)

        # 2. Обработка
        subset = filter_by_year_range(data, start, end)
        context = dict(
            metrics=METRICS, metric=metric, top_n=top_n,
            year_min=year_min, year_max=year_max,
            year_from=start, year_to=end,
            top_n_min=TOP_N_MIN, top_n_max=TOP_N_MAX,
            empty=subset.empty,
        )

        # 3. Выход
        if not subset.empty:
            if metric == "sum":
                series = platform_total_sales(subset, top_n)
                title, color = f"Топ-{top_n} платформ по суммарным продажам", "coral"
            else:
                series = platform_average_sales(subset, top_n)
                title, color = f"Топ-{top_n} платформ по средним продажам на игру", "steelblue"

            context.update(
                chart=bar_chart_base64(series, title, color),
                table=[(str(p), round(float(v), 3)) for p, v in series.items()],
                games=len(subset),
                platforms=int(subset["Platform"].nunique()),
                total_sales=round(float(subset["Global_Sales"].sum()), 1),
            )
        return render_template("index.html", **context)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
