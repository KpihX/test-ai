from .question import Question
from .test_ind import TestInd

NUM_QUESTIONS_TEST = 5

class Test:
    def __init__(self, level:int, context:str, questions:list[Question], image:str=""):
        self.level = level
        self.context = context
        self.questions = questions
        self.image = image
        self.score = 0
        self.numb_tentatives = 0
            
    def run(self)-> (TestInd, int):
        self.numb_tentatives += 1
        print(f"* Test of level {self.level}.\n")
        
        # TODO: display of self.image
        
        print(f"Context: {self.context}\n")
        
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}:\n")
            score = question.ask()
            if score == None:
                print("!We will not consider this answer, since checking difficulties!\n")
            else:
                self.score += score
            
        print(f"Your score for this test is: {self.score}.\n")
        
        if not self.test_sucess():
            print("You failed and so you can't continue!\n")
            answer = input("Do you want to restart? (y/n): ")
            print()
            if answer.lower() == "y":
                return TestInd.REDO, self.score
            else:
                return TestInd.ABAN, self.score
        
        answer = input("Do you want to continue ? (y/n): ")
        print()
        if answer.lower() == "y":
            return TestInd.CONT, self.score
        else:
            return TestInd.ABAN, self.score
    
    def test_sucess(self):
        return self.score >= NUM_QUESTIONS_TEST / 2
    