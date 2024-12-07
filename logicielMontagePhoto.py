from tkinter import *
from tkinter import filedialog, simpledialog #boite des fichiers
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps, ImageDraw  #bibliotheque pillow pour les images

def importerImage():
    global image, image_originale #non exclusives a la fonction
    jouerSon() #bruit d'appui
    chemin_image = filedialog.askopenfilename(
        title="Sélectionnez l'image à modifier", filetypes=[("Fichiers image", "*.jpg;*.jpeg;*.png")]
    ) #ouverture de l'image parmi les fichiers
    
    if (chemin_image != 0):
        image = Image.open(chemin_image) #ouv. de l'image si selectionnee
        image.thumbnail((500, 400))
        bouton.place_forget() #fin du bouton d'importation
        label_titre.place_forget()  #cacher l'image de titre
        image_originale = image.copy()  #version non redimentionnee pour la nouvelle image
        afficherImage(image)  #affichage de l'image
        afficherBoutonsApresLimportation() #il y en a beaucoup alors on cree une fonction

def afficherBoutonsApresLimportation():
    bouton_manipulation.place(x=200, y=545)
    bouton_filtres.place(x=415, y=545) #boutons a afficher
    bouton_dessiner.place(x=590, y=545) #et leurs places
    bouton_texte.place(x=800, y=545)
    bouton_telechargement.place(x=990, y=10)

def cacherBoutonsPrincipaux(): #une fois que l'un d'eux est presse
    bouton_filtres.place_forget()
    bouton_manipulation.place_forget()
    bouton_dessiner.place_forget()
    bouton_texte.place_forget()

def afficherImage(img):
    global label_image, image_modifiee #var. globales
    photo = ImageTk.PhotoImage(img) #ticket
    label_image.configure(image=photo)
    label_image.image = photo #label
    image_modifiee = img #passage en mode global

def telechargerImage():
    global image_modifiee #var. globale
    jouerSon() #bruit d'appui
    if (image_modifiee != 0):  # Vérifiez si une image est modifiée
        chemin_sauvegarde = filedialog.asksaveasfilename(
            title="Enregistrer l'image", defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")]
        )
        if (chemin_sauvegarde != 0):
            try:
                image_modifiee.save(chemin_sauvegarde) #message de succes dans la console
                print(f"L'image a bien ete enregistree à l'emplacement : {chemin_sauvegarde}")
            except Exception as e:
                print(f"Erreur lors de l'enregistrement de l'image : {e}")
    else:
        print("Erreur ! L'image n'a pas pu etre enregistree.") #cas d'erreur

def desactiverFiltre(action): #retour avant le filtre
    global image_modifiee, filtres_actifs #var. globales

    if action in filtres_actifs:
        filtres_actifs.remove(action) #retour a la normale si le filtre est marque deja utilise
    else:
        filtres_actifs.append(action) #ajout du filtre s'il n'y est pas encore
        image_modifiee = action(image_modifiee)
    image_modifiee = image.copy()
    for filtre in filtres_actifs: #application des changements
        image_modifiee = filtre(image_modifiee)
    afficherImage(image_modifiee)

def filtreNegatif(img): #premier filtre
    if img.mode == "RGBA": #mode transparence (.png)
        r, g, b, a = img.split()
        rgb_negatif = Image.merge("RGB", (ImageOps.invert(r), ImageOps.invert(g), ImageOps.invert(b)))
        return Image.merge("RGBA", (*rgb_negatif.split(), a)) #inversion des trois codes du modele rgb
    else: #mode basique (.jpg, .jpeg)
        return ImageOps.invert(img.convert("RGB")) #inversion des couleurs

def filtreVintage(img):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(0.5)  #ici on reduit la saturation de moitie

def filtreNB(img): #noir & blanc
    if img.mode == "RGBA":  #cas transparant (.png)
        r, g, b, a = img.split()
        rgb_nb = ImageOps.grayscale(Image.merge("RGB", (r, g, b))) #passage du rgb en nuances de gris
        return Image.merge("RGBA", (rgb_nb, rgb_nb, rgb_nb, a)) #128, 128, 128 par ex.
    else: #cas basique (.jpg, .jpeg)
        return img.convert("L")  #mode niveau de gris pour ces img

def filtreFloutage(img):
    return img.filter(ImageFilter.GaussianBlur(5)) #mise en place d'un floutage de rayon 5

