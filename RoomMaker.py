import tkinter as tink
from TinkBox import *
XSTEP=50
YSTEP=25
class Game:
    def __init__(self):
        self.root=tink.Tk()
        self.root.geometry("600x450+200+20")
        self.screen=tink.Canvas(self.root,width=600,height=450,bg="black")
        self.makeScreen()
        self.tags=0

    def gridToPos(self,index):
        pos=[index[0]*XSTEP+25+XSTEP/2,index[1]*YSTEP+25+YSTEP/2]
        return pos
    
    def makeScreen(self):
        self.screen.destroy()
        self.screen=tink.Canvas(self.root,width=600,height=450,bg="black")
        self.screen.place(x=0,y=0)
        self.roomBox()

    def roomBox(self):
        self.screen.delete("room")
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
                        self.screen.create_line([i,coords[j][1],i+6*direction,coords[j][1]],fill="white",tags="room")
            else:
                for i in range(coords[j][1]+0*direction,coords[(j+1)%4][1]+2*direction*-1,direction*25):
                    for c in range(2):
                        self.screen.create_line(coords[j][0]+c*8*direction*-1,i+7*direction,coords[j][0]+c*8*direction*-1,i+19*direction,fill="white",tags="room")

    def countFeature(self):
        self.tags+=1
        return "t"+str(self.tags)
    
    def removeFeature(self):
        if self.tags>0:
            self.screen.delete("t"+str(self.tags))
            self.tags-=1

class Tile:
    def __init__(self,index):
        self.index=index
        self.id=[game.countFeature(),"room"]
        self.draw()

    def draw(self):
        pass

class Open(Tile):
    pass


class Block(Tile):
    def draw(self):
        center=game.gridToPos(self.index)
        game.screen.create_line([center[0]+XSTEP/2,center[1]+YSTEP/2,center[0]-XSTEP/2,center[1]-YSTEP/2],fill="white",width=3,tags=self.id)
        game.screen.create_line([center[0]+XSTEP/2,center[1]-YSTEP/2,center[0]-XSTEP/2,center[1]+YSTEP/2],fill="white",width=3,tags=self.id)

class Door(Tile):
    def draw(self):
        center=game.gridToPos(self.index)
        coords=[center[0]+XSTEP/2,center[1]+(YSTEP/2),center[0]+XSTEP/2,center[1]-(YSTEP/2),center[0]-XSTEP/2,center[1]-(YSTEP/2),center[0]-XSTEP/2,center[1]+(YSTEP/2)]
        game.screen.create_polygon(coords,fill="black",tags=self.id)

class LockedDoor(Tile):
    def draw(self):
        center=game.gridToPos(self.index)
        coords=[center[0]+XSTEP/2,center[1]+(YSTEP/2),center[0]+XSTEP/2,center[1]-(YSTEP/2),center[0]-XSTEP/2,center[1]-(YSTEP/2),center[0]-XSTEP/2,center[1]+(YSTEP/2)]
        game.screen.create_polygon(coords,fill="white",tags=self.id)

