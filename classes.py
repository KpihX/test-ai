from abc import ABC, abstractmethod
from datas import NUM_QUESTIONS, MAX_NUM_TENT_TEST, QCM, QRO

class User:
	def __init__(self, user_id:int, name:str, level:int):
		self.user_id = user_id
		self.name = name
		self.level = level
		self.score = 0
  
class Usecase:
	def __init__(self, label:str, categories:list['Category'], description:str=""):
		self.label = label
		self.categories = categories
		self.description = description

class Category:
	def __init__(self, label:str, usecase:Usecase, ex_context:str, description:str=""):
		self.label = label
		self.description = description
		self.usecase = usecase
		self.ex_context = ex_context

class Question(ABC):
    def __init__(self, type:str, label:str, correct_answer) -> None:
        self.label = label
        self.correct_answer = correct_answer
        self.type = type
        
    @abstractmethod
    def ask():
        pass

class QCM(Question):
    def __init__(self, label:str, choices:list[str], correct_answer:int, type:str=QCM):
        super().__init__(QCM, label, correct_answer)
        self.choices = choices
        
    def ask(self):
        print(self.label+"\n(Enter just the corresponding number!).\n")
        
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")
            user_answer = input("Your answer (number): ")
            print("")
            
        if int(user_answer) == self.correct_choice:
            print("Good answer!\n")
            return 1
        else:
            print("Bad answer. The correct answer was '{self.correct_choice}'.\n")
            return 0

class Test:
    def __init__(self, category:Category, level:int, context:str, questions:list[Question], image:str=""):
        self.level = level
        self.category = category
        self.context = context
        self.questions = questions
        self.image = image
        self.score = 0
        self.numb_tentatives = 0
            
    def run(self):
        self.numb_tentatives += 1
        print(f"* Test of level {self.level}.\n")
        
        # TODO: display of self.image
        
        print(f"Context: {self.context}\n")
        
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}:\n")
            self.score += question.ask()
            
        print("Your score for this test is: {self.score}.\n")
        if not self.test_sucess():
            print("You failed and so you can't continue!\n")
            if self.numb_tentatives == MAX_NUM_TENT_TEST:
                print("You have reached the maximum number of tentatives.\n")
                return False, self.score
            
            answer = input("Do you want to restart? (y/n): ")
            print()
            if answer.lower() == "y":
                self.run()
            else:
                return False, self.score
        
        answer = input("Do you want to continue ? (y/n): ")
        print()
        return answer == "y", self.score
    
    def test_sucess(self):
        return self.score >= NUM_QUESTIONS / 2
