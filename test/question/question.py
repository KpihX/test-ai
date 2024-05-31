from abc import ABC, abstractmethod

class Question(ABC):
    def __init__(self, label:str, correct_answer) -> None:
        self.label = label
        self.correct_answer = correct_answer
        
    @abstractmethod
    def ask():
        pass
    
    @abstractmethod
    def __str__(self):
        pass