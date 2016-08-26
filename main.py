import os
import wx
import json

class Entity(object):
    def __init__(self,obj):
        self.text = ""
        self.x = 0
        self.y = 0

        self.background = "blue"
        self.border = "black"
        self.shape = "rectangle"

        if obj == None: return

        self.text = obj["text"]
        self.x = obj["x"]
        self.y = obj["y"]

        if "background" in obj:
            self.background = obj["background"]
        if "border" in obj:
            self.border = obj["border"]
        if "shape" in obj:
            self.shape = obj["shape"]

    def get(text,x,y):
        entity = Entity()
        entity.text = text
        entity.x = x
        entity.y = y

        entity.background = "blue"
        entity.border = "black"
        entity.shape = "rectangle"

    def __str__(self):
        return '{"text":"%s","x":%d,"y":%d,"background":"%s","border":"%s","shape":"%s"}'%(
                self.text,self.x,self.y,self.background,self.border,self.shape
            )

class Edge(object):

    def __init__(self,obj,entities):
        self.color = "black"
        self.arrow = True
        self.bend = ""

        if obj == None: return

        self.start = entities[obj["start"]]
        self.end = entities[obj["end"]]

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

    ID_SELECT = 10001
    ID_NODE   = 10002

    def __init__(self,parent,title):

        wx.Frame.__init__(self,parent,title=title,size=(800,600))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.control = wx.AutoBufferedPaintDC(self)
        self.CreateStatusBar()
        self.graph = Graph()
        self.mode = "select"

        filemenu = wx.Menu()
        toolmenu = wx.Menu()
        newMenuItem = filemenu.Append(wx.ID_NEW,"N&ew","Create a new file")
        openMenuItem = filemenu.Append(wx.ID_OPEN,"O&pen","Open a file")
        saveMenuItem = filemenu.Append(wx.ID_SAVE,"S&ave","Save current file")
        filemenu.AppendSeparator()
        exitMenuItem = filemenu.Append(wx.ID_EXIT,"E&xit","Terminate the program")
        selectMenuItem = toolmenu.Append(DrawerFrame.ID_SELECT,"S&elect","Select object mode")
        nodeMenuItem = toolmenu.Append(DrawerFrame.ID_NODE,"Add N&ode","Click to add new node")

        self.Bind(wx.EVT_MENU,self.onNew,newMenuItem)
        self.Bind(wx.EVT_MENU,self.onOpen,openMenuItem)
        self.Bind(wx.EVT_MENU,self.onSave,saveMenuItem)
        self.Bind(wx.EVT_MENU,self.onExit,exitMenuItem)
        self.Bind(wx.EVT_MENU,self.onSelectMode,selectMenuItem)
        self.Bind(wx.EVT_MENU,self.onNodeMode,nodeMenuItem)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        self.Bind(wx.EVT_MOTION,self.onMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN,self.onLeftClick)

        menubar = wx.MenuBar()
        menubar.Append(filemenu,"&File")
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(wx.ID_NEW,'',wx.Bitmap('new.png'));
        self.toolbar.AddLabelTool(wx.ID_OPEN,'',wx.Bitmap('open.png'));
        self.toolbar.AddLabelTool(wx.ID_SAVE,'',wx.Bitmap('save.png'));
        self.toolbar.AddLabelTool(DrawerFrame.ID_SELECT,'',wx.Bitmap('mouse.png'));
        self.toolbar.AddLabelTool(DrawerFrame.ID_NODE,'',wx.Bitmap('node.png'));

        self.Show(True)

    def onLeftClick(self,event):
        self.mousex = event.x
        self.mousey = event.y

        if self.mode == "node":
            entity = Entity(None)
            entity.x = self.mousex
            entity.y = self.mousey
            self.graph.entities.append(entity)
            self.Refresh()
            self.Update()

    def onMouseMove(self,event):
        self.mousex = event.x
        self.mousey = event.y
        self.Refresh()
        self.Update()

    def onSelectMode(self,event):
        self.mode = "select"

    def onNodeMode(self,event):
        self.mode = "node"

    def onPaint(self,event):
        dc = wx.PaintDC(self)
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        dc.Clear()

        self.drawGraph(self.graph,dc)

        if self.mode == "node":
            dc.SetBrush(wx.Brush("blue"))
            dc.SetPen(wx.Pen("black"))
            dc.DrawRectangle(self.mousex-10,self.mousey-10,20,20)

    def onExit(self,event):
        self.Close(True)

    def onNew(self,event):
        self.graph = Graph()

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
            self.Refresh()
            self.Update()
        dlg.Destroy()

    def drawGraph(self,graph,dc):
        for e in graph.entities:
            dc.SetBrush(wx.Brush(e.background))
            dc.SetPen(wx.Pen(e.border))
            dc.DrawRectangle(e.x-20,e.y-10,40,20)
            dc.SetTextForeground("black")
            dc.DrawText(e.text,e.x,e.y)

if __name__ == "__main__":
    app = wx.App(False)
    frame = DrawerFrame(None, "tikz")
    frame.Show(True)
    app.MainLoop()
