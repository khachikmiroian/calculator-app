import tkinter as tk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title('Calculator')
        self.master.geometry('375x450+100+200')
        self.master.configure(bg='#333333')

        self.entry = tk.Entry(master, justify=tk.RIGHT, font=("Arial", 24), bg="#000000", fg="#ffffff")
        self.entry.insert(0, '0')
        self.entry.grid(row=0, column=0, columnspan=4, sticky='we', padx=5, pady=5)

        self.create_buttons()
        self.bind_keys()

    def create_buttons(self):
        buttons = [
            ('1', 1, 0), ('2', 1, 1), ('3', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
            ('.', 4, 0), ('0', 4, 1), ('=', 4, 2), ('/', 4, 3),
            ('√', 5, 0), ('^', 5, 1), ('C', 5, 2)
        ]

        for (text, row, col) in buttons:
            if text in '+-*/^':
                self.create_button(text, self.add_operation, row, col, '#ffcc66', '#ffaa00')
            elif text == '=':
                self.create_button(text, self.calculate, row, col, '#66ff66', '#33cc33')
            elif text == 'C':
                self.create_button(text, self.clear, row, col, '#ff6666', '#ff3333')
            elif text == '√':
                self.create_button(text, self.add_sqrt, row, col, '#ffcc66', '#ffaa00')
            else:
                self.create_button(text, self.add_digit, row, col, '#e0e0e0', '#d4d4d4')

    def create_button(self, text, command, row, col, bg, active_bg):
        button = tk.Button(self.master, text=text, command=lambda: command(text),
                           font=("Arial", 18), bg=bg, fg="#000000",
                           activebackground=active_bg, padx=10, pady=10)
        button.grid(row=row, column=col, sticky='wens', padx=5, pady=5)

    def bind_keys(self):
        self.master.bind('<Key>', self.key_press)

    def add_digit(self, digit):
        value = self.entry.get()
        if value == '0':
            value = ''
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value + digit)

    def clear(self, _=None):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, '0')

    def add_operation(self, operation, _=None):
        value = self.entry.get()
        if value and value[-1] in '+-*/^':
            value = value[:-1]
        elif any(op in value for op in '+-*/^'):
            self.calculate()
            value = self.entry.get()
        if value and (value[-1] not in '+-*/^'):
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value + operation)

    def add_sqrt(self, _=None):
        try:
            result = math.sqrt(float(self.entry.get()))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Error")

    def calculate(self, _=None):
        value = self.entry.get()
        if value and value[-1] in '+-*/^':
            value = value[:-1]
        self.entry.delete(0, tk.END)
        try:
            # Replace '^' with '**' for power operations
            value = value.replace('^', '**')
            result = eval(value)
            self.entry.insert(0, result)
        except ZeroDivisionError:
            self.entry.insert(0, "Cannot divide by zero")
        except Exception:
            self.entry.insert(0, "Error")

    def key_press(self, event):
        if event.char.isdigit():
            self.add_digit(event.char)
        elif event.char in '+-*/^':
            self.add_operation(event.char)
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.clear()
        elif event.char == '.':
            self.add_digit('.')

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
