import c4d, os
from c4d import gui, utils
#Welcome to the world of Python#

# SETTINGS
PLUGINID = 1029981
DW = 600            # Document Width
DH = 400             # Document Height

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


def GetGlobalPosition(obj):
    """
    Returns the global position of obj
    """
    return obj.GetMg().off
  
def GetGlobalRotation(obj):
    """
    Returns the global rotation of obj
    """
    return utils.MatrixToHPB(obj.GetMg())
  
def GetGlobalScale(obj):
    """
    Returns the global scale of obj
    """
    m = obj.GetMg()
    return c4d.Vector(  m.v1.GetLength(),
                        m.v2.GetLength(),
                        m.v3.GetLength())

############################################################
# Checks Path and changes Layout
############################################################
def checkPath(path,geDialog):
    if os.path.exists(path):
        geDialog.Enable(BTN_EXPORT, True)
        geDialog.SetString(TEX_MESSAGE, "Path exists - you can now export")
        geDialog.SetDefaultColor(TEX_MESSAGE, c4d.COLOR_TEXT, c4d.Vector(0, 50, 0))   
    else:
        geDialog.Enable(BTN_EXPORT, False) 
        geDialog.SetString(TEX_MESSAGE, "Path doesn't exist - please enter a valid path")
        geDialog.SetDefaultColor(TEX_MESSAGE, c4d.COLOR_TEXT, c4d.Vector(200, 0, 0)) 
                        
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


def writeBegin(f,mapname):
    f.write("Begin Map Name="+mapname+"\n")
    f.write("   Begin MapPackage\n")
    f.write("      Begin TopLevelPackage Class=Package Name="+mapname+" Archetype=Package'Core.Default__Package'\n")
    f.write('         Name="'+mapname+'"\n')
    f.write("         ObjectArchetype=Package'Core.Default__Package'\n")
    f.write("      End TopLevelPackage\n")
    f.write("   End MapPackage\n")
    f.write("   Begin Level NAME=PersistentLevel\n")
    
def writeStaticMesh(f,package,layer,obi):   

    pitch    = obi['B']
    yaw      = obi['H']
    roll     = obi['P']
    
    x        = obi['x']
    y        = -obi['z']
    z        = obi['y']
    
    scalex   = obi['scalex']
    scaley   = obi['scalez']
    scalez   = obi['scaley']
    
    name     = obi['name']
    add      = obi['add']
        
    
    f.write("    Begin Actor Class=StaticMeshActor Name="+add+" Archetype=StaticMeshActor'Engine.Default__StaticMeshActor'\n")    
    f.write("        Begin Object Class=StaticMeshComponent Name=StaticMeshComponent0 ObjName=StaticMeshComponent0 Archetype=StaticMeshComponent'Engine.Default__StaticMeshActor:StaticMeshComponent0'\n")
    f.write("            StaticMesh=StaticMesh'"+package+"."+name+"'\n")
    f.write("        End Object\n")            
    f.write("        Rotation=(Pitch="+str(pitch)+",Yaw="+str(yaw)+",Roll="+str(roll)+")\n")
    f.write("        Location=(X="+str(x)+",Y="+str(y)+",Z="+str(z)+")\n") 
    f.write("        DrawScale3D=(X="+str(scalex)+",Y="+str(scaley)+",Z="+str(scalez)+")\n")             
    f.write('        Tag="StaticMeshActor"\n')
    f.write('        Layer="'+layer+'"\n')    
    f.write("        CollisionComponent=StaticMeshComponent'StaticMeshComponent0')\n")
    f.write('        Name="'+add+'"\n')
    f.write("        ObjectArchetype=StaticMeshActor'Engine.Default__StaticMeshActor'\n")
    f.write("    End Actor\n")      

def writeEnd(f):
    f.write("   End Level\n")
    f.write("Begin Surface\n")
    f.write("End Surface\n")
    f.write("End Map\n")
    f.close()

def getObjectInfo(ob):
    obi ={} 

    obi['x'] = round(ob.GetAbsPos().x,5)
    obi['y'] = round(ob.GetAbsPos().y,5)
    obi['z'] = round(ob.GetAbsPos().z,5) 
                       
    obi['scalex'] = round(ob.GetAbsScale().x,5)
    obi['scaley'] = round(ob.GetAbsScale().y,5)
    obi['scalez'] = round(ob.GetAbsScale().z,5)
    
    obi['H'] = int(utils.Deg(ob.GetAbsRot().x) * -182.0444)
    obi['P'] = int(utils.Deg(ob.GetAbsRot().y) * -182.0444) 
    obi['B'] = int(utils.Deg(ob.GetAbsRot().z) * -182.0444)       
            
    obi['name'] = ob.GetName() 
    obi['add'] = ob.GetName()       
        
    return obi

