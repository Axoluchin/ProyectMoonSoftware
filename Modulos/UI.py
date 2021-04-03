import tkinter as tk
from tkinter import BooleanVar, StringVar, ttk
import os
from PIL import ImageTk, Image

from Modulos import MakePhoto, DataBase, Links, settings

class UI:
    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("You Make A Moon 1.2.1")
        self.ventana.iconbitmap('settings/images/moon.ico')
        self.ventana.resizable(False, False)
        self.ventana.overrideredirect(True) #! ESTO

        self.ventana.tk.eval("""
        set base_theme_dir settings/theme/awthemes-10.3.0/

        package ifneeded awthemes 10.3.0 \
            [list source [file join $base_theme_dir awthemes.tcl]]
        package ifneeded colorutils 4.8 \
            [list source [file join $base_theme_dir colorutils.tcl]]
        package ifneeded awdark 7.11 \
            [list source [file join $base_theme_dir awdark.tcl]]
        package ifneeded awlight 7.6 \
            [list source [file join $base_theme_dir awlight.tcl]]
        """)

        self.ventana.tk.call("package", "require", 'awdark')
        self.ventana.tk.call("package", "require", 'awlight')

        self.style = ttk.Style()
        self.style.theme_use(settings.get_theme())
        self.tamanio = 30
        self.style.configure('TButton', font=
        ('arial', 20, 'bold'))
        self.style.configure('TLabel', font=
        ('arial', 15))
        self.style.configure('TEntry', font=
        ('arial', 15))

        title_bar = ttk.Frame(self.ventana, relief='raised')
        close_button = ttk.Button(title_bar, text='X', command=self.ventana.destroy)
        title_text = ttk.Label(title_bar,text="You Make A Moon  1.2",font=(20))
        title_bar.pack(expand=1, fill=tk.X,side = tk.TOP)
        title_text.pack(side=tk.LEFT,padx= 10)
        close_button.pack(side=tk.RIGHT)
        title_bar.bind('<B1-Motion>', self.move_window)

        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack()

        self.menuframe = ttk.LabelFrame(self.notebook, border = 0)
        self.menuframe.pack()
        self.infoframe = ttk.LabelFrame(self.notebook, border = 0)
        self.infoframe.pack()
        self.settingsframe = ttk.LabelFrame(self.notebook, border = 0)
        self.settingsframe.pack()

        self.notebook.add(self.menuframe, text= "You Make A Moon")
        self.notebook.add(self.settingsframe, text="Configuración")
        self.notebook.add(self.infoframe, text="Info")


    def move_window(self,event):
        self.ventana.geometry('+{0}+{1}'.format(event.x_root - 550, event.y_root))

    def principal (self):
        self.texto = tk.StringVar()
        self.plantilla = tk.IntVar()

        lf_mesadetrabajo = ttk.LabelFrame(self.menuframe,border= 0)
        lf_mesadetrabajo.pack(side = tk.LEFT,padx = 20)

        self.canvas2 = tk.Canvas(lf_mesadetrabajo, width="716", height="402",relief=tk.RIDGE, bd=0)
        self.canvas2.grid (row=0, column = 0, columnspan= 2)
        
        l_name = ttk.Label(lf_mesadetrabajo,text = "Ingrese el texto de su Luna: ")
        l_name.grid(row=1,column=0, padx = 20, pady = 10)

        e_text = ttk.Entry(lf_mesadetrabajo, textvariable = self.texto,font= (20),width=30)
        e_text.grid(row=1,column = 1,padx = 20)
        e_text.bind('<Key>', lambda i: MakePhoto.minifoto(i,self.canvas2,self.texto))
        

        b_generar = ttk.Button(lf_mesadetrabajo,text = "Guardar Foto", command = lambda: self.foto(self.texto.get()))
        b_generar.grid(row = 2, column = 0,columnspan=2, pady = 10)

        plantilla_l = ttk.Label(lf_mesadetrabajo,text="Plantilla: ")
        plantilla_l.grid(row = 2, column = 1, padx= 55,sticky= 'E')

        plantilla = ttk.Spinbox(lf_mesadetrabajo, from_= 1, to= len(os.listdir('settings/images/temples')),width=5,textvariable=self.plantilla,command=self.temple)
        self.plantilla.set(settings.get_temple())
        plantilla.grid(row = 2, column = 1, sticky= 'E')

        MakePhoto.default(self.canvas2)

    def temple(self):
        settings.update_json(self.var_theme.get(),settings.get_moons(), self.var_history.get(), self.plantilla.get(),settings.get_photo())
        MakePhoto.minifoto_historial(self.canvas2,self.texto.get())

    def foto(self,texto):
        MakePhoto.cearfoto(texto)
        settings.update_json(self.var_theme.get(),settings.get_moons()+1, self.var_history.get(), settings.get_temple(),settings.get_photo())
        self.lb_moon["text"] = f"Lunas creadas: {settings.get_moons()}"

        if(self.var_history.get()):
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


        lf_historial = ttk.LabelFrame(self.menuframe, border= 0)
        lf_historial.pack(expand='yes',fill='both')

        scrollbar = ttk.Scrollbar(lf_historial)
        scrollbar.pack( side = tk.RIGHT, fill = tk.Y)
        if settings.get_theme() == 'awdark':
            self.lista = tk.Listbox(lf_historial,font= self.tamanio,yscrollcommand = scrollbar.set,width=25,bg ='#232829',fg = "#FFFFFF")
        else:
            self.lista = tk.Listbox(lf_historial,font= self.tamanio,yscrollcommand = scrollbar.set,width=25)
        self.lista.pack(fill='both',expand='yes',side = tk.LEFT)
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
        creditos = ttk.LabelFrame(self.infoframe,border=0)
        creditos.pack()

        l_creditos = ttk.Label(creditos,text="You Make a Moon es un software libre desarrollado ",font = 25)
        l_creditos.pack()
        l_creditos1 = ttk.Label(creditos,text="por La Odisea de los Memes",font = 25)
        l_creditos1.pack()

        lf_enlaces = ttk.LabelFrame(creditos,text= "Links de Referencia:",border=0)
        lf_enlaces.pack(pady=20,expand='yes')

        self.i_face =tk.PhotoImage(file = ("settings/images/logos/facebook.png"))

        b_facebook = ttk.Button(lf_enlaces,image=self.i_face,command=Links.facebook)
        b_facebook.pack(side=tk.LEFT)

        self.i_twit = tk.PhotoImage(file = 'settings/images/logos/twitter.png')

        b_twitter = ttk.Button(lf_enlaces,image=self.i_twit,command=Links.twitter)
        b_twitter.pack(side=tk.LEFT,padx=30,pady=10)

        self.i_github = tk.PhotoImage(file = 'settings/images/logos/github.png')

        b_github = ttk.Button(lf_enlaces,image=self.i_github,command=Links.github)
        b_github.pack(side=tk.LEFT)

        self.logo1 = Image.open('settings/images/logos/Make.png')
        if settings.get_theme() == 'awdark':
            self.logo2 = Image.open('settings/images/logos/Logo_white.png')
        else:
            self.logo2 = Image.open('settings/images/logos/Logo_black.png')

        self.logo1 = self.logo1.resize((290, 110), Image.ANTIALIAS)
        self.logo1 = ImageTk.PhotoImage(self.logo1)

        self.logo2 = self.logo2.resize((290, 129), Image.ANTIALIAS)
        self.logo2 = ImageTk.PhotoImage(self.logo2)

        lf_logo = ttk.LabelFrame(creditos,border=0)
        lf_logo.pack()

        l_logo1 = ttk.Label(lf_logo,image=self.logo1)
        l_logo1.pack(side=tk.RIGHT,padx=20)

        l_logo2 = ttk.Label(lf_logo,image=self.logo2)
        l_logo2.pack(side=tk.RIGHT,padx=20)

        l_legal = ttk.Label(creditos,text="Super Mario Odyssey is a trademark of Nintendo Co., Ltd.", font= 40)
        l_legal.pack(side=tk.BOTTOM)

    def settings(self):
        def update_theme():
            settings.update_json(self.var_theme.get(),settings.get_moons(), self.var_history.get(),settings.get_temple(),settings.get_photo())
            lb_warning.grid(row= 0,column= 3,padx= 30)

        def update_history():
            settings.update_json(self.var_theme.get(), settings.get_moons(), self.var_history.get(), settings.get_temple(), self.var_photo.get())

        self.var_theme = StringVar()
        self.var_history = BooleanVar()
        self.var_photo = BooleanVar()

        lb_theme = ttk.Label(self.settingsframe, text= "Tema: ",font=(25))
        lb_theme.grid(row= 0,column= 0,sticky='W')

        awdark = ttk.Radiobutton(self.settingsframe, text="Oscuro", variable=self.var_theme, value="awdark", command=update_theme)
        awdark.grid(row= 0,column= 1,padx= 30)
        awlight = ttk.Radiobutton(self.settingsframe, text="Claro", variable=self.var_theme, value="awlight", command=update_theme)
        awlight.grid(row= 0,column= 2,padx= 30)
        self.var_theme.set(settings.get_theme())

        lb_theme = ttk.Label(self.settingsframe, text= "Historial de Lunas: ",font=(25))
        lb_theme.grid(row= 1,column= 0,sticky='W')
        self.var_history.set(bool(settings.get_history()))

        switchistory = ttk.Checkbutton(self.settingsframe, variable = self.var_history,command= update_history)
        switchistory.grid(row= 1,column= 1)

        lb_photo = ttk.Label(self.settingsframe, text= "Ver foto: ",font=(25))
        lb_photo.grid(row= 2,column= 0,sticky='W')
        self.var_photo.set(bool(settings.get_photo()))

        switchphoto = ttk.Checkbutton(self.settingsframe, variable = self.var_photo,command= update_history)
        switchphoto.grid(row= 2,column= 1)


        lb_warning = ttk.Label(self.settingsframe, text="Es necesario reiniciar el programa para aplicar el tema")

        self.lb_moon = ttk.Label(self.settingsframe, text=f"Lunas creadas: {settings.get_moons()}",font=25)
        self.lb_moon.grid(row= 6,column= 0,columnspan=2,sticky='W',pady=20)
        
    def mantener(self):
        self.ventana.configure(bg=self.style.lookup('TFrame', 'background'))
        self.ventana.mainloop()
