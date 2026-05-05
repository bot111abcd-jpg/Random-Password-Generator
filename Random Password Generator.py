import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500") # Увеличим размер окна для лучшего отображения истории

        self.history_file = "password_history.json"
        self.password_history = self.load_history()

        self.create_widgets()
        self.populate_history_table()

    def create_widgets(self):
        # --- Секция настроек ---
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding="10")
        settings_frame.pack(pady=10, padx=10, fill="x")

        # Ползунок длины пароля
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.password_length_slider = ttk.Scale(settings_frame, from_=8, to=64, orient="horizontal", command=self.update_length_label)
        self.password_length_slider.set(12)  # Значение по умолчанию
        self.password_length_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2, padx=5, pady=5)

        # Чекбоксы для выбора символов
        self.include_digits = tk.BooleanVar()
        self.include_letters = tk.BooleanVar()
        self.include_symbols = tk.BooleanVar()

        self.include_digits.set(True)
        self.include_letters.set(True)
        self.include_symbols.set(True)

        ttk.Checkbutton(settings_frame, text="Цифры", variable=self.include_digits).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(settings_frame, text="Буквы", variable=self.include_letters).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(settings_frame, text="Спецсимволы", variable=self.include_symbols).grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Кнопка генерации
        self.generate_button = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_button.grid(row=2, column=0, columnspan=3, pady=10)

        # --- Поле для вывода пароля ---
        output_frame = ttk.LabelFrame(self.root, text="Сгенерированный пароль", padding="10")
        output_frame.pack(pady=10, padx=10, fill="x")

        self.password_entry = ttk.Entry(output_frame, width=50, font=("Arial", 12))
        self.password_entry.pack(pady=5)

        # --- Секция истории ---
        history_frame = ttk.LabelFrame(self.root, text="История генераций", padding="10")
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, width=70, height=10, font=("Arial", 10))
        self.history_text.pack(pady=5, fill="both", expand=True)
        self.history_text.config(state=tk.DISABLED) # Запрещаем редактирование истории напрямую

    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))

    def generate_password(self):
        length = int(self.password_length_slider.get())
        characters = ""
        if self.include_digits.get():
            characters += string.digits
        if self.include_letters.get():
            characters += string.ascii_letters
        if self.include_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите хотя бы один тип символов.")
            return

        # Проверка минимальной/максимальной длины (хотя ползунок уже ограничивает)
        min_length = 8
        max_length = 64
        if not (min_length <= length <= max_length):
            messagebox.showwarning("Предупреждение", f"Длина пароля должна быть от {min_length} до {max_length} символов.")
            return

        try:
            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.add_to_history(password)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать пароль: {e}")

    def add_to_history(self, password):
        self.password_history.append(password)
        self.save_history()
        self.update_history_display()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return [] # Если файл пустой или поврежден
            except Exception as e:
                print(f"Ошибка при загрузке истории: {e}")
                return []
        return []

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.password_history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")

    def update_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for i, pwd in enumerate(self.password_history):
            self.history_text.insert(tk.END, f"{i+1}. {pwd}\n")
        self.history_text.config(state=tk.DISABLED)

    def populate_history_table(self):
        self.update_history_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