def GetNextObject(op):
    if op==None: return None
 
    if op.GetDown(): return op.GetDown()
 
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
 
    return op.GetNext()
    
# Wandelt alle Instanzen in Grundobjekte um
def InstancesMakeEditable(op,doc):
    while op:
        InstancesMakeEditable(op.GetDown(),doc)
        next = op.GetNext()
        if op.GetType() == c4d.Oinstance:
            if op.GetUp() : parent = op.GetUp()           
            objects = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_MAKEEDITABLE, list = [op], mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION, doc = doc )
            for op in objects:
                doc.InsertObject(op,parent=parent)
            next = doc.GetFirstObject()           
        op = next
        
# Löst alle Objektgruppen auf
def ungroupAll(op,doc):
    while op:
        if op.GetNext(): next = op.GetNext()
        else: next = False
        if op.GetDown():
            ungroup(op,doc)
            next = doc.GetFirstObject()
        op = next
        
# Löst eine Objektgruppe auf
def ungroup(op,doc):
    child = op.GetDown()
    while (child):
        orig = child
        orig.SetRelMl(child.GetMg()) 
        child = child.GetNext()
        orig.Remove()        
        doc.InsertObject(orig)
    if len(op.GetChildren())<1 and op.GetType() == c4d.Onull: op.Remove() 

# Löscht alle Instanzen
def deleteInstances(op):
    while (op):
        next = op.GetNext()
        if op.GetType() == c4d.Oinstance: op.Remove()
        op = next  
        
# nullt alle Objekte
def nullObjects(op):
    nullvector = c4d.Vector(0,0,0)
    einsvector = c4d.Vector(1,1,1)
    while (op):
        op.SetAbsPos(nullvector)
        op.SetAbsRot(nullvector)
        op.SetAbsScale(einsvector) 
        op = op.GetNext()   
    

def dissolve(active,mapname,package,layer,path,filename):    
    selected = active.GetSelection()    

    temp = c4d.documents.IsolateObjects(active, selected)
    #temp.SetDocumentName("temp")
    #c4d.documents.InsertBaseDocument(temp)      
    
    InstancesMakeEditable(temp.GetFirstObject(),temp)
    ungroupAll(temp.GetFirstObject(),temp) 
    writet3d(mapname,package,layer,path,filename,temp)
    
    c4d.documents.KillDocument(temp) 
    
def insert(original, new, pos):
  '''Inserts new inside original at pos.'''
  return original[:pos] + new + original[pos:] 

def correctFBX(filepath):
    f = open(filepath, "r")
    text = f.read()
    f.close()
    i = 0
    while True:
        index = text.find("LayerElementUV: ",i)
        if index == -1:break
        uv = text[index+16:index+17]
        text = insert(text,"map"+uv,index+46)
        i = index+1         
         
    f = open(filepath, "w")
    f.write(text)
    f.close()         
    
def export(active,path,filename):
    fbxpath = path+"\\"+filename+".fbx"
    selected = active.GetSelection()    

    temp = c4d.documents.IsolateObjects(active, selected)
    #temp.SetDocumentName("temp")
    #c4d.documents.InsertBaseDocument(temp)      
    
    ungroupAll(temp.GetFirstObject(),temp)
    deleteInstances(temp.GetFirstObject())
    nullObjects(temp.GetFirstObject())    
    
    c4d.documents.SaveDocument(temp,fbxpath,c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,1026370) #Exports using the FBX exporter 
    c4d.documents.KillDocument(temp) 
    correctFBX(fbxpath)   

    
def writet3d(mapname,package,layer,path,filename,doc):
    t3dpath = path+"\\"+filename+".t3d"
    f = open(t3dpath, "w")
    writeBegin(f,mapname)  
    nameList = {}
        
    ob = doc.GetFirstObject()
    if ob==None: return

    while ob:    
        obi = getObjectInfo(ob)  
        if obi['name'] not in nameList:
            nameList[obi['name']] = 0
        else:
            nameList[obi['name']] = nameList[obi['name']] + 1
            obi['add'] = obi['name']+"_"+str(nameList[obi['name']]) 
                                       
        writeStaticMesh(f,package,layer,obi)        
        ob = GetNextObject(ob)                             

    writeEnd(f)
    print "UDK Level Exporter: OK"
    
def main():
    dialog = MainDialog()
    x= (c4d.gui.GeGetScreenDimensions(1,1,False)['sx2'] / 2) - DW/2
    y= (c4d.gui.GeGetScreenDimensions(1,1,False)['sy2'] / 2) - DH/2   
    dialog.Open(dlgtype = c4d.DLG_TYPE_ASYNC,defaultw=DW,defaulth=DH,xpos=x,ypos=y)


        
if __name__=='__main__':
    main()
