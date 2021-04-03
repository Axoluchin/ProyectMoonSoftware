from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox
import os

from Modulos.DataBase import DataBase
from Modulos import settings

Mini = 'settings/images/temples/'
Fuente = "settings/font/moon_get-Heavy.ttf"

def cearfoto(texto):
    if texto != "":
        imagen = Image.open(f'settings/images/temples/{settings.get_temple_name()}')
        dibujar = ImageDraw.Draw(imagen)
        myfont = ImageFont.truetype(Fuente,53)

        w, h = dibujar.textsize(texto, font=myfont)

        dibujar.text(((1280-w)/2, 605), texto, font=myfont) 
        try:
            imagen.save(f"Lunas/{texto}.jpg")
        except IOError:
            os.mkdir("Lunas")
            imagen.save(f"Lunas/{texto}.jpg")

        finally:
            messagebox.showinfo("Imagen Guardada",f"Luna guardada en: {os.getcwd()}\\Lunas\\{texto}.jpg")
            if settings.get_history():
                salvar_texto(texto)
            if settings.get_photo():
                imagen.show()

def minifoto(label,canvas2,texto):
    imagen = Image.open(f"{Mini}{settings.get_temple_name()}")
    imagen =imagen.resize((718, 402), Image.ANTIALIAS)
    dibujar = ImageDraw.Draw(imagen)
    myfont = ImageFont.truetype(Fuente,30)

    w, h = dibujar.textsize(texto.get()+str(label.char), font=myfont)

    dibujar.text(((718-w)/2, 340), texto.get()+str(label.char), font=myfont)

    img1 = ImageTk.PhotoImage(imagen)
    canvas2.create_image(718/2, 404/2, image=img1)
    canvas2.image=img1

def minifoto_historial(canvas,texto):

    imagen = Image.open(f"{Mini}{settings.get_temple_name()}")
    imagen =imagen.resize((718, 402), Image.ANTIALIAS)

    dibujar = ImageDraw.Draw(imagen)
    myfont = ImageFont.truetype(Fuente,30)

    w, h = dibujar.textsize(texto, font=myfont)

    dibujar.text(((718-w)/2, 340), texto, font=myfont)

    img1 = ImageTk.PhotoImage(imagen)
    canvas.create_image(718/2, 404/2, image=img1)
    canvas.image=img1

def default(canvas2):
    imagen = Image.open(f"{Mini}{settings.get_temple_name()}")
    imagen =imagen.resize((718, 402), Image.ANTIALIAS)

    img1 = ImageTk.PhotoImage(imagen)
    canvas2.create_image(718/2, 404/2, image=img1)
    canvas2.image=img1


def salvar_texto(texto):
    datos = DataBase()
    datos.set_moon(texto)
    datos.desconectar()
