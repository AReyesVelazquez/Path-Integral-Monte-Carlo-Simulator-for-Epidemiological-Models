# Simulador Epidemiológico Compartimental
# Abraham Rafael Reyes Velázquez
  
# I. GUI
import tkinter as tk
from tkinter import ttk
from tkinter import font
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# 1 Funciones de GUI
# 1.1 Salir del Programa
def cerrarprograma():
    root.quit()
# 1.2 Crear una nueva entrada en Tabla Compartimentos
def nuevocomp():
    i = len(indices_comp)
    indices_comp.append(i+1)
    compartimentos.append('Compartimento ' + str(i+1))
    pobinicial.append(0)
    descripcion.append('')
    tabla_comp.insert('',index='end',iid=i+1,values=(i+1,compartimentos[i],pobinicial[i],descripcion[i]))
    tabla_comp.see(i+1)
    tabla_comp.update()
# 1.3 Eliminar una entrada seleccionada de Tabla Compartimentos
def elimcomp():
    for item in tabla_comp.selection():
        j = int(item)-1
    indices_comp.pop(j)
    compartimentos.pop(j)
    pobinicial.pop(j)
    descripcion.pop(j)
    tabla_comp.delete(*tabla_comp.get_children())
    for i in range (len(indices_comp)):
        tabla_comp.insert('',index='end',iid=i+1,values=(i+1,compartimentos[i],pobinicial[i],descripcion[i]))
    tabla_comp.update()
    if j == 0:
        try:
            tabla_comp.selection_set(j+1)
        except:
            return
    else:
        tabla_comp.selection_set(j)
# 1.4 Editar una Celda de Tabla Compartimentos
def editarcomp(event):
    def guardarcomp():
        cambio = str(entrada_comp.get(0.0,'end').replace('\n',''))
        tabla_comp.set(row, column=col, value=cambio)
        if cn == 1:
            compartimentos[rn] = cambio
        elif cn == 2:
            pobinicial[rn]=int(cambio)
        elif cn == 3:
            descripcion[rn]=cambio
        entrada_comp.destroy()
        boton_guardar_comp.destroy()
    for item in tabla_comp.selection():
        col = tabla_comp.identify_column(event.x)
        row = tabla_comp.identify_row(event.y)
        #print(col,row)
    cn = int(str(col).replace('#',''))-1
    if cn == 0:
        return
    rn = int(str(row).replace('I',''))-1
    x1 = x2 = int(tabla_comp.column(cn,'width')/9)-1
    if cn == 1:
        celda = compartimentos[rn]
    elif cn == 2:
        celda = str(pobinicial[rn])
    elif cn == 3:
        celda = descripcion[rn]
        x2 = x2+70
    it = tabla_comp.bbox(row, column=cn)
    entrada_comp = tk.Text(tabla_comp, width=x1)
    entrada_comp.config(font=ftablabody, bg=teal6, fg=white, selectbackground=cher5, inactiveselectbackground=cher3, highlightthickness=0, height=1)
    entrada_comp.insert(tk.END, celda)
    entrada_comp.tag_add(tk.SEL, '1.0', tk.END)
    boton_guardar_comp = ttk.Button(tabla_comp, style='Guar.TButton', text='Guardar', command=guardarcomp)
    entrada_comp.place(x=it[0], y=it[1]+1)
    boton_guardar_comp.place(x=it[0]+x2, y=it[1]+20)
    entrada_comp.focus_set()
# 1.5 Crear una nueva entrada en Tabla Transiciones
def nuevatrans():
    i = len(indices_trans)
    indices_trans.append(i+1)
    edo_inicial.append('A')
    edo_final.append('B')
    probs_trans.append(0)
    tiempos_trans.append(0)
    tabla_trans.insert('',index='end',iid=i+1,values=(i+1,edo_inicial[i],edo_final[i],probs_trans[i],tiempos_trans[i]))
    tabla_trans.see(i+1)
    tabla_trans.update()
# 1.6 Eliminar una entrada seleccionada de Tabla Transiciones
def elimtrans():
    for item in tabla_trans.selection():
        j = int(item)-1
    indices_trans.pop(j)
    edo_inicial.pop(j)
    edo_final.pop(j)
    probs_trans.pop(j)
    tiempos_trans.pop(j)
    tabla_trans.delete(*tabla_trans.get_children())
    for i in range (len(indices_trans)):
        tabla_trans.insert('',index='end',iid=i+1,values=(i+1,edo_inicial[i],edo_final[i],probs_trans[i],tiempos_trans[i]))
    tabla_trans.update()
    if j == 0:
        try:
            tabla_trans.selection_set(j+1)
        except:
            return
    else:
        tabla_trans.selection_set(j)
