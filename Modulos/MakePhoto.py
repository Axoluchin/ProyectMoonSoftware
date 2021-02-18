from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox
import os

from Modulos.DataBase import DataBase

Mini = 'settings/images/miniPlantilla.png'
Fuente = "settings/font/moon_get-Heavy.ttf"

def cearfoto(texto):
    if texto != "":
        imagen = Image.open('settings/images/Plantilla.jpg')
        dibujar = ImageDraw.Draw(imagen)
        myfont = ImageFont.truetype(Fuente,40)

        w, h = dibujar.textsize(texto, font=myfont)

        dibujar.text(((1280-w)/2, 600), texto, font=myfont)
        imagen.show() 
        try:
            imagen.save(f"Lunas/{texto}.jpg")
        except IOError:
            os.mkdir("Lunas")
            imagen.save(f"Lunas/{texto}.jpg")

        finally:
            messagebox.showinfo("Imagen Guardada",f"Luna guardada en: {os.getcwd()}\\Lunas\\{texto}.jpg")
            salvar_texto(texto)

def minifoto(label,canvas2,texto):
    imagen = Image.open(Mini)
    dibujar = ImageDraw.Draw(imagen)
    myfont = ImageFont.truetype(Fuente,30)

    w, h = dibujar.textsize(texto.get()+str(label.char), font=myfont)

    dibujar.text(((718-w)/2, 340), texto.get()+str(label.char), font=myfont)

    img1 = ImageTk.PhotoImage(imagen)
    canvas2.create_image(718/2, 404/2, image=img1)
    canvas2.image=img1

def minifoto_historial(canvas,texto):

    imagen = Image.open(Mini)
    dibujar = ImageDraw.Draw(imagen)
    myfont = ImageFont.truetype(Fuente,30)

    w, h = dibujar.textsize(texto, font=myfont)

    dibujar.text(((718-w)/2, 340), texto, font=myfont)

    img1 = ImageTk.PhotoImage(imagen)
    canvas.create_image(718/2, 404/2, image=img1)
    canvas.image=img1

def default(canvas2):
    imagen = Image.open(Mini)

    img1 = ImageTk.PhotoImage(imagen)
    canvas2.create_image(718/2, 404/2, image=img1)
    canvas2.image=img1

def salvar_texto(texto):
    datos = DataBase()
    datos.set_moon(texto)
    datos.desconectar()
