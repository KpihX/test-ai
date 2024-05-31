from .usecase import Usecase

class Category:
	def __init__(self, label:str, usecase:Usecase, ex_context:str, description:str=""):
		self.label = label
		self.description = description
		self.usecase = usecase
		self.ex_context = ex_context