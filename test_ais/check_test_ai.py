import subprocess

from test import Question, QCM, QRO

""" Datas """

CHECK_PROLOG_AI_PATH = "test_ais/check_test_ai/"
NUM_QCM_PROPS = 3

class CheckTestAI:
    
    @classmethod
    def check_qcm(cls, context:str, questions:list[Question], qcm:str):
        if not CheckTestAI.check_qcm_format(qcm):
            return False
        
        # file_path = CHECK_PROLOG_AI_PATH + "check_qcm.pl"
        # question = f"check_qcm('{context}, ')."
        # result = query_prolog(file_path, question)
        # return result == "True"
        return True
    
    @classmethod
    def check_qcm_format(cls, qcm_str:str):
        # print(f"* qm_str: {qcm_str}\n")
        file_path = CHECK_PROLOG_AI_PATH + "check_qcm_format.pl"
        question = f"check_qcm_format('{qcm_str}', {NUM_QCM_PROPS})."
        
        result = CheckTestAI.query_prolog(file_path, question)
        return result == "True"
        
    @classmethod
    def check_qro(cls, context:str, questions:list[Question], qro:str):
        if not CheckTestAI.check_qro_format(qro):
            return False
        
        file_path = CHECK_PROLOG_AI_PATH + "check_qro.pl"
        question = f"check_qro('{context}, ')."
        
        # result = query_prolog(file_path, question)
        # return result == "True"
        return True
    
    @classmethod
    def check_qro_format(cls, qro_str:str):
        # print(f"* qm_str: {qro_str}\n")
        file_path = CHECK_PROLOG_AI_PATH + "check_qro_format.pl"
        question = f"check_qro_format('{qro_str}')."
        
        result = CheckTestAI.query_prolog(file_path, question)
        return result == "True"
    
    @classmethod
    def check_context(cls, context:str):
        # file_path = CHECK_PROLOG_AI_PATH + "check_context.pl"
        # question = f"check_context('{context}')."
        
        # result = query_prolog(file_path, question)
        # return result == "True"
        return True
    
    @classmethod
    def query_prolog(cls, file_path:str, question:str):
        command = f"swipl -s \"{file_path}\" -g \"{question}\" -t halt"
        
        process = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        if process.returncode != 0:
            raise Exception("Une erreur s'est produite: ", process.stderr)
        
        return process.stdout.strip()
    
    