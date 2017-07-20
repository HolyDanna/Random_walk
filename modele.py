""" Renderin d'un modele avec Tkinter. """
import sys
from tkinter import *
from time import sleep
import walker

doRenderTk=True # choix de faire un rendering Tk ou pas

class Modele(object):
    """ Modele pour simulation. """

    def __init__(self, master=None):
        # canvas pour le rendering graphique
        self.canvasHeight = 600
        self.canvasWidth = 600
        self.canvas_size=(self.canvasWidth, self.canvasHeight) # taille du canvas pour le rendering
        self.walker=None
        self.x = self.canvasHeight//2
        self.y = self.canvasWidth//2
        self.maxSteps=50
        if master is not None: # fenetre de rendering si necessaire
            self.refreshTk=1.0
            self.waitTk=3

            self.controls = Frame(master)
            self.controls.pack(side=LEFT)

            self.s = Label(self.controls, text="""Combien de pas souhaitez-vous effectuer ?""",
                justify = LEFT, padx = 20)
            self.s.pack(padx=10)
            self.steps = Entry(self.controls)
            self.steps.pack()
            Label(self.controls).pack(pady=20)

            self.gtype = IntVar()
            self.gtype.set(0)
            pos_types = [("Classique", 0),("Sans-Retour",1),("Passage Unique",2)]
            self.t = Label(self.controls, text="""Quel type de déplacement souhaitez-vous utiliser ?""",
                justify = LEFT, padx = 20)
            self.t.pack(padx=10)
            for txt, val in pos_types:
                Radiobutton(self.controls, text=txt, padx = 20, variable=self.gtype,
                    value=val).pack(padx=10)

            Label(self.controls).pack(pady=20)

            self.sbutton = Button(self.controls, text="LANCER", command=self.run)
            self.sbutton.pack()
            # self.qbutton = Button(self.controls, text="QUITTER", command=quit).pack()

            self.frame = Frame(master)
            self.frame.pack(side=LEFT)

            self.bframe=Frame(self.frame)
            self.bframe.pack(side=TOP)

            self.gframe=Frame(self.frame,bd=2,relief=RAISED)

            self.g=Canvas(self.gframe,bg='white',width=self.canvas_size[0],height=self.canvas_size[1])
            self.g.pack()

            self.gframe.pack(side=LEFT)
            self.g.delete(ALL) # clean du canvas
        else: self.g=None


    # putting everything back to an initial value for another launch
    # we keep the walker as it is, not to reset the RNG
    def start(self):
        if self.walker is None:
            self.walker = walker.walker()
        else:
            self.walker.reset()
        self.walker.setType(self.gtype.get())
        print(self.gtype.get())
        if self.steps.get().isdigit():
            self.maxSteps = int(self.steps.get())
        self.x = self.canvasHeight//2
        self.y = self.canvasWidth//2
        self.mult = max(min(10000/self.maxSteps,10),2)
        if self.gtype.get() == 2:
            self.mult = self.mult//2


    def update(self): # update du modele
        direction = self.walker.update()
        return direction

    # re-rendering from Zero if we have to walk back (self-avoidance)
    def renderFromZero(self):
        self.g.delete(ALL)
        self.x = self.canvasHeight//2
        self.y = self.canvasWidth//2
        path = self.walker.getPath()
        step_nbr = self.walker.getStepNbr()
        for i in reversed(range(step_nbr)):
            direction = (path//4**i)%4
            if direction%2:
                self.g.create_line(self.x, self.y, self.x + self.mult*(direction - 2),
                    self.y, fill="#476042")
                self.x = self.x + self.mult*(direction - 2)
            else:
                self.g.create_line(self.x, self.y, self.x,
                    self.y + self.mult*(direction - 1), fill="#476042")
                self.y = self.y + self.mult*(direction - 1)

    # render the last movement, using the direction we went to
    def render(self,direction):
        if direction%2 :
            self.g.create_line(self.x, self.y, self.x + self.mult*(direction - 2),
                self.y, fill="#476042")
            self.x = self.x + self.mult*(direction - 2)
        else:
            self.g.create_line(self.x, self.y, self.x,
                self.y + self.mult*(direction - 1), fill="#476042")
            self.y = self.y + self.mult*(direction - 1)


    def run(self):
        ############################################
        # debut boucle de simulation de la dynamique
        self.g.delete(ALL)
        self.start()
        i=0
        while i < self.maxSteps:
            direction = self.update()
            # this is the case where no further tils is available
            # we go back one step
            if direction == -1:
                self.renderFromZero()
                i -= 1
            # if there's a tile available, we move forward
            else:
                self.render(direction)
                i += 1
        # we print the value containing the path in base 4
        print(self.walker.getPath())
        # print(self.walker.getStepNbr())
        print("DONE")
        # fin boucle de simulation de la dynamique
        ############################################

""" A executer seulement si ce n'est pas un import, mais bien un run du code. """
if __name__ == '__main__':
    if doRenderTk: # avec rendering Tk (animation)
        root = Tk(); root.geometry("+0+0"); root.title("simulation")
    else: root=None
    x = Modele(root) # creation du modele
#   x.run() # run du modele (simulation) avec ou sans animation
    if root is not None: root.mainloop()
