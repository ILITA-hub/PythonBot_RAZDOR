
import pyodbc

class data_class:
    def __init__(self):
        #self.a = 'govno'
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=NEYMIK-COMP\SQLEXPRESS;DATABASE=bot_data;UID=bot;PWD=bot')
        self.cursor = cnxn.cursor()

    def get_param_value(self, param):

        request = """  select 
                            param_value 
                        from 
                            main_params
                        where 
                            main_params.param = '%param'"""

        request = request.replace('%param', param)

        self.cursor.execute(request)

        row = self.cursor.fetchone()
        return row



    
