"""
Timothy Queva
CS3010 Lab
March 16, 2021

This program will act like a simple word processor except data will be saved
to a txt file. The main focus of this program is the design of the User
Interface for the fulfillment of the user interface course.
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import PhotoImage
import tkinter.font as tkfont
import os,sys

class txtProc():
    def __init__(self,obj):
        #Changes window icon
        self.__wIcon = PhotoImage(file = "Resources\\write.gif")
        obj.iconphoto(False, self.__wIcon)
        
        self.font= tkfont.Font(family="Ariel", size=12)
        
        #Setups the GUI
        self.window_setup(obj)
        self.editor_setup(obj)
        self.menu_setup(obj)
        self.ribbon(obj)
        
        #Creates tags for Text widget to use
        self.__text.tag_configure("emphasize", background="yellow",
                                  foreground="black")
        self.__text.tag_configure("normal",background="white",
                                  foreground="black")
        self.__text.tag_configure("bold",font=
                                  (self.__text.cget("font"),10, "bold"))
        self.__text.tag_configure("italic",font=
                                  (self.__text.cget("font"),10,"italic"))
        
    #sets main window title and size
    def window_setup(self,obj):
        obj.title("Text Processor")
        obj.geometry("900x500")
        
    def editor_setup(self,obj):
        self.__text= tk.Text(obj,font=self.font,height=1,width=1)
        self.__text.pack(fill=tk.BOTH,expand=True)
    
    def menu_setup(self,obj):
        #creates menubar and displays it main window
        menubar = tk.Menu(obj)
        obj.config(menu=menubar)
        
        #file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.newProgram)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_command(label="Save", command=self.savefile)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=obj.destroy)
        
        #edit menu
        editmenu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Edit",menu=editmenu)
        editmenu.add_command(label="Cut",command=lambda: 
                             self.__text.event_generate('<Control-x>'))
        editmenu.add_command(label="Copy",command=lambda: 
                             self.__text.event_generate('<Control-c>'))
        editmenu.add_command(label="Paste",command=lambda: 
                             self.__text.event_generate('<Control-v>'))
        
        #Format menu
        formatmenu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Format",menu=formatmenu)
        formatmenu.add_command(label="Bold",command= lambda: 
                               self.makeBold(obj))
        formatmenu.add_command(label="Italicize",command= lambda: 
                               self.italicize(obj))
        
        #Design menu
        designmenu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Design",menu=designmenu)
        designmenu.add_command(label="Trademark symbol",command=self.tm)
        designmenu.add_command(label="Registered symbol",command=self.rsymbol)
        designmenu.add_command(label="Copyright symbol",command=self.copyright)
        
        #Tools menu
        toolsmenu = tk.Menu(menubar,tearoff=0)
        toolsmenu.add_command(label="Highlight",command=lambda: 
                              self.highlight(obj))
        toolsmenu.add_command(label="Word count",command=lambda:
                              self.wordCount(obj))
        toolsmenu.add_command(label="Character count",command=lambda:
                              self.charCount(obj))
        menubar.add_cascade(label="Tools",menu=toolsmenu)
        
        #View menu
        viewmenu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="View",menu=viewmenu)
        viewmenu.add_command(label="Magnifier",command=self.magnify)
        viewmenu.add_command(label="Minimize",command=self.minimize)
        viewmenu.add_command(label="Reset size",command=self.reset)
        
        #Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Reference", command=lambda:
                             self.openref(obj))
        helpmenu.add_command(label="Limitations/Troubleshooting",
                             command=lambda: self.limits(obj))
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        #About menu
        aboutmenu = tk.Menu(menubar,tearoff=0)
        aboutmenu.add_command(label="Program Description",command=lambda:
                              self.progdescript(obj))
        aboutmenu.add_command(label="License",command=lambda:
                              self.display_license(obj))
        aboutmenu.add_command(label="About Author",command=lambda:
                              self.about_author(obj))
        menubar.add_cascade(label="About",menu=aboutmenu)
    
    #This deals with Ribbon GUI on bottom of window
    def ribbon(self,obj):
        self.__ribbon = tk.Frame(obj)
        self.__ribbon.pack(side='bottom',padx=1,pady=1,anchor='w')
        
        #New button
        self.__newIcon = PhotoImage(file=r"Resources\\new-pink.gif")
        self.__newIcon = self.__newIcon.subsample(25,30)
        self.__new = tk.Button(self.__ribbon,image=self.__newIcon,
                                   command=self.newProgram)
        self.__new.grid(row=0,column=0)
        
        #Open button
        self.__openIcon = PhotoImage(file=r"Resources\\open-icon.gif")
        self.__openIcon = self.__openIcon.subsample(28,29)
        self.__open=tk.Button(self.__ribbon,image=self.__openIcon,
                  command = self.openfile)
        self.__open.grid(row=0,column=1)
        
        #Save button
        self.__saveIcon = PhotoImage(file= r"Resources\\alt save-icon.gif")
        self.__saveIcon = self.__saveIcon.subsample(28,27)
        self.__save=tk.Button(self.__ribbon,image=self.__saveIcon,
                  command = self.savefile)
        #without the self "keyword" python garbage collects the image. In
        #such situations, line below is need to prevent this.
        #save.image = saveIcon
        self.__save.grid(row=0,column=2)
        
        #spacer
        tk.Label(self.__ribbon,width=1).grid(row=0,column=3)
        
        #Bold
        self.__boldIcon = PhotoImage(file=r"Resources\\bold-Icon.gif")
        self.__boldIcon = self.__boldIcon.subsample(36,34)
        self.__bold=tk.Button(self.__ribbon,image=self.__boldIcon,
                              command = lambda: self.makeBold(obj))
        self.__bold.grid(row=0,column=4)
        
        #Italicize
        self.__iIcon = PhotoImage(file=r"Resources\\italic.gif")
        self.__iIcon = self.__iIcon.subsample(19,24)
        self.__italic=tk.Button(self.__ribbon,image=self.__iIcon,
                                command =  lambda: self.italicize(obj))
        self.__italic.grid(row=0,column=5)
        
        #spacer
        tk.Label(self.__ribbon,width=1).grid(row=0,column=6)
        
        #Cut
        self.__cutIcon = PhotoImage(file=r"Resources\\cut-icon.gif")
        self.__cutIcon = self.__cutIcon.subsample(32,34)
        self.__cut=tk.Button(self.__ribbon,image=self.__cutIcon,command = lambda: 
                             self.__text.event_generate('<Control-x>'))
        self.__cut.grid(row=0,column=7)
        
        #Copy
        self.__copyIcon = PhotoImage(file=r"Resources\\alt copy-icon.gif")
        self.__copyIcon = self.__copyIcon.subsample(30,35)
        self.__copy=tk.Button(self.__ribbon,image=self.__copyIcon,command = lambda: 
                              self.__text.event_generate('<Control-c>'))
        self.__copy.grid(row=0,column=8)
        
        #Paste
        self.__pasteIcon = PhotoImage(file=r"Resources\\paste-icon.gif")
        self.__pasteIcon = self.__pasteIcon.subsample(28,28)
        self.__paste=tk.Button(self.__ribbon,image=self.__pasteIcon,command = lambda: 
                               self.__text.event_generate('<Control-v>'))
        self.__paste.grid(row=0,column=9)
        
        #spacer
        tk.Label(self.__ribbon,width=1).grid(row=0,column=10)
        
        #Highlight
        self.__hlIcon = PhotoImage(file=r"Resources\\hl-icon.gif")
        self.__hlIcon = self.__hlIcon.subsample(24,30)
        self.__hl=tk.Button(self.__ribbon,image=self.__hlIcon,
                                command = lambda: self.highlight(obj))
        self.__hl.grid(row=0,column=11)
        
        #Word Count
        self.__wcount = 0
        tk.Label(self.__ribbon,width=16,text=
                 ("Word count: " + str(self.__wcount))).grid(row=0,column=12)
        self.__refresh_wcount = PhotoImage(file=r"Resources\\refresh.gif")
        self.__refresh_wcount = self.__refresh_wcount.subsample(30,30)
        self.__refresh=tk.Button(self.__ribbon,image=self.__refresh_wcount,
                                 command=lambda: self.rib_wordCount(self.__ribbon))
        self.__refresh.grid(row=0,column=13)
        
        '''
        self.__view = tk.Frame(self.__ribbon,width=400)
        self.__view.grid(row=0,column=14,sticky="E")
        
        #self.__plus = PhotoImage(file=r"Resources\\hl-icon.gif")
        #self.__plus = self.__hlIcon.subsample(24,30)
        self.__mag=tk.Button(self.__ribbon,justify=tk.RIGHT,anchor='e',
                                command = self.donothing)
        self.__mag.grid(row=0,column=300)
        '''
    
    def magnify(self):
        size = int(self.font.cget("size"))
        size += 3
        self.font.configure(size=size)
        
    def minimize(self):
        size = int(self.font.cget("size"))
        size -= 3
        self.font.configure(size=size)
    
    def reset(self):
        size= 12
        self.font.configure(size=size)
    
    def wordCount(self,obj):
        window=tk.Toplevel(obj)
        window.iconphoto(False, self.__wIcon)
        window.geometry("200x150")
        wframe = tk.Frame(window)
        wframe.pack()
        
        #updates ribbon's word count
        if self.__text.get('1.0','end').strip() != "":    
            self.__wcount= len(self.__text.get('1.0','end').strip().split(" "))
            tk.Label(self.__ribbon,width=16,text=
                 ("Word count: " + str(self.__wcount))).grid(row=0,column=12)
        else:
            self.__wcount=0
            tk.Label(self.__ribbon,width=16,text=
                 ("Word count: " + str(self.__wcount))).grid(row=0,column=12)
        
        #displays word count in window
        tk.Label(wframe,anchor="w",justify=tk.CENTER,wraplength=150,
                 text="\n\n\nWord count: " + str(self.__wcount)).pack()
        
        #displays character count in window
        self.__ccount = len(self.__text.get('1.0','end').strip())
        tk.Label(wframe,anchor="w",justify=tk.CENTER,wraplength=150,
                 text="Character count: " + str(self.__ccount)).pack()
    
    def tm(self):
        self.__text.insert(tk.INSERT,"™")
    
    def rsymbol(self):
        self.__text.insert(tk.INSERT,"®")
    
    def copyright(self):
        self.__text.insert(tk.INSERT,"©")
    
    def charCount(self,obj):
        self.wordCount(obj)
    
    def rib_wordCount(self,ribbon):
        if self.__text.get('1.0','end').strip() != "":    
            self.__wcount= len(self.__text.get('1.0','end').strip().split(" "))
            tk.Label(ribbon,width=16,text=
                 ("Word count: " + str(self.__wcount))).grid(row=0,column=12)
        else:
            self.__wcount=0
            tk.Label(ribbon,width=16,text=
                 ("Word count: " + str(self.__wcount))).grid(row=0,column=12)
    
    def highlight(self,obj):
        obj.clipboard_clear()
        try:
            if "emphasize" in self.__text.tag_names("sel.first"):
                self.__text.tag_remove("emphasize","sel.first","sel.last")
            else:
                self.__text.tag_add("emphasize", "sel.first", "sel.last")        
        except tk.TclError: 
            pass
    
    def makeBold(self,obj):
        try:
            if "bold" in self.__text.tag_names("sel.first"):
                self.__text.tag_remove("bold","sel.first","sel.last")
            else:
                self.__text.tag_add("bold","sel.first","sel.last")
        except tk.TclError:
            pass
    
    def italicize(self,obj):
        try:
            if "italic" in self.__text.tag_names("sel.first"):
                self.__text.tag_remove("italic","sel.first","sel.last")
            else:
                self.__text.tag_add("italic","sel.first","sel.last")
        except tk.TclError:
            pass
    
    def display_license(self,obj):
        window=tk.Toplevel(obj)
        window.iconphoto(False, self.__wIcon)
        window.geometry("300x200")
        wframe = tk.Frame(window)
        wframe.pack()
        tk.Label(wframe,wraplength=150,text="This program is licensed under "
                 " the Creative Commons License.\n\n"+
                 "Feel free to do with as you wish. No warranties "+
                 "guaranteed or implied.").pack()
    
    def about_author(self,obj):
        window=tk.Toplevel(obj)
        window.iconphoto(False, self.__wIcon)
        window.geometry("300x200")
        wframe = tk.Frame(window)
        wframe.pack()
        tk.Label(wframe,wraplength=200,
                 text="\nThis program was created by:\n\n\n" +
                 "TIMOTHY QUEVA\n" +
                 "A student in the Grande Prairie Regional College Computer "+
                 "Science Diploma Program in fulfillment of CS3130 course "
                 "objectives.").pack()
    
    def progdescript(self,obj):
        window=tk.Toplevel(obj)
        window.iconphoto(False, self.__wIcon)
        window.geometry("200x150")
        wframe = tk.Frame(window)
        wframe.pack()
        tk.Label(wframe,wraplength=200,
                 text="\nThis program is an enhanced text editor. Only " +
                 "the text is saved.\n\nNote: any highlighting, bolding, or "+
                 "italicized markings are not saved.").pack()
    
    def limits(self,obj):
        window=tk.Toplevel(obj)
        window.iconphoto(False, self.__wIcon)
        window.geometry("300x200")
        wframe = tk.Frame(window)
        wframe.pack()
        tk.Label(wframe,justify=tk.LEFT,wraplength=270,
                 text="Known Limitations:\n" +
                 "-Program does not have undo/redo options.\n" +
                 "-Program does not have a right-click popup menu.\n" +
                 "-Exiting without first saving will result in data loss."+
                 " (ie. user not protected from mistakes).\n" +
                 "").pack()
    
    def openref(self,obj):
        window=tk.Toplevel(obj)
        window.iconphoto(False, self.__wIcon)
        window.geometry("380x260")
        wframe = tk.Frame(window)
        wframe.pack()
        tk.Label(wframe,anchor="w",justify=tk.LEFT,wraplength=340,
                 text="How to use program:\n" +
                 "-This program is a text editor. To begin, simply click the "+
                 "white canvas and begin typing.\n\n" +
                 "-To increase font size for viewing relief, navigate to View"+
                 "--> magnifier. This effectively will increase the font "+
                 "size.\n\n" +
                 "-Cut/copy/paste buttons are displayed on the ribbon as " +
                 "scissors, two pages, and clipboard icons respecitvely.\n\n" +
                 "-Bolding, italics, and highlighting allow for ease of use " +
                 "and showing other screen viewers important points-however" +
                 ", they are not saved as part of a file.\n\n" +
                 "IMPORTANT: before exiting, make sure to save by clicking " +
                 "the floppy disk icon or by navigating to File-->Save").pack()
    
    def newProgram(self):
        pass
        #os.execl("txtProc.py","txtProc.py")
    
    def donothing(self):
        print("donothing() was invoked")
    
    def savefile(self):
        text = self.__text.get('1.0','end')
        self.save = tk.filedialog.asksaveasfile()
        if self.save:
            self.save.write(text)
            self.save.close()
    
    def openfile(self):
        self.open = tk.filedialog.askopenfile()
        if self.open:
            text = self.open.read()
            self.__text.insert('1.0',text)
            self.open.close()
    
    #runs program after everything has been setup
    def run(self,obj):
        obj.mainloop()

root = tk.Tk()
program = txtProc(root)
program.run(root)