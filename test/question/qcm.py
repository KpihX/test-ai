try:
    from .question import Question
except ImportError:
    from question import Question

class QCM(Question):
    def __init__(self, label:str, choices:list[str], correct_answer:int):
        super().__init__(label, correct_answer)
        self.choices = choices
        
    def ask(self):
        print(self.label+"\n(Enter just the corresponding number!).\n")
        
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")
            
        user_answer = input("Your answer (number): ")
        print("")
            
        if int(user_answer) == self.correct_answer:
            print("Good answer!\n")
            return 1
        else:
            print(f"Bad answer. The correct answer is the option '{self.correct_answer}'.\n")
            return 0
        
    def __str__(self):
        return f"{'{'}type: QCM, label: {self.label}, choices: {self.choices}, correct: {self.correct_answer}{'}'}"
    
if __name__ == "__main__":
    print("\n* Test of qcm.ask() *\n")
    qcm = QCM("What is the capital of Cameroon ?", ["Paris", "London", "Yaoundé", "Madrid"], 3)
    qcm.ask()
    
    print("\n* Test of print(qcm) *\n")
    print(qcm)