class Usecase:
	def __init__(self, label:str, categories:list['Category'], description:str=""):
		self.label = label
		self.categories = categories
		self.description = description
  
from .category import Category