class Enemy(Tile):
    def draw(self):
        game.screen.delete("enemy")
        center=game.gridToPos(self.index)
        game.screen.create_oval([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill="white",tags=self.id)

class Mannequin(Tile):
        
    def draw(self):
        game.screen.delete("enemy")
        center=game.gridToPos(self.index)
        game.screen.create_oval([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill="white",tags=self.id)

class Switch(Tile):
    def draw(self):
        center=game.gridToPos(self.index)
        stateAngle=90
        cornerDistance=5*math.sqrt(2)
        points=[]
        for i in range(45,360,90):
            points.append([center[0]+sin(stateAngle+i)*cornerDistance,center[1]+cos(stateAngle+i)*cornerDistance])
        for i in range(0,360,180):
            points.append([center[0]+cos(stateAngle+i)*5,center[1]+sin(stateAngle+i)*5])
        game.screen.create_line(points[0],points[1],fill="white",tags=self.id)
        game.screen.create_line(points[3],points[2],fill="white",tags=self.id)
        game.screen.create_line(points[5],points[4],fill="white",tags=self.id)


class BombPlant(Tile):
    def draw(self):
        center=game.gridToPos(self.index)
        game.screen.create_line([center[0]+5,center[1],center[0]-5,center[1]],fill="green")

class Golem(Tile):
    def draw(self):
        game.screen.delete("enemy")
        center=game.gridToPos(self.index)
        game.screen.create_oval([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill="white",tags=self.id)

class BowPickup(Tile):
    def draw(self):
        game.screen.delete("enemy")
        center=game.gridToPos(self.index)
        game.screen.create_oval([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill="blue",tags=self.id)



game=Game()
class Reticle:
    def __init__(self):
        self.pos=[0,0]
        self.options=Tile.__subclasses__()
        self.features=[]
        self.baseStack=[]
        print(self.options)
        self.draw()
        self.active=Block
        self.tileIndex=1
        self.UI=tink.Label(game.screen,text=self.active.__name__,fg="white",bg="black")
        self.UI.place(x=30,y=400)
        self.keyBinds()

    def keyBinds(self):
        buttons="adswASDW"
        for elem in buttons:
            game.root.bind(elem,self.move)
        game.root.bind("<space>",self.place)
        game.root.bind("f",self.transcribe)
        game.root.bind("<Left>",self.switch)
        game.root.bind("<Right>",self.switch)
        game.root.bind("z",self.undo)
        game.root.bind("c",self.addToCircuit)
        game.root.bind("r",self.reset)
        game.root.bind("b",self.branch)


    def switch(self,direction):
        shortcut={"Left":-1,"Right":1}
        direction=shortcut[direction.keysym]
        self.tileIndex=(self.tileIndex+direction)%len(self.options)
        self.active=self.options[self.tileIndex]
        self.UI.configure(text=self.active.__name__)

    def move(self,key):
        key=key.keysym.lower()
        shorthand={"a":[-1,0],"d":[1,0],"s":[0,1],"w":[0,-1]}
        direction=shorthand[key]
        newPos=[self.pos[0]+direction[0],self.pos[1]+direction[1]]
        if newPos[0]>=0 and newPos[0]<=10 and newPos[1]>=0 and newPos[1]<=10:
            self.pos=newPos
            self.draw()

    def place(self,key):
        self.active(self.pos)
        if self.active.__name__=="Door" or self.active.__name__=="LockedDoor":
            self.features.append([self.active.__name__,[],self.pos[0],self.pos[1],liveString("connects to which room?").loop()])
        else:
            self.features.append([self.active.__name__,[],self.pos[0],self.pos[1]])
        print(self.features)

    def draw(self):
        game.screen.delete("reticle")
        center=game.gridToPos(self.pos)
        game.screen.create_line([center[0]+5,center[1],center[0]-5,center[1]],tags="reticle",fill="white")
        game.screen.create_line([center[0],center[1]+5,center[0],center[1]-5],tags="reticle",fill="white")

    def undo(self,key):
        if len(self.features)>0:
            game.removeFeature()
            self.features.pop()

    def addToCircuit(self,key):
        if len(self.features)>0:
            input1=liveString("I/O?").loop().lower()
            input2=liveString("add to which circuit ").loop().lower()
            if (input1=="i" or input1=="o") and input2 in "1234567890":
                self.features[len(self.features)-1][1].append([input1,input2])
            else:
                print("invalid inputs")
        else:
            print("what?")

    def branch(self,key):
        self.features.append(["Condition",liveString("FileName").loop(),liveString("flag conditions. [flagName][colon][1 or 0]").loop()])
        self.baseStack=self.features
        self.features=[]
        print("newBranch")

    def reset(self,key):
        for i in range(len(self.features)):
            game.screen.delete(self.features.pop())
        game.roomBox()

    def transcribe(self,key):
        fileName=liveString("please enter file name").loop()
        file=open("FZG2/RoomStore/"+fileName,"w")
        while True:
            circuitTotal=liveString("how many circuits total").loop()
            if circuitTotal in "1234567890":
                break
        file.write(circuitTotal+"\n")
        for i in range(int(circuitTotal)):
            file.write(liveString("triggers which flags ").loop()+"\n")
        for feature in self.features:
            file.write(str(feature[0]+""))
            string=" "
            if feature[0]=="Condition":
                string+=feature[1]
            else:
                for elem in feature[1]:
                    print("polo2")
                    string+=elem[0]+elem[1]
            file.write(string)
            for elem in feature[2:]:
                file.write(" "+str(elem))
            file.write("\n")
        if self.baseStack!=[]:
            for i in range (len(self.features)):
                game.removeFeature()
            self.features=self.baseStack
            self.baseStack=[]


class liveString:
    def __init__(self,question):
        self.string=""
        self.finished=False
        for letter in "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM1234567890:":
            game.root.bind(letter,self.addLetter)
        game.root.bind("<space>",self.addLetter)
        game.root.bind("<Return>",self.finish)
        game.root.bind("<BackSpace>",self.removeLetter)
        self.questionLabel=tink.Label(game.screen,text=question,bg="black",fg="white")
        self.questionLabel.place(x=300,y=350)
        self.answerLabel=tink.Label(game.screen,text="",bg="black",fg="white")
        self.answerLabel.place(x=300,y=400)

    def loop(self):
        while not self.isFinished():
            game.root.update()
        return self.getString()

    def finish(self,key):
        self.finished=True
        self.answerLabel.destroy()
        self.questionLabel.destroy()
        reticle.keyBinds()

    def addLetter(self,key):
        self.string+=key.char
        self.update()

    def removeLetter(self,key):
        self.string=self.string[0:len(self.string)-1]
        self.update()

    def update(self):
        self.answerLabel.configure(text=self.string)

    def isFinished(self):
        return self.finished

    def getString(self):
        return self.string




reticle=Reticle()
while True:
    game.root.update()