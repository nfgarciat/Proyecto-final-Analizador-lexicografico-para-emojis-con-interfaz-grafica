from tkinter import *
from PIL import Image, ImageTk
import os
import unidecode
import re

def analizador_lexicográfico(texto):
    lista_sin_emojis = []
    emojis = []
    matches = re.finditer(r'\b\w+\b|:\S(?!\S)|;\S(?!\S)|\S\S\S|\S\S', texto) #se utiliza la libreria de expresiones regulares re
    #la funcion finditer es para que encuentre alguna de esas expresiones regulares
    # el | es una o,  el b es el limite de la palabra al comienzo y al final, w + es al menos una letra
    # el S es cualquier caracter que no sea espacio en blanco y que el que le sigue, no sea un caracter que no sea espacio en blanco
    #same pero con punto y coma
    # cualquier 2 caracteres, cualquier 3 (no espacio en blanco)
    palabras = []

    # Inicializar la posición de la palabra
    pos_palabra = 0

    for match in matches:
        palabra = match.group() #se obtiene la nueva palabra
        palabras.append(palabra)  #se añade a la lista de palabras
        respEsp = analizarEspanol(palabra)

        if respEsp == False:
            respEmoji = analizarEmoji(palabra)
            if respEmoji != False:
                emojis.append([pos_palabra, os.path.join("emojis", f"{respEmoji}.png")])
        else:
            lista_sin_emojis.append(palabra)

        # Actualizar la posición de la palabra
        pos_palabra += 1

    return [lista_sin_emojis, f"Se encontraron {len(lista_sin_emojis)} palabras y {len(emojis)} emojis", emojis, palabras]

def analizarEspanol(palabra):
    # Carpeta que contiene los archivos de texto
    carpeta_dics = "dics"

    # Recorre todos los archivos en la carpeta
    for letra in palabra:
        archivo = unidecode.unidecode(letra.lower()) + ".txt"  # Convierte a minúsculas y quita tildes
        ruta_archivo = os.path.join(carpeta_dics, archivo)

        # Verifica si la palabra está en el archivo actual
        if os.path.exists(ruta_archivo):
            # Abrir el archivo en modo lectura
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                # Leer las líneas del archivo, convertirlas a minúsculas y quitar tildes
                palabras_en_diccionario = [unidecode.unidecode(line.strip()) for line in file]
                if unidecode.unidecode(palabra.casefold()) in palabras_en_diccionario:
                    return True
    return False

def analizarEmoji(secuencia_clave):
    # Definir las secuencias clave y los nombres de las imágenes correspondientes
    emoji_mapping = {
        "<3": "001-emoji",
        ":3": "001-emoji",
        "B)": "002-emoticonos",
        "(:": "003-feliz",
        ":o": "004-conmocionado",
        ":D": "005-sonriente",
        ":)": "006-feliz-1",
        ":?": "007-pensando",
        ":|": "008-confuso",
        ":(": "009-triste",
        "XD": "010-risa",
        "|(": "011-enojado",
        ":O": "012-conmocionado-1",
        "8|": "013-preocuparse",
        ":-)": "014-sonrisa",
        "^x^": "015-emoji-1",
        "*.*": "016-estrella",
        "*.*!": "017-partido",
        ";)": "018-guino",
        "wtf": "021-cabeza-alienigena",
        "meaw": "022-gato",
        "x.x": "023-cabeza-alienigena-1",
        "zzz": "024-emoji-2",
        "BD": "025-nerd",
        "SM": "026-superhombre",
        "\.//": "027-fresco",
        "(n)": "028-pulgares-abajo",
        "dog": "029-triste-1",
        "it": "030-payaso",
    }

    # Verificar si la secuencia clave está en el mapeo
    if secuencia_clave in emoji_mapping:
        # Obtener el nombre de la imagen correspondiente
        nombre_imagen = emoji_mapping[secuencia_clave]

        # Verificar si la imagen existe en la carpeta "emojis"
        ruta_imagen = os.path.join("emojis", f"{nombre_imagen}.png")
        if os.path.exists(ruta_imagen):
            return nombre_imagen
        else:
            return False
    else:
        return False

