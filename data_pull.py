from datetime import datetime
import pandas_datareader.data as reader
import pandas as pd

start = datetime(2015, 6, 14)
end = datetime(2019, 6, 14)


def df_to_ts(df):
    prophet_df = pd.DataFrame(df).reset_index()
    prophet_df.columns = ["ds", "y"]
    return prophet_df


def pull_stock_history(stockname):
    df = reader.DataReader(stockname, "yahoo", start, end)["Open"]
    formatted = df_to_ts(df)
    return formatted
