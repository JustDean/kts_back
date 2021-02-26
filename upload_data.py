import pandas as pd
import numpy as np
import requests

URL = 'https://geo-quiz-bot.herokuapp.com/api'

data = pd.read_csv('./quiz.csv')


for i in range(data.shape[0]):
    question = data.iloc[i, 0]
    answer = data.iloc[i, 1]
    points = data.iloc[i, 2]

    send = requests.post(f'{URL}/quiz.post', params={'question': question, 
                                                      'answer': answer, 
                                                      'points':points})
