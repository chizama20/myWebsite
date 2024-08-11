from typing import Any, Tuple
import customtkinter as ctk
from settings import *  # Ensure this file contains the proper color definitions and font size

class App(ctk.CTk):
    def __init__(self):
        # Window setup
        super().__init__()
        self.configure(bg_color=GREEN)  # Use bg_color or fg_color based on actual library support
        self.title('')
        self.geometry('600x600+100+100')  # Position the window at (100, 100)
        self.resizable(False, False)

        # Data
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()

        # Tracing
        self.height_int.trace('w', self.update_bmi)
        self.weight_float.trace('w', self.update_bmi)

        # Widgets
        ResultText(self, self.bmi_string)
        WeightInput(self, self.weight_float)
        HeightInput(self, self.height_int)
        UnitSwitcher(self)

        self.mainloop()

    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2, 2)
        self.bmi_string.set(bmi_result)

class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family='Calibri', size=150, weight='bold')
        super().__init__(master=parent, textvariable=bmi_string, font=font, text_color=WHITE)
        self.grid(column=0, row=0, rowspan=2, sticky='nsew')

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.weight_float = weight_float

        # Update the text to show current weight
        self.output_string = ctk.StringVar()
        self.update_weight()

        # Layout configuration
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')

        # Text
        font = ctk.CTkFont(family='Calibri', size=INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, textvariable=self.output_string, text_color=BLACK, font=font)
        label.grid(row=0, column=2)

        # Buttons
        minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'large')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY)
        minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)

        plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'large')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY)
        plus_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)

        small_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'small')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY)
        small_plus_button.grid(row=0, column=3, padx=8, pady=8)

        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'small')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY)
        small_minus_button.grid(row=0, column=1, padx=8, pady=8)

    def update_weight(self, info=None):
        if info:
            amount = 1 if info[1] == 'large' else 0.1
            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        self.output_string.set(f'{round(self.weight_float.get(), 1)}kg')

class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

        # Widgets
        slider = ctk.CTkSlider(
            master=self,
            command=self.update_text,
            button_color=GREEN,
            button_hover_color=GRAY,
            progress_color=GREEN,
            fg_color=LIGHT_GRAY,
            variable=height_int,
            from_=100,
            to=250
        )
        slider.pack(side='left', fill='x', expand=True, pady=10, padx=10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        output_text = ctk.CTkLabel(self, textvariable=self.output_string, text_color=BLACK, font=ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE))
        output_text.pack(pady=10)  # Use pack() to place the label

    def update_text(self, amount):
        text_string = str(int(amount))
        meter = text_string[0]
        cm = text_string[1:]
        self.output_string.set(f'{meter}.{cm}m')

class UnitSwitcher(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(master=parent, text='metric', text_color=DARK_GREEN, font=ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold'))
        self.place(relx=0.98, rely=0.01, anchor='ne')

if __name__ == '__main__':
    App()

