import logging
import os
import re
import shutil
import time

logger_ex = logging.getLogger('[Exception_logger]')
logger_info = logging.getLogger('[Data_logger]')
logger_ex.setLevel(logging.ERROR)
logger_info.setLevel(logging.INFO)



s_handler = logging.StreamHandler()
ex_f_handler = logging.FileHandler('ex_file.log')
data_f_handler = logging.FileHandler('server.log')


common_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(common_format)
ex_f_handler.setFormatter(common_format)
data_f_handler.setFormatter(common_format)

# Add handlers to the logger_obj
logger_ex.addHandler(s_handler)
logger_ex.addHandler(ex_f_handler)

logger_info.addHandler(s_handler)
logger_info.addHandler(data_f_handler)


class InvalidValueFolderError(Exception): # исключение под невалидные имена файлов
    """ Incorrect folder name is used """

class ElementNotExistError(Exception): # исключение под несуществующие каталоги
    """ The specified directory was not found """

def _is_unsafe_folder_name(path: str) -> bool:
    # security check
    return bool(re.search(r'(^|[\\/])\.\.($|[\\/])', path))  #возвращает True если нашел небезопасное имя

def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.
    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.
    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if _is_unsafe_folder_name(path):
        logger_ex.error(f'An InvalidValueFolderError exception occurred.Incorrect value of folder: {path}')
        raise InvalidValueFolderError(f'Incorrect value of folder: {path}')  # если имя(путь) некорректный - выбрасываем исключение

    if not os.path.exists(path): #False т.к.условие if not, но изначально os.path.exists(path) = True, если path указывает на существующий путь или дескриптор открытого файла
        if autocreate:   # по умолчанию True
            os.makedirs(path) # создаёт директорию, создавая при этом промежуточные директории.
        else:
            logger_ex.error(f'An ElementNotExistError exception occurred.Directory {path} is not found')
            raise ElementNotExistError(f'Directory {path} is not found')
    os.chdir(path)  #смена текущей директории
    logger_info.debug(f'change working directory to {path}')


def get_files() -> list:
    """Get info about all files in working directory.
    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    path = os.getcwd() #текущая рабочая директория
    # get list of files in `path`
    files = []
    for root, dirnames, filenames in os.walk(path): #генерация имён файлов в дереве каталогов,возвращает кортеж (путь к каталогу, список каталогов, список файлов)
        for filename in filenames:
            files.append(os.path.join(root, filename)) # заполняем список полученными полными путями к файлам
    # collect information about each file

    data = []  # список словарей, далее заполним значениями
    prefix_size = len(path) + 1  #длина пути в текущий католог + включая слеш (перед именем файла)
    for full_filename in files: #пробегаем по списку файлов
        filename = full_filename[prefix_size:] # забираем имя файла
        data.append({
            'name': filename,
            #'create_date': TimeUtils.floattime_to_datatime(os.path.getctime(full_filename)),
            #'edit_date': TimeUtils.floattime_to_datatime(os.path.getmtime(full_filename)),   #  не работает TimeUtils, нужно разобраться
            'create_date': time.ctime(os.path.getctime(full_filename)),
            'edit_date':   time.ctime(os.path.getmtime(full_filename)),
            'size': str(round((os.path.getsize(full_filename)/1024),2))+' KByte',
        }) #заполняем ранее созданный список данными о каждом файле в текущем каталоге
    logger_info.debug(f'returned information about files in the {path} directory ')
    return data # выводим информацию в виде списка словарей



def _filename_to_local_path(filename: str, folder_autocreate: bool = False) -> str:
    """Get local path for filename.
    Args:
        filename (str): Filename
        folder_autocreate (bool): Create a subfolder if True
    Returns:
        (str) Local path.
    Raises:
        ValueError: if filename is invalid.
    """

    if _is_unsafe_folder_name(filename):
        logger_ex.error(f'An InvalidValueFolderError exception occurred.Incorrect value of filename: {filename}')
        raise InvalidValueFolderError(f'Incorrect value of filename: {filename}')  # если имя(путь) некорректный - выбрасываем исключение

    path = os.getcwd() #текущая рабочая директория
    full_filename = os.path.join(path, filename) # объединяем текущий путь + переданное наименование файла

    folder = os.path.dirname(full_filename) #  получаем имя директории пути filename
    if folder_autocreate:
        os.makedirs(folder) # создаем папку, если получили True
    logger_info.debug('full name file {filename} returned')
    return full_filename # выводим полное имя файла


def get_file_data(filename: str) -> dict:
    """Get full info about file.
    Args:
        filename (str): Filename.
    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes
    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    local_file = _filename_to_local_path(filename) # получение через функцию полного имени файла
    if not os.path.exists(local_file): #False т.к.условие if not, но изначально os.path.exists(path) = True, если path указывает на существующий путь или дескриптор открытого файла
        logger_ex.error(f'An ElementNotExistError exception occurred.File {filename} does not exist')
        raise ElementNotExistError(f'File {filename} does not exist') # если файла нет - выбрасываем исключение

    with open(local_file, 'rb') as file_handler: # открываем файл на чтение
        logger_info.debug(f'information about the {filename} file was returned')
        return {
            'name': filename,
            'create_date': time.ctime(os.path.getctime(local_file)),
            'edit_date':   time.ctime(os.path.getmtime(local_file)),
            'size': str(round((os.path.getsize(local_file)/1024),2))+' KByte',
            'context': file_handler.read(),
        } # собираем дынные о файле в словарь и выводим


def create_file(filename: str, content: str = None) -> dict:
    """Create a new file.
    Args:
        filename (str): Filename.
        content (str): String with file content.
    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes
    Raises:
        ValueError: if filename is invalid.
    """

    local_file = _filename_to_local_path(filename) # получение через функцию полного имени файла

    if os.path.exists(local_file): #os.path.exists(path) = True, если path указывает на существующий путь
        logging.warning('file %s exists', local_file) # выводим сообщение о существовании файла

    with open(local_file, 'wb') as file_handler: # открываем файл на запись
        if content: # если контент был проставлен, то записываем его в новый файл, если нет то пропускаем блок  -- bool(None) == False
            data = bytes(content)
            file_handler.write(data)
    logger_info.info(f'{filename} file created')
    return {
        'name': filename,
        'create_date': time.ctime(os.path.getctime(local_file)),
        'size': str(round((os.path.getsize(local_file)/1024),2))+' KByte',
        'content': content,
    } # собираем дынные о файле в словарь и выводим


def delete_file(filename: str) -> None:
    """Delete file.
    Args:
        filename (str): filename
    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    local_file = _filename_to_local_path(filename) # получение через функцию полного имени файла

    if _is_unsafe_folder_name(filename):
        logger_ex.error(f'An InvalidValueFolderError exception occurred.Incorrect value of filename: {filename}')
        raise InvalidValueFolderError(f'Incorrect value of filename: {filename}') # если имя(путь) некорректный - выбрасываем исключение
    if not os.path.exists(local_file): #False т.к.условие if not, но изначально os.path.exists(path) = True, если path указывает на существующий путь
        logger_ex.error(f'An ElementNotExistError exception occurred.File {filename} does not exist')
        raise ElementNotExistError(f'File {filename} does not exist') # если такого файла нет - выбрасываем исключение

    if os.path.isdir(local_file): # проверка является ли путь директорией (иначе файлом)
        shutil.rmtree(local_file) #удаляет текущую директорию и все поддиректории
    else:
        os.remove(local_file) # удаляет файл
    logger_info.info(f'{filename} file deleted')

