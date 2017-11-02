import arbolGit
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import font

class App():
	def __init__(self):
		self.arbol = arbolGit.arbol()
		self.ventana = Tk()
		self.ventana.geometry("720x530+200+100")
		self.ventana.resizable(width = FALSE, height = FALSE)
		self.ventana.title("Diccionario: Equipo 4")
		add = PhotoImage(file = "bib.gif")
		back = Label(self.ventana, image = add).place(x = 0, y = 0)

		barraMenu = Menu(self.ventana)
		mnuArchivo = Menu(barraMenu)
		mnuArchivo.add_command(label = "Cargar diccionario desde archivo", command = self.abrirArchivo)
		mnuArchivo.add_command(label = "Guardar diccionario en archivo", command = self.crearArchivo)
		barraMenu.add_cascade(label = "Archivo", menu = mnuArchivo)
		self.ventana.config(menu = barraMenu)

		self.btnAg = Button(self.ventana, text = "Agregar palabra", command = self.textEntry)
		self.btnAg.place(x = 330, y = 260)

		self.btnEl = Button(self.ventana, text = "Eliminar palabra", command = self.eliminarPalabra)
		self.btnEl.place(x = 329, y = 230)

		self.btnBs = Button(self.ventana, text = "Buscar palabra", command = self.buscarPalabra)
		self.btnBs.place(x = 333, y = 200)

		self.palabraUsuario = StringVar()
		self.miPalabra = Entry(self.ventana, textvariable = self.palabraUsuario, justify = CENTER, font = font.Font(family = "Arial", size = 14))
		self.palabraUsuario.set("Escribe aquí la palabra")
		self.miPalabra.place(x = 260, y = 100)
		self.miPalabra.bind("<Button-1>", self.limpiar)

		self.significadoPalabra = StringVar()
		self.miSignificado = Entry(self.ventana, textvariable = self.significadoPalabra, width = 50, justify = CENTER, font = font.Font(family = "Arial", size = 11))
		self.significadoPalabra.set("Escribe aquí el significado. Presiona [ENTER] al finalizar.")
		self.miSignificado.place(x = 170, y = 150)
		self.miSignificado.bind("<Button-1>", self.limpiar)
		self.miSignificado.lower()

		self.ventana.mainloop()

	def limpiar(self, x):
		x.widget.delete(0, END)

	def abrirArchivo(self):
		try:
			archivo = askopenfilename(filetypes = [("Text files","*.txt")])
			messagebox.showinfo(title = "Carga de diccionario desde archivo", message = self.arbol.cargaDesdeArchivo(archivo))
		except Exception as e:
			return

	def crearArchivo(self):
		try:
			archivo = asksaveasfilename(defaultextension = ".txt", filetypes = [("Text files","*.txt")])
			messagebox.showinfo(title = "Guardar diccionario en archivo", message = self.arbol.guardarArchivo(archivo))
		except Exception as e:
			return

	def obtenerPalabra(self):
		v = self.palabraUsuario.get() #Se obtiene la palabra
		v = v.lower()
		if v == "" or  not v.isalpha(): 
			return None
		return(list(v))

	def textEntry(self):
		self.miSignificado.lift()
		self.miSignificado.bind("<Return>", self.agregarPalabra)

	def agregarPalabra(self, sig):
		palabra = self.obtenerPalabra()
		significado = sig.widget.get()
		if(palabra != None and (significado != "" and significado != "Escribe aquí el significado")):
			self.arbol.agregarPalabra(palabra,significado)
			messagebox.showinfo(title = "Palabra agregada", message = "Palabra agregada exitosamente")
		else:
			messagebox.showwarning(title = "Atención", message = "Por favor revise los campos")
		self.miSignificado.delete(0, END)
		self.significadoPalabra.set("Escribe aquí el significado. Presiona [ENTER] al finalizar.")
		self.miSignificado.lower()

	def eliminarPalabra(self):
		if self.arbol.estaVacio() != True:
			palabra = self.obtenerPalabra()
			if(palabra != None):
				if(self.arbol.eliminarPalabra(palabra) == True):
					messagebox.showinfo(title = "Eliminación de palabra", message = "La palabra fue eliminada exitosamente")
				else:
					messagebox.showerror(title = "Eliminación de palabra", message = "No es posible eliminar la palabra")
			else:
				messagebox.showwarning(title = "Atención", message = "Escriba la palabra a eliminar")
		else:
			messagebox.showinfo(title = "Atención", message = "El diccionario se encuentra vacío")
	
	def buscarPalabra(self):
		if self.arbol.estaVacio() != True:
			palabra = self.obtenerPalabra()
			if(palabra != None):
				self.newWin = Toplevel()
				self.newWin.geometry("300x150+200+200")
				self.newWin.resizable(width = FALSE, height = FALSE)

				resultado = self.arbol.buscarPalabra(palabra)
				self.newWin.title(resultado[0])
				self.newWin.transient(self.ventana)

				if not isinstance(resultado[1],list):
					lblPalabra = Label(self.newWin, text = resultado[1], wraplength = 280)
					lblPalabra.pack()
				else:
					self.lstBox = Listbox(self.newWin)
					self.lstBox.pack()
					for item in resultado[1]:
						self.lstBox.insert(END,item[0])
				self.newWin.bind("<Button-1>", self.palabraSeleccionada)
				self.newWin.grab_set()
				self.ventana.wait_window(self.newWin)
			else: 
				messagebox.showwarning(title = "Atención", message = "Escriba la palabra a buscar")
		else:
			messagebox.showinfo(title = "Atención", message = "El diccionaro se encuentra vacío")
	
	def palabraSeleccionada(self,x):
		item = int(self.lstBox.curselection()[0])
		self.palabraUsuario.set(self.lstBox.get(item))
App()