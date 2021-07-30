""" Tests of Qualtrics object
For this purpose, the 'Prace info and social' survey and
"fra1" datacenter id for Ku Leuven are used.
"""


from qualtrics.qualtrics import Qualtrics
import pandas as pd
import os


def test_getSurvey():
    q = Qualtrics('TOKEN')
    #assert q.getSurvey('csv', 'SV_b8xdruuWYk0EQUB').empty == False, "Data Frame is not empty"
    assert len(q.getSurvey('csv', 'your survey id').columns) == 19, "should be 19"


def test_downloadSurvey():
    q = Qualtrics('TOKEN')
    if os.path.exists('yourPath.csv') == True:
        os.remove('yourPath.csv')
    q.downloadSurvey('yourPath.csv', 'csv', 'your survey id')
    assert os.path.exists('yourPath.csv') == True,\
                          "the csv file should exist"


def test_getSurveyQuestions():
    q = Qualtrics('TOKEN')
    assert len(q.getSurveyQuestions('csv', 'your survey id')) == 2, "For now there are only two questions"


if __name__ == '__main__':

    test_downloadSurvey()
    test_getSurvey()
    test_getSurveyQuestions()
    print("Everything passed")
