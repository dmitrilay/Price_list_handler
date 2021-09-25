from ParsFile import *

my_list_file = ['dns.xlsx', 'mts.xlsx', 'mvideo1.xlsx', 'mvideo2.xlsx', 'eldorado.xlsx']
archive_file = os.path.join(PathOpen, 'Архив')
current_time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M") + '_'

input_data = {'mvideo1.xlsx': [db1, 'mvideo'],
              'mvideo2.xlsx': [db1, 'mvideo'],
              'dns.xlsx': [db3, 'dns'],
              'mts.xlsx': [db2, 'mts'],
              'eldorado.xlsx': [db4, 'eldorado'], }

for file_folder in os.listdir(PathOpen):
    for my_files in my_list_file:
        if file_folder == my_files:
            u1 = os.path.join(PathOpen, file_folder)
            u2 = os.path.join(archive_file, current_time + file_folder)
            pr1 = input_data.get(my_files)
            if pr1 is not None:
                pm = ParserFile(path_to_open=u1, path_to_save=PathSave, db=pr1[0], mg=my_files)
                pm.open_file()  # Открывам файл
                pm.file_processing()  # Готовим данные к обработке
                pm.unloading_from_the_database()  # Сохраняем данные в словарь
                pm.find_in_the_database()
                pm.writing_database_price()  # Запись новых данных
                pm.updating_database_price()  # Обновление данных
                # os.replace(src=u1, dst=u2)
