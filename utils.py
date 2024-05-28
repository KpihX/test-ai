import subprocess

def query_prolog(file_path, question):
    command = f"swipl -s \"{file_path}\" -g \"{question}\" -t halt"
    
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if process.returncode != 0:
        raise Exception("Une erreur s'est produite: ", process.stderr)
    
    return process.stdout.strip()

if __name__ == "__main__":
    file_path = "check_test_ai/check_qcms_format"
    question = "check_qcms_format('Q1*p1*p2+Q2*p1*p2', 2, 1)."
    
    result = query_prolog(file_path, question)
    
    print("Résultat: ", result)