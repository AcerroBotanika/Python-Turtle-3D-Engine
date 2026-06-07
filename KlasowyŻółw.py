class Class:                 #Silnik renderujący
    def __init__(self):
        pass

    def Macierz_projekcji(self): #macierz projekcji
        fov=90                   #>parametry kamery
        aspect=1.0
        blisko=1
        daleko=3                 #>
        MP=np.array([[(1/aspect*math.tan(math.radians(fov)/2)),0,0,0],
                          [0,(1/math.tan(math.radians(fov)/2)),0,0],
                          [0,0,(-1*((daleko+blisko)/(daleko-blisko))),(-1*(2*(daleko*blisko)/(daleko-blisko)))],
                          [0,0,-1,0]])
        MP=torch.tensor(MP).to(device)
        self.MP=MP

    def Macierz_translacji(self): #macierz translacji/macierz widoku
        MT=np.array([[1,0,0,0],
                          [0,1,0,0],
                          [0,0,1,-3],
                          [0,0,0,1]])
        MT=torch.tensor(MT).to(device)
        self.MT=MT

    def Macierz_rotacji(self,kat): #macierz rotacji
        MR=np.array([[math.cos(math.radians(kat)),0,math.sin(math.radians(kat)),0], #obrót wokół osi Y
                          [0,1,0,0],
                          [-1*(math.sin(math.radians(kat))),0,math.cos(math.radians(kat)),0],
                          [0,0,0,1]])
        MR=torch.tensor(MR).to(device)
        self.MR=MR

    def Konfiguracja_turtle(self): # Konfiguracja okna i żółwia
        window = turtle.Screen()
        window.bgcolor("black")
        window.tracer(0,0)

        t = turtle.Turtle()
        t.color("blue")
        t.fillcolor("green")
        t.speed(3)
        t.penup()

        self.t=t
        self.window=window

    def Mnozenie_macierzy(self,punkty):
        self.MM=self.MP @ self.MT @ self.MR
        self.MM=self.MM.float().to(device)

        punktC=[]
        punkty_gpu=torch.tensor(punkty).to(device)
        punktC=self.MM @ punkty_gpu.T
        punktC=punktC.T

        x=200*(punktC[:,0]/punktC[:,3])
        y=200*(punktC[:,1]/punktC[:,3])

        x=x.cpu().numpy()
        y=y.cpu().numpy()



        #print("PunktC przed podziałem: ",punktC)

        self.punktC=list(zip(x,y))

    def Rysowanie_punktów(self):
       for i in self.punktC:
           self.t.goto(i)
           self.t.dot(10, "red")

    def Rysowanie_linii(self,linie):
        for i in linie:
           #print("linia: ",i)
           #print("Punktc: ", self.punktC)
           self.t.goto(self.punktC[i[0]])
           self.t.pendown()
           self.t.goto(self.punktC[i[1]])
           self.t.penup()

    def Rysowanie_scian(self,sciany):
        for i in sciany:
           self.t.goto(self.punktC[i[0]])
           self.t.begin_fill()
           for j in range(len(i)):
               self.t.goto(self.punktC[i[j]])
           self.t.end_fill()

import turtle
import numpy as np
import math
import torch
import torch_directml
import ObjLoader as klasa1

device = torch_directml.device()
print("Wybrane urządzenie:", torch_directml.device_name(0))

#sześcian
punkty=[
    [1,  1,  1, 1],  # 0: przód prawy góra
    [-1,  1,  1, 1], # 1: przód lewy góra
    [1, -1,  1, 1],  # 2: przód prawy dół
    [-1, -1,  1, 1], # 3: przód lewy dół
    [1,  1, -1, 1],  # 4: tył prawy góra
    [-1,  1, -1, 1], # 5: tył lewy góra
    [1, -1, -1, 1],  # 6: tył prawy dół
    [-1, -1, -1, 1]  # 7: tył lewy dół
]

linie=[[0,1],
       [1,3],
       [3,2],
       [2,0],
       [0,4],
       [1,5],
       [2,6],
       [3,7],
       [7,6],
       [6,4],
       [4,5],
       [5,7]]

sciany=[[0,1,3,2], #przód
        [0,1,5,4], #góra
        [2,3,7,6], #dół
        [0,2,6,4], #prawo
        [1,3,7,5], #lewo
        [4,5,7,6]] #tył

#Wavefront object
punkty=klasa1.punkty
linie=klasa1.linie
sciany=klasa1.sciany
silnik=Class()
silnik.Konfiguracja_turtle()
kat=0
while 1==1:
    # Rysowanie kwadratu za pomocą pętli
   silnik.Macierz_rotacji(kat)
   silnik.Macierz_projekcji()
   silnik.Macierz_translacji()
   silnik.Mnozenie_macierzy(punkty)
   silnik.t.clear()
   silnik.Rysowanie_punktów()
   silnik.Rysowanie_linii(linie)
   silnik.Rysowanie_scian(sciany)
           
   turtle.update()
   kat+=1  

   #print("sigma")