# 1.7 Editar una Celda de Tabla Transiciones
def editartrans(event):
    def guardartransA(event):
        cambio = str(opcion.get())
        tabla_trans.set(row, column=col, value=cambio)
        if cn == 1:
            edo_inicial[rn] = cambio
        elif cn == 2:
            edo_final[rn] = cambio
        menu_trans.destroy()
    def guardartransB():
        cambio = str(entrada_trans.get(0.0,'end').replace('\n',''))
        tabla_trans.set(row, column=col, value=cambio)
        if cn == 3:
            probs_trans[rn]=float(cambio)
        elif cn == 4:
            tiempos_trans[rn]=float(cambio)
        entrada_trans.destroy()
        boton_guardar_trans.destroy()
    for item in tabla_trans.selection():
        col = tabla_trans.identify_column(event.x)
        row = tabla_trans.identify_row(event.y)
    cn = int(str(col).replace('#',''))-1
    if cn == 0:
        return
    rn = int(str(row).replace('I',''))-1
    x1 = int(tabla_trans.column(cn,'width'))
    x2 = int(x1/9)-1
    it = tabla_trans.bbox(row, column=cn)
    if cn == 1 or cn == 2:
        opcion = tk.StringVar()
        menu_trans = tk.OptionMenu(tabla_trans, opcion, *compartimentos, command=guardartransA)
        menu_trans.configure(background=teal6,font=ftablabody)
        menu_trans.place(x=it[0]+it[2]/2-11, y=it[1])
    if cn == 3 or cn == 4:
        if cn == 3:
            celda = str(probs_trans[rn])
        if cn == 4:
            celda = str(tiempos_trans[rn])
        entrada_trans = tk.Text(tabla_trans, width=x2)
        entrada_trans.config(font=ftablabody,bg=teal6,fg=white,selectbackground=cher5,inactiveselectbackground=cher3,highlightthickness=0,height=1)
        entrada_trans.insert(tk.END, celda)
        entrada_trans.tag_add(tk.SEL, '1.0', tk.END)
        boton_guardar_trans = ttk.Button(tabla_trans,style='Guar.TButton',text='Guardar',command=guardartransB)
        entrada_trans.place(x=it[0]+1, y=it[1])
        boton_guardar_trans.place(x=it[0]+x2,y=it[1]+19)
        entrada_trans.focus_set()
# 1.8 Añadir entrada a Tabla Contagios
def nuevocont():
    i = len(indices_cont)
    indices_cont.append(i+1)
    edo_A.append('A')
    edo_B.append('B')
    edo_C.append('C')
    edo_D.append('D')
    r_0.append(0)
    tiempos_cont.append(0)
    tabla_cont.insert('',index='end',iid=i+1,values=(i+1,edo_A[i],edo_B[i],edo_C[i],edo_D[i],r_0[i],tiempos_cont[i]))
    tabla_cont.see(i+1)
    tabla_cont.update()
# 1.9 Eliminar entrada seleccionada de Tabla Contagios
def elimcont():
    for item in tabla_cont.selection():
        j = int(item)-1
    indices_cont.pop(j)
    edo_A.pop(j)
    edo_B.pop(j)
    edo_C.pop(j)
    edo_D.pop(j)
    r_0.pop(j)
    tiempos_cont.pop(j)
    tabla_cont.delete(*tabla_cont.get_children())
    for i in range (len(indices_cont)):
        tabla_cont.insert('',index='end',iid=i+1,values=(i+1,edo_A[i],edo_B[i],edo_C[i],edo_D[i],r_0[i],tiempos_cont[i]))
    tabla_cont.update()
