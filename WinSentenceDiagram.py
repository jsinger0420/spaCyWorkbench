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


from pathlib import Path
import PIL
from PIL import ImageTk 
from spacy import displacy
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
 
class WinSentenceDiagram(Toplevel):
     
    def __init__(self, master = None, sentence=None):
         
        super().__init__(master = master)
        self.title("Sentence Diagram")
        self.master = master
        self.sentence = sentence
        
        self.tab3 = ttk.Frame(self)
        self.diagramCanvas = Canvas(self.tab3)
        #vertical scrollbar
        self.vsbDiagram = Scrollbar(self.tab3, orient=VERTICAL)
        self.diagramCanvas.config(yscrollcommand=self.vsbDiagram.set)
        self.vsbDiagram.config(command=self.diagramCanvas.yview)        
        # horizaontal scrollbar
        self.hsbDiagram = Scrollbar(self.tab3, orient=HORIZONTAL)
        self.hsbDiagram.config(command=self.diagramCanvas.xview)     
        self.diagramCanvas.config(xscrollcommand=self.hsbDiagram.set)
        
        # grid the widgets
        self.tab3.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)
        self.diagramCanvas.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)
        self.vsbDiagram.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=NS)
        self.hsbDiagram.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=EW)    
        # handle resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tab3.grid_columnconfigure(0, weight=1)
        self.tab3.grid_rowconfigure(0, weight=1)    
        
        self.generateDiagram()
        
        # size the window
        self.geometry("{}x{}".format(int(self.winfo_screenwidth()*.8), int(self.winfo_screenheight()*.7)))
        
    def generateDiagram(self):
        # generate svg diagram
        mySVG = displacy.render(self.sentence, style="dep")
        # save svg as a png image file
        output_path = Path('temp.svg')
        output_path.open("w", encoding="utf-8").write(mySVG)
        drawing = svg2rlg('temp.svg')        
        renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
        # get the image file and make load it into the frame
        with PIL.Image.open('temp.png') as img:
            pimg = ImageTk.PhotoImage(img)
        self.diagramCanvas.create_image(0,0,anchor='nw',image=pimg)
        self.diagramCanvas.configure(scrollregion=self.diagramCanvas.bbox("all"))
        # position to the bottom of the diagram
        self.diagramCanvas.yview_moveto('1.0')

