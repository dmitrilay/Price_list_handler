# ----------------
# version 0.6 для мвидео
# ________________
import openpyxl
from openpyxl import Workbook
import models1 as db1
import models2 as db2
import models3 as db3
import models4 as db4
from settings import *
import datetime

import logical_price_processing as lgp


class ParserFile:
    def __init__(self, path_to_open, path_to_save, db, mg):
        self.mg = mg
        self.db = db
        self.path_to_open = path_to_open
        self.path_to_save = path_to_save
        self.price_db_new = {'Наименование': [], 'Цена': []}
        self.price_db = {'Наименование': [], 'Цена': [], 'Цена2': [], 'дата': [], 'Вывод': []}
        self.price_db_exit = {'Наименование': [], 'Цена': []}
        self.price_dict_exit = {'Наименование': [], 'Цена': []}

        self.price_dict_entrance = {'Наименование': [], 'Цена_1': [], 'Цена_2': [],
                                    'Скидка_1': [], 'Скидка_2': []}

        self.price_db_update = {'Наименование': [], 'Цена': []}

    def open_file(self, file=None):
        """
        Открываем файл
        вход артикул, цена, цена2, скидка, скидка2
        """
        if file is None:
            file = self.path_to_open

        print('-- Открываем файл')
        wb = openpyxl.load_workbook(file)  # открываем файл
        sheet = wb.active  # Выбираем активный лист
        rows = sheet.max_row  # cols = self.sheet.max_column

        for i in range(1, rows + 1):
            self.price_dict_entrance['Наименование'].append(sheet.cell(row=i, column=1).value)
            self.price_dict_entrance['Цена_1'].append(sheet.cell(row=i, column=2).value)
            self.price_dict_entrance['Цена_2'].append(sheet.cell(row=i, column=3).value)
            self.price_dict_entrance['Скидка_1'].append(sheet.cell(row=i, column=4).value)
            self.price_dict_entrance['Скидка_2'].append(sheet.cell(row=i, column=5).value)

        self.file_processing()

    def file_processing(self):
        """
        Подготовака даннх к обработке
        """
        print('-- Обрабатываем файл')

        if self.mg == 'mts.xlsx':
            self.price_dict_exit = lgp.logical_price_processing_mts(self.price_dict_entrance)
        elif self.mg == 'dns.xlsx':
            self.price_dict_exit = lgp.logical_price_processing_dns(self.price_dict_entrance)
        else:
            for i in range(0, len(self.price_dict_entrance['Наименование'])):
                article = self.price_dict_entrance['Наименование'][i]
                price_1 = self.price_dict_entrance['Цена_1'][i]
                price_2 = self.price_dict_entrance['Цена_2'][i]
                discount_1 = self.price_dict_entrance['Скидка_1'][i]
                discount_2 = self.price_dict_entrance['Скидка_2'][i]

                if price_1 is not None:
                    try:
                        if int(price_1) > 0:
                            if int(price_1) > int(price_2) > 0:
                                self.price_dict_exit['Цена'].append(price_2)
                            else:
                                self.price_dict_exit['Цена'].append(price_1)
                            self.price_dict_exit['Наименование'].append(article)

                    except Exception:
                        print('ОШИБКА, текст переменной:', price_1)

        self.price_dict_entrance = None

    def unloading_from_the_database(self):
        """
        Выгружаем данные из базы даннхы
        """
        print('-- Выгружаю данные из базы')
        with self.db.db:
            for data in self.db.PriceParser.select():
                self.price_db['Наименование'].append(data.name)
                self.price_db['Цена'].append(data.price_old)
                self.price_db['Цена2'].append(data.price_new)
                self.price_db['дата'].append(data.date_recording)
                self.price_db['Вывод'].append(data.display)

    def find_in_the_database(self):
        """
        Ищем позицию в базе, если находим - проверяем было ли
        изменнеие в цене. Если позиция не найдена то сохраняем
        в словарь для дальнейшей записи.
        """
        stop = len(self.price_dict_exit['Наименование'])
        for i in range(0, stop):
            name_1 = self.price_dict_exit['Наименование'][i]
            try:
                index_db = self.price_db['Наименование'].index(name_1)
                price_1 = int(self.price_db['Цена'][index_db])
                price_2 = self.price_dict_exit['Цена'][i]
                if price_2 < price_1:
                    self.checking_data_types(name=name_1,
                                             price=price_2,
                                             record_type='update')
            except Exception:
                name_wr = self.price_dict_exit['Наименование'][i]
                price_wr = self.price_dict_exit['Цена'][i]
                self.checking_data_types(name=name_wr, price=price_wr, record_type='write')

        self.writing_file_db()
        self.updating_the_database_price()

    def checking_data_types(self, name, price, record_type=None):
        """
        Привидение даннх к нужному формамату(int...)
        """
        if record_type == 'write':
            self.price_db_new['Наименование'].append(name)
            self.price_db_new['Цена'].append(int(price))
        if record_type == 'update':
            self.price_db_update['Наименование'].append(name)
            self.price_db_update['Цена'].append(int(price))

    def updating_the_database_price(self, ):
        """
        Запись обработанных данных в базу
        Обнавление цены
        """
        dt_now = datetime.datetime.now()
        # query = PriceParser.update(price_new=0)
        # query.execute()
        print('-- Сохраняем обнавленные данные в базу данных')
        length_for = len(self.price_db_update['Наименование'])
        with self.db.db:
            for i in range(0, length_for):
                name = self.price_db_update['Наименование'][i]
                price = self.price_db_update['Цена'][i]
                product = self.db.PriceParser.get(self.db.PriceParser.name == name)
                product.price_new = price
                product.date_recording = dt_now
                product.save()

    def writing_file_db(self):
        """
        Сохранение новых данных в базу
        """
        data = []
        i2, dt_now = 0, datetime.datetime.now()
        stop_for = len(self.price_db_new['Наименование'])
        if stop_for:
            print('-- Сохраняем новые данные в базу')
        for i in range(0, stop_for):
            name = self.price_db_new['Наименование'][i]
            price = self.price_db_new['Цена'][i]
            data.append({'name': name,
                         'price_old': price,
                         'price_new': 0,
                         'date_recording': dt_now,
                         'display': 0, })

            if i2 == 100 or i == stop_for - 1:
                self.db.PriceParser.insert_many(data).execute()
                i2 = 0
                data = []
            i2 = i2 + 1

    def writing_file_excel(self):
        """
        Сохраняем данные в формате excel(вместо базы данных)
        """
        print('-- Сохраняем файл')
        wb = Workbook()
        ws = wb.active

        stop_for = len(self.price_dict_exit['Наименование'])
        for i in range(0, stop_for):
            ws.cell(row=i + 1, column=1, value=self.price_dict_exit['Наименование'][i])
            ws.cell(row=i + 1, column=2, value=self.price_dict_exit['Цена'][i])

        wb.save(filename=self.path_to_save)

    def writing_file_excel_db(self, path_to_save='database_excel.xlsx'):
        """
        Сохраняем базу данных в формате excel
        """
        wb = Workbook()
        ws = wb.active
        stop_for = len(self.price_db['Наименование'])
        for i in range(0, stop_for):
            ws.cell(row=i + 1, column=1, value=self.price_db['Наименование'][i])
            ws.cell(row=i + 1, column=2, value=self.price_db['Цена'][i])
            ws.cell(row=i + 1, column=3, value=self.price_db['Цена2'][i])
            ws.cell(row=i + 1, column=4, value=self.price_db['дата'][i])
            ws.cell(row=i + 1, column=5, value=self.price_db['Вывод'][i])

        wb.save(filename=path_to_save)


