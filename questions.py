import pandas as pd
import logging
from connection import Connection
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

user = "abhishek"
password = "none"

class Employee:
    def __init__(self):
        pass

    # Question 1
    def list_of_employees(self):
        connection = Connection.get_connection(self, user, password)
        cur = connection.cursor()
        data = cur.execute("""SELECT t1.empno as EmployeeNumber, 
                                t1.ename as EmployeeName, 
                                t2.ename as Manager FROM emp t1, 
                                emp t2 WHERE t1.mgr=t2.empno;""")
        rows = cur.fetchall()
        emp_no = []
        name = []
        manager = []

        for row in rows:
            temp_list = list(row)
            emp_no.append(temp_list[0])
            name.append(temp_list[1])
            manager.append(temp_list[2])

        df = pd.DataFrame({'Employee_No': emp_no, 'Name': name, 'Manager': manager})
        print(df.head())
        writer = pd.ExcelWriter('ques1.xlsx')
        df.to_excel(writer, sheet_name='ques1', index=False)
        writer.save()
        connection.close()
        logging.info("Connection Close")

    # Question 2

    def total_compensation(self):
        connection = Connection.get_connection(self, user, password)
        cur = connection.cursor()
        cur.execute("UPDATE jobhist SET enddate=CURRENT_DATE WHERE enddate IS NULL;")
        data = cur.execute(
            "SELECT emp.ename, "
            "jh.empno, dept.dname, jh.deptno, "
            "ROUND((jh.enddate-jh.startdate)/30*jh.sal,0) "
            "AS total_compensation, ROUND((jh.enddate-jh.startdate)/30,0) as months_spent FROM "
            "jobhist as jh INNER JOIN dept ON jh.deptno=dept.deptno INNER JOIN emp ON jh.empno=emp.empno;")
        rows = cur.fetchall()
        emp_name = []
        emp_no = []
        dept_name = []
        dept_no = []
        total_compensation = []
        month_spent = []

        for row in rows:
            temp_list = list(row)
            emp_name.append(temp_list[0])
            emp_no.append(temp_list[1])
            dept_name.append(temp_list[2])
            dept_no.append(temp_list[3])
            total_compensation.append(temp_list[4])
            month_spent.append(temp_list[5])
        df = pd.DataFrame(
            {'Employee_Name': emp_name, 'Employee_No': emp_no, 'Dept_Name': dept_name,
             'Dept_Number': dept_no, 'Total_Compensation': total_compensation, 'Months_Spent': month_spent})
        print("\n\n", df.head())
        writer = pd.ExcelWriter('ques2.xlsx')
        df.to_excel(writer, sheet_name='Q2', index=False)
        writer.save()
        connection.close()
        logging.info("Connection Close")

    # Question 3
    def file_to_table(self, data, file):
        engine = Connection.get_engine(self, user, password)
        try:
            if data == 'Q2':
                df = pd.read_excel(file, 'Q2')
                df.to_sql(name='total_compensation', con=engine, if_exists='append', index=False)
        except:
            logging.info("Execution unsuccessful. Exception occurred.")
        finally:
            logging.info("Execution Successful.")

    def create_table(self):
        with pd.ExcelFile('ques2.xlsx') as xls1:
            for sheet_name in xls1.sheet_names:
                emp.file_to_table(sheet_name, xls1)

    # Question 4
    def compensation_at_dept_level(self, data, file):
        try:
            if data == 'Q2':
                df = pd.read_excel(file, 'Q2')
                print(df.head())
                return df
        except:
            logging.info("Execution unsuccessful. Exception occurred.")
        finally:
            logging.info("Execution Successful.")

    def read_sheets(self):
        with pd.ExcelFile('ques2.xlsx') as xls2:
            for sheet_name in xls2.sheet_names:
                new_df = emp.compensation_at_dept_level(sheet_name, xls2)

        temp1_df = new_df.groupby(['Dept_Name', 'Dept_Number']).agg(
            Total_Compensation=pd.NamedAgg(column='Total_Compensation', aggfunc="sum")).reset_index()

        writer = pd.ExcelWriter('ques4.xlsx')
        temp1_df.to_excel(writer, sheet_name='Excel_file_Q4', index=False)
        writer.save()


emp = Employee()
# q1
emp.list_of_employees()
# q2
emp.total_compensation()
# q3
emp.create_table()
# q4
emp.read_sheets()
