import pygame, sys, random, math, time, numpy
from pygame.locals import*
from random import*
from numpy import*

LARGEUR = 825
HAUTEUR = 825
NOIR = (0,0,0)

#

#Initialisation de pygame
pygame.init()

#Initialisation de la fenetre graphique
fenetre = pygame.display.set_mode((LARGEUR,HAUTEUR))

#Initialisation du son
pygame.mixer.init()

#chargement de l'image en mémoire vive
image_jeu  = pygame.image.load("poulpito-pixilart(1).png")
image_méga = pygame.image.load("meg-qui-bouge-et-croque-et-inversé-pixilart.png")
FUMéE  = pygame.image.load("fumée.png")
FUMéE2  = pygame.image.load("fumée2.png")
COIN  = pygame.image.load("coin_yeux.png")
PIERRE  = pygame.image.load("pierre.png")
FOND = pygame.image.load("fond_abyssale.png")
image_game_over = pygame.image.load("Game_Over.png")
image_game_clear = pygame.image.load("Game_Clear.png")
image_touche = pygame.image.load("touche.png")

#chargement du son en mémoire vive
#musique_jeu = pygame.mixer.Sound("music.mp3")
#-----------------------------------FONCTIONS-----------------------------------------------



def miseAjour():
    global personnage

# changer l'orientation d'une image
def blitOriente(fenetre, image, x, y, zone, angle):
    image_portion = image.subsurface(zone)
    # Coordonnées du centre de la portion d'image
    centre_x = image_portion.get_width() // 2
    centre_y = image_portion.get_height() // 2
    # Fais pivoter la copie de la portion d'image autour de son centre
    image_portion_pivot = pygame.transform.rotate(image_portion, angle)
    # Calcule les nouvelles coordonnées de la portion d'image pivotée
    nouveau_x = x+centre_x - image_portion_pivot.get_width() // 2
    nouveau_y = y+centre_y - image_portion_pivot.get_height() // 2
    # Dessine la portion d'image pivotée sur la surface d'origine
    fenetre.blit(image_portion_pivot, (nouveau_x, nouveau_y))

#----------------PERSONNAGE-----------------------

#Si le personnage n'a plus de pv, le jeu s'arrête
    if personnage["pv"] <= 0:
        personnage["direction"] = 0
        personnage["zone"] = 56,225,51,71
        fenetre.blit(image_game_over,(game_over["x"], game_over["y"]),game_over["zone"])
        return  # Sortir de la fonction si le personnage est mort


#on déplace le personnage dans le sens de la flèche en continu
    if personnage["direction"] == 1:
        personnage["x"] =  personnage["x"] + personnage["vitesse"]
    if personnage["direction"] == -1:
        personnage["x"] =  personnage["x"] - personnage["vitesse"]
    if personnage["direction"] == 2:
        personnage["y"] =  personnage["y"] - personnage["vitesse"]
    if personnage["direction"] == -2:
        personnage["y"] =  personnage["y"] + personnage["vitesse"]

#Le personnage ne sort pas de la fenêtre
    if personnage['x'] <= 25:
        personnage['x'] = 25
    elif personnage['x'] >= LARGEUR - personnage['zone'][2] - 25:
        personnage['x'] = LARGEUR - personnage['zone'][2] -25

    if personnage['y'] <= 25:
        personnage['y'] = 25
    elif personnage['y'] >= HAUTEUR - personnage['zone'][3] - 25:
        personnage['y'] = HAUTEUR - personnage['zone'][3] - 25



# Vérification de la collision entre le personnage et le monstre
    rect_personnage = pygame.Rect(personnage['x'], personnage['y'], personnage['zone'][2], personnage['zone'][3])
    rect_monstre = pygame.Rect(monstre['x'], monstre['y'], monstre['zone'][2], monstre['zone'][3])

    if rect_personnage.colliderect(rect_monstre):
        personnage["pv"] = personnage["pv"] - monstre["attaque"]
        monstre["pv"] = monstre["pv"] - personnage["attaque"]
        print("Collision entre le personnage et le monstre!")
        print(" Le Calamar a encore", personnage["pv"], "points de vie")
        print(" Le Requin a encore", monstre["pv"], "points de vie")








    global image_méga
