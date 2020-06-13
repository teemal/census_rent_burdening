import os
import pygsheets

#might want to consider renaming this since, while it uses google under the hood,
#everything in here is interacting with pygsheets
class Google(object):
    def __init__(self):
        super().__init__()

    def auth(self, env):
        if(os.environ[env] == 'dev'):
            api = self._auth(env, 'SERVICE_ACCOUNT_DEV')
        elif(os.environ[env] == 'testing'):
            api = self._auth(env, 'SERVICE_ACCOUNT_TESTING')
        else: #staging and production
            api = self._auth(env, 'SERVICE_ACCOUNT')
        return api

    def _auth(self, env, service_account):
        if(os.environ[env] == 'dev' or os.environ[env] == 'testing'):
            return pygsheets.authorize(service_file = os.getenv(service_account))
        else: 
            return pygsheets.authorize(service_account_env_var = service_account)

    def open_workbook(self, api, env):
        if(os.environ[env] == 'dev'):
            wb = self._open_workbook(api, 'COIC-dashboard-dev')
        elif(os.environ[env] == 'testing'):
            wb = self._open_workbook(api, 'COIC-dashboard-testing')
        elif(os.environ[env] == 'staging'):
            wb = self._open_workbook(api, 'COIC-dashboard-staging')
        else: 
            wb = self._open_workbook(api, 'COIC-dashboard-production')
        return wb

    def _open_workbook(self, api, book_name):    
        return api.open(book_name)

    def worksheet_by_title_wrapper(self, wb, sheet_title):
        return wb.worksheet_by_title(sheet_title)

    def clear_wrapper(self, sheet):
        sheet.clear()

    def set_dataframe_wrapper(self, sheet, df, tup):
        sheet.set_dataframe(df, tup)