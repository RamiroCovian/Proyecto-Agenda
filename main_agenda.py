from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.colorchooser import askcolor
from tkinter.messagebox import *
import sqlite3
import re

el_id = 0
titulo_app = "Syntia SPA"


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


main = Tk()

main.title(titulo_app)
main.geometry("675x615")
main.resizable(width=False, height=False)
main.iconbitmap("masaje_negro.ico")
main.configure(bg="lightblue")
recuadro = LabelFrame(main, text="Registro de Personas", bg="lightblue")
recuadro.grid(row=0, column=0, pady=30, padx=10)
var_nombre = StringVar()
var_apellido = StringVar()
var_celular = StringVar()
nombre = Label(recuadro, text="Nombre", width=25, bg="lightblue")
nombre.grid(row=0, column=1, sticky=W, pady=10)
apellido = Label(recuadro, text="Apellido", width=25, bg="lightblue")
apellido.grid(row=1, column=1, sticky=W, pady=10)
contacto = Label(recuadro, text="Contacto", width=25, bg="lightblue")
contacto.grid(row=2, column=1, sticky=W, pady=10)
fecha = Label(recuadro, text="Fecha", width=25, bg="lightblue")
fecha.grid(row=3, column=1, sticky=W, pady=10)
hora = Label(recuadro, text="Horario", width=25, bg="lightblue")
hora.grid(row=4, column=1, sticky=W, pady=10)

entry_nombre = Entry(recuadro, textvariable=var_nombre, width=25)
entry_nombre.grid(row=0, column=2, sticky=W)
entry_nombre.focus_set()
entry_nombre.bind("<Button-1>", click_nombre)
entry_nombre.bind("<FocusIn>", on_focus_nombre)
entry_apellido = Entry(recuadro, textvariable=var_apellido, width=25)
entry_apellido.grid(row=1, column=2, sticky=W)
entry_apellido.config(fg="grey")
entry_apellido.insert(0, "-----")
entry_apellido.bind("<Button-1>", click_apellido)
entry_apellido.bind("<FocusIn>", on_focus_apellido)
entry_contacto = Entry(
    recuadro,
    textvariable=var_celular,
    width=25,
)
entry_contacto.grid(row=2, column=2, sticky=W)
entry_contacto.config(fg="grey")
entry_contacto.insert(0, "Sin espacios y sin simbolos")
entry_contacto.bind("<Button-1>", click_contacto)
entry_contacto.bind("<FocusIn>", on_focus_contacto)
combo = ttk.Combobox(
    recuadro,
    state="readonly",
    values=[
        "9:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
    ],
)
combo.set("Seleccione Hora")
combo.grid(row=4, column=2, sticky=W)
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


################################################################################
# BOTONES ######################################################################
################################################################################

boton_guardar = Button(
    recuadro,
    text="Reservar Turno",
    width=25,
    command=lambda: funcion_reserva(
        tkc.get_date(),
        combo.get(),
        var_nombre.get(),
        var_apellido.get(),
        var_celular.get(),
        tree,
    ),
    bg="green",
)
boton_guardar.grid(row=5, column=1, sticky=W + E)

boton_eliminar = Button(
    recuadro,
    text="Cancelar Turno",
    width=25,
    command=lambda: funcion_cancelar(),
    bg="red",
)
boton_eliminar.grid(row=6, column=2, sticky=W + E)

boton_consultar = Button(
    recuadro,
    text="Consultar",
    width=25,
    command=lambda: funcion_consultar(),
    bg="yellow",
)
boton_consultar.grid(row=6, column=1, sticky=W)

boton_modificar = Button(
    recuadro,
    text="Modificar",
    width=25,
    command=lambda: funcion_modificar(
        tkc.get_date(),
        combo.get(),
        var_nombre.get(),
        var_apellido.get(),
        var_celular.get(),
        tree,
    ),
    bg="orange",
)
boton_modificar.grid(row=5, column=2, sticky=W)

boton_salir = Button(
    main, text="Salir", width=25, command=lambda: funcion_salir(), bg="red"
)
boton_salir.grid(row=7, column=0, columnspan=2, sticky=W + E, padx=10)
################################################################################
# MENU #########################################################################
################################################################################

menubar = Menu(main)

menu_archivo = Menu(menubar, tearoff=0)
menu_archivo.add_command(
    label="Reservar Turno",
    command=lambda: funcion_reserva(
        tkc.get_date(),
        combo.get(),
        var_nombre.get(),
        var_apellido.get(),
        var_celular.get(),
        tree,
    ),
)
menu_archivo.add_command(label="Cancelar Turno", command=lambda: funcion_cancelar())
menu_archivo.add_separator()
menu_archivo.add_command(label="Consultar Turnos", command=lambda: funcion_consultar())
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=lambda: funcion_salir())
menubar.add_cascade(label="Archivo", menu=menu_archivo)

menu_edicion = Menu(menubar, tearoff=0)
menu_edicion.add_command(
    label="Modificar Datos",
    command=lambda: funcion_modificar(
        tkc.get_date(),
        combo.get(),
        var_nombre.get(),
        var_apellido.get(),
        var_celular.get(),
        tree,
    ),
)
menu_edicion.add_separator()
menubar.add_cascade(label="Editar", menu=menu_edicion)


submenu = Menu(menu_edicion, tearoff=0)
submenu.add_command(label="Color de fondo", command=lambda: funcion_color())
menu_edicion.add_cascade(label="Otros", menu=submenu)


main.config(menu=menubar)


################################################################################
# CALENDARIO ###################################################################
################################################################################

recuadro_calendario = LabelFrame(main, text="Calendario", bg="lightblue")
recuadro_calendario.grid(row=0, column=1, pady=30, padx=10)
tkc = Calendar(recuadro_calendario, selectmode="day", year=2022, month=12, date=1)
tkc.grid(row=0, column=0)


def funcion_fecha():
    date.config(text=tkc.get_date())


boton_seleccionar = Button(
    recuadro_calendario,
    text="Seleccionar fecha",
    command=lambda: funcion_fecha(),
    bg="lightgreen",
    fg="blue",
)
boton_seleccionar.grid(row=1, column=0, sticky=W + E)
date = Label(recuadro, text="Seleccione fecha en calendario", bg="black", fg="yellow")
date.grid(row=3, column=2, sticky=W)
################################################################################
# TREEVIEW #####################################################################
################################################################################

tree = ttk.Treeview(main)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
tree.column("#0", width=20, minwidth=10, anchor=W)
tree.column("col1", width=70, minwidth=60)
tree.column("col2", width=90, minwidth=80)
tree.column("col3", width=90, minwidth=80)
tree.column("col4", width=90, minwidth=50)
tree.column("col5", width=90, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Fecha")
tree.heading("col2", text="Hora")
tree.heading("col3", text="Nombre")
tree.heading("col4", text="Apellido")
tree.heading("col5", text="Contacto")
tree.grid(row=6, column=0, columnspan=2, sticky=W + E, padx=10)

main.mainloop()
