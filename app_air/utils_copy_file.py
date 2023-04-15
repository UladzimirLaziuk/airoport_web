import os
import re
import shutil


def copy_and_rename_files(source_folder, destination_folder, directory_exclude_to_rename=None, new_prefix="new_"):
    """
    Копирует содержимое папки source_folder в папку destination_folder.
    Переименовывает выбранные файлы из списка files_to_rename, добавляя к их именам префикс new_prefix.
    """
    # Копируем содержимое папки
    shutil.copytree(source_folder, destination_folder)

    # Получаем список файлов в папке
    data = os.listdir(destination_folder)

    # Проходим по списку файлов для переименования
    for file in data:
        if file in directory_exclude_to_rename:
            continue
        if os.path.isdir(file):
            copy_and_rename_files(file, os.path.join(destination_folder, file), directory_exclude_to_rename,
                                  new_prefix=new_prefix)
            # Если это файл, переименовываем его
        elif os.path.isfile(file):
            # Строим старый и новый пути к файлу
            old_file_path = file
            new_file_path = os.path.join(new_prefix + file)

            # Переименовываем файл
            os.rename(old_file_path, new_file_path)
        # Строим старый и новый пути к файлу
        old_file_path = os.path.join(destination_folder, file)
        new_file_path = os.path.join(destination_folder, new_prefix + file)

        # Переименовываем файл
        os.rename(old_file_path, new_file_path)


def copy_and_rename_file(filename, arg, path_static='static/img/home/'):
    # Формируем путь и имя файла
    basename = os.path.basename(filename)
    name, extension = os.path.splitext(basename)
    new_basename = f"{name}_{arg}{extension}"
    src = os.path.join(path_static, basename)
    dst = os.path.join(path_static, new_basename)

    # Копируем и переименовываем файл
    shutil.copy(src, dst)


def copy_and_full_rename(filename, arg, path_static='static/img/home/'):
    basename = os.path.basename(filename)
    name, file_extension = os.path.splitext(basename)

    list_extensions = ['.webp', file_extension]

    for extension in list_extensions:

        new_basename = f"{arg}{extension}"
        src = os.path.join('static/dir_basis_images', basename)
        dst = os.path.join(path_static, new_basename)
        if not os.path.exists(dst):
            shutil.copy(src, dst)


def open_read_file(path_file):
    with open(path_file, 'r', encoding="utf-8") as f:
        webpage = f.read()

    return webpage


def write_html(path_file, webpage):
    with open(path_file, 'w') as fp:
        # write the current soup content
        fp.write(webpage)


def pase_page(webpage, patt_search=r'img/', file_path_to_write=None):
    """@img/school-bg.png"""
    pattern = re.compile(rf'({patt_search})([^.]*).(svg|png|jpeg|jpg|webp|ico)')
    find_iter_data = re.finditer(pattern, webpage)

    list_replace = []
    for m in find_iter_data:
        # print('%02d-%02d: %content_new %content_new %content_new %content_new ' % (m.start(), m.end(), m.group(0), m.group(1), m.group(2), m.group(3)))
        # str_replace = f'/static/img/{m.group(2)}.{m.group(3)}'
        str_replace = '#% static "img/{0}.{1}" %#'.format(m.group(2), m.group(3)).replace('#', '{', 1).replace('#', '}',
                                                                                                               1)
        list_replace.append({str_replace: (m.group(0), m.start(), m.end())})  # dict_replace.copy())

    webpage_new = webpage[:]
    cursor_start = 0
    content_new = ''
    for element in list_replace:
        for string_for_replace, (patt, m_start, m_end) in element.items():
            content_new += webpage_new[cursor_start:m_start] + string_for_replace
            cursor_start = m_end

    content_new += webpage_new[cursor_start:]
    write_html(file_path_to_write, content_new)


def replace_static_urls_in_html_file(html_file_path: str, static_path: str = '', media_path: str = ''):
    """
    Заменяет в указанном файле все вхождения ссылок на статические и медиафайлы на ссылки вида
    `{% static 'path/to/static/file' %}` и `{% media 'path/to/media/file' %}` соответственно.
    """
    with open(html_file_path, 'r+') as f:
        # Считываем содержимое файла
        content = f.read()

        # Ищем все вхождения ссылок на статические файлыr'src="(.*?).js"
        static_urls = re.findall(r'src="(.*.js)', content)

        # Заменяем найденные ссылки на ссылки вида `{% static 'path/to/static/file' %}`
        for url in static_urls:
            new_url = "src='{% static '" + url + "' %}'"
            content = content.replace(f'src="{url}"', new_url)

        css_urls = re.findall(r'href="(.*.css)"', content)
        for url in css_urls:
            new_url = "href='{% static '" + url + "' %}'"
            content = content.replace(f'href="{url}"', new_url)
        f.seek(0)
        f.write(content)
        f.truncate()


def parse_file_compile(path_file):
    file_html = open_read_file(path_file)
    file_path_to_write = path_file
    pase_page(file_html, patt_search=r'img/', file_path_to_write=file_path_to_write)
