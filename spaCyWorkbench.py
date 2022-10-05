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
import json
import datetime

from pathlib import Path
import PIL
from PIL import ImageTk 
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from tkinterweb import HtmlFrame 
import spacy
from spacy import displacy

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog as fd 
from tkinter import scrolledtext    
from tkinter import Menu

import WinWorkbenchProps as WinWorkbenchProps

class WorkBench():
    def __init__(self, mode=None, workbenchName=None):
        self.workbenchDict = {}
        self.workbenchDict["workbenchName"] = workbenchName
        if mode == "New":
            self.newWorkbench()
        if mode == "Open":
            self.openWorkbench()
        if mode == "Save":
            self.saveWorkbench()
        
        self.changed = False
    
    def newWorkbench(self):
        self.workbenchDict["workbenchName"] = "Untitled"
        self.workbenchDict["workbenchDir"] = None
        self.workbenchDict["modelName"] = None
        self.workbenchDict["textFile"] = None

        
class spaCyWorkbenchUI(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.app = container
        # create new workbench object
        self.workbench = WorkBench(mode="New")  
        self.NLP = None
        
        # field options
        options = {'padx': 5, 'pady': 5}
                # this hack fixes treeview tag configure problem
        style = ttk.Style(self)
        actualTheme = style.theme_use()
        style.theme_create("copy", parent=actualTheme)
        style.theme_use("copy")
        # frame styles
        style.configure('redFrame.TFrame', background='red')
        style.configure('blueFrame.TFrame', background='blue')
        # configure style for treeviews
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        
        style.configure("mystyle.Treeview",
                background="white",
                foreground="#000000",
                fieldbackground="#E1E1E1")
        style.map('mystyle.Treeview', background=[('selected', '#BFBFBF')])
        
        # menu system
        menu = Menu(self.master)
        self.master.config(menu=menu)
        wbMenu = Menu(menu)
        wbMenu.add_command(label="Open Work Bench", command=self.openWorkbench)        
        wbMenu.add_command(label="Save Work Bench", command=self.saveWorkbench)
        wbMenu.add_command(label="Save Work Bench as...", command=self.saveAsSWBFile)
        wbMenu.add_command(label="Work Bench Properties...", command=self.propertiesDlg)
        wbMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="Work Bench", menu=wbMenu)
        

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        
        self.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=E+W+N+S)
        self.grid_columnconfigure(0, minsize=150, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        
        # main frames
        self.buttonFrame = ttk.Frame(self, style='blueFrame.TFrame')
        self.frmRawText = ttk.LabelFrame(self, text="Raw Text" ) #, style='blueFrame.TFrame')
        self.frmSentences = ttk.LabelFrame(self, text="Sentences" ) # , style='blueFrame.TFrame')
        self.frmDocData= ttk.LabelFrame(self, text="Document Data" ) # , style='blueFrame.TFrame')
        self.frmSentDiagram = ttk.LabelFrame(self, text="Sentence Diagram" ) # , style='blueFrame.TFrame')
        self.frmEntityText = ttk.LabelFrame(self, text="Entity Text" ) # , style='blueFrame.TFrame')
        self.frmTokens = ttk.LabelFrame(self, text="Tokens" ) # , style='blueFrame.TFrame')
        self.buttonFrame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=N+S+E+W)
        #raw text
        self.frmRawText.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
        self.frmRawText.grid_columnconfigure(0, weight=1)
        self.frmRawText.grid_rowconfigure(0, weight=1)            
        #sentences
        self.frmSentences.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
        self.frmSentences.grid_columnconfigure(0, weight=1)
        self.frmSentences.grid_rowconfigure(0, weight=1)      
        # sentence diagram
        self.frmSentDiagram.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
        self.frmSentDiagram.grid_columnconfigure(0, weight=1)
        self.frmSentDiagram.grid_rowconfigure(0, weight=1)       
        # entity text
        self.frmEntityText.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
        self.frmEntityText.grid_columnconfigure(0, weight=1)
        self.frmEntityText.grid_rowconfigure(0, weight=1)        
        # tokens
        self.frmTokens.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
        self.frmTokens.grid_columnconfigure(0, weight=1)
        self.frmTokens.grid_rowconfigure(0, weight=1)                
        # document data grids
        self.frmDocData.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=N+S+E+W)
        # side panel buttons
        self.btnRaw = Button(self.buttonFrame, text = 'Raw Text',  command = self.btnShowRawText) 
        self.btnSentences = Button(self.buttonFrame, text = 'Sentences',  command = self.btnShowSentences) 
        self.btnDocData = Button(self.buttonFrame, text = 'Document Data',  command = self.btnShowDocData) 
        self.btnSentDiagram = Button(self.buttonFrame, text = 'Sentence Diagram',  command = self.btnShowSentDiagram) 
        self.btnEntityText = Button(self.buttonFrame, text = 'Entity Text',  command = self.btnShowEntityText) 
        self.btnTokens = Button(self.buttonFrame, text = 'Tokens',  command = self.btnShowTokens) 
        self.btnRaw.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=W)
        self.btnSentences.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=W)
        self.btnDocData.grid(row = 2, column = 0, padx = 5, pady = 5, sticky=W)
        self.btnSentDiagram.grid(row = 3, column = 0, padx = 5, pady = 5, sticky=W)
        self.btnEntityText.grid(row = 4, column = 0, padx = 5, pady = 5, sticky=W)
        self.btnTokens.grid(row = 5, column = 0, padx = 5, pady = 5, sticky=W)

    
        # scrollable text box for raw text
        self.textArea = scrolledtext.ScrolledText(self.frmRawText, wrap=WORD, font=("Times New Roman", 15))
        self.textArea.bind('<Any-ButtonRelease>', self.textAreaSelect)
        self.textArea.grid(row=0, column=0,  padx = 5, pady = 5, sticky=E+W+N+S)
        self.textArea.grid_columnconfigure(0, weight=1)
        self.textArea.grid_rowconfigure(0, weight=1)
        
        # scrollable text box for sentence text
        self.sentArea = Treeview(self.frmSentences, show="headings", style="mystyle.Treeview", selectmode='browse')  
        self.sentArea.grid(row=0, column=0,  padx = 5, pady = 5, sticky=E+W+N+S)
        # columns         
        self.sentArea['columns'] = ('Num', 'Text')
        self.sentArea.column('Num', width=100, anchor=W)
        self.sentArea.column('Text', width=200, anchor=W)
        self.sentArea.heading('Num', text=' # ', anchor=W)
        self.sentArea.heading('Text', text='Text', anchor=W)     
        #scrollbars
        self.vsbSent = Scrollbar(self.frmSentences, orient=VERTICAL)
        self.hsbSent = Scrollbar(self.frmSentences, orient=HORIZONTAL)
        self.vsbSent.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=NS)
        self.hsbSent.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=EW)  
        # link treeview to scrollbars
        self.sentArea.config(yscrollcommand=self.vsbSent.set)
        self.vsbSent.config(command=self.sentArea.yview)        
        self.sentArea.config(xscrollcommand=self.hsbSent.set)
        self.hsbSent.config(command=self.sentArea.xview)        
        
        
        # canvas for sentence diagram
        self.diagramCanvas = Canvas(self.frmSentDiagram)
        #vertical scrollbar
        self.vsbDiagram = Scrollbar(self.frmSentDiagram, orient=VERTICAL)
        self.diagramCanvas.config(yscrollcommand=self.vsbDiagram.set)
        self.vsbDiagram.config(command=self.diagramCanvas.yview)        
        # horizaontal scrollbar
        self.hsbDiagram = Scrollbar(self.frmSentDiagram, orient=HORIZONTAL)
        self.hsbDiagram.config(command=self.diagramCanvas.xview)     
        self.diagramCanvas.config(xscrollcommand=self.hsbDiagram.set)
        # grid widgets
        self.diagramCanvas.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)
        self.vsbDiagram.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=NS)
        self.hsbDiagram.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=EW)    
        # handle resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frmSentDiagram.grid_columnconfigure(0, weight=1)
        self.frmSentDiagram.grid_rowconfigure(0, weight=1)            

        # entity text
        self.HTMLText = HtmlFrame(self.frmEntityText, messages_enabled = False)
        # grid the widgets
        self.HTMLText.grid(row = 0, column = 0, padx = 5, pady = 5, sticky=NSEW)
        # handle resizing
        self.HTMLText.grid_columnconfigure(0, weight=1)
        self.HTMLText.grid_rowconfigure(0, weight=1)                    

        # token data grid
        self.tvTokens = Treeview(self.frmTokens, show="headings", style="mystyle.Treeview", selectmode='browse')  
        self.tvTokens.grid(row=0, column=0,  padx = 5, pady = 5, sticky=E+W+N+S)
        # columns           
        self.tvTokens['columns'] = ('Text', 'Lemma', 'POS', 'Tag', 'Dep', 'Shape', 'Is-Alpha', 'Is-Stop', 'Is-Sentence-Start', 
                                            'Head','Left-Edge', 'Right-Edge','Entity-Type',  'Entity-Tag','Morphological')
        self.tvTokens.column("Text", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Lemma", width=150, anchor=W, stretch=False)
        self.tvTokens.column("POS", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Tag", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Dep", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Shape", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Is-Alpha", width=100, anchor=W, stretch=False)
        self.tvTokens.column("Is-Stop", width=100, anchor=W, stretch=False)
        self.tvTokens.column("Is-Sentence-Start", width=100, anchor=W, stretch=False)
        self.tvTokens.column("Head", width=100, anchor=W, stretch=False)
        self.tvTokens.column("Left-Edge", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Right-Edge", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Entity-Type", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Entity-Tag", width=150, anchor=W, stretch=False)
        self.tvTokens.column("Morphological", width=150, anchor=W, stretch=False)
        
        self.tvTokens.heading("Text", text='Text', anchor=W)
        self.tvTokens.heading('Lemma', text='Lemma', anchor=W)        
        self.tvTokens.heading('POS', text='Part Of Speach', anchor=W)
        self.tvTokens.heading('Tag', text='Tag', anchor=W)        
        self.tvTokens.heading('Dep', text='Dep', anchor=W)
        self.tvTokens.heading('Shape', text='Shape', anchor=W)        
        self.tvTokens.heading('Is-Alpha', text='Is-Alpha', anchor=W)
        self.tvTokens.heading('Is-Stop', text='Is-Stop', anchor=W)        
        self.tvTokens.heading('Is-Sentence-Start', text='Is-Sentence-Start', anchor=W)       
        self.tvTokens.heading('Head', text='Head', anchor=W)    
        self.tvTokens.heading('Left-Edge', text='Left-Edge', anchor=W)    
        self.tvTokens.heading('Right-Edge', text='Right-Edge', anchor=W)    
        self.tvTokens.heading('Entity-Type', text='Entity-Type', anchor=W)    
        self.tvTokens.heading('Entity-Tag', text='Entity-Tag', anchor=W)    
        self.tvTokens.heading('Morphological', text='Morphological', anchor=W)    
        #vertical scrollbar
        self.vsbToken = Scrollbar(self.frmTokens, orient=VERTICAL)
        self.tvTokens.config(yscrollcommand=self.vsbToken.set)
        self.vsbToken.config(command=self.tvTokens.yview)        
        # horizaontal scrollbar
        self.hsbToken = Scrollbar(self.frmTokens, orient=HORIZONTAL)
        self.hsbToken.config(command=self.tvTokens.xview)            
        self.tvTokens.config(xscrollcommand=self.hsbToken.set)
        self.vsbToken.grid(row = 0, column = 1, padx = 5, pady = 5,sticky=N+S)   
        self.hsbToken.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=W+E)   
         
        # initialize UI
        self.setWindowTitle()
        self.btnShowRawText()
        
    def setWindowTitle(self):
        if self.workbench.workbenchDict['workbenchName'] is None:
            name = "New File"
        else:
            name = self.workbench.workbenchDict['workbenchName']
        self.master.wm_title("Space Workbench File - {}".format(name))
        
    def logMsg(self, msg, display=None):
        ct = datetime.datetime.now()
        print("{}:{}".format(str(ct), msg))
        if display == True:
            messagebox.showinfo("spaCy Workbench", msg)
            
    def clearGrid(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)     
            
    def textAreaSelect(self, event):   
        '''capture mouse button release events for raw text widget'''
        # create spacy document
        self.createDoc()
        # update sentences grid
        self.displaySentences()        
        
    def btnShowRawText(self):
        self.frmRawText.tkraise()
        
    def btnShowSentences(self):
        self.frmSentences.tkraise()
        
    def btnShowDocData(self):
        self.frmDocData.tkraise()

    def btnShowEntityText(self):
        self.frmEntityText.tkraise()
        self.generateHTML()
        
    def btnShowTokens(self):
        self.frmTokens.tkraise()
        self.gridTokens()
        
    def generateHTML(self):
        # get the currently selected sentence
        sentence = self.selectedSentence()
        if not sentence is None:
            # generate html
            myHTML = displacy.render(sentence, style="ent")
            # replace mark tags with span tags so htmllabel will work.  
            fix1 = myHTML.replace("<mark", "<span")
            fix2 = fix1.replace("</mark","</span")
            # display the text
            self.HTMLText.load_html(fix2) 
        
    def btnShowSentDiagram(self):
        self.frmSentDiagram.tkraise()
        self.generateDiagram()
        
    def generateDiagram(self):
        # get the currently selected sentence
        sentence = self.selectedSentence()
        if not sentence is None:
            # generate svg diagram
            mySVG = displacy.render(sentence, style="dep")
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

    def gridTokens(self):
        # clear grid
        self.clearGrid(self.tvTokens)  
        # fill grid with word data
        for token in self.doc:
            self.tvTokens.insert("",'end',
                values=(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                            token.shape_, token.is_alpha, token.is_stop, token.is_sent_start, 
                            token.head, token.left_edge, token.right_edge, token.ent_type_, token.ent_iob_, token.morph ))

    def selectedSentence(self):
        'return the currently selected item in the sentence grid or None'
        try:
            # get the first selected row in the grid
            idx = self.sentArea.selection()[0]
            # get the sentence number stored in the first column
            sentNum = self.sentArea.item(idx)['values'][0]
            # convert the iterator to a list and get the desired sentence span
            sentence = list(self.doc.sents)[sentNum-1]
        except:
            sentence = None
        finally:
            return sentence

    def runSpacy(self):
        '''this method will process the raw text and populate the sentences widget and document widgets.'''
        # validate and load the spaCy model
        if self.loadSpacyModel():
            # validate and populate the raw text
            self.readTextFile()
            # create spacy document
            self.createDoc()
            # update sentences grid
            self.displaySentences()
            
        return

    def loadSpacyModel(self):
        'load the SpaCy Model'
        self.NLP = None
        try:
            self.app.config( cursor="wait" )
            self.app.update()
            modelName = self.workbench.workbenchDict["modelName"]
            self.NLP = spacy.load(modelName)
            self.logMsg("SpaCy pipeline:{} successfully loaded".format(modelName))
        except Exception as e:
            self.logMsg("Error loading SpaCy pipeline:{} - {}".format(modelName, e), display=True)  
            self.app.config( cursor="" )
            return False
        
        self.app.config( cursor="" )
        return True

    def createDoc(self):
        '''this method creates a spacy document object from the selected text in the raw text area.'''
        if self.validate() == False:
            return
            
        self.app.config( cursor="wait" )
        self.app.update()
        'initialize doc object'
        self.doc = None
        
        try:
            # get the selected text
            sel_text = self.textArea.selection_get()
        except:
            # if no selected text just get all of it
            sel_text = self.textArea.get('1.0', tk.END)
        
        try:
            # create the document object
            self.doc = self.NLP(sel_text)
        except:
            self.logMsg("Error Creating Doc Object - {}".format(e), display=True)
        finally:
            self.app.config( cursor="" )
        


        
########################################################################
#  sentences methods
########################################################################
    def displaySentences(self):
        # clear grid
        self.clearGrid(self.sentArea)
        sentNum = 1
        for sentence in list(self.doc.sents):
#            print("Sentence: {}".format(sentence.text)) 
            self.sentArea.insert("",'end',
                values=(str(sentNum), sentence.text ))    
            sentNum = sentNum + 1
        
        # select the first sentence
        self.sentArea.selection_set(self.sentArea.get_children()[0])
        self.sentArea.update()
        
########################################################################
#  validation and error messages
########################################################################
    def validate(self):
        return True
        
    def validateTextFile(self):
        '''This method determines if the workbench has a valid text file defined.'''
        return True
        
    def textFileNotDefined(self):
        messagebox.showinfo("spaCy Workbench", "No text file selected in Workbench Properties.")

########################################################################
#  raw text methods
########################################################################
    def readTextFile(self):
        '''this method reads the raw text file after validating that a file has been defined and populates the raw text window.'''
        self.textData = None
        if self.validateTextFile():
            try:
                # Open text file
                self.textArea.delete("1.0","end")
                with open(self.workbench.workbenchDict["textFile"],'r') as txtFile:
                    while(True):  
                        line = txtFile.readline()
                        if not line:
                            break;
                        self.textArea.insert('end', line)
                self.logMsg("Text file successfully read.")            
            except Exception as e:
                self.logMsg("Error reading text file. {}".format(e), display=True)
        else:
            self.textFileNotDefined()

##########################################################################
# workbench related methods
##########################################################################
    def propertiesDlg(self):
        dlg = WinWorkbenchProps.WinWorkbenchProps(self.app, workbench=self.workbench)
        dlg.wait_window(dlg)
        if dlg.changed:
            self.runSpacy()
        
    def newWorkbenchFile(self):
        'if file already open see if they want to save it'
        if not self.workbench.workbenchDict['workbenchName'] is None:
            self.saveAsSWBFile()
        'create a new workbench object'
        self.workbench = WorkBench(mode="New")  
        self.setWindowTitle()
        
    def openWorkbench(self):
        'open a .swb file and load the UI widgets'
        try:
            'open swb file'
            name= fd.askopenfilename(filetypes =[('Workbench File', '*.swb')]) 
            if len(name) > 0:
                self.loadSWBFile(name)
                self.logMsg("SWB file {} successfully opened.".format(self.workbench.workbenchDict['workbenchName']))
        except Exception as e:
            self.logMsg("Error opening SWB file. {}".format(e), display=True)
        finally:
            self.setWindowTitle()
            self.runSpacy()
            
    def loadSWBFile(self, name):
        #        'read json  swb file'
        try:
            # create new workbench object
            self.workbench = WorkBench(mode="New") 
            f = open(name)
            self.workbench.workbenchDict = json.load(f)
            self.workbench.workbenchDict['workbenchName'] = name   
            self.logMsg("SWB file successfully read.")            
        except Exception as e:
            self.logMsg("Error reading SWB file. {}".format(e), display=True)
        finally:
            f.close()
        
    def saveWorkbench(self):
        'save a .swb file'
        if self.workbench.workbenchDict['workbenchName'] == 'Untitled':
            self.saveAsSWBFile()
        else:
            self.writeSWBFile()
        return
        
    def saveAsSWBFile(self):
        'save as a .swb file'
        try:
            'open swb file'
            name= fd.asksaveasfilename(filetypes =[('SpaceWorkbench File', '*.swb')], defaultextension=".swb") 
            if len(name) > 0:
                self.workbench.workbenchDict['workbenchName'] = name
                self.writeSWBFile()
                self.setWindowTitle()
        except Exception as e:
            self.logMsg("Error Save As SWB file. {}".format(e), display=True)
        
        
    def writeSWBFile(self):
        'write out the space workbench dictionary'
        try:
            # write results to a file
            with open(self.workbench.workbenchDict['workbenchName'] , 'w') as output:
                print(json.dumps(self.workbench.workbenchDict, indent=4), file=output)
                self.logMsg("SWB file {} successfully saved.".format(self.workbench.workbenchDict['workbenchName']))
        except Exception as e:
            self.logMsg("Error writing SWB file. {}".format(e), display=True)       

    def exitProgram(self):
        # see if should save workbench file
        self.saveWorkbench()
        # exit the program        
        self.master.destroy()
        exit()
        


def main():
    'package init calls this method to start the app'
    masterWindow = Tk()
    masterWindow.title('spaCyWorkBench')
    masterWindow.geometry('800x600')    
#        masterWindow.resizable(True, True)
    spaCyWorkbenchUI(masterWindow)
    masterWindow.mainloop()
