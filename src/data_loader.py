import pandas as pd

class DataLoader:
    def __init__(self, original_csv_path, processed_csv_path):
        self.original_file_path = original_csv_path
        self.processed_file_path = processed_csv_path

    def load_and_process(self):
        df = pd.read_csv(self.original_file_path, encoding="utf-8", error_bad_lines=False).dropna()

        required_columns = {"Name", "Genres", "Synopsis"}

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        df["combined"] = (
            "Title: " + df["Name"] + " Overview: " + df["Synopsis"] + " Genre: " + df["Genres"] + " "
        )

        df[["combined"]].to_csv(self.processed_file_path, index=False, encoding="utf-8")

        return self.processed_file_path
