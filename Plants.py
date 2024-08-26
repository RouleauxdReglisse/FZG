from Enemies import *
class Plant:
    def __init__(self,features,fruit,speed):
        self.accessible=True
        self.contents=None
        self.index=[int(features[0]),int(features[1])]
        self.colour="green"
        self.iframes=0
        self.speed=speed
        self.fruit=fruit
        self.cooldown=0
        self.id=game.generateEnemyId()
        self.draw()

    #look inside: wires >:/
    def install(self,layout,wires):
        layout[self.index[0]][self.index[1]]=self
        game.enemies.append(self)
        for i in range(0,len(wires),2):
            if wires[i]=="i":
                game.circuits[int(wires[i+1])].addInput(self)
            else:
                game.circuits[int(wires[i+1])].addOutput(self)

    def do(self):
        pass

    def tick(self):
        if self.contents==None:
            self.cooldown+=1
            if self.cooldown>=self.speed:
                self.act()

    def act(self):
        if self.contents==None:
            self.spawn()
            self.cooldown=0

    def spawn(self):
        self.contents=self.fruit(self.index)

    def circuitInput(self):
        return False
    
    def circuitAction(self):
        pass

    def draw(self):
        center=game.gridToPos(self.index)
        game.screen.create_line([center[0]+5,center[1],center[0]-5,center[1]],fill="green")

class BombPlant(Plant):
    def __init__(self,features):
        super().__init__(features,BombFruit,180)

class Fruit(Enemy):
    def act(self):
        pass

class BombFruit(Fruit):
    def __init__(self,features):
        super().__init__(features,1,60)

    def die(self):
        super().die()
        Explosion(self.index)

        