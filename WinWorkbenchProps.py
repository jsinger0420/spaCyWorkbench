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
import spacy
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog as fd 
from tkinter import scrolledtext    

class WinWorkbenchProps(Toplevel):
    def __init__(self, parent, workbench=None):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()      
        # get workbench dictionary
        if not workbench is None:
            self.workbenchDict = workbench.workbenchDict
        else:
            self.workbenchDict = None  # should throw error here
        self.changed = False
        # configure the window
        self.title('Workbench Properties')
        self.resizable(True, True)
        window_width = 600
        window_height = 200

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # define ui stringvars
#        self.textStreamURL = StringVar()
#        self.textTranscriptFile = StringVar()
        self.textFileName = StringVar()
        self.spacyFolderName = StringVar()

        # 
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        
        # text file controls
        self.lbl1 = Label(self, text="Text File Name:")
        self.txtBoxName = Label(self, textvariable = self.textFileName)
        # model file controls
        self.lbl2 = Label(self, text="Spacy Model File Name:")
        
        self.txtBoxspacy = Label(self, textvariable = self.spacyFolderName)
        # buttons
        self.btnPickText = Button(self, text = 'Select Text File',  command = self.openTextFile)
        self.btnPickSpacy = Button(self, text = 'Select Model',  command = self.openModelFolder)
        self.btnClose = Button(self, text = 'Close',  command = self.close)
        # grid controls
        self.lbl1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky="w")
        self.txtBoxName.grid(row = 0, column = 1, padx = 5, pady = 5, sticky=W)
        self.lbl2.grid(row = 1, column = 0, padx = 5, pady = 5, sticky=W)
        self.txtBoxspacy.grid(row = 1, column = 1, padx = 5, pady = 5, sticky=W)
        self.btnPickText.grid(row = 0, column = 2, padx = 5, pady = 5, sticky=E)
        self.btnPickSpacy.grid(row = 1, column = 2, padx = 5, pady = 5, sticky=E)
        self.btnClose.grid(row=2, column=1, padx = 5, pady = 5, sticky=E)

        # load stringvars from dictionary
        self.textFileName.set(self.workbenchDict['textFile'])
        self.spacyFolderName.set(self.workbenchDict['modelName'])

    def close(self):
        self.workbenchDict['textFile'] = self.textFileName.get()
        self.workbenchDict['modelName'] = self.spacyFolderName.get()
        self.destroy()
        return "finished"
        
    def openTextFile(self):
        'select text file'
        try:
            name= fd.askopenfilename(filetypes =[('text file', '*.txt')]) 
            self.textFileName.set(name)
            self.changed=True
#            self.readTextFile()
        except Exception as e:
            self.logMsg(e)
            self.logMsg("Error selecting text file.")
            
    def openModelFolder(self):
        'open the spacy model folder'
        try:
            name= fd.askdirectory(title='Select the Model Directory') 
            self.spacyFolderName.set(name)
            self.changed=True
#            self.loadSpacyModel()
        except Exception as e:
            self.logMsg(e)
            self.logMsg("Error selecting SpaCy Model file.")        
