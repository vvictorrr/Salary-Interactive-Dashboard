import pandas as pd

DATA_FILE_PATH = "ds_salaries.csv"

POSITION_COL = "job_title"
SALARY_COL = "salary_in_usd"
WORK_YEAR_COL = "work_year"
REMOTE_COL = "remote_ratio"

class SalaryAPI:

    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.process_data()

    def process_data(self):
        self.df = self.df.dropna(subset=[POSITION_COL, SALARY_COL])

        self.df[SALARY_COL] = self.df[SALARY_COL].astype(int)
        self.df[WORK_YEAR_COL] = self.df[WORK_YEAR_COL].astype(int)
        self.df[REMOTE_COL] = self.df[REMOTE_COL].astype(int)

    def get_positions(self):
        return ["All Positions"] + sorted(self.df[POSITION_COL].unique())

    def get_remote_ratio(self):
        return ["All"] + sorted(self.df[REMOTE_COL].unique())

    def get_year_range(self):
        return [self.df[WORK_YEAR_COL].min(), self.df[WORK_YEAR_COL].max()]

    def get_filtered_data(self, position, year_range, min_salary, remote, min_samples):
        df = self.df.copy()

        if position != "All Positions":
            df = df[df[POSITION_COL] == position]

        df = df[
            (df[WORK_YEAR_COL] >= year_range[0]) &
            (df[WORK_YEAR_COL] <= year_range[1]) &
            (df[SALARY_COL] >= min_salary)
        ]

        counts = df["job_title"].value_counts()
        valid_roles = counts[counts >= min_samples].index
        df = df[df["job_title"].isin(valid_roles)]

        if remote != "All":
            df = df[df["remote_ratio"] == remote]

        return df