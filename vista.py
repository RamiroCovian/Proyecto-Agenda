from tkinter import StringVar
from tkinter import Label
from tkinter import LabelFrame
from tkinter import Entry
from tkinter import ttk
from tkinter import Button
from tkinter import Menu
from tkcalendar import Calendar
from modelo import click_nombre
from modelo import click_contacto
from modelo import click_apellido
from modelo import on_focus_nombre
from modelo import on_focus_apellido
from modelo import on_focus_contacto
from modelo import funcion_reserva
from modelo import funcion_modificar
from modelo import funcion_cancelar
from modelo import funcion_consultar
from modelo import funcion_color
from modelo import funcion_salir

################################################################################
# VISTA PRINCIPAL ##############################################################
################################################################################


def vista_principal(main):
    titulo_app = "Syntia SPA"
    main.title(titulo_app)
    main.geometry("675x615")
    main.resizable(width=False, height=False)
    main.iconbitmap("icono.ico")
    var_nombre = StringVar()
    var_apellido = StringVar()
    var_celular = StringVar()
    main.configure(bg="lightblue")
    recuadro = LabelFrame(main, text="Registro de Personas", bg="lightblue")
    recuadro.grid(row=0, column=0, pady=30, padx=10)

    nombre = Label(recuadro, text="Nombre", width=25, bg="lightblue")
    nombre.grid(row=0, column=1, sticky="w", pady=10)
    apellido = Label(recuadro, text="Apellido", width=25, bg="lightblue")
    apellido.grid(row=1, column=1, sticky="w", pady=10)
    contacto = Label(recuadro, text="Contacto", width=25, bg="lightblue")
    contacto.grid(row=2, column=1, sticky="w", pady=10)
    fecha = Label(recuadro, text="Fecha", width=25, bg="lightblue")
    fecha.grid(row=3, column=1, sticky="w", pady=10)
    hora = Label(recuadro, text="Horario", width=25, bg="lightblue")
    hora.grid(row=4, column=1, sticky="w", pady=10)

    entry_nombre = Entry(recuadro, textvariable=var_nombre, width=25)
    entry_nombre.grid(row=0, column=2, sticky="w")
    entry_nombre.focus_set()
    entry_nombre.bind("<Button-1>", click_nombre)
    entry_nombre.bind("<FocusIn>", on_focus_nombre)
    entry_apellido = Entry(recuadro, textvariable=var_apellido, width=25)
    entry_apellido.grid(row=1, column=2, sticky="w")
    entry_apellido.config(fg="grey")
    entry_apellido.insert(0, "-----")
    entry_apellido.bind("<Button-1>", click_apellido)
    entry_apellido.bind("<FocusIn>", on_focus_apellido)
    entry_contacto = Entry(
        recuadro,
        textvariable=var_celular,
        width=25,
    )
    entry_contacto.grid(row=2, column=2, sticky="w")
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
    combo.grid(row=4, column=2, sticky="w")

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
    boton_guardar.grid(row=5, column=1, sticky="w + e")

    boton_eliminar = Button(
        recuadro,
        text="Cancelar Turno",
        width=25,
        command=lambda: funcion_cancelar(),
        bg="red",
    )
    boton_eliminar.grid(row=6, column=2, sticky="w + e")

    boton_consultar = Button(
        recuadro,
        text="Consultar",
        width=25,
        command=lambda: funcion_consultar(),
        bg="yellow",
    )
    boton_consultar.grid(row=6, column=1, sticky="w")

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
    boton_modificar.grid(row=5, column=2, sticky="w")

    boton_salir = Button(
        main, text="Salir", width=25, command=lambda: funcion_salir(), bg="red"
    )
    boton_salir.grid(row=7, column=0, columnspan=2, sticky="w + e", padx=10)

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
    menu_archivo.add_command(
        label="Consultar Turnos", command=lambda: funcion_consultar()
    )
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
    boton_seleccionar.grid(row=1, column=0, sticky="w + e")
    date = Label(
        recuadro, text="Seleccione fecha en calendario", bg="black", fg="yellow"
    )
    date.grid(row=3, column=2, sticky="w")
    ################################################################################
    # TREEVIEW #####################################################################
    ################################################################################

    tree = ttk.Treeview(main)
    tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
    tree.column("#0", width=20, minwidth=10, anchor="w")
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
    tree.grid(row=6, column=0, columnspan=2, sticky="w + e", padx=10)
