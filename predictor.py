import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class BikePredictor():
    """Bike predictor class."""

    def __init__(self):
        """Returns function to predict bike rental for next day, based on current day."""
        df = pd.read_csv("data/train.csv")

        df = df[["start_time", "bikenumber"]]
        df["start_time"] = pd.to_datetime(df["start_time"], format="%Y-%m-%d %H:%M:%S")
        df_days = df.groupby(by=df["start_time"].dt.date).count()[["bikenumber"]]
        df_days.rename(columns={'bikenumber': 'rented_bikes'}, inplace=True)
        df_days.reset_index(inplace=True)
        df_days = df_days[["rented_bikes"]]
        df_days["prediction_tomorrow"] = df_days["rented_bikes"].shift(-1, fill_value=df_days["rented_bikes"][0]).astype(int)

        X = df_days["rented_bikes"]
        y = df_days["prediction_tomorrow"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.lin_reg = LinearRegression()
        self.lin_reg.fit(self.X_train.values.reshape(-1, 1), self.y_train)

        self.y_pred = self.lin_reg.predict(self.X_test.values.reshape(-1, 1))
        self.rmse = mean_squared_error(self.y_test, self.y_pred)**0.5

        self.predictor = lambda x: self.lin_reg.coef_[0] * x + self.lin_reg.intercept_

    def showStats(self) -> None:
        """Shows the statistics of the current model."""
        print(f"RMSE: {self.rmse:.4f}")
        print(f"Score: {self.lin_reg.score(self.X_test.values.reshape(-1, 1), self.y_test):.4f}")


if __name__ == "__main__":
    pred = BikePredictor()
    print(pred.predictor(42))
