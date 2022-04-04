from tkinter import *
from time import *
from random import *
from copy import *

app=Tk()
app.title("TETRIS")
canvas=Canvas(app,width=500,height=600,bg='white')
canvas.pack()
app.update()

class Cell:
    cellw=18
    cellh=18

    def __init__(self,canvas,x,y,color,color2):
        self.canvas=canvas
        self.x=x
        self.y=y
        self.id=canvas.create_rectangle(x,y,x+Cell.cellw,y+Cell.cellh,fill=color,outline=color2)
        self.num=0 # accumulated block : -1 general block : 0

    def chcol(self,color):
        self.canvas.itemconfig(self.id,fill=color)


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Ac_Block:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color

class Block:
    ID=1
    bl_col=['red','orange','grey','green','blue','navy','violet']
    bl_point=[[Point(1,0),Point(0,0),Point(2,0),Point(3,0)],
              [Point(1,1),Point(0,1),Point(0,0),Point(2,1)],
              [Point(1,1),Point(0,1),Point(2,1),Point(2,0)],
              [Point(0,0),Point(1,0),Point(0,1),Point(1,1)],
              [Point(1,1),Point(0,1),Point(1,0),Point(2,0)],
              [Point(1,1),Point(0,1),Point(1,0),Point(2,1)],
              [Point(1,1),Point(1,0),Point(0,0),Point(2,1)]]

    def __init__(self,canvas,type,is_static):
        self.canvas=canvas
        self.type=type
        self.point=deepcopy(Block.bl_point[type])
        self.is_static=is_static
        if is_static==False:
            self.canvas.bind_all("<KeyPress-Left>",self.move_left)
            self.canvas.bind_all("<KeyPress-Right>", self.move_right)
            self.canvas.bind_all("<KeyPress-Down>", self.move_down)
            self.canvas.bind_all("<KeyPress-Up>",self.rotate)
            self.id=deepcopy(Block.ID)
            Block.ID+=1
            for i in self.point:
                i.x+=int(width/2)
                if cell[i.x*height+i.y].num==-1:
                    End()
                    break

    def dele(self):
        for i in self.point:
            acb.append(Ac_Block(i.x,i.y,Block.bl_col[self.type]))

    def move_left(self,event):
        for i in self.point:
            if i.x==0 or cell[(i.x-1)*height+i.y].num==-1:
                return

        for i in self.point:
            i.x-=1

        app.update()

    def move_right(self,event):
        for i in self.point:
            if i.x==width-1 or cell[(i.x+1)*height+i.y].num==-1:
                return

        for i in self.point:
            i.x+=1

        app.update()

    def move_down(self,event):
        for i in self.point:
            if i.y==height-1 or cell[i.x*height+i.y+1].num==-1:
                return
        for i in self.point:
            i.y+=1

        app.update()

    def rotate(self,event):
        if self.type==3:
            return
        pivot=self.point[0]
        for i in range(len(self.point)):
            if not(0<=self.point[i].y-pivot.y+pivot.x<width):
                return
            if not(0<=-(self.point[i].x-pivot.x)+pivot.y<height):
                return
            if cell[(self.point[i].y-pivot.y+pivot.x)*height-(self.point[i].x-pivot.x)+pivot.y].num==-1:
                return

        for i in range(len(self.point)):
            self.point[i]=Point(self.point[i].y-pivot.y+pivot.x,-(self.point[i].x-pivot.x)+pivot.y)

        app.update()

    def is_stop(self):
        for i in self.point:
            #print(i.x,i.y)
            if i.y==height-1 or cell[i.x*height+i.y+1].num==-1:
                return True
        return False

    def draw(self):
        for i in self.point:
            cell[i.x*height+i.y].chcol(Block.bl_col[self.type])
            cell[i.x*height+i.y].num=self.id

        app.update()

    def nexdraw(self):
        for i in self.point:
            nexcell[i.x*2+i.y].chcol(Block.bl_col[self.type])

        app.update()

def Reset():
    for i in range(width):
        for j in range(height):
            cell[i*height+j].chcol('White')
            cell[i*height+j].num=0

    for i in range(4):
        for j in range(2):
            nexcell[i*2+j].chcol('White')

    for i in acb:
        cell[i.x*height+i.y].chcol(i.color)
        cell[i.x*height+i.y].num=-1

    Your_score['text']="Your score : "+str(score)
    Your_level['text']="Your level : "+str(level)

    app.update()

def Check(x):
    for i in range(width):
        if cell[i*height+x].num!=-1:
            return False
    return True

def Del_row():
    tmp_row=[]
    tmp=[]
    for j in range(height):
        if Check(j)==True:
            tmp_row.append(j)

    global score
    score+=(len(tmp_row)*len(tmp_row))

    for j in tmp_row:
        for i in range(width):
            cell[i*height+j].chcol('cyan')
    app.update()

    for i in acb:
        f=1
        for j in tmp_row:
            if i.y==j:
                f=0
        if f==1:
            cnt=0
            for j in tmp_row:
                if j>i.y:
                    cnt+=1
            tmp.append(Ac_Block(i.x,i.y+cnt,i.color))
    del acb[0:]

    for i in tmp:
        acb.append(i)

    if len(tmp_row)>=1:
        return True

