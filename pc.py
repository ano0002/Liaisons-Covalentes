import pygame as p
import sys
from vpython import *
from math import *
import sys
p.init()

def init_var() :
    """Crée toute les variables utilisés pour le projet"""
    global createdatome,on,drag,mousepos,appuiboutton,scrollmenu,survolindice,molecules,affichage
    
    affichage  = []
    scrollmenu =1
    appuiboutton = False
    createdatome = []
    on = True
    drag = None
    mousepos = p.mouse.get_pos()
    survolindice = None
    molecules =[]

def init_atome():
    """Création des flèches de menu, des atomes du menu et des infos affichés au survol"""
    global tableau,tableaunew,arrowup,arrowdown,infosmall,infomedium,infobig,validmol,movemol

    """Création des flèches de menu"""
    arrowup = p.image.load("ressources/images/arrow.png")
    arrowdown = p.transform.flip(p.image.load("ressources/images/arrow.png"),False,True)

    """Création des atomes du menu et des infos affichés au survol"""
    tableau = ["h","he","li","be","b","c","n","o","f","ne","na","mg","al","si","p","s","cl","ar"]
    tableaunew =[]
    infosmall=[]
    infomedium = []
    infobig= []
    validmol = p.image.load("ressources/images/valid.png")
    movemol = p.image.load("ressources/images/move.png")
    for atome in tableau :
        tableaunew.append(p.image.load("ressources/images/"+atome+".png"))
        infosmall.append(p.image.load("ressources/images/"+atome+"info.png"))
        infomedium.append(p.image.load("ressources/images/"+atome+"infomedium.png"))
        infobig.append(p.image.load("ressources/images/"+atome+"infobig.png"))

def init_fenetre():
    """Création de la fenêtre avec don icône de fenêtre et son titre"""
    global icon,info,size,screen,menu,x,scene

    """Création d'un icône pourla fenêtre"""
    icon = p.image.load('ressources/images/logo.png')
    p.display.set_icon(icon)

    """Création de la fenêtre"""
    p.display.set_caption("Les liaisons covalentes")
    info = p.display.Info()
    scene = canvas(width=info.current_w*0.75,height=info.current_h*0.75)
    size = int(info.current_w*0.75),int(info.current_h*0.75)
    screen = p.display.set_mode(size,p.RESIZABLE)
    menu = p.Rect(int(size[0]-100),0,100,size[1])

def resize(event):
    
    """Permet de redimmensionner la fenêtre de façon propre"""
    global screen,menu,x,size

    size = [event.w,event.h]
    if event.h<600 :
        size[1] = 600
    if event.w < 800 :
        size[0] = 800
    screen = p.display.set_mode(size,p.RESIZABLE)
    menu = p.Rect(int(event.w-100),0,int(100),event.h)
    x= (event.w-int(menu.width/2))-25

def mousemove(event):
    """Tiens à jour, la position de la souris(xmouse,ymouse)"""
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

def scrollup(event):
    """Gère toutes les actions lorsque l'utilisateur scrollup"""
    global scrollmenu
    
    if menu.collidepoint(event.pos) :
        scrollmenu += -1
    if scrollmenu < 1 :
        scrollmenu = 1
        
def scrolldown(event):
    """Gère toutes les actions lorsque l'utilisateur scrollup"""
    global scrollmenu
    
    if menu.collidepoint(event.pos) :
        scrollmenu += 1
    if scrollmenu > 3:
        scrollmenu = 3

def survol(event):
    """Règle l'apparition des informations supplémentaire au survol des atomes"""
    global x,y,scrollmenu,tableaunew,drag,survolindice
    
    y = 60
    survolindice = None
    for atome in range((scrollmenu-1)*7,scrollmenu*7 ) :
        try:
            rectato = tableaunew[atome].get_rect(topleft=(x,y))
            if rectato.collidepoint(event.pos) :
                survolindice = atome
            y+=70
        except:
            pass
        
    for atome in createdatome :
        if atome.show :
            rectatome = atome.atome.get_rect(topleft=atome.coord)
            if rectatome.collidepoint(event.pos) :
                indice = 0
                for atomebase in tableau :
                    if atome.name == atomebase :
                        survolindice = indice
                    indice += 1

