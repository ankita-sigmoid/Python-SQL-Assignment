import psycopg2
from configuration import config
import xlsxwriter

"""
Task 1:
Write a Python program to list employee numbers, 
names and their managers and save in a xlsx file.
"""

class EmployeeList:

    def write_to_excel(self, records):
        workbook = xlsxwriter.Workbook('task_1.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        column = 0

        # iterating through content list
        for emp_no, emp_name, manager in records:

            # write operation perform
            worksheet.write(row, column, emp_no)
            worksheet.write(row, column + 1, emp_name)
            worksheet.write(row, column + 2, manager)
            row += 1

        workbook.close()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # query
            query = 'SELECT e1.empno, e1.ename as emp_name, e2.ename as mgr_name from ' \
                    'emp as e1 LEFT JOIN emp as e2 on (e1.mgr=e2.empno);'
            cur.execute(query)
            records = cur.fetchall()

            # inserting header in query result
            records.insert(0, [cur.description[i].name for i in range(len(cur.description))])

            # writing files to xlsx file
            self.write_to_excel(records)

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')


if __name__ == '__main__':
    obj = EmployeeList()
    obj.connect()