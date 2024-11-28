from tkinter import *
from tkinter import filedialog #boite des fichiers
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps  #bibliotheque pillow pour les images

def import_img():
    global image, image_originale #non exclusives a la fonction
    chemin_image = filedialog.askopenfilename(
        title="Sélectionnez l'image à modifier", filetypes=[("Fichiers image", "*.jpg;*.jpeg;*.png")]
    ) #ouverture de l'image parmi les fichiers
    
    if (chemin_image != 0):
        image = Image.open(chemin_image) #ouv. de l'image si selectionnee
        image.thumbnail((500, 400))
        image_originale = image.copy()  #version non redim. pour la nouvelle image
        afficher_image(image)  #affichage de l'image
        bouton_filtres.place(x=220, y=545)

def afficher_image(img):
    """Affiche une image donnée dans l'interface."""
    global label_image, image
    photo = ImageTk.PhotoImage(img)
    label_image.configure(image=photo)
    label_image.image = photo
    image = img

def toggle_filtre(action): #retour avant le filtre
    global image, image_originale, filtres_actifs #var. globales

    if action in filtres_actifs:
        afficher_image(image_originale) #retour a la normale si le filtre est marque deja utilise
        filtres_actifs.remove(action)
    else:
        image_modifiee = action(image_originale)
        afficher_image(image_modifiee) #application du filtre s'il n'y est pas encore
        filtres_actifs.append(action)


def filtre_negatif(img): #premier filtre
    if img.mode == "RGBA":  #mode transparence (.png)
        r, g, b, a = img.split()
        rgb_negatif = Image.merge("RGB", (ImageOps.invert(r), ImageOps.invert(g), ImageOps.invert(b)))
        return Image.merge("RGBA", (*rgb_negatif.split(), a)) #inversion des trois codes du modele rgb
    else: #mode basique (.jpg, .jpeg)
        return ImageOps.invert(img.convert("RGB")) #inversion des couleurs


def filtre_vintage(img):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(0.5)  #ici on reduit la saturation de moitie


def filtre_nb(img): #noir & blanc
    if img.mode == "RGBA":  #cas transparant (.png)
        r, g, b, a = img.split()
        rgb_nb = ImageOps.grayscale(Image.merge("RGB", (r, g, b))) #passage du rgb en nuances de gris
        return Image.merge("RGBA", (rgb_nb, rgb_nb, rgb_nb, a))         #128, 128, 128 par ex.
    else: #cas basique (.jpg, .jpeg)
        return img.convert("L")  #mode niveau de gris pour ces img


def filtre_floutage(img):
    return img.filter(ImageFilter.GaussianBlur(5)) #mise en place d'un floutage de rayon 5

def icones_filtres():
    #chemins des quatre images à afficher
    chemins_images = ["filtre1.png", "filtre2.png", "filtre3.png", "filtre4.png"]
    
    #positions et fonctions pour chaque image
    positions = [(25, 525), (295, 525), (565, 525), (835, 525)]
    actions = [filtre_negatif, filtre_vintage, filtre_nb, filtre_floutage]
    
    for chemin, pos, action in zip(chemins_images, positions, actions):
        try:
            #ouverture et redimension des images
            icone = Image.open(chemin).resize((240, 80))  # Taille ajustée
            photo = ImageTk.PhotoImage(icone)
            
            #label pour les icones de filtre
            bouton_filtre = Button(
                fenetre, bg="floral white", image=photo, command=lambda act=action: toggle_filtre(act)
            )
            bouton_filtre.image = photo #sauvegarde pour plus tard
            bouton_filtre.place(x=pos[0], y=pos[1])
        except Exception as e: #code erreur lorsque le chemin vers l'image echoue
            print(f"Erreur lors du chargement de {chemin}: {e}")
    bouton_filtres.place_forget() #camouflage du bouton filtre pressé

fenetre = Tk() #ticket
fenetre.geometry('1100x650') #taille de la fenetre
fenetre.title('Logiciel de Montage Photo') #nom
fenetre['bg'] = 'floral white'
fenetre.resizable(height=True, width=True) #redim.

image, image_originale = None, None #var. globales
filtres_actifs = []  #filtres en cours d'utilisation

bouton = Button(fenetre, text="Importez votre image", bg='light cyan', fg='DeepSkyBlue4', command=import_img) #texte, couleurs, action
bouton.place(x=500, y=370) #coordonnées

bouton_filtres = Button(fenetre, text="Filtres", bg='ghost white', fg='black', height=2, width=10, command=icones_filtres)
bouton_filtres.place_forget() #cache au debut

label_image = Label(fenetre, bg='floral white') #label pour aff. une image
label_image.place(x=300, y=100)  #position de l'image

fenetre.mainloop() #boucle pour l'affichage