def selectatome(event):
    """Observe si le click est effectué sur un atome et dans ce cas le sélectionne dans la liste drag"""
    global x,y,tableaunew,appuiboutton,drag,scrollmenu

    if arrowup.get_rect(topleft=(x,20)).collidepoint(event.pos) :
        scrollmenu += -1
    elif arrowdown.get_rect(topleft=(x,550)).collidepoint(event.pos) :
        scrollmenu += 1
    if scrollmenu < 1 :
        scrollmenu = 1
    elif scrollmenu > 3:
        scrollmenu = 3
    else :
        for mol in molecules :
            if mol.valid :
                rectmol = p.Rect(mol.coord[0],mol.coord[1],10,10)
                if rectmol.collidepoint(event.pos):
                    threeDmol(mol)
            rectmol = p.Rect(mol.coord[0],mol.coord[1]-12,10,10)
            if rectmol.collidepoint(event.pos):
                if mol.atomelist.__len__() > 1 :
                    drag = [2,mol]
                    for atome in mol.atomelist :
                        atome.show = False
        if drag == None :
            y = 60
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
                    createdatome[drag[1]].show = False
                    for instance in molecules:
                        try:
                            instance.atomelist.remove(createdatome[drag[1]])
                        except ValueError:
                            pass
                    createdatome[drag[1]].delall()
    appuiboutton= True

def distance(pointa,pointb) :
    """Renvoie la distance entre deux points"""
    distance = sqrt((pointa[0]-pointb[0])**2+(pointa[1]-pointb[1])**2)
    return int(distance)

