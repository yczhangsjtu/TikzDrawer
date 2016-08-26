import os
import wx
import json

class Entity(object):
    def __init__(self,text,x=0,y=0):
        self.text = text
        self.x = x
        self.y = y

        self.background = "blue"
        self.border = "black"
        self.shape = "rectangle"

    def __init__(self,obj):
        self.text = obj["text"]
        self.x = obj["x"]
        self.y = obj["y"]

        self.background = "blue"
        self.border = "black"
        self.shape = "rectangle"

        if "background" in obj:
            self.background = obj["background"]
        if "border" in obj:
            self.border = obj["border"]
        if "shape" in obj:
            self.shape = obj["shape"]

    def __str__(self):
        return '{"text":"%s","x":%d,"y":%d,"background":"%s","border":"%s","shape":"%s"}'%(
                self.text,self.x,self.y,self.background,self.border,self.shape
            )

class Edge(object):
    def __init__(self,start,end):
        self.start = start
        self.end = end

        self.color = "black"
        self.arrow = True
        self.bend = ""

    def __init__(self,obj,entities):
        self.start = entities[obj["start"]]
        self.end = entities[obj["end"]]


        self.color = "black"
        self.arrow = True
        self.bend = ""
        if "color" in obj:
            self.color = obj["color"]
        if "arrow" in obj:
            self.arrow = obj["arrow"]
        if "bend" in obj:
            self.bend = obj["bend"]

    def __str__(self):
        return '{"start":%d,"end":%d,"color":"%s","arrow":%s,"bend":"%s"}'%(
                self.start.index,self.end.index,self.color,str(self.arrow).lower(),self.bend
            )

class Graph(object):
    def __init__(self):
        self.entities = []
        self.edges = []

    def __str__(self):
        entities = ",".join(map(str,self.entities))
        for i,e in enumerate(self.entities):
            e.index = i
        edges = ",".join(map(str,self.edges))
        return '{"entities":[%s],"edges":[%s]}'%(entities,edges)
    
    def fromStr(self,s):
        self.entities = []
        self.edges = []
        data = json.loads(s)
        for e in data["entities"]:
            self.entities.append(Entity(e))
        for e in data["edges"]:
            self.edges.append(Edge(e,self.entities))

class DrawerFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,600))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.control = wx.AutoBufferedPaintDC(self)
        self.CreateStatusBar()
        self.graph = Graph()

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
        self.Bind(wx.EVT_PAINT,self.onPaint)

        menubar = wx.MenuBar()
        menubar.Append(filemenu,"&File")
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(wx.ID_NEW,'',wx.Bitmap('new.png'));
        self.toolbar.AddLabelTool(wx.ID_OPEN,'',wx.Bitmap('open.png'));
        self.toolbar.AddLabelTool(wx.ID_SAVE,'',wx.Bitmap('save.png'));

        self.Show(True)

    def onPaint(self,event):
        dc = wx.PaintDC(self)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

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
            path = os.path.join(self.dirname,self.filename)
            with open(path,"w") as f:
                f.write(str(self.graph))
        dlg.Destroy()

    def onOpen(self,event):
        self.dirname = ''
        dlg = wx.FileDialog(self,"Choose a File",self.dirname,"","*.*",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            path = os.path.join(self.dirname,self.filename)
            with open(path) as f:
                s = f.read()
            self.graph.fromStr(s)
        dlg.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = DrawerFrame(None, "tikz")
    frame.Show(True)
    app.MainLoop()