# 1.10 Editar celda de Tabla Contagios
def editarcont(event):
    def guardarcontA(event):
        cambio = str(opcion.get())
        tabla_cont.set(row,column=col,value=cambio)
        if cn == 1:
            edo_A[rn] = cambio
        elif cn == 2:
            edo_B[rn] = cambio
        elif cn == 3:
            edo_C[rn] = cambio
        elif cn == 4:
            edo_D[rn] = cambio
        menu_cont.destroy()
    def guardarcontB():
        cambio = str(entrada_cont.get(0.0,'end').replace('\n',''))
        tabla_cont.set(row,column=col,value=cambio)
        if cn == 5:
            r_0[rn] = float(cambio)
        elif cn == 6:
            tiempos_cont[rn] = float(cambio)
        entrada_cont.destroy()
        boton_guardar_cont.destroy()
    for item in tabla_cont.selection():
        col = tabla_cont.identify_column(event.x)
        row = tabla_cont.identify_row(event.y)
    cn = int(str(col).replace('#',''))-1
    if cn == 0:
        return
    rn = int(row)-1
    x1 = int(tabla_cont.column(cn,'width'))
    x2 = int(x1/9)-1
    it = tabla_cont.bbox(row, column=cn)
    if cn == 1 or cn == 2 or cn == 3 or cn == 4:
        opcion = tk.StringVar()
        opcion.set(compartimentos[0])
        menu_cont = tk.OptionMenu(tabla_cont,opcion,*compartimentos,command=guardarcontA)
        menu_cont.configure(background=teal6, font=ftablabody)
        menu_cont.place(x=it[0]+it[2]/2-11, y=it[1])
    if cn == 5 or cn == 6:
        if cn == 5:
            celda = str(r_0[rn])
        if cn == 6:
            celda = str(tiempos_cont[rn])
        entrada_cont = tk.Text(tabla_cont, width=x2)
        entrada_cont.config(font=ftablabody,bg=teal6,fg=white,selectbackground=cher5,inactiveselectbackground=cher3,highlightthickness=0,height=1)
        entrada_cont.insert(tk.END, celda)
        entrada_cont.tag_add(tk.SEL, '1.0', tk.END)
        boton_guardar_cont = ttk.Button(tabla_cont,style='Guar.TButton',text='Guardar',command=guardarcontB)
        entrada_cont.place(x=it[0]+1, y=it[1])
        boton_guardar_cont.place(x=it[0]+x2, y=it[1]+19)
        entrada_cont.focus_set()
# 2 Inicialización de la Pantalla Principal (root)
root = tk.Tk()
root.wm_attributes('-fullscreen', 1)
wmf,hmf = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (wmf,hmf,0,0))
root.title('Simulador Epidemiológico Compartimental')

# 3 Diseño Visual de Interfaz
# 3.1 Cambiar tema
tema = ttk.Style()
tema.theme_use('clam')
# 3.2 Paleta de colores
# teal
teal1 = '#101d20'
teal2 = '#26494d'
teal3 = '#2e5155'
teal4 = '#34575b'
teal5 = '#3d6064'
teal6 = '#476a6e'
teal7 = '#4f7276'
# cherry
cher1 = '#84264d'
cher2 = '#8c2e55'
cher3 = '#92345b'
cher4 = '#9b3d64'
cher5 = '#a5476e'
cher6 = '#ad4f76'
# pine
teak1 = '#baad6d'
teak2 = '#c2b575'
teak3 = '#c8bb7b'
teak4 = '#d1c484'
teak5 = '#dbce8e'
teak6 = '#e3d696'
# otros
white = '#FFFFFF'
black = '#000000'
gray = '#d5d5d5'
# 3.3 Fuentes
familia = 'Montserrat'
fmainframe = tk.font.Font(family=familia, size=30)
fetiquetas = tk.font.Font(family=familia, size=20)
ftablahead = tk.font.Font(family=familia, size=17, weight='bold')
ftablabody = tk.font.Font(family=familia, size=14)
fbotones = tk.font.Font(family=familia, size=17)
# 3.4 Estilos de Widgets
# 3.4.1 Frames
sframes = ttk.Style()
sframes.configure('Main.TFrame', background=teal1)
sframes.configure('Comp.TFrame', background=teal1)
sframes.configure('Par.TFrame', background=teal1)
sframes.configure('Res.TFrame', background=teal4)
# 3.4.2 Tabla
stabla = ttk.Style()
stabla.configure('Comp.Treeview.Heading', font=ftablahead, foreground=white, relief='flat')
stabla.map('Comp.Treeview.Heading', background=[('active',teal2),('!active',teal2)])
stabla.configure('Comp.Treeview', font=ftablabody, foreground=white, fieldbackground=teal3, bordercolor=teal1,darkcolor=teal1,lightcolor=teal1, rowheight=21, relief='flat')
stabla.map('Treeview', background=[('selected', teal6),('!selected', teal4)])
stabla.configure('Comp.Treeview.Item', indicatormargins=0)
# 3.4.3 Scrollbars
sscroll = ttk.Style()
sscroll.configure('Comp.Vertical.TScrollbar', arrowcolor=white, troughcolor=teak6, arrowsize=18, bordercolor=teal1, relief='flat',lightcolor=teal1,darkcolor=teal1)
sscroll.map('Comp.Vertical.TScrollbar', background=[('active',teal3), ('!active', teal4), ('disabled', gray)])
# 3.4.4 Botones
sboton = ttk.Style()
sboton.configure('TButton', foreground=white, font=fbotones, width=20)
sboton.configure('Guar.TButton', foreground=white, font=ftablabody, width=10)
sboton.configure('Cerr.TButton', width=15)
sboton.map('TButton', background=[('active', cher1), ('!active', cher2)], relief=[('active','flat'), ('!active', 'flat')])
# 3.4.5 Etiquetas
setiq = ttk.Style()
setiq.configure('MainName.TLabel', background=teal1, foreground=white, font=fmainframe)
setiq.configure('Head.TLabel', background=teal1, foreground=white, font=fetiquetas, padding=0)
setiq.configure('Head2.TLabel', background=teal1, foreground=white, font=fetiquetas)
setiq.configure('Res.TLabel', background=teal3, foreground=white, font=fetiquetas)

