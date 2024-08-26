import tkinter as tink
import time
import math
def outline(screen,points,tag):
    for i in range(len(points)):
            screen.create_line([points[i][0],points[i][1],points[(i+1)%len(points)][0],points[(i+1)%len(points)][1]],tags=tag)

def circle(canvas,center,radius,fill="black",tags=None):
    canvas.create_oval(center[0]+radius,center[1]+radius,center[0]-radius,center[1]-radius,fill=fill,tags=tags)

class Timer:
    def __init__(self):
        self.FpsTimer=time.time()

    def stall(self,FPS):
        while not time.time()-self.FpsTimer>=1/FPS:
            time.sleep(1/(2**8))
        self.FpsTimer=time.time()

class LiveString:
    def __init__(self,question,questionLabel,answerLabel,root):
        self.root=root
        self.string=""
        self.finished=False
        for letter in "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM1234567890:":
            root.bind(letter,self.addLetter)
            root.bind("<space>",self.addLetter)
            root.bind("<Return>",self.finish)
            root.bind("<BackSpace>",self.removeLetter)
        self.questionLabel=questionLabel
        self.answerLabel=answerLabel
        self.questionLabel.configure(text=question)

    def loop(self):
        while not self.isFinished():
            self.root.update()
        self.questionLabel.destroy()
        self.answerLabel.destroy()
        return self.getString()

    def finish(self,key):
        self.finished=True
        self.answerLabel.destroy()
        self.questionLabel.destroy()

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

def cos(theta):
    radians=(theta/360)*2*math.pi
    return round(math.cos(radians),4)
def sin(theta):
    radians=(theta/360)*2*math.pi
    return round(math.sin(radians),4)
def tan(theta):
    radians=(theta/360)*2*math.pi
    return round(math.tan(radians),4)
def arccos(theta):
    radians=math.acos(theta)
    return round(radians/(2*math.pi)*360,4)
def arcsin(theta):
    radians=math.asin(theta)
    return round(radians/(2*math.pi)*360,4)
def arctan(theta):
    radians=math.atan(theta)
    return round(radians/(2*math.pi)*360,4)

file=open("Font","r")
characterInfo={}
for elem in file.read().split("\n"):
    parts=elem.split(" ")
    for i in range(1,len(parts)):
        parts[i]=parts[i].split(",")
        for j in range (len(parts[i])):
            parts[i][j]=parts[i][j].split(":")
    characterInfo[parts[0]]=parts[1:]
file.close()


def write(message,screen,start,size=1,fill="black",lineWidth=3,end=1000):
    ogpos=[start[0],start[1]]
    start=start
    for word in message.split(" "):
        if len(word)*30*size+start[0]>end:
            start[0]=ogpos[0]
            start[1]+=30*size+1
        for letter in word:
            if letter!=" ":
                data=characterInfo[letter]
                for part in data:
                    for i in range (1,len(part)):
                        point1=[start[0]+int(part[i-1][0])*size,start[1]+int(part[i-1][1])*size]
                        point2=[start[0]+int(part[i][0])*size,start[1]+int(part[i][1])*size]
                        screen.create_line([point1,point2],width=lineWidth,fill=fill)
            start[0]+=30*size+1
        start[0]+=30*size

def testScreen():
    root=tink.Tk()
    root.geometry("1000x450")
    screen=tink.Canvas(root,height=450,width=1000,bg="black")
    screen.place(x=0,y=0)
    string=""
    for elem in "macking cheese in the michealwave":
        string+=elem
        write(string,screen,[30,30],size=1,fill="white",end=550)
        root.update()
        time.sleep(0.2)
    #write("macking cheese\nin the michealwave",screen,[100,100],size=1,fill="white")
    while True:
        root.update()

    
#testScreen()