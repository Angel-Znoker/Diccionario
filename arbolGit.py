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
			palabra = [nodo(n) for n in palabra]
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

		for n in range(len(palabra)):
			if palabra[0].id not in self.raiz.hijos.keys():
				self.agregarRama(self.raiz, palabra[0])
				palabra[0].agregarPadre(self.raiz)
			if n != len(palabra) - 1:
				self.agregarRama(palabra[n], palabra[n + 1])
				palabra[n + 1].agregarPadre(palabra[n])
			else:
				palabra[n].significado = sig