import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class DataPipeline:
    """Performs data cleaning, feature engineering, and feature scaling."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.scaler = MinMaxScaler()

    def clean_data(self) -> "DataPipeline":
        """Executes data validation and type casting."""
        # Ensure start_date is formatted as datetime
        self.df["start_date"] = pd.to_datetime(self.df["start_date"])
        return self

    def engineer_features(self, benchmark_date_str: str = "2024-12-31") -> "DataPipeline":
        """Derives start year and service tenure in years."""
        self.df["start_year"] = self.df["start_date"].dt.year
        
        benchmark_date = pd.Timestamp(benchmark_date_str)
        self.df["years_of_service"] = (
            (benchmark_date - self.df["start_date"]).dt.days / 365.25
        ).round(1)
        
        return self

    def scale_features(self, column_name: str = "salary") -> "DataPipeline":
        """Scales continuous features using MinMaxScaler onto a [0, 1] range."""
        scaled_col_name = f"{column_name}_scaled"
        self.df[scaled_col_name] = self.scaler.fit_transform(
            self.df[[column_name]]
        ).round(4)
        return self

    def get_processed_data(self) -> pd.DataFrame:
        """Returns the modified DataFrame."""
        return self.df

    def print_diagnostics(self):
        """Displays data summary and missing value counts."""
        print("--- Data Structure & Types ---")
        print(self.df.info())
        print("\n--- Missing Value Check ---")
        print(self.df.isnull().sum())
        print("\n--- Summary Statistics ---")
        print(self.df.describe())