from classes import User, Usecase, Category, Test, Question
from gen_test_ai import GenTestAI
from datas import USECASES, NUMB_LEVELS

class Game:
    def run(self):
        print("Welcome to this game!\n")
        
        user = User(1, 'KpihX', '1')
        
        usecase_datas = USECASES[0]
        usecase = Game.to_usecase(usecase_datas)
        category = usecase.categories[0]
        
        print("Hi " + user.name + "! We are about to start a test in the category " + category.label + " of the usecase " + usecase.label + ".\n")
        
        gen_ai = GenTestAI(user, category)
        
        for i in range(1, 4):
            context, qcms = gen_ai.gen_next_test()
        
            print(f"*Test {i}\n")
            print(context, end = "\n\n")
            print(qcms, end = "\n\n")
        
    def to_usecase(usecase_datas):
        categories = [Game.to_category(category_datas, None) for category_datas in usecase_datas["categories"]]
        usecase = Usecase(usecase_datas["label"], categories, usecase_datas["description"])
        for category in categories:
            category.usecase = usecase
            
        return usecase

        
    def to_category(category_datas, usecase):
        return Category(category_datas["label"], usecase, category_datas["ex_context"], category_datas["description"])
    
game = Game()

game.run()