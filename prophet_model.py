from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from collections import namedtuple
from data_pull import pull_stock_history

model_prediction = namedtuple('ModelPrediction', 'forecast, cv')

def format_forecast(results):
    formatted = [(str(a[1]).split(" ")[0], a[2]) for a in results.itertuples()]
    return formatted


def make_prediction(df_ts, cv_score=0):
    model = Prophet()
    model.fit(df_ts)
    if cv_score:
        cv_df = cross_validation(
            m, initial=f"{len(df_ts)} days", period="10 days", horizon="30 days"
        )
        perf_df = performance_metrics(cv_df)
        cv_score = perf_df["mape"].to_list()
    future = model.make_future_dataframe(periods=20)
    forecast = model.predict(future)
    forecast_df = forecast[["ds", "yhat"]][-30:]
    formatted = format_forecast(forecast_df)
    return model_prediction(formatted, cv_score)


def train_model(stock):
    stock_history = pull_stock_history(stock)
    results = make_prediction(stock_history)
    return results
