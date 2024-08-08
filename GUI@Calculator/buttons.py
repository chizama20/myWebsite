from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    def __init__(self, parent, text, func, col, row, color ='dark-gray', image= None):
        super().__init__(
            master = parent,
            command= func
            text = text,
            corner_radius= STYLING['corner-radius'],
            font = font, 
            fg_color= COLORS[color]['fg'],
            hover_color= COLORS[color]['fg']
            text_color= COLORS[color]['hover']
        )
        if image:
            self.configure
        self.grid(column = col, row = row, sticky = 'NSEW', padx= STYLING['gap'], pady= STYLING['gap'])

class NumButton():
        def __init__(self, parent, func, col, row, image, text= '' color ='light-gray'):


class imageButton(CTkButton):
    def __init__(self, parent, func, col, row, image, text= '' color ='dark-gray'):
        super().__init__(
            master = parent,
            command= func
            text = text,
            corner_radius= STYLING['corner-radius'],
            font = font, 
            fg_color= COLORS[color]['fg'],
            hover_color= COLORS[color]['fg']
            text_color= COLORS[color]['hover']
        )
    
        self.grid(column = col, row = row, sticky = 'NSEW', padx= STYLING['gap'], pady= STYLING['gap'])
