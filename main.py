"""Crée un jeu de démineur"""

import tkinter as tk
from sys import exit
from random import randint

nombre_cases_ligne = 10
nombre_bombes = 20
coups_joues = 0

class Case:
    """Crée une case de démineur"""

    def __init__(self, *coos):
        self.__coos = coos
        self.__reveal = False
        self.__bomb = False
        self.__flag = False
        self.__flag_adress = 0
        self.__canvas = tk.Canvas(fenetre,bg = '#E23C4E', cursor = 'pirate', width = int(500/nombre_cases_ligne)-2, height = int(500/nombre_cases_ligne)-2, highlightthickness=1, highlightbackground="black")
        self.__canvas.bind('<1>', self.reveler)
        self.__canvas.bind('<3>', self.chFlag)


    def addBomb(self):
        self.__bomb = True

    def positionner(self, x, y):
        self.__canvas.grid(column = x, row = y)

    def reveler(self, *evt):
        if not self.__reveal and not self.__flag:
            if not plateau.doesBomb():
                plateau.addBombs(self.__coos)
            global coups_joues
            coups_joues += 1
            self.__reveal = True
            if self.__bomb == True:
                lose()

            else:
                self.showNumber(self.nombre())

            if coups_joues + nombre_bombes >= nombre_cases_ligne**2:
                win()

    def chFlag(self, evt):
        if not self.__reveal:
            if self.__flag:
                self.__canvas.delete(self.__flag_adress)
                self.__canvas.configure(bg = '#E23C4E')

            else:
                self.__flag_adress = self.__canvas.create_image(int(250/nombre_cases_ligne)-1, int(250/nombre_cases_ligne)-1, image = FLAG)
                self.__canvas.configure(bg = '#FFFFFF')

            self.__flag = not self.__flag

    def nombre(self):
        somme = 0
        adjacents = [(-1,-1), (0, -1), (1, 0), (-1, 0), (1,-1), (-1, 1), (1,1), (0,1)]
        for i in adjacents:
            try:
                if plateau.getCase(self.__coos[0]+i[0],self.__coos[1]+i[1]).isABomb():
                    somme+=1
            except IndexError:
                pass

        return somme


    def showNumber(self, nombre):
        if nombre != 0:
            self.__canvas.create_text(int(250/nombre_cases_ligne)-1, int(250/nombre_cases_ligne)-1, text = nombre, font = ('Helvetica', str(int(360/nombre_cases_ligne))))

        else:
            self.__canvas.configure(bg = '#505050')
            adjacents = [(-1,-1), (0, -1), (1, 0), (-1, 0), (1,-1), (-1, 1), (1,1), (0,1)]
            for i in adjacents:
                try:
                    plateau.getCase(self.__coos[0]+i[0],self.__coos[1]+i[1]).reveler()
                except IndexError:
                    pass

    def isABomb(self):
        return self.__bomb


class Plateau:
    """Crée le plateau de jeu"""

    def __init__(self):
        self.__bombs = False
        self.__cases = [[Case(i, j) for j in range(nombre_cases_ligne)] for i in range(nombre_cases_ligne)]
        [[self.__cases[x][y].positionner(x, y) for x in range(len(self.__cases[y]))] for y in range(len(self.__cases))]

    def doesBomb(self):
        i = self.__bombs
        self.__bombs = True
        return i

    def addBombs(self, coos):
        adjacents = [(-1,-1), (0, -1), (1, 0), (-1, 0), (1,-1), (-1, 1), (1,1), (0,1)]
        non = [coos]
        for i in adjacents:
            non.append((coos[0]+i[0],coos[1] + i[1]))
        bombs = []
        while len(bombs) != nombre_bombes:
            x = randint(0, nombre_cases_ligne-1)
            y = randint(0, nombre_cases_ligne-1)
            if not (x,y) in bombs and not (x, y) in non:
                bombs.append((x,y))

        for i in bombs:
            self.__cases[i[0]][i[1]].addBomb()


    def getCase(self, x, y):
        if x >= 0 and y >= 0:
            return self.__cases[x][y]
        else:
            raise IndexError

def lose():
    
    for w in fenetre.winfo_children():
        w.destroy()
    perdu = tk.Canvas(fenetre, bg = '#A23C4E', cursor = 'pirate', width = 500, height = 500)
    perdu.create_text(250, 200, text = "PERDU", font = ('Helvetica', '60'))
    perdu.pack()


def win():
    for w in fenetre.winfo_children():
        w.destroy()
    perdu = tk.Canvas(fenetre, bg = '#A23C4E', cursor = 'pirate', width = 500, height = 500)
    perdu.create_text(250, 200, text = "VICTOIRE", font = ('Helvetica', '60'))
    perdu.pack()

def difficulte():
    canvas = tk.Canvas(fenetre, bg = '#A23C4E', cursor = 'pirate', width = 500, height = 500)
    facile = canvas.create_text(250,150, text = "facile", font = ('Helvetica', '36'))
    moyen = canvas.create_text(250,350, text = "moyen", font = ('Helvetica', '36'))
    canvas.tag_bind(facile,'<1>', setFacile)
    canvas.tag_bind(moyen,'<1>', setMoyen)
    canvas.pack()
    fenetre.mainloop()
    for w in fenetre.winfo_children():
        w.destroy()

def setFacile(*evt):
    global nombre_cases_ligne
    global nombre_bombes
    nombre_cases_ligne = 10
    nombre_bombes = 20
    fenetre.quit()

def setMoyen(*evt):
    global nombre_cases_ligne
    global nombre_bombes
    nombre_cases_ligne = 20
    nombre_bombes = 100
    fenetre.quit()



if __name__ == '__main__':
    fenetre = tk.Tk()
    fenetre.title('El famoso Demineuro')
    fenetre.geometry("500x500+0+0")
    difficulte()

    FLAG = tk.PhotoImage(master = fenetre, file = 'flag.pgm')

    plateau = Plateau()
    fenetre.resizable(height = False, width = False)
    fenetre.mainloop()