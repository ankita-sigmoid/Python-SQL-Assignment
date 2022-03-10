import pandas as pd
from sqlalchemy import create_engine
import logging


"""
From the xlsx in 2) create another xlsx to list total compensation given at
Department level till date. Columns: Dept No, Dept,Name, Compensation
"""


class Compensation:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging
        try:
            self.engine = create_engine("postgresql+psycopg2://postgres:ankitarp@localhost:5432/assignment_data")
            self.logger.info("Engine created successfully")
        except:
            self.logger.warning("Couldn't create engine")

    def read_sheets(self, data, file):
        try:
            if data == 'Q2':
                # print(file)
                df = pd.read_excel(file, 'Q2')
                # print(df)
                df1 = df.groupby(['Dept No', 'Dept Name']).agg(
                    Total_Compensation=pd.NamedAgg(column='Total Compensation', aggfunc="sum")).reset_index()
                return df1
        except:
            self.logger.warning("Execution unsuccessful. Exception occurred.")
        finally:
            self.logger.info("Execution Successful.")

    def convert_to_sql(self):
        with pd.ExcelFile('Output/task_2.xlsx') as xls:
            for sheet_name in xls.sheet_names:
                new_df = self.read_sheets(sheet_name, xls)
                return new_df

    def write_to_excel(self, df):
        writer = pd.ExcelWriter('Output/task_4.xlsx')
        df.to_excel(writer, sheet_name='Q4', index=False)
        writer.save()


if __name__ == "__main__":
    excel = Compensation()
    df = excel.convert_to_sql()
    # print(df)
    excel.write_to_excel(df)
