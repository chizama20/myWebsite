from typing import Any, Tuple
import customtkinter as ctk
from tkcalendar import Calendar
from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.configure(bg_color=GREEN)
        self.title('BMI Tracker')
        self.geometry('800x800')
        self.resizable(False, False)

        # Grid configuration for centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Data
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.unit = ctk.StringVar(value='Metric')
        self.update_bmi()

        # Tracing
        self.height_int.trace('w', self.update_bmi)
        self.weight_float.trace('w', self.update_bmi)
        self.unit.trace('w', self.update_bmi)

        # Widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        # Header
        header = ctk.CTkLabel(self, text="BMI Tracker", font=ctk.CTkFont(family='Calibri', size=24, weight='bold'), text_color=WHITE)
        header.grid(row=0, column=0, pady=(20, 10))

        # Result text
        ResultText(self, self.bmi_string)

        # Weight input
        WeightInput(self, self.weight_float, self.unit)

        # Height input
        HeightInput(self, self.height_int, self.unit)

        # Unit switcher
        UnitSwitcher(self, self.unit)

        # Calendar
        CalendarFrame(self)

    def update_bmi(self, *args):
        if self.unit.get() == 'Metric':
            height_meter = self.height_int.get() / 100
            weight_kg = self.weight_float.get()
            bmi_result = round(weight_kg / height_meter ** 2, 2)
        else:  # Imperial
            height_inch = self.height_int.get()
            weight_lb = self.weight_float.get()
            bmi_result = round((weight_lb / height_inch ** 2) * 703, 2)

        self.bmi_string.set(f'BMI: {bmi_result}')

class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family='Calibri', size=MAIN_TEXT_SIZE, weight='bold')
        super().__init__(master=parent, textvariable=bmi_string, font=font, text_color=WHITE)
        self.grid(column=0, row=1, pady=(10, 20))

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, unit):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=2, sticky='ew', padx=10, pady=10)
        self.weight_float = weight_float
        self.unit = unit

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
            if self.unit.get() == 'Imperial':
                amount = 2 if info[1] == 'large' else 0.5

            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)
        
        unit_label = 'kg' if self.unit.get() == 'Metric' else 'lb'
        self.output_string.set(f'{round(self.weight_float.get(), 1)} {unit_label}')

class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, unit):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        self.height_int = height_int
        self.unit = unit

        # Widgets
        slider = ctk.CTkSlider(
            master=self,
            command=self.update_text,
            button_color=GREEN,
            button_hover_color=GRAY,
            progress_color=GREEN,
            fg_color=LIGHT_GRAY,
            variable=height_int,
            from_=100 if unit.get() == 'Metric' else 39,
            to=250 if unit.get() == 'Metric' else 98
        )
        slider.pack(side='left', fill='x', expand=True, pady=10, padx=10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        output_text = ctk.CTkLabel(self, textvariable=self.output_string, text_color=BLACK, font=ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE))
        output_text.pack(pady=10)

    def update_text(self, amount):
        if self.unit.get() == 'Metric':
            self.output_string.set(f'{amount / 100:.2f} m')
        else:
            self.output_string.set(f'{amount} in')

class UnitSwitcher(ctk.CTkButton):
    def __init__(self, parent, unit):
        super().__init__(master=parent, text='Metric', text_color=DARK_GREEN, font=ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold'))
        self.unit = unit
        self.configure(command=self.switch_units)
        self.place(relx=0.98, rely=0.01, anchor='ne')

    def switch_units(self):
        if self.unit.get() == 'Metric':
            self.unit.set('Imperial')
            self.configure(text='Imperial')
        else:
            self.unit.set('Metric')
            self.configure(text='Metric')

class CalendarFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row=4, column=0, padx=20, pady=20, sticky='ew')

        self.calendar = Calendar(self, selectmode='day')
        self.calendar.pack(side='left', padx=10, pady=10)

        save_button = ctk.CTkButton(self, text="Save BMI", command=self.save_bmi)
        save_button.pack(side='right', padx=10, pady=10)

    def save_bmi(self):
        selected_date = self.calendar.get_date()
        bmi_value = parent.bmi_string.get()
        # You can add functionality to save the date and BMI value as needed.
        print(f"Date: {selected_date}, BMI: {bmi_value}")

if __name__ == '__main__':
    App()