#---------------------MONSTRE-------------------

#Le monstre ne sort pas de la fenêtre
    if monstre['x'] <= 0:
        monstre['x'] = 0
    elif monstre['x'] >= LARGEUR - monstre['zone'][2]:
        monstre['x'] = LARGEUR - monstre['zone'][2]

    if monstre['y'] <= 0:
        monstre['y'] = 0
    elif monstre['y'] >= HAUTEUR - monstre['zone'][3]:
        monstre['y'] = HAUTEUR - monstre['zone'][3]

#Requin qui patrouille dans sa zone de confort
    rect_ZoneMonstre = pygame.Rect(400,250,315,380)
    if monstre['x'] < rect_ZoneMonstre[0] or monstre['x'] > (rect_ZoneMonstre[0]+rect_ZoneMonstre[2]):
        monstre["directionX"] = monstre["directionX"]*(-1)
    if monstre['y'] < rect_ZoneMonstre[1] or monstre['y'] > (rect_ZoneMonstre[1]+rect_ZoneMonstre[3]):
        monstre["directionY"] = monstre["directionY"]*(-1)
        monstre["vitesse"] = 0.1


#Si le personnage entre dans la zone, le requin le poursuit
    if personnage['x'] >= rect_ZoneMonstre[0] and personnage['x'] - 40 <= (rect_ZoneMonstre[0]+rect_ZoneMonstre[2]) and personnage['y'] >= rect_ZoneMonstre[1] and personnage['y'] <= (rect_ZoneMonstre[1]+rect_ZoneMonstre[3]+25):
       monstre["directionX"] = personnage['x'] - monstre['x']
       monstre['directionY'] = personnage['y'] - monstre['y']

#Le requin se déplace en fonctoin de la direction
    if monstre["directionX"] >= 0:
        monstre["x"] =  monstre["x"] + monstre["vitesse"]
        monstre['zone'] = (261,0,87,38)
    if monstre["directionX"] <= 0:
        monstre["x"] =  monstre["x"] - monstre["vitesse"]
        monstre['zone'] = (0,0,87,38)

    if monstre["directionY"] >= 0:
        monstre["y"] =  monstre["y"] + monstre["vitesse"]
    if monstre["directionY"] <= 0:
         monstre["y"] =  monstre["y"] - monstre["vitesse"]




#On met en place la zone de sortie du jeu et la victoire
    rect_ZoneSortie = pygame.Rect(825-128,420,102,30)
    if personnage['x'] >= rect_ZoneSortie[0] and personnage['x'] <= (rect_ZoneSortie[0]+rect_ZoneSortie[2]) and personnage['y'] >= rect_ZoneSortie[1] and personnage['y'] <= (rect_ZoneSortie[1]+rect_ZoneSortie[3]+25):
        fenetre.blit(image_touche,(touche["x"], touche["y"]),touche["zone"])
        if personnage['sortie'] == True:
            fenetre.blit(image_game_clear,(game_clear["x"], game_clear["y"]),game_clear["zone"])
            personnage['x'] = 1500
            monstre['y'] = 1500
            return

def affichage():
    '''on place ici toutes les insructions produisant des affichages.
    Cette fonction sera appelé 20 fois par seconde (valeur définie dans la boucle infinie)
    Elle REDESSINE toute la scène'''
    #on efface la scène en redessinant le fond
    fenetre.fill(NOIR)
    # fond d'écran
    fenetre.blit (FOND,(0, 0))


    #on affiche les murs
    #On affiche le plafond partie1
    for j in range (33) :
        fenetre.blit (FUMéE, (fuméex[j], fuméey))

    #On affiche le plafond partie2 (traversable)
    for j in range (33) :
        fenetre.blit (FUMéE2, (fumée2x[j], fumée2y))

    #les quatres coins
    blitOriente (fenetre, COIN, coin[0]['x'], coin[0]['y'], coin[0]['zonep'], 180)
    blitOriente (fenetre, COIN, coin[1]['x'], coin[1]['y'], coin[1]['zonep'], 90)
    blitOriente (fenetre, COIN, coin[2]['x'], coin[2]['y'], coin[2]['zonep'], 270)
    fenetre.blit (COIN, (coin[3]['x'], coin[3]['y']))

    #le sol
    for j in range (31) :
        fenetre.blit (PIERRE, (pierrex[j], pierrey))

