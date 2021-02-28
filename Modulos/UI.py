import tkinter as tk
from PIL import ImageTk, Image

from Modulos import MakePhoto, DataBase, Links

class UI:
    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("You Make A Moon 1.1")
        self.ventana.iconbitmap('settings/images/moon.ico')
        self.ventana.resizable(False, False)

        self.menu=tk.Menu(self.ventana)
        self.menu.add_command(label="Info",command=self.info)
        self.ventana.config(m=self.menu)

        self.tamanio = 10


    def principal(self):
        self.texto = tk.StringVar()

        lf_mesadetrabajo = tk.LabelFrame(self.ventana,border= 0)
        lf_mesadetrabajo.pack(side = tk.LEFT)

        self.canvas2 = tk.Canvas(lf_mesadetrabajo, width="718", height="404", relief=tk.RIDGE, bd=0)
        self.canvas2.grid (row=0, column = 0, columnspan= 2)
        
        l_name = tk.Label(lf_mesadetrabajo,text = "Ingrese el texto de su Luna: ",font= self.tamanio)
        l_name.grid(row=1,column=0, padx = 20, pady = 10)

        e_text = tk.Entry(lf_mesadetrabajo, textvariable = self.texto,font= self.tamanio, width="30")
        e_text.grid(row=1,column = 1,padx = 20)
        e_text.bind('<Key>', lambda i: MakePhoto.minifoto(i,self.canvas2,self.texto))
        

        b_generar = tk.Button(lf_mesadetrabajo,text = "Guardar Foto",font= self.tamanio, command = lambda: self.foto(self.texto.get()))
        b_generar.grid(row = 2, column = 0,columnspan=2, pady = 10)

        MakePhoto.default(self.canvas2)

    def foto(self,texto):
        MakePhoto.cearfoto(texto)
        self.colocar_historial()
    
    def historial(self):
        def borrar():
            texto = self.lista.get(self.lista.curselection()[0])
            base = DataBase.DataBase()
            base.delet_moon(texto)
            base.desconectar()
            self.colocar_historial()

        def seleccionado():
            try:
                self.texto.set(self.lista.get(self.lista.curselection()[0]))
                MakePhoto.minifoto_historial(self.canvas2,self.texto.get())
            except IndexError:
                pass


        lf_historial = tk.LabelFrame(self.ventana,text = "Historial",font= self.tamanio,border= 0)
        lf_historial.pack(expand='yes',fill='both')

        scrollbar = tk.Scrollbar(lf_historial)
        scrollbar.pack( side = tk.RIGHT, fill = tk.Y ,pady= 10)

        self.lista = tk.Listbox(lf_historial,font= self.tamanio,yscrollcommand = scrollbar.set,width=25)
        self.lista.pack(fill='both',expand='yes',side = tk.LEFT,pady= 10)
        self.lista.bind("<<ListboxSelect>>", lambda x: seleccionado())
        self.lista.bind("<BackSpace>", lambda x: borrar())

        scrollbar.config( command = self.lista.yview )

        self.colocar_historial()

    def colocar_historial(self):
        base_datos = DataBase.DataBase()
        textos = base_datos.get_moons()

        self.lista.delete(0, tk.END)

        for a in textos:
            self.lista.insert(tk.END,a[1])
        
        base_datos.desconectar()


    def info(self):
        creditos = tk.Toplevel(self.ventana)
        creditos.iconbitmap('settings/images/moon.ico')
        creditos.resizable(False, False)

        l_creditos = tk.Label(creditos,text="You Make a Moon es un software libre desarrollado ",font = 25)
        l_creditos.pack()
        l_creditos1 = tk.Label(creditos,text="por La Odisea de los Memes",font = 25)
        l_creditos1.pack()

        lf_enlaces = tk.LabelFrame(creditos,text= "Links de Referencia:",border=0,font = 20)
        lf_enlaces.pack(pady=20,expand='yes')

        self.i_face =tk.PhotoImage(file = ("settings/images/facebook.png"))

        b_facebook = tk.Button(lf_enlaces,image=self.i_face,command=Links.facebook)
        b_facebook.pack(side=tk.LEFT)

        self.i_twit = tk.PhotoImage(file = 'settings/images/twitter.png')

        b_twitter = tk.Button(lf_enlaces,image=self.i_twit,command=Links.twitter)
        b_twitter.pack(side=tk.LEFT,padx=30,pady=10)

        self.i_github = tk.PhotoImage(file = 'settings/images/github.png')

        b_github = tk.Button(lf_enlaces,image=self.i_github,command=Links.github)
        b_github.pack(side=tk.LEFT)

        self.logo1 = Image.open('settings/images/Make.png')
        self.logo2 = Image.open('settings/images/Logo.png')

        self.logo1 = self.logo1.resize((290, 110), Image.ANTIALIAS)
        self.logo1 = ImageTk.PhotoImage(self.logo1)

        self.logo2 = self.logo2.resize((290, 129), Image.ANTIALIAS)
        self.logo2 = ImageTk.PhotoImage(self.logo2)

        lf_logo = tk.LabelFrame(creditos,border=0)
        lf_logo.pack()

        l_logo1 = tk.Label(lf_logo,image=self.logo1)
        l_logo1.pack(side=tk.RIGHT,padx=20)

        l_logo2 = tk.Label(lf_logo,image=self.logo2)
        l_logo2.pack(side=tk.RIGHT,padx=20)

        l_legal = tk.Label(creditos,text="Super Mario Odyssey is a trademark of Nintendo Co., Ltd.")
        l_legal.pack(side=tk.BOTTOM)



    def mantener(self):
        self.ventana.mainloop()
