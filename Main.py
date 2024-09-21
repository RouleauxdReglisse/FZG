import tkinter as tink
from TinkBox import *
from Player import *
from Rooms import *

class Main:
    def __init__(self):
        self.set()
        while True:
            game.root.update()
            game.timer.stall(60)
            self.enemyRoutine()
            if game.player.HP<=0:
                break
            game.player.tick()
            self.circuitRoutine()
            if self.sillyMode:
                self.silly()
        self.gameOver()

    def set(self):
        self.sillyMode=False
        game.currentRoom=Room("StartRoom")
        game.player=Player([5,5])
        if game.flags["Bow"]==1:
            game.player.getBow()
        self.sillyX=0
        self.sillyY=0
        self.sillyXDir=1
        self.sillyYDir=1

    def gameOver(self):
        game.makeScreen()
        gameOverLabel=tink.Label(game.screen,bg="black",fg="white",text="GAME OVER")
        gameOverLabel.place(x=260,y=200)
        reset=tink.Button(game.screen,bg="black",fg="white",text="try again",command=self.__init__)
        reset.place(x=260,y=240)
        while True:
            game.root.update()


    def silly(self):
        game.root.geometry("600x450+"+str(self.sillyX)+"+"+str(self.sillyY))
        self.sillyX+=self.sillyXDir
        self.sillyY+=self.sillyYDir
        if self.sillyX<=0 or self.sillyX>=820:
            self.sillyXDir*=-1
        if self.sillyY<=0 or self.sillyY>=460:
            self.sillyYDir*=-1

    def enemyRoutine(self):
        #presence check
        #game.screen.delete("test")
        #for y in range(10):
        #    for x in range(10):
        #        if game.currentRoom.layout[x][y].contents!=None:
        #            center=game.gridToPos([x,y])
        #            game.screen.create_line([center[0]+5,center[1]+5,center[0]-5,center[1]-5],fill="yellow",width="5",tags="test")
        tpt=[]
        for elem in game.enemies:
            tpt.append(elem)
        for elem in tpt:
            if elem in game.enemies:
                elem.tick()

    def circuitRoutine(self):
        for elem in game.circuits:
            elem.check()
Main()