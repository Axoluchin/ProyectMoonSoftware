import sqlite3


class DataBase:
    def __init__(self) -> None:
        self.basedatos = sqlite3.connect(f"settings/DataBase/Moon.db")
        self.cursor = self.basedatos.cursor()

    def desconectar(self):
        self.basedatos.close()

    def crearbase(self):
        self.basedatos.execute("CREATE TABLE moonText (ID INTEGER PRIMARY KEY AUTOINCREMENT, Texto TEXT)")

    def get_moons(self):
        accion = """SELECT * FROM moonText ORDER BY id DESC"""

        try:
            self.cursor.execute(accion)
            return  self.cursor.fetchall()

        except sqlite3.DatabaseError:
            self.crearbase()
            return False

    def set_moon(self, texto):
        texto = texto.replace("\"","")
        acccion = "INSERT INTO moonText (Texto) VALUES (\"{}\")".format(texto)

        try:
            self.cursor.execute(acccion);
        except sqlite3.DatabaseError:
            self.crearbase()
            self.cursor.execute(acccion);
        finally:
            self.basedatos.commit()

    def delet_moon(self,texto):
        acccion = "DELETE FROM moonText WHERE Texto = \"{}\"".format(texto)
        self.cursor.execute(acccion);
        self.basedatos.commit()