if __name__ == "__main__":
    list_db = [[db1, 'mvideo.xlsx'], [db2, 'mts.xlsx'], [db3, 'dns.xlsx'], [db4, 'eldorado.xlsx']]
    action3 = input('Выберите базу данных:\n'
                    '1)МВИДЕО\n'
                    '2)МТС\n'
                    '3)ДНС\n'
                    '4)ЭЛЬДОРАДО\n')

    if action3 == '1':
        v_db = list_db[0][0]
        mg = list_db[0][1]
        t2 = (os.path.join(PathOpen, list_db[0][1]))
    elif action3 == '2':
        v_db = list_db[1][0]
        mg = list_db[1][1]
        t2 = (os.path.join(PathOpen, list_db[1][1]))
    elif action3 == '3':
        v_db = list_db[2][0]
        mg = list_db[2][1]
        t2 = (os.path.join(PathOpen, list_db[2][1]))
    elif action3 == '4':
        v_db = list_db[3][0]
        mg = list_db[3][1]
        t2 = (os.path.join(PathOpen, list_db[3][1]))

    pm = ParserFile(path_to_open=t2, path_to_save=PathSave, db=v_db, mg=mg)
    action = input('Выбери действие:\n '
                   '1) Обновить db из файл(данные парсинга)\n '
                   '2) Импорт базы данных на сервер\n '
                   '3) Выгрузить базу и сохранить в excel\n '
                   '4) Exit\n ')

    if action == '1':
        text, i2 = '', 0
        for i in os.listdir(PathOpen):
            text = text + f'{i2 + 1})' + i + '\n'
            i2 = i2 + 1
        action2 = input(f'Пожалуйста выбери файл из списка:\n{text}')
        t1 = os.listdir(PathOpen)[int(action2) - 1]
        path_data = (os.path.join(PathOpen, t1))

        pm.open_file(path_data)
        pm.unloading_from_the_database()
        pm.find_in_the_database()
    elif action == '2':
        path_data = (os.path.join(os.getcwd(), 'data'))
        text = ''
        i2 = 0
        for i in os.listdir(path_data):
            text = text + f'{i2 + 1})' + i + '\n'
            i2 = i2 + 1
        action2 = input(f'\nПожалуйста выбери файл из списка:\n\n{text}')
        t1 = os.listdir(path_data)[int(action2) - 1]
        path_data = (os.path.join(path_data, t1))
        pm.open_file(path_data)
        pm.unloading_from_the_database()
        pm.find_in_the_database()
    elif action == '3':
        pm.unloading_from_the_database()
        pm.writing_file_excel_db()
    elif action == '4':
        pass
