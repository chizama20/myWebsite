import customtkinter as ctk
from buttons import Button, ImageButton, NumButton, MathButton, MathImageButton
from PIL import Image
import darkdetect
from settings import *

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        # Setup
        super().__init__(fg_color=(WHITE, BLACK))
        ctk.set_appearance_mode('dark' if is_dark else 'light')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')

        # Grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(MAIN_COLS)), weight=1, uniform='a')

        # Data 
        self.result_string = ctk.StringVar(value='0')
        self.formula_string = ctk.StringVar(value='0')
        self.display_nums = []
        self.full_operation = []
        
        # Widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
    # Fonts
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)

        # Output labels
        OutputLabel(self, 0, 'SE', main_font, self.formula_string)  # Formula
        OutputLabel(self, 1, 'E', result_font, self.result_string)  # Result

        # Clear (AC) button
        Button(
            parent=self,
            func=self.clear,
            text=OPERATORS['clear']['text'],
            col=OPERATORS['clear']['col'],
            row=OPERATORS['clear']['row'],
            font=main_font
        )

        # Percentage button
        Button(
            parent=self,
            func=self.percent,
            text=OPERATORS['percent']['text'],
            col=OPERATORS['percent']['col'],
            row=OPERATORS['percent']['row'],
            font=main_font
        )

        # Invert (±) button
        Button(
            parent=self,
            func=self.invert,
            text='±',
            col=OPERATORS['invert']['col'],
            row=OPERATORS['invert']['row'],
            font=main_font
        )

        # Number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent=self,
                text=str(num),
                func=self.num_press,
                col=data['col'],
                row=data['row'],
                font=main_font,
                span=data['span']
            )

        # Math buttons
        for operator, data in MATH_POSITIONS.items():
            MathButton(
                parent=self,
                text=data['character'],
                operator=operator,
                func=self.math_press,
                col=data['col'],
                row=data['row'],
                font=main_font
            )


    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number)

    def math_press(self, value):
        current_number = ''.join(self.display_nums)

        if current_number:
            self.full_operation.append(current_number)
            if value != '=':

                #update data
                self.full_operation.append(value)
                self.display_nums.clear()
                
                #update output
                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))
            
            
            else:
                formula = ''.join(self.full_operation)
                result = eval(formula)

                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)

                self.full_operation.clear()
                self.display_nums = [str(result)]

                self.result_string.set(result)
                self.formula_string.set(formula)
        
    def clear(self):
        self.result_string.set(0)
        self.formula_string.set('')

        self.display_nums.clear()
        self.full_operation.clear()
        
    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent_number = current_number / 100
            self.display_nums = list(str(percent_number))
            self.result_string.set(''.join(self.display_nums))


    def invert(self):
        current_number = ''.join(self.display_nums)
        if current_number:
            if float(current_number) > 0:
                self.display_nums.insert(0, '-')
            else:
                del self.display_nums[0]

            self.result_string.set(''.join(self.display_nums))


class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master=parent, font=font, textvariable=string_var)
        self.grid(column=0, columnspan=4, row=row, sticky=anchor, padx=10)

if __name__ == '__main__':
    Calculator(darkdetect.isDark())
    #Calculator(False) for light screen

