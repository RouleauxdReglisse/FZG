from Globals import *
from Enemies import *
from Plants import *
#10 by 10
#50 px step horizontal
#22.7 px step vertical
class Room:
    def __init__(self,fileName):
        self.layout=[[Open([x,y]) for x in range (11)] for y in range(11)]
        for x in range(11):
            for y in range(11):
                if x==0 or x==10 or y==0 or y==10:
                    self.layout[x][y]=Wall([x,y])
        game.newRoom()
        self.readFile(fileName)
        self.display()

    def readFile(self,fileName):
        file=open("FZG2/RoomStore/"+fileName)
        features=file.read().split("\n")
        features.pop()
        self.text=features[0]
        circuitsTotal=int(features[1])
        game.circuits+=[Circuit() for i in range(circuitsTotal)]
        for i in range(circuitsTotal):
            flags=features[i+2].split(" ")
            game.circuits[i].linkFlags(flags)
        roomFeatures={"NoteTile":NoteTile,"Mannequin":Mannequin,"BowPickup":BowPickup,"Open":Open,"Block":Block,"Door":Door,"LockedDoor":LockedDoor,"Enemy":TestFoe,"Bat":Bat,"Wight":Wight,"Switch":Switch,"Golem":Golem,"BombPlant":BombPlant,"Corvimus":Corvimus}
        for item in features[2+circuitsTotal:]:
            details=item.split(" ")
            if details[0]=="Condition":
                condition=True
                for i in range(2,len(details)):
                    parts=details[i].split(":")
                    if game.flags[parts[0]]!=parts[1]:
                        condition=False
                        break
                if condition:
                    self.readFile(details[1])
            else:
                roomFeatures[details[0]](details[2:]).install(self.layout,details[1])
        file.close()

    def display(self):
        game.makeScreen()
        game.roomBox()
        game.textBox()
        #write(self.text,game.screen,[66,339],0.5,fill="white",lineWidth=2,end=530)
        for row in self.layout:
            for elem in row:
                elem.draw()
        for elem in game.enemies:
            elem.draw()

class Circuit:
    def __init__(self):
        self.inputs=[]
        self.outputs=[]
        self.flags=[]
        self.activated=False

    def check(self):
        if self.activated==False:
            input=True
            for elem in self.inputs:
                if elem.circuitInput()==False:
                    input=False
                    break
            if input:
                for elem in self.outputs:
                    elem.circuitAction()
                    self.activated=True
                boolflip={"1":"0","0":"1"}
                for elem in self.flags:
                    game.flags[elem]=boolflip[game.flags[elem]]

    def addInput(self,input):
        self.inputs.append(input)

    def addOutput(self,output):
        self.outputs.append(output)

    def linkFlags(self,flags):
        for flag in flags:
            self.flags.append(flag)

class Tile:
    def __init__(self,features,accessible):
        self.accessible=accessible
        self.index=[int(features[0]),int(features[1])]
        self.contents=None

    def draw(self):
        pass

    def do(self):
        pass

    #look inside: wires >:/
    def install(self,layout,wires):
        layout[self.index[0]][self.index[1]]=self
        for i in range(0,len(wires),2):
            if wires[i]=="i":
                game.circuits[int(wires[i+1])].addInput(self)
            else:
                game.circuits[int(wires[i+1])].addOutput(self)

    def circuitInput(self):
        return False
    
    def circuitAction(self):
        pass

class Open(Tile):
    def __init__(self,index):
        super().__init__(index,True)


class Block(Tile):
    def __init__(self,index):
        super().__init__(index,False)

    def draw(self):
        tags="t"+str(self.index[0])+str(self.index[1])
        game.screen.delete(tags)
        center=game.gridToPos(self.index)
        if self.accessible==False:
            game.screen.create_line([center[0]+XSTEP/2,center[1]+YSTEP/2,center[0]-XSTEP/2,center[1]-YSTEP/2],fill="white",width=3,tags=tags)
            game.screen.create_line([center[0]+XSTEP/2,center[1]-YSTEP/2,center[0]-XSTEP/2,center[1]+YSTEP/2],fill="white",width=3,tags=tags)
        else:
            for i in range(3):
                offset=[random.uniform(-XSTEP/2,XSTEP/2),random.uniform(-YSTEP/2,YSTEP/2)]
                dot=[center[0]+offset[0],center[1]+offset[1]]
                circle(game.screen,dot,2,fill="white",tags=tags)

    def circuitAction(self):
        self.accessible=True
        self.draw()

class Wall(Tile):
    def __init__(self,index):
        super().__init__(index,False)

class Door(Tile):
    def __init__(self,features,Accessible=True):
        super().__init__(features[0:2],Accessible)
        self.connect=features[2]
        

    def draw(self):
        tag="t"+str(self.index[0])+str(self.index[1])
        game.screen.delete(tag)
        center=game.gridToPos(self.index)
        if self.accessible==True:
            fill="black"
        else:
            fill="white"
        coords=[center[0]+XSTEP/2,center[1]+(YSTEP/2),center[0]+XSTEP/2,center[1]-(YSTEP/2),center[0]-XSTEP/2,center[1]-(YSTEP/2),center[0]-XSTEP/2,center[1]+(YSTEP/2)]
        game.screen.create_polygon(coords,fill=fill,tags=tag)

    #room transition
    def do(self):
        game.currentRoom=Room(self.connect)
        game.player.roomTransition()

    #lock/unlock
    def circuitAction(self):
        self.accessible=not self.accessible
        self.draw()

class LockedDoor(Door):
    def __init__(self,features):
        super().__init__(features,False)

class BowPickup(Tile):
    def __init__(self,features):
        super().__init__(features,True)
        self.pickedUp=False
        
    def draw(self):
        tags="t"+str(self.index[0])+str(self.index[1])
        game.screen.delete(tags)
        center=game.gridToPos(self.index)
        if not self.pickedUp:
            game.screen.create_oval([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill="blue",tags=tags)

    def circuitInput(self):
        return self.pickedUp
    
    def do(self):
        self.pickedUp=True
        game.player.getBow()
        self.draw()
        game.spawnPopup("You got the bow. (e to charge, wasd to fire)",4)

class NoteTile(Open):
    def do(self):
        if (not hasattr(self,"note")) or self.note.destroyed :
            self.note=MessageWindow("To another damned soul: I don't know how i got here, but if others should follow, I leave you advice. You can battle the monsters of this place by moving towards them to deal damage, but be warned, creatures can fight back in the same way. Some creatures may be too tough to be harmed this way. Why dont you practice on these mannequins. perhaps we shall meet further down. -L")

    def draw(self):
        center=game.gridToPos(self.index)
        coords=[center[0]+3,center[1]+4,center[0]-3,center[1]+4,center[0]-3,center[1]-4,center[0]+3,center[1]-4]
        game.screen.create_polygon(coords,fill="white")

class MessageWindow:
    def __init__(self,text):
        self.window=tink.Tk()
        self.window.geometry("305x400")
        self.screen=tink.Canvas(self.window,height=400,width=305,bg="black")
        self.screen.place(x=0,y=0)
        write(text,self.screen,[3,3],0.5,"white",3,300)
        self.window.bind("<Destroy>",self.destroy)
        self.destroyed=False
        closeButton=tink.Button(self.window,bg="black",fg="white",text="close",command=lambda : self.window.destroy())
        closeButton.place(x=5,y=360)


    def destroy(self,key=None):
        self.destroyed=True






        

