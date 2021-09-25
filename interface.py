from ParsFile import *

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
                   '4) Удалить базу данных\n '
                   '5) Exit\n ')

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
        pm.import_db()
        pm.writing_database_price()  # Запись новых данных
    elif action == '3':
        pm.unloading_from_the_database()
        pm.writing_file_excel_db()
    elif action == '4':
        action = input('Выбери действие:\n '
                       '1) Подтвердите удаление данных\n '
                       '2) Отмена\n ')
        if action == 1:
            pm.delete_db()
        else:
            pass
    elif action == '5':
        pass
