import os
import wx


class DrawerFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,600))
        self.control = wx.TextCtrl(self,style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        filemenu = wx.Menu()
        newMenuItem = filemenu.Append(wx.ID_NEW,"N&ew","Create a new file")
        openMenuItem = filemenu.Append(wx.ID_OPEN,"O&pen","Open a file")
        saveMenuItem = filemenu.Append(wx.ID_SAVE,"S&ave","Save current file")
        filemenu.AppendSeparator()
        exitMenuItem = filemenu.Append(wx.ID_EXIT,"E&xit","Terminate the program")
        self.Bind(wx.EVT_MENU,self.onNew,newMenuItem)
        self.Bind(wx.EVT_MENU,self.onOpen,openMenuItem)
        self.Bind(wx.EVT_MENU,self.onSave,saveMenuItem)
        self.Bind(wx.EVT_MENU,self.onExit,exitMenuItem)

        menubar = wx.MenuBar()
        menubar.Append(filemenu,"&File")
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(wx.ID_NEW,'',wx.Bitmap('new.png'));
        self.toolbar.AddLabelTool(wx.ID_OPEN,'',wx.Bitmap('open.png'));
        self.toolbar.AddLabelTool(wx.ID_SAVE,'',wx.Bitmap('save.png'));

        self.Show(True)

    def onExit(self,event):
        self.Close(True)

    def onNew(self,event):
        pass

    def onSave(self,event):
        self.dirname = ''
        dlg = wx.FileDialog(self,"Choose a File",self.dirname,"","*.*",wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            print os.path.join(self.dirname,self.filename)
        dlg.Destroy()

    def onOpen(self,event):
        self.dirname = ''
        dlg = wx.FileDialog(self,"Choose a File",self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            print os.path.join(self.dirname,self.filename)
        dlg.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = DrawerFrame(None, "tikz")
    frame.Show(True)
    app.MainLoop()
