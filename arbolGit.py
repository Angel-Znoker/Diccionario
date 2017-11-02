# Nodos del arbol
class nodo:
	def __init__(self, i):
		# Metodo constructor
		self.id = i
		self.padre = None
		self.hijos = {}
		self.significado = ""

	# Metodo que agrega hijos a un nodo
	def agregarHijo(self, hijo):
		if hijo not in self.hijos:
			self.hijos.setdefault(hijo.id, hijo)

	# Metodo que agrega padre a un nodo
	def agregarPadre(self, padre):
		self.padre = padre

# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#

class arbol(object):
	def __init__(self):
		self.raiz = nodo("$")
		self.raiz.significado = "raiz"

	def estaVacio(self):
		if not self.raiz.hijos.keys():
			return True

	def agregarPalabra(self, palabra, sig):
		if palabra[0] not in self.raiz.hijos.keys():
			for n in range(len(palabra)):
				if n == 0:
					palabra[0] = nodo(palabra[0])
					self.agregarRama(self.raiz, palabra[0])
					palabra[0].agregarPadre(self.raiz)
				else:
					palabra[n] = nodo(palabra[n])
					self.agregarRama(palabra[n - 1], palabra[n])
					palabra[n].agregarPadre(palabra[n - 1])
				if n == len(palabra) - 1:
					palabra[n].significado = sig
		else:
			act = self.raiz.hijos[palabra[0]]
			palabra[0] = act
			for n in range(1, len(palabra)):
				if palabra[n] in act.hijos.keys():
					palabra[n] = act.hijos[palabra[n]]
					act = act.hijos[palabra[n].id]
				else:
					palabra[n] = nodo(palabra[n])
					act = palabra[n]
					self.agregarRama(palabra[n - 1], act)
					act.agregarPadre(palabra[n - 1])
				if n == len(palabra) - 1:
					palabra[n].significado = sig

	def agregarRama(self, a, b):
		a.agregarHijo(b)

	def existePalabra(self, act, palabra):
		if len(palabra) <= 0:
			if act.significado != "":
				return act
			else: return False
		else:
			if palabra[0] in act.hijos.keys():
				act = act.hijos[palabra[0]]
				return self.existePalabra(act, palabra[1:])
			else: return False

	def eliminarPalabra(self, palabra):
		eliminar = self.existePalabra(self.raiz, palabra)
		if eliminar != False:
			eliminar.significado = ""
			act = eliminar
			for n in range(len(palabra) - 1, -1, -1):
				if not act.hijos and act.significado == "":
					del(act.padre.hijos[act.id])
					act = act.padre
				else: break
			return True
		return False

	def buscarPalabra(self, palabra):
		encontrado = self.existePalabra(self.raiz, palabra)
		if encontrado != False:
			return [''.join(palabra), encontrado.significado]
		else:
			return ['Tal vez desee buscar:', self.resultadosRecorrido(palabra)]

	def recorridoInfix(self, act, palabra, lista):
		if len(act.hijos) > 0:
			orden = [n for n in act.hijos.keys()]
			orden.sort()
			for n in orden:
				if act.hijos[n].significado != "":
					lista.append([palabra + n, act.hijos[n].significado])
					self.recorridoInfix(act.hijos[n], palabra + n, lista)
				else:
					self.recorridoInfix(act.hijos[n], palabra + n, lista)
			return lista

	def resultadosRecorrido(self, palabra):
		lista = []
		act = self.raiz
		con = ""
		for n in palabra:
			if n in act.hijos.keys():
				con += n
				act = act.hijos[n]
			else:
				break
		lista = self.recorridoInfix(act, con, lista)
		return lista

	def guardarArchivo(self,ruta):
		try:
			archivo = open(ruta,'w')
			resultado = self.resultadosRecorrido('.')
			for item in resultado:
				archivo.write(item[0] + "|" + item[1] + "\n")
			return("El diccionario ha sido guardado")
		except IOError as e:
			return("Error al guardar el diccionario en el archivo")
		finally:
			archivo.close()

	def cargaDesdeArchivo(self, ruta):
		try:
			archivo = open(ruta,'r')
			for linea in archivo.readlines():
				linea = linea.split("|")
				if(len(linea) == 2):
					linea[1] = linea[1].replace('\n','').replace('\t','')
					self.agregarPalabra(list(linea[0].lower()),linea[1])
				else:
					return("El archivo no tiene el formato esperado")
			return("El diccionario se ha cargado exitosamente")
		except IOError as e:
			return("Error al cargar el diccionario desde el archivo")
		finally:
			archivo.close()