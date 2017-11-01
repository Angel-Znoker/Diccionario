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
		