# Nodos del arbol
class nodo:
	def __init__(self, i):
		# Metodo constructor
		self.id = i
		self.padre = None
		self.hijos = {}
		self.significado = ""