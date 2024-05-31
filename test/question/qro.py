import os, sys
import google.generativeai as genai

try:
    from .question import Question
except ImportError:
    from question import Question

""" Datas """

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "AIzaSyDuuizDPb4lJMwdxbSYFixMksmJ-Ov7Ljs")
DEFAULT_MODEL = 'gemini-pro'
MAX_GENERATION = 3

class QRO(Question):
    def __init__(self, label:str, correct_answer:str):
        super().__init__(label, correct_answer)
        
    def ask(self):
        print(self.label+"\n")
            
        user_answer = input("Your answer: ")
        print("")
        
        check_answer = self.check_answer(user_answer)
        if check_answer == None:
            return None
            
        if check_answer:
            print("Good answer!\n")
            return 1
        else:
            print(f"Bad answer. The correct answer is '{self.correct_answer}'.\n")
            return 0
        
    def check_answer(self, proposition:str):
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(DEFAULT_MODEL)
        
        prompt = f"For the question '{self.label}' you provided this answer '{self.correct_answer}' ; and the user provide this answer '{proposition}'!\
        Analyse all this to state whether the answer of the user is correct or no!If the good answer upstream is something as 'any answer', it means that any answer given by the user is correct\
        Answer only by yes or no, nothing else!"
        
        try:
            print("We are checking the answer ...\n")
            answer = model.generate_content(prompt).text
        except:
            print("!We are having issues with our distant generation model!\n", file=sys.stderr)
            return None
        
        number_generation = 1
        answer = answer.lower()
        while answer not in {"yes", "no"}:
            if number_generation >= MAX_GENERATION:
                print("!We are no more able to check your answer for this qro. Retry later!\n", file=sys.stderr)
                return None
            
            print("!Problem while checking your answer, retrying ...\n", file=sys.stderr)
            try:
                answer = model.generate_content(prompt).text
            except:
                print("!We are having issues with our distant generation model!\n", file=sys.stderr)
                return None
            number_generation += 1
            
        return answer == "yes"
        
    def __str__(self):
        return f"{'{'}type: QRO, label: {self.label}, correct: {self.correct_answer}{'}'}"
    
if __name__ == "__main__":
    print("\n* Test of qro.ask() *\n")
    qcm = QRO("What is the capital of Cameroon ?", "Yaoundé")
    qcm.ask()
    
    print("\n* Test of print(qro) *\n")
    print(qcm)