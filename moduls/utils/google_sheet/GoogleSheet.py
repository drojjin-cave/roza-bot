from pprint import pprint

import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:
    def __init__(self, token, id_table):
        self.CREDENTIALS_FILE = token
        self. spreadsheet_id = id_table

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
            return values
        else:
            if len(values[0]) == 1:
                data = sum(values, [])
                return data
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
            if rows[1] == str(user_id):
                res.append(rows)
        if res:
            return res
        else:
            return None

    def search_users_from_stage(self, stage, data):
        """Находит все данные по слову по полю"""
        res = []
        for rows in data:
            if rows[1] == stage:
                res.append(rows)
        if res:
            return res
        else:
            return res

    def search_referee(self, id, data):
        """Находит всех участников, которых занес судья"""
        res = []
        for rows in data:
            if str(id) in rows:
                if len(rows) == 6:
                    one_user = {'ID': rows[1], 'Время': rows[2], 'Имя': rows[4]}
                else:
                    one_user = {'ID': rows[1], 'Время': rows[2], 'Имя': '<b>Не определено!</b>'}
                res.append(one_user)
        if res:
            return res
        else:
            return res

    def info(self, range, category):

        category = '"А" - опытные до 18 лет' if 'А' in category else \
            '"В" - начинающие до 18 лет' if 'В' in category else \
                '"С" - без опыта' if 'С' in category else False


        if category:

            data = self.read_data(range)
            header = data[0]
            category_col = header.index('Дистанция')
            time_col = header.index('Время дистанции')
            res = []


            for row in data:
                if row[0] and row[category_col] == category:
                    res.append(row)
            # print(header)
            # for row in res:
            #     print(row)

            done_disnatce = [time[time_col] for time in res if time[time_col]]
            info = {'Колчество участников': len(res),
                    'Пройдено дистанцию': len(done_disnatce),
                    'Лучшее время': min(done_disnatce),
                    'Худшее время': max([time for time in done_disnatce if time != 'прев. КВ']),
                    'Превышено КВ': len([kv for kv in done_disnatce if kv == 'прев. КВ'])}
            return info


if __name__ == "__main__":
    token_sheet = 'roza-token.json'
    id_table = '1zYjSJhbwD_lwWMIYx4h7uJC6YIuWkzlmDzDhWBP1dX4'
    google_sheet = GoogleSheet(token_sheet, id_table)
    range_name = 'Данные участников сводка'

    #google_sheet.read_data(range_name)
    #google_sheet.write_data(range_name, [['20:04','1', '', '', '15:36:89']])
    #google_sheet.update_data(range_name, [['обновили', 'ура']])

    category = 'Категория А'


    google_sheet.info(range_name, category)
    #print(data)
    # dt = google_sheet.search_user_from_id('2', data)

    #dt = google_sheet.search_users_from_stage('УЗЛЫ', data)
    #print(len(dt))
    # for el in data:
    #     print(el)
    #print(dt)