#côté droit
    for p in range (29) :
        blitOriente (fenetre, PIERRE, pierredx, pierredy[p], pierrez, 90)

#côté gauche
    for r in range (29) :
        blitOriente (fenetre, PIERRE, pierregx, pierregy[r], pierrez, 270)

    #On affiche le personnage
    fenetre.blit(image_jeu,(personnage["x"], personnage["y"]),personnage["zone"])
    fenetre.blit(image_méga,(monstre["x"], monstre["y"]),monstre["zone"])





# --------------------PROGRAMME PRINCIPAL--------------------------------

#Initialisation des variables
personnage = {'x': 105, 'y': 120, 'zone':(0*50,0*60,48,59), 'direction':0, 'pv': 150, 'attaque': 10, 'vitesse': 0.1, 'sortie': False}
monstre = {'x': 500, 'y': 400, 'zone':(0,0,87,38), 'directionX':-1, 'directionY':0,'pv': 200, 'attaque': 150, 'vitesse': 0.04}
ZoneConfortMonstre = [monstre['x']-200,monstre['y'],600,60]
game_over = {'x': 0, 'y': 0, 'zone': (0,0,825,825)}
game_clear = {'x': 0, 'y': 0, 'zone': (0,0,825,825)}
touche = {'x': 715,'y': 825-486,'zone': (0,0,64,64)}
#fumée sombre
fuméex = [i*25 for i in range (34)]
fuméey = 0
#fumée claire
fumée2x = [i*25 for i in range (34)]
fumée2y = 25
#coin
coin = [{'x': 0, 'y': 50, 'zonep':(0,0,25,25)}, {'x': 800, 'y': 50, 'zonep':(0,0,25,25)}, {'x': 0, 'y': 800, 'zonep':(0,0,25,25)}, {'x': 800, 'y': 800, 'zonep':(0,0,25,25)}]
#sol
pierrex = [i*25 for i in range (1,32,1)]
pierrey = 800
#coté droit
pierredx = 800
pierredy = [i*25+75 for i in range (31)]
#coté gauche
pierregx = 0
pierregy = [i*25+75 for i in range (31)]
#zone de définition de pierre
pierrez = (0,0,25,25)

##############Les instructions qui sont exécutées en boucle
#En permanence le programme doit analyser les événements (comme l'appui sur une touche ou un clic souris)
#et mettre à jour l'affichage
while True:

#receptionnaire evenements
    for event in pygame.event.get():
        #Si on clique sur la croix
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #Si on appuie sur une touche du clavier
        if event.type == pygame.KEYDOWN:

            if (event.key==K_RIGHT):#(appui sur la flèche droite)
                print("flèche droite")
                personnage["direction"] = 1
            if (event.key==K_LEFT):#(appui sur la flèche gauche)
                print("flèche gauche")
                personnage["direction"] = -1
            if (event.key==K_UP):#(appui sur la flèche haut)
                print("flèche haut")
                personnage["direction"] = 2
            if (event.key==K_DOWN):#(appui sur la flèche bas)
                print("flèche bas")
                personnage["direction"] = -2
            if (event.key==K_s):
                personnage['sortie'] = True




        #si on relâche une touche
        if event.type == pygame.KEYUP:
            print("touche relâchée")
            if (event.key==K_UP):#(appui sur la flèche haut)
                print("(flèche haut)")

            if (event.key==K_RIGHT) or (event.key==K_LEFT):
                print("(flèche haut)")
            personnage["direction"] = 0


#mise a jour affichage ------------------------------------

    #Action du tour de jeu
    miseAjour()
    affichage()
    pygame.display.update()
    #pygame.mixer.music.play(-1)
    pygame.time.wait(5)



#------------------------------------------------------------------------------------------