import logging
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import scrolledtext
import os
import pathlib
import shutil

global_dict = {
    "src_path": "None"
}


class TextHandler(logging.Handler):
    # This class allows logging messages to be sent to a Tkinter Text widget
    def __init__(self, text):
        # Initialize the instance of the class
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        # Emit a message to the Text widget
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(tk.END)

        self.text.after(0, append)


# Initialize the Tkinter GUI
root = tk.Tk()
root.title('Sortirator')
root.geometry('1024x868')

# func
def choose_directory():
    global global_dict
    directory = fd.askdirectory(title="Открыть папку", initialdir="/")
    if directory:
        global_dict['src_path'] = directory
        logging.info(f"Выбрана директория: {global_dict['src_path']}")


def has_extension(filename):
    return bool(pathlib.Path(filename).suffix)


def sort_files():
    if global_dict["src_path"] != "None":
        for file in os.listdir(global_dict["src_path"]):
            full_path = os.path.join(f"{global_dict['src_path']}/{file}")

            if os.path.isfile(full_path):
                if has_extension(file):
                    file_extension = pathlib.Path(file).suffix[1:]
                    new_path = os.path.join(f"{global_dict['src_path']}/{file_extension}")
                    if not os.path.exists(new_path):
                        os.mkdir(new_path)
                        logging.info(f"Создание папки: {new_path}")
                    shutil.move(full_path, f"{new_path}/{file}")
                    logging.info(f"Перемещение файла: {file} в {new_path}")
                else:
                    logging.warning(f"Файл без расширения: {file}")

    else:
        logging.error("Система не может найти указанный путь.")
    logging.info("Операция завершена")


# Filemenu
menubar = tk.Menu(root)
file = tk.Menu(menubar, tearoff=1)
menubar.add_cascade(label='Папка', menu=file)
file.add_command(label='Выбрать папку', command=choose_directory)
file.add_command(label='Сохранить историю', command=None)
file.add_separator()
file.add_command(label='Выход', command=root.destroy)

# Editmenu
edit = tk.Menu(menubar, tearoff=1)
menubar.add_cascade(label='История', menu=edit)
edit.add_separator()
edit.add_command(label='Найти', command=None)

# Helpmenu
help_ = tk.Menu(menubar, tearoff=1)
menubar.add_cascade(label='Помощь', menu=help_)
help_.add_command(label='Проверить обновления', command=None)
help_.add_separator()
help_.add_command(label='О программе', command=None)
root.config(menu=menubar)

# Create a Text widget for logging messages
text = scrolledtext.ScrolledText(root)
text.configure(state='disabled')
text.pack(fill=tk.BOTH, expand=True)

# button
btn_dir = tk.Button(text="Начать сортировку", command=sort_files)
btn_dir.pack(padx=60, pady=10)

# Create a custom formatter and add it to the logging system
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = TextHandler(text)
handler.setFormatter(formatter)

# Set the logging level and add the custom handler to the root logger
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

if __name__ == "__main__":
    root.mainloop()