# 4 Mainframe
# 4.1 Inicialización
root.configure(bg=teal1)
ipadmf = 10
hname = 40
mainframe = ttk.Frame(root, style='Main.TFrame', width=wmf, height=hmf, padding=ipadmf)
mainframe.grid(column=0, row=0)
maintitle = ttk.Label(mainframe, style='MainName.TLabel', justify='center', text='Simulador Epidemiológico Compartimental')
maintitle.grid(column=0, row=0, columnspan=2)
epadf = 6
wfs = (wmf-2*ipadmf-4*epadf)/2
wfi = (wmf-2*ipadmf-2*epadf)
hf = (hmf-2*ipadmf-hname-4*epadf)/2
wico = wfs-49
walfa = int(wico/2)
wbeta = int(wico/4)
wgamma = int(wico/5)
wdelta = int(wico/10)
# 4.2 Frames de Interfaz (Compartimentos, Parámetros, Resultados)
frame_comp = ttk.Frame(mainframe, style='Comp.TFrame', width=wfs, height=hf)
frame_par = ttk.Frame(mainframe, style='Par.TFrame', width=wfs, height=hf)
frame_res = ttk.Frame(mainframe, style='Res.TFrame', width=wfi, height=hf)
frame_comp.grid(column=0, row=1, pady=epadf, padx=epadf, sticky=tk.E+tk.W)
frame_par.grid(column=1, row=1, pady=epadf, padx=epadf)
frame_res.grid(column=0, row=2, columnspan=2, pady=epadf)

# 5 Frame Compartimentos
# 5.1 Nombre Frame
tabla_comp_name = ttk.Label(frame_comp, style='Head.TLabel', text='Compartimentos del sistema')
# 5.2 Tabla Compartimentos
rh = int((hf-98)/21)
tabla_comp = ttk.Treeview(frame_comp, style='Comp.Treeview', show='headings', columns=("#","Nombre", "Población Inicial", "Descripción"), height=rh)
tabla_comp.column(0, width=25, anchor='center')
tabla_comp.column(1, width=wbeta, anchor='center')
tabla_comp.column(2, width=wbeta, anchor='center')
tabla_comp.column(3, width=walfa, anchor='center')
tabla_comp.heading(0, text="#")
tabla_comp.heading(1, text="Nombre")
tabla_comp.heading(2, text="Población Inicial")
tabla_comp.heading(3, text="Descripción")
tabla_comp.bind('<Double-1>', editarcomp)
# 5.3 Scroll Tabla Compartimento
scroll_comp = ttk.Scrollbar(frame_comp, style='Comp.Vertical.TScrollbar', command=tabla_comp.yview)
tabla_comp.configure(yscrollcommand=scroll_comp.set)
# 5.4 Botones Compartimentos
nuevestad = ttk.Button(frame_comp, style='TButton', text="Añadir entrada", command=nuevocomp)
elimestad = ttk.Button(frame_comp, style='TButton', text="Borrar entrada", command=elimcomp)
# 5.5 Layout de Elementos en Frame Compartimentos
tabla_comp_name.grid(column=0, row=0, columnspan=3, pady=3)
nuevestad.grid(column=0, row=2, pady=3)
elimestad.grid(column=1, row=2, pady=3)
tabla_comp.grid(column=0, row=1, columnspan=2)
scroll_comp.grid(column=2, row=1, columnspan=1,sticky=tk.N+tk.S)
quitbu = ttk.Button(root, style='Cerr.TButton', text="Cerrar programa", command=cerrarprograma)
quitbu.place(x=maintitle.winfo_rootx()+ipadmf+epadf, y=maintitle.winfo_rooty()-18)


