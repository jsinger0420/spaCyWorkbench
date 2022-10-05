'''
Copyright 2022 SingerLinks Consulting

This file is part of spaCyWorkbench.
spaCyWorkbench is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
spaCyWorkbench is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
You should have received a copy of the GNU General Public License
    along with NLPSpacy. If not, see <https://www.gnu.org/licenses/>.
'''
try:
    from tkinter import *
    from tkinter import ttk
    from tkinter.ttk import *
except ImportError:
    from Tkinter import *
    from Tkinter import ttk
    from Tkinter.ttk import *

from tkinterweb import HtmlFrame 
#from tkinterweb import HtmlLabel
#from pathlib import Path
from spacy import displacy

 
class WinEntityDisplay(Toplevel):
     
    def __init__(self, master = None, sentence=None):
         
        super().__init__(master = master)
        self.title("Named Entities")
        self.master = master
        self.sentence = sentence
        
        self.frmMain = Frame(self)
        self.HTMLText = HtmlFrame(self.frmMain)
        
        # grid the widgets
        self.frmMain.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)
        self.HTMLText.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)

        # handle resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frmMain.grid_columnconfigure(0, weight=1)
        self.frmMain.grid_rowconfigure(0, weight=1)    
        self.HTMLText.grid_columnconfigure(0, weight=1)
        self.HTMLText.grid_rowconfigure(0, weight=1)            
        
        self.generateDiagram()
        
        # size the window
        self.geometry("{}x{}".format(int(self.winfo_screenwidth()*.8), int(self.winfo_screenheight()*.7)))
        
    def generateDiagram(self):
        # generate html
        myHTML = displacy.render(self.sentence, style="ent")
        # replace mark tags with span tags so htmllabel will work.  
        fix1 = myHTML.replace("<mark", "<span")
        fix2 = fix1.replace("</mark","</span")
#        print(fix2)
        # display the text
        self.HTMLText.load_html(fix2) 

