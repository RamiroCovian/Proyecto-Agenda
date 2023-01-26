import sqlite3
import re
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno
from tkinter.colorchooser import askcolor

from vista import titulo_app
from vista import combo
from vista import main
from vista import tree
from vista import END
from vista import entry_nombre
from vista import entry_apellido
from vista import entry_contacto
from vista import var_nombre
from vista import var_apellido
from vista import var_celular


################################################################################
# BASE DE DATOS ################################################################
################################################################################


def crear_base():
    con = sqlite3.connect("turnos.db")
    return con


def crear_tabla(con):
    cursor = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS agenda(id INTEGER PRIMARY KEY AUTOINCREMENT, fecha numeric, hora text, nombre text, apellido text, contacto integer)"
    cursor.execute(sql)
    con.commit()


con = crear_base()
crear_tabla(con)

################################################################################
# FUNCIONES ####################################################################
################################################################################


def funcion_reserva(fecha, hora, nombre, apellido, contacto, tree):
    cadena = nombre
    cadena1 = apellido
    cadena2 = contacto
    patron = "^[A-Za-z\s áéíóú]*$"
    patron1 = "^[0-9]*$"
    if re.match(patron, cadena) and cadena != "":
        if re.match(patron, cadena1) and cadena1 != "":
            if re.match(patron1, cadena2) and cadena2 != "":
                cursor = con.cursor()
                data = (fecha, hora, nombre, apellido, contacto)
                sql = "INSERT INTO agenda(fecha, hora, nombre, apellido, contacto) VALUES(?, ?, ?, ?, ?)"
                cursor.execute(sql, data)
                con.commit()
                actualizar_treeview(tree)
                showinfo(titulo_app, "Turno reservado")
                entry_nombre.focus_set()
                var_nombre.set("-----")
            else:
                showerror(
                    "¡¡Atencion!",
                    "¡Debe ingresar el Contacto sin espacios y sin simbolos!",
                )
        else:
            showerror("¡Atencion!", "¡Debe ingresar el Apellido!")
    else:
        showerror("¡Atencion!", "¡Debe ingresar el Nombre!")


def funcion_cancelar():
    if askyesno(
        "¡Atencion!", "Usted esta a punto de cancelar el turno, ¿Desea continuar?"
    ):
        showinfo(titulo_app, "¡Turno cancelado!")
        valor = tree.selection()
        item = tree.item(valor)
        el_id = item["text"]
        cursor = con.cursor()
        data = (el_id,)
        sql = "DELETE FROM agenda WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
    else:
        showinfo(titulo_app, "¡El turno no se cancelo!")


def funcion_modificar(fecha, hora, nombre, apellido, contacto, tree):
    cadena = nombre
    cadena1 = apellido
    cadena2 = contacto
    patron = "^[A-Za-z\s áéíóú]*$"
    patron2 = "^[0-9]*$"
    if re.match(patron, cadena):
        if re.match(patron, cadena1):
            if re.match(patron2, cadena2):
                if askyesno("¡Atencion!", "¿Desea modificar los datos?"):
                    showinfo(titulo_app, "Modificacion exitosa")
                    valor = tree.selection()
                    item = tree.item(valor)
                    el_id = item["text"]
                    cursor = con.cursor()
                    data = (fecha, hora, nombre, apellido, contacto, el_id)
                    sql = "UPDATE agenda SET fecha=?, hora=?, nombre=?, apellido=?, contacto=? WHERE id=?;"
                    cursor.execute(sql, data)
                    con.commit()
                    actualizar_treeview(tree)
                else:
                    showinfo(titulo_app, "¡Modificacion cancelada!")
            else:
                showerror(
                    "Atencion",
                    "¡Debe ingresar el Contacto sin espacios y sin simbolos!",
                )
        else:
            showerror("Atencion", "¡Debe ingresar el Apellido!")
    else:
        showerror("Atencion", "¡Debe ingresar el Nombre!")


def funcion_consultar():
    actualizar_treeview(tree)


def funcion_salir():
    if askyesno("Atencion", "¿Esta seguro que desea salir?"):
        main.quit()


def actualizar_treeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM agenda ORDER BY fecha ASC"
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        tree.insert(
            "",
            "end",
            text=fila[0],
            values=(fila[1], fila[2], fila[3], fila[4], fila[5]),
        )
    entry_nombre.focus_set()
    var_nombre.set("-----")
    var_apellido.set("-----")
    var_celular.set("Sin espacios y sin simbolos")
    combo.set("Seleccione Hora")


def funcion_color():
    resultado = askcolor(color="#00ff00", title="Elija color")
    main.config(bg=resultado[1])


def click_nombre(event):
    entry_nombre.delete(0, END)
    entry_nombre.config(foreground="black")


def on_focus_nombre(event):
    if var_nombre.get() == "":
        entry_nombre.insert(0, "-----")
        entry_nombre.config(foreground="grey")


def click_apellido(event):
    entry_apellido.delete(0, END)
    entry_apellido.config(foreground="black")


def on_focus_apellido(event):
    if var_apellido.get() == "":
        entry_apellido.insert(0, "-----")
        entry_apellido.config(foreground="grey")


def click_contacto(event):
    entry_contacto.delete(0, END)
    entry_contacto.config(foreground="black")


def on_focus_contacto(event):
    if var_celular.get() == "":
        entry_contacto.insert(0, "Sin espacios y sin simbolos")
        entry_contacto.config(foreground="grey")