def End():
    global End_id
    global Game_End
    global Game_Time
    global Res

    Game_End = Label(app, text="Game End", bg='White', font=("Times New Roman", 12))
    Game_Time = Label(app, textvariable=Remain_Time, bg='White', font=("Times New Roman", 11))
    Res = Button(app, text="Restart?", command=Restart, font=("Times New Roman", 13))
    End_id=canvas.create_rectangle(0,0,canvas.winfo_width(),canvas.winfo_height(),fill='White',outline='lightgrey')
    Game_End.place(x=canvas.winfo_width()/2,y=canvas.winfo_height()/2,anchor='s')
    Game_Time.place(x=canvas.winfo_width()/2,y=canvas.winfo_height()/2+20,anchor='s')
    Res.place(x=canvas.winfo_width()/2,y=canvas.winfo_height()/2+60,anchor='s')

    global is_End
    is_End=True

def Restart():
    global acb
    global curb
    global nexb
    global cell
    global nexcell

    del acb[0:]
    del cell[0:]
    del nexcell[0:]

    for i in range(width):
        for j in range(height):
            cell.append(Cell(canvas, i * Cell.cellw + startx, j * Cell.cellh + starty, 'White', 'lightgrey'))

    for i in range(4):
        for j in range(2):
            nexcell.append(Cell(canvas, i * Cell.cellw + 350, j * Cell.cellh + 150, 'White', 'White'))

    curb = Block(canvas, randrange(0, 7), False)
    nexb = Block(canvas, randrange(0, 7), True)

    Reset()

    global is_End
    global score
    global level
    global speed

    is_End=False
    score=0
    level=1
    speed=0.2

    canvas.delete(End_id)

    global End_Time
    End_Time=0

    global Res
    global Game_End
    global Game_Time

    Res.destroy()
    Game_End.destroy()
    Game_Time.destroy()


'''
def winput(event):
    global width
    width=int(eval(wid_entry.get()))

def hinput(event):
    global height
    height=int(eval(hei_entry.get()))



def init():
    canvas.create_rectangle(0,0,canvas.winfo_width(),canvas.winfo_height(),fill='lightgrey',outline='lightgrey')


    wid_entry=Entry(app,width=30,bg='lightgrey')
    wid_entry.place(x=canvas.winfo_width()/4,y=100,anchor='s')
    wid_entry.bind("<Return>",winput)

    hei_entry=Entry(app,width=30,bg='lightgrey')
    hei_entry.place(x=canvas.winfo_height()*3/4,y=100,anchor='s')
    hei_entry.bind("<Return>",hinput)

#app.after(1000,init())

#width=int(eval(wid_entry.get()))
#height=int(eval(hei_entry.get()))
'''

startx=10
starty=70
width=10
height=29
is_End=False
End_Time=0
score=0
level=1
speed=0.2
End_id=0

cell=[]
nexcell=[]
acb=[]

Remain_Time=StringVar()
Game_End=Label(app,text="Game End",bg='White',font=("Times New Roman",12))
Game_Time=Label(app,textvariable=Remain_Time,bg='White',font=("Times New Roman",11))
Res=Button(app,text="Restart?",command=Restart,font=("Times New Roman",13))

Welcome=Label(app,text="TETRIS",bg='White',font=("Times New Roman",30))
Welcome.place(x=canvas.winfo_width()/2,y=60,anchor='s')

Next_Block=Label(app,text="Next Block",bg='White',font=("Times New Roman",15))
Next_Block.place(x=375,y=120,anchor='s')
canvas.create_rectangle(325,130,425,200,fill="white",outline='black')

Your_score=Label(app,text="Your Score : ",bg='White',font=("Times New Roman",15))
Your_score.place(x=375,y=250,anchor='s')

Your_level=Label(app,text="Your Level : ",bg='White',font=("Times New Roman",15))
Your_level.place(x=375,y=285,anchor='s')

Made_by=Label(app,text="Made by kohandy",bg='White',font=("Calibri",9))
Made_by.place(x=440,y=600,anchor='s')

for i in range(width):
    for j in range(height):
        cell.append(Cell(canvas,i*Cell.cellw+startx,j*Cell.cellh+starty,'White','lightgrey'))

for i in range(4):
    for j in range(2):
        nexcell.append(Cell(canvas,i*Cell.cellw+350,j*Cell.cellh+150,'White','White'))

curb=Block(canvas,randrange(0,7),False)
nexb=Block(canvas,randrange(0,7),True)

while 1:
    #print(len(acb)
    #print(is_End)
    if is_End==True:
        #global End_Time
        if End_Time==0:
            End_Time=deepcopy(time())

        #print(int(time()-End_Time))
        Remain_Time.set(int(5-time()+End_Time))
        #print(Game_Time['text'])

        app.update()

        if is_End==False:
            continue

        if time()-End_Time>=5:
            break
        continue

    if Del_row()==True:
        sleep(0.2)

    #print(curb.is_stop())
    if curb.is_stop()==True:
        curb.dele()

        sleep(0.2)

        '''
        for i in range(width):
            if cell[i*height].num==-1:
                End()
                break
        '''

        curb=Block(canvas,nexb.type,False)
        nexb=Block(canvas,randrange(0,7),True)

    Reset()
    curb.draw()
    nexb.nexdraw()

    if score>=level*10:
        level+=1
        Your_level.config(bg="cyan")
        app.update()
        speed*=0.8
        sleep(0.2)
        Your_level.config(bg="White")

    sleep(speed)
    curb.move_down(True)
    app.update()