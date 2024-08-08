import customtkinter as ctk
from buttons import Button, imageButton
from PIL import Image
import darkdetect
from settings import *

class Calculator(ctk.CTk):
    def __init__(self, is_dark):

        #setup
        super().__init__(fg_color=(WHITE, BLACK))
        ctk.set_appearance_mode('dark' if is_dark else 'light')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')

        #grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight = 1, uniform = 'a')
        self.columnconfigure(list(range(MAIN_COLS)), weight = 1, uniform = 'a')

        #data 
        self.result_string =ctk.StringVar(value ='0')
        self.formula_string =ctk.StringVar(value ='0')
        
        #widgets
        self.create_widgets()

        self.mainloop()


    def create_widgets(self):

        #fonts
        main_fonts = ctk.CTkFont(family= FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family= FONT, size=OUTPUT_FONT_SIZE)
        
        #output labels
        OutputLabel(self, 0, 'SE', main_fonts, self.formula_string) #formula
        OutputLabel(self, 1, 'E', result_font, self.result_string) #result

        #clear (AC) button
        Button(
            parent= self, 
            func= self.clear,
            text= OPERATORS['clear']['text'], 
            col= OPERATORS['clear']['col'], 
            row= OPERATORS['clear']['row'],
            font = main_fonts
            )
        
        #percentage
        Button(
            parent= self, 
            func= self.percent,
            text= OPERATORS['percent']['text'], 
            col= OPERATORS['percent']['col'], 
            row= OPERATORS['percent']['row'],
            font = main_fonts
            )
        
        invert_image= ctk.CTkImage(
            light_image= Image.open(OPERATORS['invert']['image path']['dark']),
            dark_image= Image.open(OPERATORS['invert']['image path']['light']),
        )
        imageButton(
            parent= self,  
            func = self.invert, 
            col = OPERATORS['invert']['col'], 
            row = OPERATORS['invert']['row'], 
            image= invert_image
        )
        
        def clear(self):
            pass
        
        def percent(self):
            pass
        
        def percent(self):
            pass    

class OutputLabel(ctk.CTK):
    def __init__(self, parent, row, anchor, font):
        super().__init__(master =parent, font = font, textvariable = string_var)
        self.grid(column= 0, columnspan= 4, row = row, sticky = anchor, padx = 10)
        
        


if __name__ == '__main__':
    Calculator(darkdetect.isDark())

