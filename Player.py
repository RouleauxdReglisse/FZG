from Globals import *
from Enemies import *
class Player:
    def __init__(self,index):
        self.pos=game.gridToPos(index)
        self.moveInput=None
        self.index=index
        self.maxHealth=10
        self.HP=self.maxHealth
        self.iframes=0
        self.speed=17
        self.cooldown=self.speed
        self.colour="white"
        self.bowCharge=False
        self.moving=None
        self.hasBow=False
        if game.flags["Bow"]=="1":
            self.hasBow=True
        self.install()
        self.draw()
        self.bindKeys()
        self.showHealth()

    def getBow(self):
        self.hasBow=True

    def bindKeys(self):
        keys="AaDdSsWweE"
        for elem in keys:
            game.root.bind(elem,self.keyPress)
        game.root.bind("<KeyRelease>",self.keyRelease)

    def chargeBow(self):
        if self.hasBow:
            self.bowCharge=True

    def roomTransition(self):
        wrapAround=[((self.index[0]-1)%9)+1,((self.index[1]-1)%9)+1]
        self.index=wrapAround
        self.pos=game.gridToPos(self.index)
        game.currentRoom.layout[self.index[0]][self.index[1]].contents=self
        self.showHealth()

    #destination as an index
    #does not validate destination, used for room transition
    def pseudoMove(self,destination):
        game.shift(self.index,destination)
        self.index=destination
        self.pos=game.gridToPos(self.index)

    def finish(self,key):
        self.damage(1)

    def showHealth(self):
        game.makeBar([10,20],[30,180],self.maxHealth,self.HP,"green","red","playerHP")

    def damage(self,amount,source=None):
        if self.iframes<=0:
            self.HP-=amount
            self.showHealth()
            self.iframes=30

    def install(self):
        game.currentRoom.layout[self.index[0]][self.index[1]].contents=self

    def draw(self):
        center=self.pos
        game.screen.delete("player")
        circle(game.screen,center,9,fill=self.colour,tags="player")
        circle(game.screen,center,7,fill="black",tags="player")
        game.screen.create_line(center[0]+3,center[1]-3,center[0]+3,center[1]+1,tags="player",fill=self.colour)
        game.screen.create_line(center[0]-3,center[1]-3,center[0]-3,center[1]+1,tags="player",fill=self.colour)
        game.screen.create_line(center[0]+2,center[1]+3,center[0]-3,center[1]+3,tags="player",fill=self.colour)

    def tick(self):
        if self.moveInput!=None:
            self.act(self.moveInput)
        if self.moving!=None:
            self.pos[0]+=self.moving[0]
            self.pos[1]+=self.moving[1]
            if ((self.destination[0]-self.pos[0])>=0)!=(self.moving[0]>=0) or ((self.destination[1]-self.pos[1])>=0)!=(self.moving[1]>=0):
                self.moving=None
                self.pos=self.destination
                game.currentRoom.layout[self.index[0]][self.index[1]].do()
        if self.iframes>0:
            self.iframes-=1
            if self.iframes%6>=3:
                self.colour="red"
            else:
                self.colour="white"
        self.cooldown+=1
        self.draw()

    def keyPress(self,key):
        key=key.keysym.lower()
        if key in "asdw":
            shortcut={"a":[-1,0],"d":[1,0],"s":[0,1],"w":[0,-1]}
            self.moveInput=shortcut[key]
            #self.act(shortcut[key])
        elif key=="e":
            self.chargeBow()

    def keyRelease(self,key):
        key=key.keysym.lower()
        shortcut={"a":[-1,0],"d":[1,0],"s":[0,1],"w":[0,-1]}
        if key in shortcut:
            if shortcut[key]==self.moveInput:
                self.moveInput=None

    def act(self,direction):
        if self.cooldown>=self.speed:
            self.cooldown=0
            if self.bowCharge:
                self.shootBow(direction)
            elif self.moving==None:
                self.destination=[self.index[0]+direction[0],self.index[1]+direction[1]]
                if self.destination[0]>=0 and self.destination[0]<=10 and self.destination[1]>=0 and self.destination[1]<=10 and game.currentRoom.layout[self.destination[0]][self.destination[1]].accessible:
                    contents=game.currentRoom.layout[self.destination[0]][self.destination[1]].contents
                    if contents==None:
                        game.shift(self.index,[self.index[0]+direction[0],self.index[1]+direction[1]])
                        self.index[0]+=direction[0]
                        self.index[1]+=direction[1]
                        self.destination=game.gridToPos(self.destination)
                        self.moving=[direction[0]*XSTEP/16,direction[1]*YSTEP/16]
                    else:
                        self.attack(contents)

    def attack(self,target):
        target.damage(1)
    
    def shootBow(self,direction):
        self.bowCharge=False
        game.enemies.append(Arrow(self.index,direction))

class Arrow(Transient):
    def __init__(self,index,direction):
        self.index=[index[0]+direction[0],index[1]+direction[1]]
        self.direction=direction
        self.id=game.generateEnemyId()
        self.trail=[]
        self.time=0
        while not self.hitCheck():
            self.trail.append([self.index[0],self.index[1]])
            self.index[0]+=direction[0]
            self.index[1]+=direction[1]

        
    def hitCheck(self):
        target=game.getTile(self.index)
        if target.accessible==False or self.index[0]<=0 or self.index[1]<=0 or self.index[0]>=10 or self.index[1]>=10:
            return True
        if target.contents!=None:
            target.contents.damage(1)
            return True
        return False
    
    def tick(self):
        self.draw()
        self.time+=1
        if self.time>=100:
            self.die()
    
    def draw(self):
        game.screen.delete(self.id)
        for i in range (len(self.trail)):
            elem=self.trail[i]
            center=game.gridToPos(elem)
            offset=1+(self.time/100)
            #circle(game.screen,center,5,fill="white",tags=self.id)
            start=[center[0]+(XSTEP/2)*self.direction[0],center[1]+(YSTEP/2)*self.direction[1]]
            end=[center[0]-(XSTEP/2)*self.direction[0],center[1]-(YSTEP/2)*self.direction[1]]
            fade=100+i*20-self.time*2
            if fade>100:
                fade=100
            if fade>=0:
                game.screen.create_line([start,end],fill="grey"+str(fade),tags=self.id)

        
