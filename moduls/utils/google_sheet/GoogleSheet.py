from pprint import pprint

import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:
    def __init__(self):
        self.CREDENTIALS_FILE = 'roza-token.json'
        self. spreadsheet_id = '1bdPGdB6B4HO3Hz5Bs1prAASblSMXZ8DFqq6mh9NwErw'

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        self.service = apiclient.discovery.build('sheets', 'v4', credentials=credentials)

    def read_data(self, range_name):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            if len(values[0]) == 1:
                data = sum(values, [])
                print(data)
            else:
                return values
                # for row in values:
                #     print(row)

    def write_data(self, range_name, values):
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()

    def update_data(self, range_name, values):
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()

    def search_data_cell(self, search_word, data):
        """Находит ячейку первого вхождения слова в таблицу"""
        res = ''
        for i, rows in enumerate(data):
            for j, word in enumerate(rows):
                if search_word == word:
                    res = chr(ord('A') + j) + str(i + 1)
                    break
            if res:
                break
        return res

    def search_user_from_id(self, user_id, data):
        """Находит все данные по слову по полю"""
        res = []
        for rows in data:
            if rows[2] == str(user_id):
                res.append(rows)
        if res:
            return res
        else:
            return 'Пользователь не найден'

    def search_users_from_stage(self, stage, data):
        """Находит все данные по слову по полю"""
        res = []
        for rows in data:
            if rows[1] == stage:
                res.append(rows)
        if res:
            return res
        else:
            return 'На этапе никого не было'



google_sheet = GoogleSheet()
range_name = 'Тест'

#google_sheet.read_data(range_name)
#google_sheet.write_data(range_name, [['Петя', 'asdfasd', 1]])
#google_sheet.update_data(range_name, [['обновили', 'ура']])

data = google_sheet.read_data(range_name)
#dt = google_sheet.search_user_from_id(2, data)

dt = google_sheet.search_users_from_stage('УЗЛЫ', data)
print(len(dt))
for row in dt:
    print(row)