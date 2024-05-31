import google.generativeai as genai
import os, sys, random
# from pyswip import Prolog
from user import User
from test import Category, Test, QuestTypes, QCM, QRO,NUM_QUESTIONS_TEST
from .check_test_ai import CheckTestAI


""" Datas """

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "AIzaSyDuuizDPb4lJMwdxbSYFixMksmJ-Ov7Ljs")
DEFAULT_MODEL = 'gemini-pro'
MAX_GENERATION = 3
NUM_QCM_PROPS = 3
QCM_FORMAT = f"question*number_correct_answer*prop1*..*prop{NUM_QCM_PROPS}"
QCM_EX = "Which transport mean we you usually use in a city ?*3*Bus*Train*Taxi"
QRO_FORMAT = f"question*correct_answer"
QRO_EX = "Which transport mean we you usually use in a city ?*Taxi"

class GenTestAI:
    def __init__(self, user: User, category: Category, model=DEFAULT_MODEL, api_key=GOOGLE_API_KEY):
        self.model = genai.GenerativeModel(model)
        genai.configure(api_key=api_key)
        self.category = category
        self.user = user
        self.history  = ""
        self.context = ""
        self.questions = []
        self.test_level = 0
        
    @classmethod
    def list_models():
        return [model for model in genai.list_models() if 'generateContent' in model.supported_generation_methods]
    
    def generate_content(self, prompt):
        preambule = f"We are in a context of generating a learning test in the category f{self.category.label} of the usecase f{self.category.usecase.label}.\n"
        context_prompt = f"In order to stay coherent with what you generated upstream: '{self.history}', generate a result for {prompt}."
        print("We are generating the result to the given prompt ...\n")
        result = self.model.generate_content(preambule + "\n" + context_prompt)
        self.history = result
        
        return result
    
    def gen_test(self, context_gen_func)-> Test:
        context = context_gen_func()
        
        if not context:
            return None
        
        self.context = context
        # print(f"* context: {self.context}\n")
            
        self.questions = []
        global quest_numb
        quest_numb = 0
        
        quest_types = self.quest_types()
        # print(f"*quest_types: {quest_types}\n")
        for quest_type in quest_types:
            quest_numb += 1
            # print(f"*quest_type: {quest_type}\n")
            if quest_type == QuestTypes.QCM:
                gen_next_quest = self.gen_next_qcm
            else: # quest_type = QuestTypes.qro
                gen_next_quest = self.gen_next_qro
                
            question = gen_next_quest()
            
            if not question:
                return None
                
            self.questions.append(question)
        
        return Test(self.test_level, self.context, self.questions)
    
    def gen_next_test(self)-> Test:
        self.test_level += 1
        print(f"We are generating the test N°{self.test_level} ...\n")
        return self.gen_test(self.gen_next_context)
    
    def regen_test(self)-> Test:
        print(f"We are regenerating the test N°{self.test_level} ...\n")
        return self.gen_test(self.regen_context)
    
    def quest_types(self)-> list[QuestTypes]:
        # return [QuestTypes.QCM for i in range(NUM_QUESTIONS_TEST)]
        return random.choices(list(QuestTypes), k=NUM_QUESTIONS_TEST)
    
    def gen_next_context(self):
        preambule = f"We are {'still' if self.test_level >= 2 else ''} in a context of generating a learning test in the category {self.category.label} of the usecase f{self.category.usecase.label}.\n"
        if self.test_level == 1:
            example = f"{self.user.name} {self.category.ex_context}"
            prompt = f"You then have to generate (in one paragraph) a context for this test of level {self.test_level} (first level), throught which I will be able to ask questions to test the learner skills in this context. \
                What you'll generate has to have the same form as this example: '{example}'. You can change the subject.\n"
        elif self.test_level >= 2:
            prompt = f"In order to stay coherent with your previous context: '{self.context}', which was of level {self.test_level-1}, \
                generate (in one paragraph) a new context for this test (context must follow the form of the previous but must be different) of level {self.test_level} (next level), throught which I will be able to ask questions to test the learner skills in this context.\n"
            
        end = f"Generate only the context in the form of the previous. Don't add any conversation. And your context must used the same name {self.user.name} as in the {'example' if self.test_level == 1 else 'previous context'}."
        
        try:
            print("We are generating the context ...\n")
            answer = self.model.generate_content(preambule + prompt + end).text
        except:
            print("!We are having issues with our distant generation model!\n", file=sys.stderr)
            return None
        
        number_generation = 1
        while not CheckTestAI.check_context(answer):
            if number_generation >= MAX_GENERATION:
                print("!We are no more able to generate coherent context for this test. Retry later!\n", file=sys.stderr)
                return None
            
            print("!No coherent context generated, retrying ...\n", file=sys.stderr)
            try:
                answer = self.model.generate_content(preambule + prompt + end).text
            except:
                print("!We are having issues with our distant generation model!\n", file=sys.stderr)
                return None
            number_generation += 1
            
        self.context = answer
        self.history = "context: "  + self.context + "\n"
        return self.context
    
    def regen_context(self):
        preambule = f"We are still in a context of generating a learning test in the category {self.category.label} of the usecase f{self.category.usecase.label}.\n"
        prompt = f"You previously generated this context: '{self.context}', which was of level {self.test_level-1}, \
            regenerate (in one paragraph) a similar one of the same level (context must follow the form of the previous but must be different), throught which I will be able to reask questions to test the learner skills in this updated context.\n"
            
        end = f"Generate only the context in the form of the previous. Don't add any conversation. And your context must used the same name {self.user.name} as in the previous context."
        
        try:
            print("We are regenerating the context ...\n")
            answer = self.model.generate_content(preambule + prompt + end).text
        except:
            print("!We are having issues with our distant generation model!\n", file=sys.stderr)
            return None
        
        number_generation = 1
        while not CheckTestAI.check_context(answer):
            if number_generation >= MAX_GENERATION:
                print("!We are no more able to generate coherent context for this test. Retry later!\n", file=sys.stderr)
                return None
            
            print("!No coherent context generated, retrying ...\n", file=sys.stderr)
            try:
                answer = self.model.generate_content(preambule + prompt + end).text
            except:
                print("!We are having issues with our distant generation model!\n", file=sys.stderr)
                return None
            number_generation += 1
            
        self.context = answer
        self.history = "context: "  + self.context + "\n"
        return self.context
   
    def gen_next_qcm(self) -> QCM:
        preambule = f"We are in a context of generating a learning test in the category {self.category.label} of the usecase f{self.category.usecase.label}. \
            and you already generated the following context {'' if quest_numb == 1 else 'and questions'}: '{self.history}', for this test of level {self.test_level};\n"
        prompt = f"Now generate a qcm that goes with the learning context, the category, the context{'' if quest_numb == 1 else ' ; and has to be coherent with the previous questions'}. The qcm must be a question asked to {self.user.name}. \
            Your response have to be exactly in the format: {QCM_FORMAT}. Goes straight to the point by providing your answer in this format and your answer must have the same number propostion as in the format. \
            Your proposition must follow exactly this example: {QCM_EX}."
        
        # print(f"* prompt: {preambule + prompt}\n")
        try:   
            print("We are generating the next question (qcm) ...\n") 
            qcm_str = self.model.generate_content(preambule + prompt).text
        except Exception as e:
            print(f"!We are having issues with our distant generation model! {e}\n", file=sys.stderr)
            return None
            
        number_generation = 1
        while not CheckTestAI.check_qcm(self.context, self.questions, qcm_str):
            if number_generation >= MAX_GENERATION:
                print("!We are no more able to generate coherent qcm for this test!\n", file=sys.stderr)
                return None
            
            print("!No coherent qcm generated, retrying...\n", file=sys.stderr)
            try:    
                qcm_str = self.model.generate_content(preambule + prompt).text
            except Exception as e:
                print(f"!We are having issues with our distant generation model! {e}\n", file=sys.stderr)
                return None
            number_generation += 1
            
        # print(f"* qcm: {qcm_str}\n")
        qcm_datas = qcm_str.split("*")
        qcm = QCM(qcm_datas[0], qcm_datas[2:], int(qcm_datas[1]))
        self.history += f"QCM{quest_numb}: "  + qcm_str + "\n"
        return qcm
    
    def gen_next_qro(self):
        preambule = f"We are in a context of generating a learning test in the category {self.category.label} of the usecase f{self.category.usecase.label} ; \
            and you already generated the following context {'' if quest_numb == 1 else 'and questions'}: '{self.history}', for this test of level {self.test_level};\n"
        prompt = f"Now generate a open response question (qro) that goes with the learning context, the category, the context{'' if quest_numb == 1 else ' ; and has to be coherent with the previous questions'}. The qro must be a question asked to {self.user.name}. \
            Your response have to be exactly in the format: {QRO_FORMAT}. Goes straight to the point by providing your answer in this format and your answer must have the same number propostion as in the format. \
            Your proposition must follow exactly this example: {QRO_EX}."
        
        # print(f"* prompt: {preambule + prompt}\n")
        try:   
            print("We are generating the next question (qro) ...\n") 
            qro_str = self.model.generate_content(preambule + prompt).text
        except Exception as e:
            print(f"!We are having issues with our distant generation model! {e}\n", file=sys.stderr)
            return None
            
        number_generation = 1
        while not CheckTestAI.check_qro(self.context, self.questions, qro_str):
            if number_generation >= MAX_GENERATION:
                print("!We are no more able to generate coherent qcm for this test!\n", file=sys.stderr)
                return None
            
            print("!No coherent qcm generated, retrying...\n", file=sys.stderr)
            try:    
                qro_str = self.model.generate_content(preambule + prompt).text
            except Exception as e:
                print(f"!We are having issues with our distant generation model! {e}\n", file=sys.stderr)
                return None
            number_generation += 1
            
        # print(f"* qro: {qro_str}\n")
        qro_datas = qro_str.split("*")
        qro = QRO(qro_datas[0], qro_datas[1])
        self.history += f"QRO{quest_numb}: "  + qro_str + "\n"
        return qro
    
