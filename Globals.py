import tkinter as tink
from TinkBox import *
XSTEP=50
YSTEP=25
class Game:
    def __init__(self):
        self.root=tink.Tk()
        self.player=None
        self.root.geometry("600x450+400+200")
        self.screen=tink.Canvas(self.root)
        self.timer=Timer()
        self.currentRoom=None
        self.enemies=[]
        self.circuits=[]
        self.entities=0
        self.getFlags()

    def generateEnemyId(self):
        self.entities+=1
        return "e"+str(self.entities)
    
    def getFlags(self):
        flagFile=open("flags.txt","r")
        self.flags={}
        reading=flagFile.read().split("\n")
        reading.pop()
        for line in reading:
            part=line.split(" ")
            self.flags[part[0]]=part[1]
        flagFile.close()

    def newRoom(self):
        self.enemies=[]
        self.circuits=[]

    def getTile(self,index):
        return self.currentRoom.layout[index[0]][index[1]]
        
    
    #vertical bar
    def makeBar(self,topLeft,bottomRight,max,value,colourFull,colourEmpty,tag):
        game.screen.delete(tag)
        width=bottomRight[0]-topLeft[0]
        centerX=topLeft[0]+width/2
        borderThickness=4
        game.screen.create_line([centerX,bottomRight[1]+borderThickness,centerX,topLeft[1]-borderThickness],width=width+borderThickness*2,tags=tag,fill="white")
        game.screen.create_line([centerX,bottomRight[1],centerX,topLeft[1]],width=width,tags=tag,fill=colourEmpty)
        percent=value/max
        difference=topLeft[1]-bottomRight[1]
        fullness=difference*percent
        game.screen.create_line([centerX,bottomRight[1],centerX,bottomRight[1]+fullness],fill=colourFull,tags=tag,width=width)

    def makeScreen(self):
        self.screen.destroy()
        self.screen=tink.Canvas(self.root,height=450,width=600,bg="black",highlightthickness=0)
        self.screen.place(x=0,y=0)

    def roomBox(self):
        topLeft=[65,48]
        coords=[topLeft,[topLeft[0]+XSTEP*9+20,topLeft[1]],[topLeft[0]+XSTEP*9+20,topLeft[1]+YSTEP*9+2],[topLeft[0],topLeft[1]+YSTEP*9+2]]
        for j in range(len(coords)):
            if coords[j][0]!=coords[(j+1)%4][0]:
                vector=0
            else:
                vector=1
            direction=int((coords[(j+1)%4][vector]-coords[j][vector])/abs(coords[(j+1)%4][vector]-coords[j][vector]))
            if vector==0:
                for i in range(coords[j][0],coords[(j+1)%4][0],direction*9):
                        self.screen.create_line([i,coords[j][1],i+6*direction,coords[j][1]],fill="white")
            else:
                for i in range(coords[j][1]+0*direction,coords[(j+1)%4][1]+2*direction*-1,direction*25):
                    for c in range(2):
                        self.screen.create_line(coords[j][0]+c*8*direction*-1,i+7*direction,coords[j][0]+c*8*direction*-1,i+19*direction,fill="white")

    def shift(self,start,finish):
        startTile=self.currentRoom.layout[start[0]][start[1]]
        endTile=self.currentRoom.layout[finish[0]][finish[1]]
        endTile.contents=startTile.contents
        startTile.contents=None

    def textBox(self):
        coords=[[50,335],[550,335],[550,435],[50,435]]
        for j in range(len(coords)):
            if coords[j][0]!=coords[(j+1)%4][0]:
                vector=0
            else:
                vector=1
            direction=int((coords[(j+1)%4][vector]-coords[j][vector])/abs(coords[(j+1)%4][vector]-coords[j][vector]))
            if vector==0:
                for i in range(coords[j][0],coords[(j+1)%4][0],direction*9):
                        self.screen.create_line([i,coords[j][1],i+6*direction,coords[j][1]],fill="white")
            else:
                for i in range(coords[j][1]+5*direction,coords[(j+1)%4][1]+5*direction*-1,direction*25):
                    for c in range(2):
                        self.screen.create_line(coords[j][0]+c*10*direction*-1,i,coords[j][0]+c*10*direction*-1,i+17*direction,fill="white")


    def gridToPos(self,index):
        pos=[index[0]*XSTEP+25+XSTEP/2,index[1]*YSTEP+25+YSTEP/2]
        return pos
    
    def posToGrid(self,pos):
        index=[int((pos[0]-14)//XSTEP),int((pos[1]-25)//YSTEP)]
        return index
    
    def spawnPopup(self,text,duration):
        popup=Popup(text)
        self.root.update()
        time.sleep(duration)
        popup.kill()

game=Game()

class Popup:
    def __init__(self,text):
        self.window=tink.Canvas(game.root,width=300,height=225,bg="black")
        self.window.place(x=150,y=122)
        write(text,self.window,[2,2],0.5,"white",2,300)

    def kill(self):
        self.window.destroy()
flip={0:1,1:0}