# 6 Frame Parámetros
rh = int(((hf/2)-121)/21)
# 6.1 Transiciones
# 6.1.1 Nombre Tabla Transiciones
tabla_trans_name = ttk.Label(frame_par, style='Head2.TLabel', text='Transiciones en el sistema' + '\n' + '                   (A->B)', anchor='center')
# 6.1.2 Tabla Transiciones
tabla_trans = ttk.Treeview(frame_par,style='Comp.Treeview',show='headings',columns=('#','Inicial','Final','Probabilidad','Tiempo'),height=rh)
tabla_trans.column(0, width=25, anchor='center')
tabla_trans.column(1, width=wbeta, anchor='center')
tabla_trans.column(2, width=wbeta, anchor='center')
tabla_trans.column(3, width=wbeta, anchor='center')
tabla_trans.column(4, width=wbeta, anchor='center')
tabla_trans.heading(0, text="#")
tabla_trans.heading(1, text="Inicial")
tabla_trans.heading(2, text="Final")
tabla_trans.heading(3, text="Probabilidad")
tabla_trans.heading(4, text="Tiempo")
tabla_trans.bind('<Double-1>', editartrans)
# 6.1.3 Scroll Tabla Transiciones
scroll_trans = ttk.Scrollbar(frame_par, style='Comp.Vertical.TScrollbar', command=tabla_trans.yview)
tabla_trans.configure(yscrollcommand=scroll_trans.set)
# 6.1.4 Botones Tabla Transiciones
nuetrans = ttk.Button(frame_par, style='TButton', text='Añadir entrada', command=nuevatrans)
elimitrans = ttk.Button(frame_par, style='TButton', text='Eliminar entrada', command=elimtrans)
# 6.2 Contagios
# 6.2.1 Nombre Tabla Contagios
tabla_cont_name = ttk.Label(frame_par, style='Head2.TLabel', text='Contagios en el sistema' + '\n' +'           (A+B->C+D)')
# 6.2.2 Tabla Contagios
tabla_cont = ttk.Treeview(frame_par,style='Comp.Treeview',show='headings',columns=('#','Estado A','Estado B','Estado C','Estado D','R_0','Tiempo'),height=rh)
tabla_cont.column(0, width=25, anchor='center')
tabla_cont.column(1, width=wgamma, anchor='center')
tabla_cont.column(2, width=wgamma, anchor='center')
tabla_cont.column(3, width=wgamma, anchor='center')
tabla_cont.column(4, width=wgamma, anchor='center')
tabla_cont.column(5, width=wdelta, anchor='center')
tabla_cont.column(6, width=wdelta, anchor='center')
tabla_cont.heading(0, text='#')
tabla_cont.heading(1, text='Estado A')
tabla_cont.heading(2, text='Estado B')
tabla_cont.heading(3, text='Estado C')
tabla_cont.heading(4, text='Estado D')
tabla_cont.heading(5, text='R_0')
tabla_cont.heading(6, text='Tiempo')
tabla_cont.bind('<Double-1>', editarcont)
# 6.2.3 Scroll Tabla Contagios
scroll_cont = ttk.Scrollbar(frame_par, style='Comp.Vertical.TScrollbar', command=tabla_cont.yview)
tabla_cont.configure(yscrollcommand=scroll_cont.set)
# 6.2.4 Botones Tabla Contagios
nuecont = ttk.Button(frame_par, style='TButton', text='Añadir entrada', command=nuevocont)
elicont = ttk.Button(frame_par, style='TButton', text='Eliminar entrada', command=elimcont)
# 6.3 Layout de Elementos en Frame Parámetros
tabla_trans_name.grid(column=0, row=0, columnspan=3, pady=3)
tabla_trans.grid(column=0, row=1, columnspan=2)
scroll_trans.grid(column=2, row=1, sticky=tk.N+tk.S)
nuetrans.grid(column=0, row=2, pady=3)
elimitrans.grid(column=1, row=2, pady=3)
tabla_cont_name.grid(column=0, row=3, columnspan=3, pady=3)
tabla_cont.grid(column=0, row=4, columnspan=2)
scroll_cont.grid(column=2, row=4, sticky=tk.N+tk.S)
nuecont.grid(column=0, row=5, pady=3)
elicont.grid(column=1, row=5, pady=3)

