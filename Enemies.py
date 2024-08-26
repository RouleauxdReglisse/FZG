from Globals import *
import random

class Enemy():
    def __init__(self,features,HP,speed):
        self.index=[int(features[0]),int(features[1])]
        self.pos=game.gridToPos(self.index)
        self.colour="white"
        self.iframes=0
        self.maxHP=HP
        self.HP=HP
        self.speed=speed
        self.cooldown=0
        self.moving=None
        self.damageTags=[]
        self.id=game.generateEnemyId()
        game.enemies.append(self)
        self.draw()

#20 160
    def showHealth(self,colour):
        game.makeBar([550,20],[570,180],self.maxHP,self.HP,colour,"black",self.id)

    def tick(self):
        if self.iframes%6>=3:
            self.colour="red"
        else:
            self.colour="white"
        self.draw()
        if self.moving!=None:
            self.pos[0]+=self.moving[0]
            self.pos[1]+=self.moving[1]
            if ((self.destination[0]-self.pos[0])>=0)!=(self.moving[0]>=0) or ((self.destination[1]-self.pos[1])>=0)!=(self.moving[1]>=0):
                self.moving=None
                self.pos=self.destination
        if self.cooldown==self.speed:
            self.act()
            self.cooldown=0
        else:
            self.cooldown+=1
        if self.iframes>0:
            self.iframes-=1

    def die(self):
        game.enemies.remove(self)
        game.currentRoom.layout[self.index[0]][self.index[1]].contents=None
        game.screen.delete(self.id)

    def damage(self,amount,source=None):
        if self.iframes<=0:
            self.HP-=amount
            self.iframes=30
            if self.HP<=0:
                self.die()

    def options(self):
        directions=[[0,1],[1,0],[-1,0],[0,-1]]
        for i in range(3,-1,-1):
            targetIndex=[self.index[0]+directions[i][0],self.index[1]+directions[i][1]]
            target=game.getTile(targetIndex)
            if target.accessible==False or targetIndex[0]<=0 or targetIndex[0]>=10 or targetIndex[1]<=0 or targetIndex[1]>=10:
                directions.pop(i)
        return directions
    
    def move(self,direction):
        newIndex=[self.index[0]+direction[0],self.index[1]+direction[1]]
        target=game.getTile(newIndex)
        if target.contents==None and target.accessible:
            game.shift(self.index,newIndex)
            self.index=newIndex
            self.destination=game.gridToPos(self.index)
            self.moving=[direction[0]*XSTEP/16,direction[1]*YSTEP/16]
            return True
        else:
            return False
        
    def attack(self,direction):
        targetIndex=[self.index[0]+direction[0],self.index[1]+direction[1]]
        target=game.getTile(targetIndex).contents
        if target!=None:
            target.damage(1,self.damageTags)

    def choose(self,options):
        return random.choice(options)

    def act(self):
        moves=self.options()
        choice=self.choose(moves)
        if not self.move(choice):
            self.attack(choice)

    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        game.screen.create_oval([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill=self.colour,tags=self.id)

    def install(self,layout,wires):
        layout[self.index[0]][self.index[1]].contents=self
        for i in range(0,len(wires),2):
            if wires[i]=="i":
                game.circuits[int(wires[i+1])].addInput(self)
            else:
                game.circuits[int(wires[i+1])].addOutput(self)

    def circuitInput(self):
        return self.HP<=0
    
    def circuitAction(self):
        pass
    
class TestFoe(Enemy):
    def __init__(self,features):
        super().__init__(features,6,60)

class Flying(Enemy):
    def options(self):
        directions=[[0,1],[1,0],[-1,0],[0,-1]]
        for i in range(3,-1,-1):
            targetIndex=[self.index[0]+directions[i][0],self.index[1]+directions[i][1]]
            target=game.getTile(targetIndex)
            if targetIndex[0]<=0 or targetIndex[0]>=10 or targetIndex[1]<=0 or targetIndex[1]>=10:
                directions.pop(i)
        return directions
    
    def move(self,direction):
        newIndex=[self.index[0]+direction[0],self.index[1]+direction[1]]
        target=game.getTile(newIndex)
        if target.contents==None:
            game.shift(self.index,newIndex)
            self.index=newIndex
            self.destination=game.gridToPos(self.index)
            self.moving=[direction[0]*XSTEP/16,direction[1]*YSTEP/16]
            return True
        else:
            return False

class Agressive(Enemy):
    def choose(self,options):
        targets=[]
        for elem in options:
            targets.append([self.index[0]+elem[0],self.index[1]+elem[1]])
        min=targets[0]
        p=game.player.index
        currentDistance=abs(p[0]-self.index[0])+abs(p[1]-self.index[1])
        choices=[]
        for elem in targets:
            newDistance=abs(elem[0]-p[0])+abs(elem[1]-p[1])
            if newDistance<currentDistance:
                choices.append(elem)
        if len(choices)==0:
            choices=targets
        return options[targets.index(random.choice(choices))]
    
class Transient(Enemy):
    def die(self):
        game.enemies.remove(self)
        game.screen.delete(self.id)

class Mannequin(Enemy):
    def __init__(self,features):
        super().__init__(features,2,100)

    def act(self):
        pass

    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        game.screen.create_line(center[0],center[1]+6,center[0],center[1]-6,fill=self.colour,tags=self.id)
        game.screen.create_line(center[0]+4,center[1]-2,center[0]-4,center[1]-2,fill=self.colour,tags=self.id)
        circle(game.screen,[center[0],center[1]-10],4,self.colour,self.id)

        

class Bat(Flying):
    def __init__(self,features):
        super().__init__(features,1,30)

    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        #if self.moving:
        if self.cooldown<self.speed/2:
            side=-1
        else:
            side=1
        side=sin(self.cooldown*6)
        middle=[center[0],center[1]+2*side]
        left=[center[0]-6,center[1]-7*side]
        right=[center[0]+6,center[1]-7*side]
        game.screen.create_line(middle,left,fill="white",tags=self.id)
        game.screen.create_line(middle,right,fill="white",tags=self.id)

class Wight(Agressive):
    def __init__(self,features):
        super().__init__(features,3,60)

    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        #mouth
        game.screen.create_line(center[0]-4,center[1]+1,center[0]+4,center[1]+9,fill=self.colour,tags=self.id,width=1)
        game.screen.create_line(center[0]+4,center[1]+1,center[0]-4,center[1]+9,fill=self.colour,tags=self.id,width=1)
        #eyes
        game.screen.create_line(center[0]+4,center[1]-1,center[0]+4,center[1]-4,fill=self.colour,tags=self.id,width=3)
        game.screen.create_line(center[0]-4,center[1]-1,center[0]-4,center[1]-4,fill=self.colour,tags=self.id,width=3)

class Switch(Enemy):
    def __init__(self,features):
        self.active=False
        super().__init__(features,1,100)

    def damage(self,amount,source=None):
        self.cooldown=0
        self.active=True
        self.draw()
    
    def tick(self):
        self.cooldown+=1
        if self.cooldown>=self.speed:
            self.active=False
            self.draw()

    #points 1 and 2 connect, points 3 and 4 connect, point 5 is between 1 and 2, point 6 is between 3 and 4.
    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        if self.active:
            stateAngle=0
            colour="yellow"
        else:
            stateAngle=90
            colour="blue"
        cornerDistance=5*math.sqrt(2)
        points=[]
        for i in range(45,360,90):
            points.append([center[0]+sin(stateAngle+i)*cornerDistance,center[1]+cos(stateAngle+i)*cornerDistance])
        for i in range(0,360,180):
            points.append([center[0]+cos(stateAngle+i)*5,center[1]+sin(stateAngle+i)*5])
        game.screen.create_line(points[0],points[1],fill=colour,tags=self.id)
        game.screen.create_line(points[3],points[2],fill=colour,tags=self.id)
        game.screen.create_line(points[5],points[4],fill=colour,tags=self.id)

    def circuitInput(self):
        return self.active
    
class Explosion(Transient):
    def __init__(self,features):
        super().__init__(features,1,50)
        self.damageTags=["explosion"]
        for i in range(0,360,90):
            direction=[int(sin(i)*math.sqrt(2)),int(cos(i)*math.sqrt(2))]
            self.attack(direction)

    def act(self):
        self.die()
    
    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        for i in range(0,360,90):
            direction=[sin(i),cos(i)]
            distance=[(XSTEP*1)*direction[0],(YSTEP*1.5)*direction[1]]
            start=[center[0]+distance[0]*(self.cooldown/self.speed),center[1]+distance[1]*(self.cooldown/self.speed)]
            end=[center[0]+distance[0],center[1]+distance[1]]
            game.screen.create_line(start,end,fill="orange",tags=self.id,width=self.cooldown//10)

class DustTrail(Transient):
    def __init__(self,features,direction):
        self.direction=direction
        super().__init__(features,1,20)

    def act(self):
        self.die()

    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        if self.direction[1]==0:
            i=self.direction[0]*-1
            for s in range(-15,6,20):
                start=[center[0]+s*i,center[1]+4]
                coords=[start,[start[0]+self.cooldown*i*0.5,start[1]],[start[0]+self.cooldown*i,start[1]-self.cooldown*0.5]]
                game.screen.create_polygon(coords,tags=self.id,fill="white",stipple="gray50")
        else:
            for i in range(-1,2,2):
                start=[center[0]+5*i,center[1]+4]
                coords=[start,[start[0]+self.cooldown*i*0.5,start[1]],[start[0]+self.cooldown*i,start[1]-self.cooldown*0.5]]
                game.screen.create_polygon(coords,tags=self.id,fill="white",stipple="gray50")

class Golem(Agressive):
    def __init__(self,features):
        self.moves=0
        self.momentum=None
        self.setDash=None
        super().__init__(features,6,40)

    def damage(self,amount,source=[]):
        if "explosion" in source:
            self.HP-=1
            self.iframes=30
            if self.HP<=0:
                self.die()

    def tick(self):
        self.draw()
        if self.moving!=None:
            self.pos[0]+=self.moving[0]
            self.pos[1]+=self.moving[1]
            if ((self.destination[0]-self.pos[0])>=0)!=(self.moving[0]>=0) or ((self.destination[1]-self.pos[1])>=0)!=(self.moving[1]>=0):
                self.moving=None
                self.pos=self.destination
        if self.cooldown==self.speed:
            self.moves+=1
            self.act()
            self.cooldown=0
        else:
            self.cooldown+=1
        if self.iframes>0:
            self.iframes-=1
            if self.iframes%6>=3:
                self.colour="red"
            else:
                self.colour="green"
        
    def act(self):
        if self.setDash==None:
            moves=self.options()
            move=self.choose(moves)
            if not self.move(move):
                self.smash(move)
        else:
            self.dash(self.setDash)
            self.setDash=None

    def move(self,direction):
        if (self.index[0]==game.player.index[0]) !=(self.index[1]==game.player.index[1]):
            if self.HP>2:
                self.momentum=direction
            else:
                self.setDash=direction
                DustTrail(self.index,[0,1])
                return True
        dustIndex=[self.index[0],self.index[1]]
        moveSucc=super().move(direction)
        if self.momentum!=None and moveSucc:
            DustTrail(dustIndex,self.momentum)
        return moveSucc

    def smash(self,direction):
        targetIndex=[self.index[0]+direction[0],self.index[1]+direction[1]]
        target=game.getTile(targetIndex)
        self.momentum=None
        if target.contents!=None:
            target.contents.damage(2,self.damageTags)
        elif target.accessible==False:
            target.circuitAction()

    def options(self):
        directions=[[0,1],[1,0],[-1,0],[0,-1]]
        for i in range(3,-1,-1):
            targetIndex=[self.index[0]+directions[i][0],self.index[1]+directions[i][1]]
            target=game.getTile(targetIndex)
            if targetIndex[0]<=0 or targetIndex[0]>=10 or targetIndex[1]<=0 or targetIndex[1]>=10:
                directions.pop(i)
        return directions
    
    def choose(self,options):
        if self.momentum in options:
            return self.momentum
        else:
            self.momentum=None
            return super().choose(options)
    
    def dash(self,direction):
        for i in range(3):
            newIndex=[self.index[0]+direction[0],self.index[1]+direction[1]]
            if newIndex[0]<=0 or newIndex[0]>=10 or newIndex[1]<=0 or newIndex[1]>=10:
                break
            nextTarget=game.getTile(newIndex)
            if nextTarget.contents!=None or nextTarget.accessible==False:
                self.smash(direction)
                break
            else:
                newIndex=[self.index[0]+direction[0],self.index[1]+direction[1]]
                game.shift(self.index,newIndex)
                DustTrail(self.index,direction)
                self.index=newIndex
                self.pos=game.gridToPos(self.index)

    def draw(self):
        if self.iframes%6>=3:
            self.colour="red"
        else:
            self.colour="white"
            game.screen.delete(self.id)
        self.showHealth("gray50")
        center=self.pos
        #square
        for i in range(-1,2,2):
            if (self.momentum!=None and self.momentum[0]!=i) or (self.setDash!=None and self.setDash[0]!=i):
                coords=[center[0]-7*i,center[1]-4,center[0]-12*i,center[1],center[0]-7*i,center[1]+4]
            else:
                coords=[center[0]-7*i,center[1]-4,center[0]-9*i,center[1]-4,center[0]-9*i,center[1]+4,center[0]-7*i,center[1]+4]
            game.screen.create_line(coords,fill=self.colour,tags=self.id)
        #eyes
        for i in range(-1,2,2):
            coords=[center[0]-2*i,center[1]-4,center[0]-2*i,center[1]-6]
            game.screen.create_line(coords,fill=self.colour,tags=self.id)
        #hash horizontal
        for i in range(0,4,3):
            coords=[center[0]-5,center[1]+2+i,center[0]+5,center[1]+2+i]
            game.screen.create_line(coords,fill=self.colour,tags=self.id)
        #hash vertical (angled)
        for i in range(-1,2,2):
            coords=[center[0]-2*i,center[1],center[0]-2*i+1,center[1]+7]
            game.screen.create_line(coords,fill=self.colour,tags=self.id)

    
class Corvimus(Enemy):
    def __init__(self,features):
        super().__init__(features,6,30)
        self.spellPool=[self.HWall,self.VWall]
        self.reserveSpellPool=[self.HWall2,self.VWall2,self.rain]
        self.moves=0
        self.currentSpell=self.HWall

    def die(self):
        super().die()
        game.spawnPopup("You got a key",4)

    
    def damage(self,amount,source=[]):
        if "fire" not in source and self.iframes<=0:
            super().damage(amount,source)
            if self.HP%2==1:
                self.spellPool.append(self.reserveSpellPool.pop())
            if self.HP>0:
                self.currentSpell=None
                self.teleport()
                self.moves=0

    def act(self):
        if self.currentSpell==None:
            self.currentSpell=random.choice(self.spellPool)
        else:
            if self.moves>=8:
                self.currentSpell=None
                self.teleport()
                self.moves=0
            else:
                self.currentSpell(self.moves)
                self.moves+=1

    def teleport(self):
        while True:
            targetIndex=[random.randint(1,9),random.randint(1,9)]
            target=game.getTile(targetIndex)
            if target.contents==None:
                game.shift(self.index,targetIndex)
                self.index=targetIndex
                self.pos=game.gridToPos(self.index)
                self.draw()
                break

    def HWall(self,step):
        for i in range(1,10):
            self.mark([step+1,i])

    def HWall2(self,step):
        for i in range(1,10):
            self.mark([(step*2)%9+1,i])

    def VWall(self,step):
        for i in range(1,10):
            self.mark([i,step+1])

    def VWall2(self,step):
        for i in range(1,10):
            self.mark([i,(step*2)%9+1])

    def rain(self,step):
        for i in range(step):
            coords=[random.randint(1,9),random.randint(1,9)]
            self.mark(coords)

    def mark(self,index):
        FireRune(index)

    def draw(self):
        center=self.pos
        self.showHealth("purple")
        circle(game.screen,[center[0]+3,center[1]],3,"gray",self.id)
        circle(game.screen,[center[0]-3,center[1]],3,"gray",self.id)
        #hat point
        game.screen.create_line([center[0]+3,center[1]-4,center[0],center[1]-9],fill="white",tags=self.id)
        game.screen.create_line([center[0],center[1]-9,center[0]-3,center[1]-4],fill="white",tags=self.id)
        #hat base
        game.screen.create_line([center[0]-6,center[1]-4,center[0]+6,center[1]-4],fill="white",tags=self.id)
        #beak
        game.screen.create_line([center[0]+3,center[1]+5,center[0]+3,center[1]+9],fill="white",tags=self.id)
        game.screen.create_line([center[0]-4,center[1]+5,center[0]+3,center[1]+9],fill="white",tags=self.id)


class FireRune(Transient):
    def __init__(self,features):
        super().__init__(features,1,30)

    def draw(self):
        center=self.pos
        game.screen.delete(self.id)
        circle(game.screen,center,9,fill="white",tags=self.id)
        circle(game.screen,center,5,fill="black",tags=self.id)

    def act(self):
        target=game.getTile(self.index)
        if target.contents==None:
            target.contents=ActiveFlame(self.index)
        else:
            target.contents.damage(1,["fire"])
        self.die()

class ActiveFlame(Enemy):
    def __init__(self,features):
        super().__init__(features,1,30)

    def act(self):
        self.die()

    def draw(self):
        game.screen.delete(self.id)
        center=self.pos
        circle(game.screen,center,5,fill="orange",tags=self.id)
        innerFlame=[center[0],center[1]+3]
        circle(game.screen,innerFlame,2,fill="yellow",tags=self.id)





