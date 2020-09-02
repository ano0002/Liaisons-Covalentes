import pygame as p
import sys
from math import *
p.init()

def init_var() :
    global createdatome,on,drag,mousepos,appuiboutton,scrollmenu,survolindice
    scrollmenu =1
    appuiboutton = False
    createdatome = []
    on = True
    drag = None
    mousepos = p.mouse.get_pos()
    survolindice = None

def init_atome():
    global tableau,tableaunew,arrowup,arrowdown,infosmall,infomedium,infobig

    """Création des flèches de menu"""
    arrowup = p.image.load("ressources/images/arrow.png")
    arrowdown = p.transform.flip(p.image.load("ressources/images/arrow.png"),False,True)

    """Création des atomes du menu et des infos affichés au survol"""
    tableau = ["h","he","li","be","b","c","n","o","f","ne","na","mg","al","si","p","s","cl","ar"]
    tableaunew =[]
    infosmall=[]
    infomedium = []
    infobig= []

    for atome in tableau :
        tableaunew.append(p.image.load("ressources/images/"+atome+".png"))
        infosmall.append(p.image.load("ressources/images/"+atome+"info.png"))
        infomedium.append(p.image.load("ressources/images/infomedium.png"))
        infobig.append(p.image.load("ressources/images/infobig.png"))

def init_fenetre():
    global icon,info,size,screen,menu,x

    """Création d'un icônepourla fenêtre"""
    icon = p.image.load('ressources/images/logo.png')
    p.display.set_icon(icon)

    """Création de la fenêtre"""
    p.display.set_caption("Les liaisons covalentes")
    info = p.display.Info()
    size = int(info.current_w*0.75),int(info.current_h*0.75)
    screen = p.display.set_mode(size,p.RESIZABLE)
    menu = p.Rect(int(size[0]-100),0,100,size[1])

def resize(event):
    global screen,menu,x,size

    size = (event.w,event.h)
    if event.w <300 and event.h <180 :
        screen = p.display.set_mode((300,180),p.RESIZABLE)
    else:
        screen = p.display.set_mode((event.w, event.h),p.RESIZABLE)
    menu = p.Rect(int(event.w-100),0,int(100),event.h)
    x= (event.w-int(menu.width/2))-25

def mousemove(event):
    global xmouse,ymouse

    xmouse,ymouse = event.pos
    if xmouse < 25 :
        xmouse = 25
    elif xmouse>menu.right-25 :
        xmouse = menu.right-25
    if ymouse < 25 :
        ymouse = 25
    elif ymouse>menu.bottom-25 :
        ymouse = menu.bottom-25

def survol(event):
    global x,y,scrollmenu,tableaunew,drag,survolindice
    y = 80
    survolindice = None
    for atome in range((scrollmenu-1)*7,scrollmenu*7 ) :
        try:
            rectato = tableaunew[atome].get_rect(topleft=(x,y))
            if rectato.collidepoint(event.pos) :
                survolindice = atome
            y+=70
        except:
            pass

def selectatome(event):
    global x,y,tableaunew,appuiboutton,drag,scrollmenu

    if arrowup.get_rect(topleft=(x,40)).collidepoint(event.pos) :
        scrollmenu += -1
    elif arrowdown.get_rect(topleft=(x,570)).collidepoint(event.pos) :
        scrollmenu += 1
    if scrollmenu < 1 :
        scrollmenu = 1
    elif scrollmenu > 3:
        scrollmenu = 3
    else :
        y = 80
        for atome in range((scrollmenu-1)*7,scrollmenu*7 ) :
            try:
                rectato = tableaunew[atome].get_rect(topleft=(x,y))
                if rectato.collidepoint(event.pos) :
                    drag = [0,atome]
                y+=70
            except:
                pass
        indice = 0
        for instance in createdatome :
            rectinstance = instance.atome.get_rect(topleft=instance.coord)
            if rectinstance.collidepoint(event.pos) :
                drag = [1,indice]
            indice+=1
        if drag != None :
            if drag[0] == 1 :
                createdatome[drag[1]].delall()
    appuiboutton= True

def distance(pointa,pointb) :
    """renvoie la distance entre deux points"""
    distance = sqrt((pointa[0]-pointb[0])**2+(pointa[1]-pointb[1])**2)
    return int(distance)

