from main import *
import models as db_universal

my_list_file = ['dns.xlsx', 'mts.xlsx', 'mvideo1.xlsx', 'mvideo2.xlsx', 'eldorado.xlsx']
archive_file = os.path.join(PathOpen, 'Архив')
current_time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M") + '_'

input_data = {'mvideo1.xlsx': db_universal.Mvm,
              'mvideo2.xlsx': db_universal.Mvm,
              'dns.xlsx': db_universal.Dns,
              'mts.xlsx': db_universal.Mts,
              'eldorado.xlsx': db_universal.Eld}

for file_folder in os.listdir(PathOpen):
    for my_files in my_list_file:
        if file_folder == my_files:
            u1 = os.path.join(PathOpen, file_folder)
            u2 = os.path.join(archive_file, current_time + file_folder)
            db = input_data.get(my_files)
            print(db)
            pm = ParserFile(path_to_open=u1, path_to_save=PathSave, db=db_universal, mg=my_files, db_shop=db)
            pm.open_file()  # Открывам файл
            pm.file_processing()  # Готовим данные к обработке
            pm.unloading_from_the_database()  # Сохраняем данные в словарь
            pm.find_in_the_database()
            pm.writing_database_price()  # Запись новых данных
            pm.updating_database_price()  # Обновление данных
            # os.replace(src=u1, dst=u2)
