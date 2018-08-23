#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import datetime
import wx
import wx.lib.inspection

wildcard = "Python files (*.py)|*.py|" \
"Text files (*.txt)|*.txt|" \
"CSV files (*.csv)|*.csv|" \
"XML files (*.xml)|*.xml|" \
"All files (*.*)|*.*"

class Example(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)
        self.InitUI()
        self.text = None

    def InitUI(self):
        self.initMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Status bar")

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        a = wx.StaticText(panel, label='Drag\'n\'drop here')
        vbox.Add(a, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        #
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(panel, label='Count occurence of'), flag=wx.RIGHT, border=8)
        self.occurenceOf = wx.TextCtrl(panel, value="<Row")
        hbox.Add(self.occurenceOf, proportion=1)
        x = wx.Button(panel, wx.NewIdRef(), "Count")
        self.Bind(wx.EVT_BUTTON, self.onCountOccurences, x)
        hbox.Add(x)
        vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 10))
        # console
        a = wx.StaticText(panel, label='Console')
        vbox.Add(a)
        self.console = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        vbox.Add(self.console, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)
        vbox.Add((-1, 25))
        # ok / close
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)

        self.SetSize((950, 600))
        self.SetTitle('File drag and drop')
        self.Centre()

    def initMenuBar(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        # file
        fileMenu = wx.Menu()
        qmi = fileMenu.Append(wx.ID_OPEN, '&Open\tCtrl+O')
        self.Bind(wx.EVT_MENU, self.onOpen, qmi)
        qmi = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q')
        self.Bind(wx.EVT_MENU, self.onQuit, qmi)
        # tools
        toolsMenu = wx.Menu()
        qmi = toolsMenu.Append(wx.NewIdRef(), 'Count occurences')
        self.Bind(wx.EVT_MENU, self.onCountOccurences, qmi)
        # help
        helpMenu = wx.Menu()
        qmi = helpMenu.Append(wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.onAbout, qmi)

        menubar.Append(fileMenu, '&File')
        menubar.Append(toolsMenu, 'Tools')
        menubar.Append(helpMenu, "&Help")

    def onOpen(self, e):
        dlg = wx.FileDialog(self, message="Choose a file",
            defaultDir=os.getcwd(),defaultFile="",
            wildcard=wildcard,style=wx.FD_OPEN | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.loadFile(paths[0])
        dlg.Destroy()

    def log(self, text, addTime=True, addNewLine=True):
        if addTime:
            self.console.AppendText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' - ')
        self.console.AppendText(text)
        if addNewLine:
            self.console.AppendText('\n')
    def loadFile(self, filepath):
        self.log('Loading file: '+filepath)
        busyDlg = wx.BusyInfo("Loading file...")
        try:
            file = open(filepath, 'r')
            self.text = file.read()
        except IOError as error:
            msg = "Error opening file\n {}".format(str(error))
            dlg = wx.MessageDialog(None, msg)
            dlg.ShowModal()
            return False
        except UnicodeDecodeError as error:
            msg = "Cannot open non text files\n {}".format(str(error))
            dlg = wx.MessageDialog(None, msg)
            dlg.ShowModal()
            return False
        finally:
            file.close()
        busyDlg = None
        nbLines = self.text.count('\n')+1
        nbChars = len(self.text)
        self.log(f"Loaded succesfully {nbLines:,d} lines for {nbChars:,d} characters")

    def onCountOccurences(self, event):
        print('onCountOccurences')
        if not self.text or len(self.text)<1:
            self.log('A file has to be loaded')
            return
        occurence = self.occurenceOf.GetValue()
        if len(occurence)<1:
            self.log('An occurence has to be set')
            return
        nbOccurences = sum(1 for m in re.finditer(occurence, self.text))
        self.log('- Nb of '+occurence+': '+str(nbOccurences))
        nbOccurences = self.text.count(occurence)
        self.log('- Nb of '+occurence+': '+str(nbOccurences))

    def onAbout(self, event):
        wx.MessageBox("Software developed by Florian Courgey (https://floriancourgey.com).\nVersion 0.1",
                      "About",
                      wx.OK|wx.ICON_INFORMATION)
    def onQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    ex = Example(None)
    # wx.lib.inspection.InspectionTool().Show()
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