def liaison(atomedrag,atomestay):
    """Fonction établissant les liaisons"""
    if atomedrag.attachments.__len__() < atomedrag.liaisonsmax and atomestay.attachments.__len__() < atomestay.liaisonsmax:
        rectdrag = atomedrag.atome.get_rect(center = (xmouse,ymouse))
        rectatome = atomestay.atome.get_rect(topleft= atomestay.coord)
        left = distance(rectatome.center,rectdrag.midright)
        right = distance(rectatome.center,rectdrag.midleft)
        top = distance(rectatome.center,rectdrag.midbottom)
        bottom = distance(rectatome.center,rectdrag.midtop)
        for attach in atomestay.attachments :
            if atomestay.attachments[attach][0] =="left" :
                left = 900
            elif atomestay.attachments[attach][0] == "right":
                right = 900
            elif atomestay.attachments[attach][0] == "top":
                top=900
            elif atomestay.attachments[attach][0] == "bottom":
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
    """Permet de créer les nouveaux atomes et de les stocker dans la liste des atomes"""
    global createdatome,lien,molecules

    lien = False
    
    if len(createdatome) != 0 :
        for instance in createdatome :
            if lien == False :
                tempato = ato(drag[1],(xmouse-25,ymouse-25))
                lien = liaison(tempato,instance)
                
    if lien != False :
        
        if lien[0] == "left":
            createdatome.append(ato(drag[1],(lien[1].coord[0]-50,lien[1].coord[1]),attachments={lien[1] : [lien[2],1]}))
        
        elif lien[0] == "right":
            createdatome.append(ato(drag[1],(lien[1].coord[0]+50,lien[1].coord[1]),attachments={lien[1] : [lien[2],1]}))
        
        elif lien[0] == "top":
            createdatome.append(ato(drag[1],(lien[1].coord[0],lien[1].coord[1]-50),attachments={lien[1] : [lien[2],1]}))
        
        elif lien[0] == "bottom":
            createdatome.append(ato(drag[1],(lien[1].coord[0],lien[1].coord[1]+50),attachments={lien[1] : [lien[2],1]}))
        
        for element in molecules :
            for atome in element.atomelist :
                if lien[1] == atome:
                    element.addnew(createdatome[createdatome.__len__()-1])
                    
        indice = -1
        
        for element in createdatome :
            indice+=1
            
        lien[1].addattach([createdatome[indice],lien[0]])
        
        for element in createdatome :
            if element.coord == (createdatome[indice].coord[0]-50,createdatome[indice].coord[1]) and element.liaisonsmax>= element.attachments.__len__()+1:
                element.addattach([createdatome[indice],"right"])
                
            if element.coord == (createdatome[indice].coord[0]+50,createdatome[indice].coord[1]) and element.liaisonsmax>= element.attachments.__len__()+1:
                element.addattach([createdatome[indice],"left"])
                
            if element.coord == (createdatome[indice].coord[0],createdatome[indice].coord[1]-50) and element.liaisonsmax>= element.attachments.__len__()+1:
                element.addattach([createdatome[indice],"bottom"])
                
            if element.coord == (createdatome[indice].coord[0],createdatome[indice].coord[1]+50) and element.liaisonsmax>= element.attachments.__len__()+1:
                element.addattach([createdatome[indice],"top"])
        if createdatome[indice].attachments.__len__()>createdatome[indice].liaisonsmax :
            createdatome[indice].delall()
            supperpose = True
            x=xmouse
            y=ymouse
            while supperpose==True :
                supperpose= False
                for atomec in createdatome :
                    if distance(atomec.atome.get_rect(topleft=atomec.coord).center,(x,y)) < 60:
                        supperpose = True
                if supperpose == True :
                    x+=-10
                    y+=10
            x+=-25
            y+=-25
            createdatome[indice].coord=(x,y)
            molecules.append(molecule(createdatome[createdatome.__len__()-1]))
    else:
        supperpose = True
        x=xmouse
        y=ymouse
        while supperpose==True :
            supperpose= False
            for atomec in createdatome :
                if distance(atomec.atome.get_rect(topleft=atomec.coord).center,(x,y)) < 60:
                    supperpose = True
            if supperpose == True :
                x+=-10
                y+=10
        x+=-25
        y+=-25
        createdatome.append(ato(drag[1],(x,y),attachments={}))
        molecules.append(molecule(createdatome[createdatome.__len__()-1]))

    pass

def moveatome(event):
    """Modifie la position des atomes une fois le click lacher"""
    global createdatome,lien,molecules

    if len(createdatome) != 0 :
        for instance in createdatome :
            if lien == False and instance != createdatome[drag[1]]:
                lien = liaison(createdatome[drag[1]],instance)
        createdatome[drag[1]].show=True
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
                
                if element.coord == (createdatome[drag[1]].coord[0]-50,createdatome[drag[1]].coord[1]) and element.liaisonsmax>= element.attachments.__len__()+1:
                    element.addattach([createdatome[drag[1]],"right"])
                if element.coord == (createdatome[drag[1]].coord[0]+50,createdatome[drag[1]].coord[1]) and element.liaisonsmax>= element.attachments.__len__()+1:
                    element.addattach([createdatome[drag[1]],"left"])
                if element.coord == (createdatome[drag[1]].coord[0],createdatome[drag[1]].coord[1]-50) and element.liaisonsmax>= element.attachments.__len__()+1:
                    element.addattach([createdatome[drag[1]],"bottom"])
                if element.coord == (createdatome[drag[1]].coord[0],createdatome[drag[1]].coord[1]+50) and element.liaisonsmax>= element.attachments.__len__()+1 :
                    element.addattach([createdatome[drag[1]],"top"])
                    
            if createdatome[drag[1]].attachments.__len__()>createdatome[drag[1]].liaisonsmax :
                createdatome[drag[1]].delall()
                supperpose = True
                x=xmouse
                y=ymouse
                while supperpose==True :
                    supperpose= False
                    for atomec in createdatome :
                        if distance(atomec.atome.get_rect(topleft=atomec.coord).center,(x,y)) < 60:
                            supperpose = True
                    if supperpose == True :
                        x+=-10
                        y+=10
                x+=-25
                y+=-25
                createdatome[drag[1]].coord=(x,y)
                molecules.append(molecule(createdatome[drag[1]]))
                
            for element in molecules :
                
                for atome in element.atomelist :
                    if lien[1] == atome and createdatome[drag[1]].attachments.__len__() != 0:
                        element.addnew(createdatome[drag[1]])


        else :
            
            supperpose = True
            x=xmouse
            y=ymouse
            
            while supperpose==True :
                supperpose= False
                for atomec in createdatome :
                    if atomec!= createdatome[drag[1]]:
                        if distance(atomec.atome.get_rect(topleft=atomec.coord).center,(x,y)) < 60:
                            supperpose = True
                if supperpose == True :
                    x+=-5
                    y+=10
                    
            x+=-25
            y+=-25
            
            createdatome[drag[1]].coord=(x,y)
                        
            molecules.append(molecule(createdatome[drag[1]]))
            
    else:
        createdatome[drag[1]].coord=(xmouse-25,ymouse-25)
        molecules.append(molecule(createdatome[drag[1]]))