def iconesFiltres():
    #chemins des quatre images à afficher
    chemins_images = ["filtre1.png", "filtre2.png", "filtre3.png", "filtre4.png"]
    
    #positions et fonctions pour chaque image
    positions = [(25, 525), (295, 525), (565, 525), (835, 525)]
    actions = [filtreNegatif, filtreVintage, filtreNB, filtreFloutage]
    
    for chemin, pos, action in zip(chemins_images, positions, actions): #on parcours en fait trois listes a la fois
        try:
            #ouverture et redimension des images
            icone = Image.open(chemin).resize((240, 80))
            photo = ImageTk.PhotoImage(icone)
            
            #label pour les icones de filtre
            bouton_filtre = Button(
                fenetre, bg="floral white", image=photo, command=lambda act=action:desactiverFiltre(act)
            )
            bouton_filtre.image = photo #sauvegarde pour plus tard
            bouton_filtre.place(x=pos[0], y=pos[1])
            boutons_temp.append(bouton_filtre) #mise des nouveaux boutons en temporaire
        except Exception as e: #code erreur lorsque le chemin vers l'image echoue
            print(f"Erreur lors du chargement de {chemin}: {e}")
    cacherBoutonsPrincipaux() #camouflage une fois le bouton filtre presse
    jouerSon() #bruit d'appui
    afficherBoutonRetour() #retour en arriere

def afficherBoutonsManipulation(): #peu de changements avec iconesFiltres
    cacherBoutonsPrincipaux()
    afficherBoutonRetour()
    chemins_images = ["rotation.png", "inversement.png", "rogner.png"]
    positions = [(75, 525), (395, 525), (705, 525)]
    actions = [lambda: rotationImage(90), inverserHorizontalement, rognerImage]
    for chemin, pos, action in zip(chemins_images, positions, actions):
        try:
            icone = Image.open(chemin).resize((240, 80))
            photo = ImageTk.PhotoImage(icone)
            bouton_manipulation = Button(fenetre, bg="floral white", image=photo, command=action)
            bouton_manipulation.image = photo
            bouton_manipulation.place(x=pos[0], y=pos[1])
            boutons_temp.append(bouton_manipulation)
        except Exception as e:
            print(f"Erreur lors du chargement de {chemin}: {e}")

def rotationImage(angle):
    global image, image_modifiee #l'image est tourne a droite de 90°
    image_modifiee = image_modifiee.rotate(-angle, expand=True)
    image = image_modifiee #sauvegarde de l'image
    afficherImage(image_modifiee)
    jouerSon() #bruit d'appui

def inverserHorizontalement():
    nouvelle_image = ImageOps.mirror(image_modifiee) #mise en place d'un effet mirroir
    mettreAJourImage(nouvelle_image) #sauvegarde pour plus tard
    jouerSon() #bruit d'appui

def mettreAJourImage(nouvelle_image):
    global image, image_modifiee #var.globales
    image_modifiee = nouvelle_image #version a afficher
    image = image_modifiee.copy() #copie
    afficherImage(image_modifiee)