def liaison(atomedrag,atomestay):
    """fonction établissant les liaisons"""
    if atomedrag.attachments.__len__() < atomedrag.liaisonsmax and atomestay.attachments.__len__() < atomestay.liaisonsmax:
        rectdrag = atomedrag.atome.get_rect(center = (xmouse,ymouse))
        rectatome = atomestay.atome.get_rect(topleft= atomestay.coord)
        left = distance(rectatome.center,rectdrag.midright)
        right = distance(rectatome.center,rectdrag.midleft)
        top = distance(rectatome.center,rectdrag.midbottom)
        bottom = distance(rectatome.center,rectdrag.midtop)
        for attach in atomestay.attachments :
            if atomestay.attachments[attach] =="left" :
                left = 900
            elif atomestay.attachments[attach] == "right":
                right = 900
            elif atomestay.attachments[attach] == "top":
                top=900
            elif atomestay.attachments[attach] == "bottom":
                bottom= 900
        if left<right and left<bottom and left<top and left<45 :
            return ("left",atomestay,"right")
        elif right<left and right<bottom and right<top and right<45 and atomestay.coord[0]+75 < menu.left:
            return ("right",atomestay,"left")
        elif top<right and top<bottom and top<left and top<45 :
            return ("top",atomestay,"bottom")
        elif bottom<right and bottom<left and bottom<top and bottom<45 :
            return ("bottom",atomestay,"top")
        else:
            return False
    else :
        return False

def newatome(event):
    global createdatome,lien

    lien = False
    if len(createdatome) != 0 :
        for instance in createdatome :
            if lien == False :
                tempato = ato(drag[1],(xmouse-25,ymouse-25))
                lien = liaison(tempato,instance)
    if lien != False :
        if lien[0] == "left":
            createdatome.append(ato(drag[1],(lien[1].coord[0]-50,lien[1].coord[1]),attachments={lien[1] : lien[2]}))
        elif lien[0] == "right":
            createdatome.append(ato(drag[1],(lien[1].coord[0]+50,lien[1].coord[1]),attachments={lien[1] : lien[2]}))
        elif lien[0] == "top":
            createdatome.append(ato(drag[1],(lien[1].coord[0],lien[1].coord[1]-50),attachments={lien[1] : lien[2]}))
        elif lien[0] == "bottom":
            createdatome.append(ato(drag[1],(lien[1].coord[0],lien[1].coord[1]+50),attachments={lien[1] : lien[2]}))
        indice = -1
        for element in createdatome :
            indice+=1
        lien[1].addattach([createdatome[indice],lien[0]])
        for element in createdatome :
            if element.coord == (createdatome[indice].coord[0]-50,createdatome[indice].coord[1]) :
                element.addattach([createdatome[indice],"right"])
            if element.coord == (createdatome[indice].coord[0]+50,createdatome[indice].coord[1]) :
                element.addattach([createdatome[indice],"left"])
            if element.coord == (createdatome[indice].coord[0],createdatome[indice].coord[1]-50) :
                element.addattach([createdatome[indice],"bottom"])
            if element.coord == (createdatome[indice].coord[0],createdatome[indice].coord[1]+50) :
                element.addattach([createdatome[indice],"top"])
    else:
        createdatome.append(ato(drag[1],(xmouse-25,ymouse-25),attachments={}))

    pass

def moveatome(event):
    global createdatome,lien

    if len(createdatome) != 0 :
        for instance in createdatome :
            if lien == False and instance != createdatome[drag[1]]:
                lien = liaison(createdatome[drag[1]],instance)

        if lien != False :

            if lien[0] == "left":
                createdatome[drag[1]].coord =(lien[1].coord[0]-50,lien[1].coord[1])

            elif lien[0] == "right":
                createdatome[drag[1]].coord=(lien[1].coord[0]+50,lien[1].coord[1])

            elif lien[0] == "top":
                createdatome[drag[1]].coord=(lien[1].coord[0],lien[1].coord[1]-50)

            elif lien[0] == "bottom":
                createdatome[drag[1]].coord=(lien[1].coord[0],lien[1].coord[1]+50)

            lien[1].addattach([createdatome[drag[1]],lien[0]])

            for element in createdatome :
                if element.coord == (createdatome[drag[1]].coord[0]-50,createdatome[drag[1]].coord[1]) :
                    element.addattach([createdatome[drag[1]],"right"])
                if element.coord == (createdatome[drag[1]].coord[0]+50,createdatome[drag[1]].coord[1]) :
                    element.addattach([createdatome[drag[1]],"left"])
                if element.coord == (createdatome[drag[1]].coord[0],createdatome[drag[1]].coord[1]-50) :
                    element.addattach([createdatome[drag[1]],"bottom"])
                if element.coord == (createdatome[drag[1]].coord[0],createdatome[drag[1]].coord[1]+50) :
                    element.addattach([createdatome[drag[1]],"top"])
        else :
            createdatome[drag[1]].coord=(xmouse-25,ymouse-25)
    else:
        createdatome[drag[1]].coord=(xmouse-25,ymouse-25)