def delatome(event):
    """Gère la suppression des atomes si ils sont Drag&Drop dans le menu"""
    indice = 0
    
    for element in createdatome :
        myrect = element.atome.get_rect(topleft=element.coord)
        if myrect.collidepoint(event.pos) :
            for instance in molecules:
                try:
                    instance.atomelist.remove(element)
                except ValueError:
                    pass
                        
            createdatome[indice].delall()
            createdatome.pop(indice)
            
        indice += 1

def draw():
    """Gère l'affichage et le raffraichissement de la fenêtre"""
    global screen,menu,tableaunew,createdatome,drag,xmouse,ymouse,y,x,scrollmenu,arrowup,arrowdown,survolindice,infosmall,infomedium,infobig,molecules,movemol
    
    screen.fill((196, 184, 179))

    indice = 0
    for element in createdatome :
        if drag != None and drag[1] == indice and drag[0] == 1 :
            pass
        else:
            if element.show :
                screen.blit(element.atome,element.coord)
        indice+=1

    p.draw.rect(screen,(128,128,128),menu)

    if survolindice != None:
        if size[1]<670  and size[0]<900:
            pass
        elif size[0]<900:
            screen.blit(infosmall[survolindice],(size[0]-100,size[1]-100))
        elif size[0]<1300:
            screen.blit(infomedium[survolindice],(0,size[1]-200))
        else:
            screen.blit(infobig[survolindice],(0,size[1]-304))


    for mol in molecules:
        tempx = 0
        tempy = size[1]
        for atome in mol.atomelist:
            if atome.coord[0]>tempx :
                tempx = atome.coord[0]
            if atome.coord[1]<tempy :
                tempy = atome.coord[1]
        mol.coord = [tempx+50,tempy]
        if mol.atomelist.__len__()>1 :
            if drag != None :
                if drag[0] == 2 :
                    screen.blit(movemol,(xmouse,ymouse))
                    if mol.valid :
                        screen.blit(validmol,(xmouse,ymouse+12))
                else :
                    screen.blit(movemol,(mol.coord[0],mol.coord[1]-12))
                    if mol.valid :
                        screen.blit(validmol,mol.coord)
            else :
                screen.blit(movemol,(mol.coord[0],mol.coord[1]-12))
                if mol.valid :
                    screen.blit(validmol,mol.coord)
        else :
            if mol.valid :
                screen.blit(validmol,mol.coord)
            
    y = 20
    screen.blit(arrowup,(x,y))
    y=60
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
        elif drag[0] == 2 :
            for atome in drag[1].atomelist :
                screen.blit(atome.atome,(atome.coord[0]-drag[1].coord[0]+xmouse,atome.coord[1]-drag[1].coord[1]+ymouse+12))

    p.display.flip()
    
