import c4d, os
from c4d import gui, utils
#Welcome to the world of Python#

# SETTINGS
PLUGINID = 1029981
DW = 600            # Document Width
DH = 400            # Document Height

# Dialog Constants

GROUP_ID1          = 1000
TEX_MAPNAME        = 1001
ETEX_MAPNAME       = 1002

GROUP_ID2          = 2000
TEX_PACKAGENAME    = 2001
ETEX_PACKAGENAME   = 2002

GROUP_ID3          = 3000
TEX_LAYERNAME      = 3001
ETEX_LAYERNAME     = 3002
BTN_LAYER          = 3003

GROUP_ID4          = 4000
TEX_FILENAME       = 4001
ETEX_FILENAME      = 4002
BTN_FILE           = 4003

GROUP_ID5          = 5000
TEX_PATH           = 5001
ETEX_PATH          = 5002
BTN_OPEN           = 5003

GROUP_ID6          = 6000
BTN_EXPORT         = 6001

GROUP_ID7          = 7000
TEX_MESSAGE        = 7001

class MainDialog(gui.GeDialog):    
    global active 
    active = c4d.documents.GetActiveDocument()
    
    def CreateLayout(self):
        #creat the layout of the dialog  
        self.SetTitle("UDK Level Exporter")            

        self.GroupBegin(GROUP_ID1, c4d.BFH_SCALEFIT, 3, 1, title="teil1")        
        self.AddStaticText(TEX_MAPNAME, c4d.BFH_LEFT, name="Map Name: ", initw=200)
        self.AddEditText(ETEX_MAPNAME, c4d.BFH_LEFT, initw=400)         
        self.GroupEnd() 
        
        self.GroupBegin(GROUP_ID2, c4d.BFH_SCALEFIT, 3, 1, title="teil2")        
        self.AddStaticText(TEX_PACKAGENAME, c4d.BFH_LEFT, name="Package Name: ", initw=200)
        self.AddEditText(ETEX_PACKAGENAME, c4d.BFH_LEFT, initw=400)         
        self.GroupEnd()
        
        self.GroupBegin(GROUP_ID3, c4d.BFH_SCALEFIT, 3, 1, title="teil3")        
        self.AddStaticText(TEX_LAYERNAME, c4d.BFH_LEFT, name="Layer Name: ", initw=200)
        self.AddEditText(ETEX_LAYERNAME, c4d.BFH_LEFT, initw=400)
        self.AddButton(BTN_LAYER, c4d.BFH_RIGHT, name="Get Layer Name from Selection", initw=300)         
        self.GroupEnd()
        
        self.GroupBegin(GROUP_ID4, c4d.BFH_SCALEFIT, 3, 1, title="teil4")        
        self.AddStaticText(TEX_FILENAME, c4d.BFH_LEFT, name="File Name: ", initw=200)
        self.AddEditText(ETEX_FILENAME, c4d.BFH_LEFT, initw=400)
        self.AddButton(BTN_FILE, c4d.BFH_RIGHT, name="Get File Name from Selection", initw=300)         
        self.GroupEnd()
        
        self.GroupBegin(GROUP_ID5, c4d.BFH_SCALEFIT, 3, 1, title="teil5")        
        self.AddStaticText(TEX_PATH, c4d.BFH_LEFT, name="T3D/FBX Output Folder: ", initw=200)
        self.AddEditText(ETEX_PATH, c4d.BFH_SCALEFIT)
        self.AddButton(BTN_OPEN, c4d.BFH_RIGHT, name="...")                
        self.GroupEnd()   
        
        self.GroupBegin(GROUP_ID7, c4d.BFH_SCALEFIT, 3, 1, title="teil7")        
        self.AddStaticText(TEX_MESSAGE, c4d.BFH_LEFT, name="", initw=600)    
        self.GroupEnd()       
        
        self.GroupBegin(GROUP_ID6, c4d.BFH_SCALEFIT, 3, 1, title="teil6")        
        self.AddButton(BTN_EXPORT, c4d.BFH_SCALEFIT, name="EXPORT")                
        self.GroupEnd()   
        

        return True
 
   
    def InitValues(self):        
        #initiate the gadgets with values                
        self.SetString(ETEX_MAPNAME, "Testmap")
        self.SetString(ETEX_PACKAGENAME, "TestPackage")
        self.Enable(BTN_EXPORT, False) 
        return True
   
    def Command(self, id, msg):
        path = ""
        #handle user input
        
        # GROUP 1
        if id==ETEX_MAPNAME:
            mapname = self.GetString(ETEX_MAPNAME)   
            
        # GROUP 2
        if id==ETEX_PACKAGENAME:
            package = self.GetString(ETEX_PACKAGENAME)
            
        # GROUP 3
        if id==ETEX_PACKAGENAME:
            layer = self.GetString(ETEX_LAYERNAME)
        
        
        if id==BTN_LAYER:
            if active.GetActiveObject():
                self.SetString(ETEX_LAYERNAME, active.GetActiveObject().GetName())
            else: gui.MessageDialog('Nothing selected')
            
        if id==BTN_FILE:
            if active.GetActiveObject():
                self.SetString(ETEX_FILENAME, active.GetActiveObject().GetName())
            else: gui.MessageDialog('Nothing selected')            
        # Group 5
        if id==BTN_OPEN:
            self.SetString(ETEX_PATH,c4d.storage.LoadDialog(title="Select output folder...", flags=c4d.FILESELECT_DIRECTORY))
            path = self.GetString(ETEX_PATH)
            checkPath(path,self)
            
        if id==ETEX_PATH:
            path = self.GetString(ETEX_PATH)
            checkPath(path,self)
            
        # Group 6
        if id==BTN_EXPORT:
            mapname = self.GetString(ETEX_MAPNAME)
            package = self.GetString(ETEX_PACKAGENAME)         
            layer = self.GetString(ETEX_LAYERNAME)  
            if layer == "": layer = "None"
            filename = self.GetString(ETEX_FILENAME)
            if filename == "": filename = "Unnamed"
            path = self.GetString(ETEX_PATH)
                                   
            dissolve(active,mapname,package,layer,path,filename)
            export(active,path,filename)
  
   
        return True



def main():
    dialog = MainDialog()
    x= (c4d.gui.GeGetScreenDimensions(1,1,False)['sx2'] / 2) - DW/2
    y= (c4d.gui.GeGetScreenDimensions(1,1,False)['sy2'] / 2) - DH/2   
    dialog.Open(dlgtype = c4d.DLG_TYPE_MODAL,defaultw=DW,defaulth=DH,xpos=x,ypos=y)

if __name__=='__main__':
    main()