def analizar():
    lista = analizador_lexicográfico(cadena.get())
    p.set(lista[1])
    cad = "Palabras encontradas: "
    for i in lista[0]:
        cad = cad + "'" + str(i) + "' "

    r.set(cad)
    actualizar_imagenes(lista[3], lista[2], frame_imagenes)  # Cambiado de lista[3] a lista[0]


def actualizar_imagenes(lista_original, emojis, frame):
    print("emojis:" + str(emojis))
    
    for widget in frame.winfo_children():
        widget.destroy()

    j = 0

    # Mostrar las nuevas imágenes
    for i in range(len(lista_original)):
        if j < len(emojis):
            pos, ruta_imagen = emojis[j]

            if pos == i:  # esta palabra corresponde a una imagen
                print("reconoce que es un emoji")
                print(ruta_imagen)
                imagen = Image.open(ruta_imagen).resize((50, 50))
                photo = ImageTk.PhotoImage(imagen)

                # Mostrar la imagen en un Label dentro del Frame
                img_label = Label(frame, image=photo)
                img_label.image = photo  # Conservar una referencia para evitar que la imagen sea eliminada
                img_label.pack(side="left")
                j += 1
            else:  # esta palabra es una palabra normal
                # Mostrar la palabra en un Label dentro del Frame
                img_label = Label(frame, text=lista_original[i], font=subtitulo_font, fg="#007BFF")
                img_label.pack(side="left")
        else:  # si no hay más emojis, mostrar las palabras restantes
            img_label = Label(frame, text=lista_original[i], font=subtitulo_font, fg="#007BFF")
            img_label.pack(side="left")

   



# Configuración de la raíz
root = Tk()
root.config(bd=50)
root.title("Interfaz gráfica - Lenguajes de Programación")
root.geometry("800x600")  # Tamaño de la ventana

# Configuración de los textos y su estilo
titulo_font = ("Helvetica", 18, "bold")
subtitulo_font = ("Helvetica", 12, "bold")
texto_font = ("Helvetica", 12)
color_titulo = "black"
color_salida1 = "blue"
color_salida2 = "green"

cadena = StringVar()
p = StringVar()
r = StringVar()
e = []

#logo
logo = Image.open("logo_eafit_completo.png").resize((150, 80))
photo = ImageTk.PhotoImage(logo)
Label(root, image=photo).pack(anchor=NW, padx=10, pady=10)
Label(root, text="").pack()  # Separador
Label(root, text="UNIVERSIDAD EAFIT PROYECTO FINAL",font=titulo_font, fg="black").pack()
Label(root, text="LENGUAJES DE PROGRAMACIÓN",font=titulo_font, fg="black").pack()
Label(root, text="").pack()  # Separador

Label(root, text="Ingrese el texto:",font=subtitulo_font, fg="black").pack()
Entry(root, justify="center", textvariable=cadena,font=texto_font, width=30).pack(pady=10)
Label(root, text="").pack()  # Separador
Button(root, justify="center", text="Procesar Cadena de Texto", command=analizar,font=texto_font).pack()
Label(root, text="").pack()  # Separador
Label(root, text="Salida:",font=subtitulo_font, fg="black").pack(side="left", padx=70, pady=10)

Label(root, text="").pack()  # Separador

# Crear un Frame para contener las imágenes
frame_imagenes = Frame(root)
frame_imagenes.pack()

Label(root, textvariable=p,font=subtitulo_font, fg="#00FF00").pack()  
Label(root, textvariable=r,font=subtitulo_font, fg="gray").pack() 
# Finalmente bucle de la aplicación
root.mainloop()