def clearmolecule():
    """Nettoie les molécules"""
    global molecules
    
    for mol in molecules :
        if mol.atomelist.__len__() > 1 :
            for atome in mol.atomelist :
                if atome.attachments.__len__()==0 :
                    mol.atomelist.remove(atome)
                    molecules.append(molecule(atome))
    for moleculetest in molecules :
        if moleculetest.atomelist.__len__() == 0 :
            molecules.remove(moleculetest)
        
def validmolecules():
    """Test de stabilité des molécules"""
    for mol in molecules :
        liaisonscomplexes = []
        for eleme in mol.atomelist :
            for attach in eleme.attachments :
                eleme.attachments[attach][1] = 1
            if eleme.attachments.__len__()<eleme.liaisonsmax :
                liaisonscomplexes.append([eleme,eleme.liaisonsmax-eleme.attachments.__len__()])
        if liaisonscomplexes == [] :
            mol.valid=True
        else:
            maybe = 0
            for valeur in liaisonscomplexes : 
                for attach in valeur[0].attachments :
                    if valeur[1] != 0 :
                        for atome in liaisonscomplexes :
                            if attach == atome[0] :
                                if valeur[1]>=atome[1]:
                                    valeur[1] = valeur[1]- atome[1]
                                    atome[0].attachments[valeur[0]][1]=atome[1]+1
                                    valeur[0].attachments[atome[0]][1]=atome[1]+1
                                    atome[1]= 0
                                else:
                                    atome[1] = atome[1]- valeur[1]
                                    atome[0].attachments[valeur[0]][1]=valeur[1]+1
                                    valeur[0].attachments[atome[0]][1]=valeur[1]+1
                                    valeur[1]= 0
            
            for element in liaisonscomplexes:
                if element[1] != 0 :
                    maybe = 1
            
            if maybe == 0 :
                mol.valid=True
            else:
                mol.valid=False
        
def threeDmol(mol):
    """Gère tout le rendu 3d de la molécule"""
    global affichage
    
    for element in affichage :
        element.visible=False
    
    center = [0,0]
    
    for element in mol.atomelist :
        center[0] +=element.coord[0]
        center[1] +=element.coord[1]
    center[0] = center[0]/mol.atomelist.__len__()
    center[1] = center[1]/mol.atomelist.__len__()
    
    for elem in mol.atomelist :
        xrendu = (elem.coord[0]-center[0])/25
        yrendu = (elem.coord[1]-center[1])/-25
        affichage.append(sphere(pos=vector(xrendu,yrendu,0), radius=0.7,color = elem.color,shininess=0))
        
        for attach in elem.attachments :
            liaison = elem.attachments[attach][1]
            
            modif = (liaison-1)*0.15
            change = 0.3
            
            if elem.attachments[attach][0] == "left" or elem.attachments[attach][0] == "right":
                w = vector(0,modif,0)
            else:
                w = vector(modif,0,0)
            for blk in range(0,liaison) :
                if elem.attachments[attach][0] == "left":
                    affichage.append(cylinder(pos=vector(xrendu,yrendu,0)-w, radius=0.1,color = elem.color,shininess=0,axis = vector(-1,0,0),length = 1))
                    w.y -= change
                elif elem.attachments[attach][0] == "right":
                    affichage.append(cylinder(pos=vector(xrendu,yrendu,0)-w, radius=0.1,color = elem.color,shininess=0,axis = vector(1,0,0),length = 1))
                    w.y -= change
                elif elem.attachments[attach][0] == "top":
                    affichage.append(cylinder(pos=vector(xrendu,yrendu,0)-w, radius=0.1,color = elem.color,shininess=0,axis = vector(0,1,0),length = 1))
                    w.x -= change
                elif elem.attachments[attach][0] == "bottom":
                    affichage.append(cylinder(pos=vector(xrendu,yrendu,0)-w, radius=0.1,color = elem.color,shininess=0,axis = vector(0,-1,0),length = 1))
                    w.x -= change
        