# II. Simulador
# Listas de datos
indices_comp = []
compartimentos = []
pobinicial = []
descripcion = []

indices_trans = []
edo_inicial = []
edo_final = []
probs_trans = []
tiempos_trans = []

indices_cont = []
edo_A = []
edo_B = []
edo_C = []
edo_D = []
r_0 = []
tiempos_cont = []

# Clases
class Estado:
    def __init__(self, nombre):
        self.nombre = str(nombre)
        self.poblacion = [pobinicial[compartimentos.index(nombre)]]

class ReaccionUnitaria:
    def __init__(self, A, B):
        self.a = compartimentos.index(A)
        self.b = compartimentos.index(B)
    def efecto(self):
        pobinicial[self.a] -= 1
        pobinicial[self.b] += 1
    def peso(self):
        return pobinicial[self.a]

class ReaccionBinaria:
    def __init__(self, A, B, C):
        self.a = compartimentos.index(A)
        self.b = compartimentos.index(B)
        self.c = compartimentos.index(C)
    def efecto(self):
        pobinicial[self.a] -= 1
        pobinicial[self.c] += 1
    def peso(self):
        return pobinicial[self.a]*pobinicial[self.b]

# Funciones
def Simulacion():
    #plt.clear()
    # Variables
    t = 0
    t_react = 1
    t_stop = 1500
    N = np.sum(pobinicial)
    # Rangos
    n_est = len(indices_comp)
    n_trans = len(indices_trans)
    n_cont = len(indices_cont)
    # Listas
    Estados = []
    Tasas = []
    Reacciones = []
    tiiiempo = [0]
    # Llenado de listas
    for i in range(n_est):
        Estados.append(Estado(compartimentos[i]))
    for i in range(n_trans):
        Tasas.append(probs_trans[i]/tiempos_trans[i])
        Reacciones.append(ReaccionUnitaria(edo_inicial[i],edo_final[i]))
    for i in range(n_cont):
        Tasas.append(r_0[i]/(N*tiempos_cont[i]))
        Reacciones.append(ReaccionBinaria(edo_A[i],edo_B[i],edo_C[i]))
    n_reac = len(Reacciones)
    C = np.zeros(n_reac)
    D = np.zeros(n_reac)
    # Gillespie
    while t < t_stop:
        aa = 0
        for i in range(n_reac):
            C[i] = Reacciones[i].peso()
            D[i] = C[i]*Tasas[i]
        aa = np.sum(D)
        if aa == 0:
            #print('broken')
            break
        tau = pow(aa,-1)*np.log(1/rnd.uniform(0,1))
        bb = rnd.uniform(0,1)*aa
        m = 0
        n = 0
        while m < bb:
            m += D[n]
            n += 1
        nu = n-1
        if tau <= t_react:
            Reacciones[nu].efecto()
            t += tau
            #print(pobinicial)
        if tau > t_react:
            t = t
        for i in range(n_est):
            Estados[i].poblacion.append(pobinicial[i])
        tiiiempo.append(t)
        #print(pobinicial)
    #axiss = np.empty(n_est) 
    #print(pobinicial)
    for i in range(n_est):
        plt.plot(tiiiempo,Estados[i].poblacion,label=Estados[i].nombre)
    plt.xlabel('Tiempo')
    plt.ylabel('Población')
    plt.legend(loc='lower left')
    plt.show()
    #canvas.draw()
    #canvas.get_tk_widget().grid(row=1, col=0)

# Frame Parámetros
# Botón de Correr Simulación
Correr = ttk.Button(frame_res,style='TButton',text='Correr',command=Simulacion)
# Canvas de Gráfica
#fig = Figure(figsize=(4,3),dpi=100)
#plot = plt.plot()
#canvas = FigureCanvasTkAgg(plot, master=frame_res)
#canvas.draw()
# Layout de Frame Parámetros
Correr.grid(column=0,row=0)
#canvas.get_tk_widget().grid(column=0, row=1)

root.mainloop()

