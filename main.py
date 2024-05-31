import sys

from user import User
from test import Usecase, Category, TestInd
from test_ais import GenTestAI

""" Datas """

USECASES = [
	{
		"label": "Learn English",
		"categories": [
			{
				"label": "Vocabulary",
				"description": "Increase your vocabulary skills!",
				"ex_context": "has just reached Yaoundé and is new in the city. \
    				He starts a discussion with an M. Kpihx, an english speaking man, to know the directions to reach Polytech Yaoundé. \
           			He will then have to test his vocabulary skills throught the discussion."
			},
			{
				"label": "Grammar",
				"description": "Increase your grammar skills!",
				"ex_context": "has just reached Yaoundé and is new in the city. \
    				He starts a discussion with an M. Kpihx, an english speaking man, to know the directions to reach Polytech Yaoundé. \
           			He will then have to test his grammar skills throught the discussion."
			}
		],
		"description": "This usecase aims to increases English skills!"
	}
]

NUMB_LEVELS = 10
MAX_NUM_TENT_TEST = 3

class Game:
    def run(self):
        print("Welcome to this game!\n")
        
        user = User(1, 'KpihX', '1')
        
        usecase_datas = USECASES[0]
        usecase = Game.to_usecase(usecase_datas)
        category = usecase.categories[0]
        
        print("Hi " + user.name + "! We are about to start a test in the category '" + category.label + "' of the usecase '" + usecase.label + "'.\n")
        
        gen_test_ai = GenTestAI(user, category)
        
        i = 0
        score = 0
        test_ind =  TestInd.CONT # We help to know if the user want to restart a test or no, or even continue with the next test
        
        while i < NUMB_LEVELS:
            if test_ind == TestInd.CONT:
                num_tent_test = 0
                test = gen_test_ai.gen_next_test()
            elif test_ind == TestInd.REDO:
                num_tent_test += 1
                if num_tent_test > MAX_NUM_TENT_TEST:
                    print("!You have reached the maximum number of tentatives.\n")
                    break
                
                test = gen_test_ai.regen_test()
            else: # test_ind = TestInd.ABAN
                break
            
            if test == None:
                print("!Sorry, we have difficulties to generate a coherent test! Try again later...\n")
                sys.exit(-1)
            
            test_ind, test_score = test.run()
            score += test_score
            
        user.score = score
        user.level = gen_test_ai.test_level
        print(f"Your total score is: '{score}'!\n")
        print(f"Your actual level is: '{user.level}'!\n")
                    
        
    def to_usecase(usecase_datas):
        categories = [Game.to_category(category_datas, None) for category_datas in usecase_datas["categories"]]
        usecase = Usecase(usecase_datas["label"], categories, usecase_datas["description"])
        for category in categories:
            category.usecase = usecase
            
        return usecase

        
    def to_category(category_datas, usecase):
        return Category(category_datas["label"], usecase, category_datas["ex_context"], category_datas["description"])
    
game = Game()

if __name__ == "__main__":
    game.run()