def movemolecule(event,mol):
    for atome in mol.atomelist :
        atome.coord = (atome.coord[0]-drag[1].coord[0]+xmouse,atome.coord[1]-drag[1].coord[1]+ymouse+12)
        atome.show = True

class ato(object):
    """Classe des atomes"""

    def __init__(self,atome,coord,attachments={}) :
        self.show = True
        if atome == 0:
            self.valence = 1

        elif atome == 1 :
            self.valence= 0
        else:
            self.valence =(atome-1)%8

        if tableau[atome] == "c" :
            self.color=vector(0.4,0.4,0.4)
        elif tableau[atome] == "h":
            self.color=vector(1,1,1)
        elif tableau[atome] == "he" or tableau[atome] == "be" or tableau[atome] == "ne" or tableau[atome] == "ar":
            self.color=vector(1,0,1)
        elif tableau[atome] == "li":
            self.color=vector(0.5,0.1,0.1)
        elif tableau[atome] == "b" or tableau[atome] == "al"  or tableau[atome] == "cl":
            self.color=vector(0,1,0)
        elif tableau[atome] == "n" or tableau[atome] == "na":
            self.color=vector(0,0.5,0.8)
        elif tableau[atome] == "o":
            self.color=vector(1,0.25,0.25)
        elif tableau[atome] == "f" or tableau[atome] == "si" or tableau[atome] == "s":
            self.color=vector(1,1,0)
        elif tableau[atome] == "p":
            self.color=vector(1,0.5,0)
        self.atome= p.image.load("ressources/images/"+tableau[atome]+".png")
        self.coord= coord
        self.attachments= attachments
        self.liaisonsmax = 4-abs(4-self.valence)
        self.liaisonsmin = 1
        self.name = tableau[atome]
        if self.liaisonsmax == 0 :
            self.liaisonsmin = 0

    def __repr__(self):
        return '< Atome : '+self.name+' max liaisons('+str(self.liaisonsmax)+'), liaisons('+str(self.attachments.__len__())+') >'
    
    def addattach(self,attach,val=1):
        self.attachments[attach[0]] = [attach[1],val]
        if attach[1] == "right":
            attach[0].attachments[self] = ["left",val]
        elif attach[1] == "left":
            attach[0].attachments[self] = ["right",val]
        elif attach[1] == "top":
            attach[0].attachments[self] = ["bottom",val]
        elif attach[1] == "bottom":
            attach[0].attachments[self] = ["top",val]

    def delattach(self,attach):
        del attach[0].attachment[attach[1]]
        del self.attachments[attach[0]]

    def delall(self):
        for element in self.attachments :
            del element.attachments[self]
        self.attachments = {}

class molecule(object):
    """Classe permettant de stocker les molécules une fois créer"""
    def __init__(self, baseatome):
        self.atomelist=[baseatome]
        self.valid=False
        self.coord = [0,0]
    def addnew(self,newatome):
        self.atomelist.append(newatome)
    def delnew(self,todel):
        self.atomelist.remove(todel)

def main() :
    """Boucle principale du projet"""
    global x,y,xmouse,ymouse,createdatome,tableau,tableaunew,screen,menu,size,drag,lien,appuiboutton,icon,info,on,survolindice
    init_var()
    init_fenetre()
    init_atome()

    while on :
        lien=False

        for event in p.event.get() :
            if event.type == p.VIDEORESIZE:
                resize(event)


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

                if event.button == 4 :
                    scrollup(event)
                    
                if event.button == 5 :
                    scrolldown(event)
                    
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

                        elif drag[0] == 2:
                            movemolecule(event,drag[1])
                            
                        drag = None
                        
            elif event.type == p.QUIT :
                scene.delete()
                on = False
                

        clearmolecule()
        validmolecules()
        draw()
        

main()
p.quit()
sys.exit(0)