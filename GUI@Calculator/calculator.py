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
        
        # Invert button with image
        invert_image = ctk.CTkImage(
            light_image=Image.open(OPERATORS['invert']['image_path']['light']),
            dark_image=Image.open(OPERATORS['invert']['image_path']['dark']),
        )
        ImageButton(
            parent=self,  
            func=self.invert, 
            col=OPERATORS['invert']['col'], 
            row=OPERATORS['invert']['row'], 
            image=invert_image
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

            #math buttons
            for operator, data in MATH_POSITIONS.items():
                if data['image path']:
                    divide_image = ctk.CTkImage(
                        light_image= Image.open(data['image path']['dark']),
                        dark_image= Image.open(data['image path']['light']),
                    )

                    MathImageButton(
                        parent = self, 
                        operator = operator, 
                        func = self.math_press, 
                        col = data['col'], 
                        row = data['row'], 
                        image = divide_image)
                else:
                    MathButton(
                        parent = self, 
                        text = data['character'], 
                        operator = operator, 
                        func = self.math_press, 
                        col = data['col'], 
                        row = data['row'], 
                        font = main_font
                    )


    def num_press(self, value):
        print(value)

    def math_press(self, value):
        print(value)
        
    def clear(self):
        print('clear')
        
    def percent(self):
        print('percent')

    def invert(self):
        pass

class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master=parent, font=font, textvariable=string_var)
        self.grid(column=0, columnspan=4, row=row, sticky=anchor, padx=10)

if __name__ == '__main__':
    Calculator(darkdetect.isDark())
    #Calculator(False) for light screen

