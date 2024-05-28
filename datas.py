"""Test Datas"""

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
NUM_QUESTIONS = 5
QCM = "qcm"
QRO = "qro"
MAX_NUM_TENT_TEST = 3

""" * QCM Datas"""

NUM_QCM_PROPS = 3
QCM_FORMAT = f"question1*answer1*..*answer{NUM_QCM_PROPS}+question2*answer1*..*answer{NUM_QCM_PROPS}+...+question{NUM_QUESTIONS}*answer1*..*answer{NUM_QCM_PROPS}"
QCM_EX = "Which transport mean we you usually use in a city ?*Bus*Train*Car+You know Yaoundé a a big city with frequent trafficjams; Can you explain what'is a trafficjam ?*A type of delicious fruit preserve made in Yaoundé*A situation where a large number of vehicles are stuck in congestion on the road*A public celebration that takes place on the streets of Yaoundé"