def rognerImage():
    global canvas, image, image_selection, rect, changementDimensions #var. globales
    largeur, hauteur = image.size

    if canvas: #option canvas pour les outils de selection
        canvas.destroy() #destruc. de l'ancien s'il y en a un
    canvas = Canvas(fenetre, width=largeur, height=hauteur, bg='floral white')
    canvas.place(x=300, y=100)
    
    tk_image = ImageTk.PhotoImage(image)
    canvas.image = tk_image
    canvas.create_image(0, 0, anchor=NW, image=tk_image) #affichage

    x1, y1 = largeur // 4, hauteur // 4
    x2, y2 = 3 * largeur // 4, 3 * hauteur // 4 #zone de selection bleue
    rect = canvas.create_rectangle(x1, y1, x2, y2, outline='blue', width=2, dash=(5, 2))

    changementDimensions = { #delimitation de la zone en pointilles bleus pour la selection
        "left": canvas.create_rectangle(x1-5, (y1+y2)//2-5, x1+5, (y1+y2)//2+5, fill="lightblue"),
        "right": canvas.create_rectangle(x2-5, (y1+y2)//2-5, x2+5, (y1+y2)//2+5, fill="lightblue"),
        "top": canvas.create_rectangle((x1+x2)//2-5, y1-5, (x1+x2)//2+5, y1+5, fill="lightblue"),
        "bottom": canvas.create_rectangle((x1+x2)//2-5, y2-5, (x1+x2)//2+5, y2+5, fill="lightblue")
    }

    for dimension in changementDimensions: #motion pour deplacer la zone en pointillee
        canvas.tag_bind(changementDimensions[dimension], "<B1-Motion>", lambda provisoire, d=dimension: ajusterSelection(provisoire, d))
    
    #apparition du bouton de confirm. du rognage
    bouton_confirmer.place(x=754, y=489)
    jouerSon() #bruit d'appui

def ajusterSelection(provisoire, dimension):
    global canvas, rect
    x, y = provisoire.x, provisoire.y #coordonnees  x et y
    coords = canvas.coords(rect) #rectangle que l'on a dessine

    # Ajuster les coordonnées en fonction de la poignée déplacée
    if dimension == "left":
        coords[0] = max(0, min(x, coords[2] - 10))  #la limite permet d'eviter de depasser l'image
    elif dimension == "right":
        coords[2] = min(canvas.winfo_width(), max(x, coords[0] + 10))
    elif dimension == "top":
        coords[1] = max(0, min(y, coords[3] - 10))
    elif dimension == "bottom":
        coords[3] = min(canvas.winfo_height(), max(y, coords[1] + 10))

    canvas.coords(rect, coords) #mise a jour des coordonnees
    actualiserCarresTactiles(coords)

def actualiserCarresTactiles(coords):
    global canvas, changementDimensions
    x1, y1, x2, y2 = coords

    canvas.coords(changementDimensions["left"], x1-5, (y1+y2)//2-5, x1+5, (y1+y2)//2+5)
    canvas.coords(changementDimensions["right"], x2-5, (y1+y2)//2-5, x2+5, (y1+y2)//2+5)
    canvas.coords(changementDimensions["top"], (x1+x2)//2-5, y1-5, (x1+x2)//2+5, y1+5)
    canvas.coords(changementDimensions["bottom"], (x1+x2)//2-5, y2-5, (x1+x2)//2+5, y2+5)
    #ajustement des rectangles qui tiennent la limit. de zone

def appliquerRognage():
    global canvas, rect, bouton_confirmer
    coords = canvas.coords(rect) #variables
    left, upper, right, lower = map(int, coords)
    nouvelle_image = image_modifiee.crop((left, upper, right, lower)) #rognage
    canvas.place_forget() #masquage de la delimitation de zone sans la sup.
    bouton_confirmer.place_forget() #masquage du bouton une fois l'image rognee
    mettreAJourImage(nouvelle_image) #sauv et affichage de l'image rognee
    afficherBoutonsManipulation() #re-affichage des boutons precedents

def dessiner():
    global etatCrayon
    etatCrayon = True #activation du crayon
    cacherBoutonsPrincipaux()
    afficherBoutonRetour() #changements de boutons
    fenetre.bind("<B1-Motion>", dessinerSurImage) #utilisation d'un motion

def dessinerSurImage(provisoire):
    if etatCrayon != True:
        return 0 #on empeche le dessin dans les autres modes
    x, y = provisoire.x, provisoire.y
    draw = ImageDraw.Draw(image) #dessin tant que le clic est presse
    draw.ellipse((x, y, x + 5, y + 5), fill="black") #couleur par defaut
    afficherImage(image)

def ajouterTexte():
    cacherBoutonsPrincipaux()
    afficherBoutonRetour() #chgmt de boutons
    texte = simpledialog.askstring("Texte", "Entrez le texte et cliquez sur le dessin :")
    if (texte != 0): #ecriture avec la bibliotheque simpledialog
        fenetre.bind("<Button-1>", lambda event: positionnerTexte(event, texte))
        #on placera notre texte a l'endroit clique

def positionnerTexte(event, texte):
    fenetre.unbind("<Button-1>") #une fois le clic fait on enleve le bind
    draw = ImageDraw.Draw(image_modifiee)  #chngmnt du txt en img
    draw.text((event.x, event.y), texte, fill="black") #position
    afficherImage(image_modifiee)

def afficherMenuPrincipal(): #apres un retour
    global etatCrayon
    etatCrayon = False #desactivation du dessin
    bouton_retour.place_forget()  #dissim. du bouton retour
    jouerSon() #bruit d'appui
    
    for bouton in boutons_temp: #cacher les boutons temporaires
        bouton.place_forget()
    boutons_temp.clear()  #vidage de la liste ensuite

    afficherBoutonsApresLimportation()  #afficher les boutons principaux comme la 1ere fois

def afficherBoutonRetour():
    cacherBoutonsPrincipaux() #dissimulation des boutons de depart
    jouerSon() #bruit d'appui
    bouton_retour.place(x=10, y=10) #affich. du bouton retour

def jouerMusique():
    pygame.mixer.init()
    pygame.mixer.music.load("musique.mp3") #nom de la musique
    pygame.mixer.music.play(-1) #-1 est le temps en boucle
    pygame.mixer.music.set_volume(0.5) #volume reduit au quart

def arreterMusique():
    pygame.mixer.music.stop() #arret de la musique
    fenetre.destroy() #fermeture de la fenêtre

def jouerSon():
    son = pygame.mixer.Sound("son bouton.mp3") #nom du son
    son.set_volume(0.2) #volume
    son.play() #jouer le son

fenetre = Tk() #ticket
fenetre.geometry('1100x650') #taille de la fenetre
fenetre.title('Logiciel de Montage Photo') #nom
fenetre['bg'] = 'floral white'
fenetre.resizable(height=True, width=True) #redim.

image, image_originale, canvas, rect = None, None, None, None #var. globales
filtres_actifs = []  #filtres en cours d'utilisation
import pygame #pour la musique et les sons
jouerMusique()
fenetre.protocol("WM_DELETE_WINDOW", arreterMusique) #arreter la musique une fois la fenetre fermee

bouton = Button(fenetre, text="Importez votre image", bg='light cyan', fg='DeepSkyBlue4', command=importerImage) #texte, couleurs, action
bouton.place(x=500, y=370) #coordonnées

icone_titre = Image.open("titre.png").resize((675, 178))
photo_titre = ImageTk.PhotoImage(icone_titre) #ticket
label_titre = Label(fenetre, image=photo_titre, bg='floral white')
label_titre.image = photo_titre 
label_titre.place(x=240, y=120) #positionnement du titre

bouton_filtres = Button(fenetre, text="Filtres", bg='ghost white', fg='black', height=2, width=10, command=iconesFiltres) #boutons d'actions
bouton_manipulation = Button(fenetre, text="Manipulation", bg='ghost white', fg='black', height=2, width=15, command=afficherBoutonsManipulation)
bouton_dessiner = Button(fenetre, text="Dessiner", bg='ghost white', fg='black', height=2, width=15, command=dessiner)
bouton_texte = Button(fenetre, text="Texte", bg='ghost white', fg='black', height=2, width=15, command=ajouterTexte)

etatCrayon = False #dessin desactive au debut

icone_telechargement = Image.open("telechargement.png").resize((80, 80))
photo_telechargement = ImageTk.PhotoImage(icone_telechargement) #ticket pour l'image
bouton_telechargement = Button(fenetre, image=photo_telechargement, bg='floral white', command=telechargerImage)
bouton_telechargement.image = photo_telechargement #bouton associe a l'image

boutons_temp = [] #liste des boutons d'action affiches temporairement

try: #bouton retour, quand on clique sur les boutons de depart
    icone_retour = Image.open("retour.png").resize((100, 80)) #chargement et redimensionnement de l'image
    photo_retour = ImageTk.PhotoImage(icone_retour) #ticket
    bouton_retour = Button(
        fenetre, image=photo_retour, bg="floral white", command=afficherMenuPrincipal
    )
    bouton_retour.image = photo_retour #implem. de l'image dans le bouton
    bouton_retour.place_forget()
except Exception as e: #msg d'erreur si l'img ne s'affiche pas
    print(f"Erreur lors du chargement de l'image 'retour.png': {e}")

changementDimensions = {} #pour un rognage d'image
bouton_confirmer = Button(fenetre, text="Confirmez votre rognage", command=appliquerRognage)
bouton_confirmer.place_forget() #bouton de validation du rognage, camoufle au debut

label_image = Label(fenetre, bg='floral white') #label pour aff. une image
label_image.place(x=300, y=100)  #position de l'image

fenetre.mainloop() #boucle pour l'affichage