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
'''
WinSentenceDiagram is a standalone application that demonstrates how to display a sentence diagram generated by spaCy.
The sentence text is hard coded for simplicity.
For a more complete solution look at spaCyWorkbench.py
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
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import spacy
from spacy import displacy

class WinSentenceDiagram(Tk):
     
    def __init__(self):
         
        super().__init__()
        self.title("spaCy Sentence Diagram")
        
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
        
        # sentence text
        self.text = "spaCy can create an image file that contains a diagram of a sentence."
        
        # load spaCy model
        self.loadSpacyModel()
        
        # create the doc object
        self.createDoc()
        
        # generate the diagram image and display it
        self.generateDiagram()
        
        # size the window
        self.geometry("{}x{}".format(int(self.winfo_screenwidth()*.8), int(self.winfo_screenheight()*.7)))

    def loadSpacyModel(self):
        'load the SpaCy Model'
        self.NLP = None
        try:
            modelName = "C:\\Users\\jsing\\pyenv\\NLP\\Lib\\site-packages\\en_core_web_sm\\en_core_web_sm-3.2.0"
            self.NLP = spacy.load(modelName)
        except Exception as e:
            print("Error loading SpaCy pipeline:{} - {}".format(modelName, e))  
        
    def createDoc(self):
        '''
        Create a spacy document object from the selected text in the raw text area.
        '''
        self.doc = None
        try:
            # create the document object
            self.doc = self.NLP(self.text)
        except Exception as e:
            print("Error Creating Doc Object - {}".format(e))
        
    def generateDiagram(self):

        # convert the iterator to a list and get the first sentence span in the document object
        self.sentence = list(self.doc.sents)[0]
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



'''start the app running'''
if __name__ == "__main__":
    app = WinSentenceDiagram()
    app.mainloop()
