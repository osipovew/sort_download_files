import os
import pathlib
import shutil
import getpass

count_ = 0
paths = rf"C:\Users\{getpass.getuser()}\Downloads"


def sort(extension):
    check_path = os.path.join(f"{paths}\\{extension}")
    src_path = f"{paths}\\{files}"
    if os.path.isfile(check_path):
        file_extension = pathlib.Path(extension).suffix
        if not os.path.exists(f"{paths}\\{file_extension[1:]}"):
            os.mkdir(f"{paths}\\{file_extension[1:]}")
        shutil.move(src_path, f"{paths}\\{file_extension[1:]}\\{files}")
        return True
    else:
        if os.path.isdir(check_path):
            if next(os.scandir(src_path), None) is None:
                shutil.rmtree(src_path)
                print(f"Удалена пуская папка: {src_path}")


for files in os.listdir(paths):
    if sort(files):
        count_ += 1
print(f"перемещено файлов: {count_}")
