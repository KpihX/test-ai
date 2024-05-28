import google.generativeai as genai
import os
import sys
# from pyswip import Prolog
from utils import query_prolog

from classes import User, Category
from datas import QCM_FORMAT, QCM, QCM_EX, NUM_QUESTIONS, NUM_QCM_PROPS

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
DEFAULT_MODEL = 'gemini-pro'

class GenTestAI:
    def __init__(self, user: User, category: Category, model=DEFAULT_MODEL, api_key=GOOGLE_API_KEY):
        self.model = genai.GenerativeModel(model)
        self.category = category
        self.user = user
        genai.configure(api_key=api_key)
        self.history  = ""
        self.context = ""
        self.questions = []
        self.test_level = 1
        self.question_type = QCM
        
    @classmethod
    def list_models():
        return [model for model in genai.list_models() if 'generateContent' in model.supported_generation_methods]
    
    def generate_content(self, prompt):
        preambule = f"We are in a context of generating a learning test in the category f{self.category.label} of the usecase f{self.category.usecase.label}."
        context_prompt = f"In order to stay coherent with what you generated upstream: '{self.history}', generate a result for {prompt}."
        result = self.model.generate_content(preambule + "\n" + context_prompt)
        self.history = result
        return result
    
    def gen_next_test(self, question_type:int=QCM):
        context = self.gen_next_context()
        if question_type == QCM:
            questions = self.gen_next_qcms()
        self.test_level += 1
        return context, questions
    
    def gen_next_context(self):
        if self.test_level == 1:
            preambule = f"We are in a context of generating a learning test in the category f{self.category.label} of the usecase f{self.category.usecase.label}."
            example = f"{self.user.name} {self.category.ex_context}"
            prompt = f"{preambule}\nYou then have to generate (in one paragraph) a context for this test of level {self.test_level} (first level), throught which I will be able to ask questions to test the learner skills in this context. \
                What you'll generate has to have the same form as this example: '{example}'. You can change the subject.\
                Generate only the context in the form of the example. Don't add any conversation. And your context must used the same name {self.user.name} as in the example."
        elif self.test_level >= 2:
            preambule = f"We are still in a context of generating a learning test in the category f{self.category.label} of the usecase f{self.category.usecase.label}."
            prompt = f"{preambule}\nIn order to stay coherent with your previous context: '{self.context}', which was of level {self.test_level-1}, \
                generate (in one paragraph) a new context for this test (context must follow the form of the previous but must be different) of level {self.test_level} (next level), throught which I will be able to ask questions to test the learner skills in this context. \
                Generate only the context in the form of the previous. Don't add any conversation. And your context must used the same name {self.user.name} as in the previous"
            
        self.context = self.model.generate_content(prompt).text
        self.history = "context: "  + self.context
        return self.context
   
    def gen_next_qcms(self):
        prompt = f"We are in a context of generating a learning test in the category f{self.category.label} of the usecase f{self.category.usecase.label}. \
            and you already generated the following context: '{self.context}'. for this test of level {self.test_level}. \
            Now generate qcms that goes with the leraning context and category. The qcms must be questions posed {self.user.name}. \
            Your response have to be exactly in the format: {QCM_FORMAT}. Goes straight to the point by providing your answer in this format and your answer must have the same number of qcms and of propositions as in  the format. \
            Your proposition must follow exactly this example: {QCM_EX}; must have exactly {NUM_QUESTIONS} questions, and must be coherent with the absove context, category and usecase."
            
        qcms_str = self.model.generate_content(prompt).text
        # print("*qcms_str = " + qcms_str)
        while not self.qcms_check_format(qcms_str):
            print("!qcms format error, retrying...", file=sys.stderr)
            qcms_str = self.model.generate_content(prompt).text
            
        self.history += " qcms:" + qcms_str
        self.questions =  GenTestAI.qcms_formatter(qcms_str)
        return self.questions
    
    @classmethod
    def qcms_check_format(cls, qcms_str:str):
        file_path = "check_test_ai/check_qcms_format"
        question = f"check_qcms_format('{qcms_str}', {NUM_QUESTIONS}, {NUM_QCM_PROPS})."
        
        result = query_prolog(file_path, question)
        return result == "True"
    
    @classmethod
    def qcms_formatter(cls, qcms_str:str):
        qcms = qcms_str.split('+')
        qcms = [qcm.split('*') for qcm in qcms]
        qcms = [[qcm[0], qcm[1:]] for qcm in qcms]
        return qcms
    
# if __name__ == "__main__":
    # def test_prolog_check_qcms_format():
        # prolog = Prolog()
        # prolog.consult("check_test_ai/check_qcms_format.pl")
        # query = "check_qcms_format('Q1*p1*p2+Q2*p1*p2', 2, 1)"
        # print(prolog.query(query))