def delatome(event):

    indice = 0
    for element in createdatome :
        myrect = element.atome.get_rect(topleft=element.coord)
        if myrect.collidepoint(event.pos) :
            createdatome[indice].delall()
            createdatome.pop(indice)
        indice += 1
    pass

def draw():
    global screen,menu,tableaunew,createdatome,drag,xmouse,ymouse,y,x,scrollmenu,arrowup,arrowdown,survolindice,infosmall,infomedium,infobig

    screen.fill((196, 184, 179))

    indice = 0
    for element in createdatome :
        if drag!= None and drag[1] == indice and drag[0] == 1 :
            pass
        else:
            screen.blit(element.atome,element.coord)
        indice+=1

    p.draw.rect(screen,(128,128,128),menu)

    if survolindice != None:
        if size[0]<900:
            screen.blit(infosmall[survolindice],(size[0]-100,size[1]-100))
        elif size[0]<1300:
            screen.blit(infomedium[survolindice],(0,size[1]-200))
        else:
            screen.blit(infobig[survolindice],(0,size[1]-304))
    y = 40
    screen.blit(arrowup,(x,y))
    y=80
    for i in range((scrollmenu-1)*7,scrollmenu*7 ) :
        try:
            screen.blit(tableaunew[i],(x,y))
        except IndexError:
            pass
        y+=70

    screen.blit(arrowdown,(x,y))


    if drag!= None :
        if drag[0] == 0 :
            screen.blit(tableaunew[int(drag[1])],(xmouse-25,ymouse-25))
        elif drag[0] == 1 :
            screen.blit(createdatome[int(drag[1])].atome,(xmouse-25,ymouse-25))

    p.display.flip()

class ato:
    """Classe des atomes"""

    def __init__(self,atome,coord,attachments={}) :
        if atome == 0:
            self.valence = 1

        elif atome == 1 :
            self.valence= 0
        else:
            self.valence =(atome-1)%8

        self.atome= p.image.load("ressources/images/"+tableau[atome]+".png")
        self.coord= coord
        self.attachments= attachments
        self.liaisonsmax = 4-abs(4-self.valence)
        self.liaisonsmin = 1
        if self.liaisonsmax == 0 :
            self.liaisonsmin = 0

    def addattach(self,attach):
        self.attachments[attach[0]] = attach[1]
        if attach[1] == "right":
            attach[0].attachments[self] = "left"
        elif attach[1] == "left":
            attach[0].attachments[self] = "right"
        elif attach[1] == "top":
            attach[0].attachments[self] = "bottom"
        elif attach[1] == "bottom":
            attach[0].attachments[self] = "top"

    def delattach(self,attach):
        del attach[0].attachment[attach[1]]
        del self.attachments[attach[0]]

    def delall(self):
        for element in self.attachments :
            element.attachments.pop(self)
        self.attachments = {}

def main() :
    global x,y,xmouse,ymouse,createdatome,tableau,tableaunew,screen,menu,size,drag,lien,appuiboutton,icon,info,on,survolindice
    init_var()
    init_fenetre()
    init_atome()

    while on :
        lien=False

        for event in p.event.get() :
            if event.type == p.VIDEORESIZE:
                resize(event)

            elif event.type == p.KEYDOWN :
                if event.key == p.K_ESCAPE:
                    on = False

            elif event.type == p.MOUSEMOTION :
                mousemove(event)
                try:
                    survol(event)
                except :
                    pass

            elif event.type == p.MOUSEBUTTONDOWN :
                if event.button == 1 :
                    selectatome(event)

            elif event.type == p.MOUSEBUTTONUP :

                if event.button == 3 :
                    if appuiboutton != True :
                        delatome(event)

                if event.button == 1 :

                    appuiboutton= False

                    if drag != None :

                        if event.pos[0]>menu.left or size[0] <= 125:
                            if drag[0] == 1 :
                                createdatome.pop(drag[1])

                        elif drag[0] == 0 :
                            newatome(event)

                        elif drag[0] ==1:
                            moveatome(event)

                        drag = None

            elif event.type == p.QUIT :
                on = False

        draw()

main()