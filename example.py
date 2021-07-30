from qualtrics.qualtrics import Qualtrics


if __name__== "__main__":

    #Instantiate an object of Qualtrics
    q1 = Qualtrics('wLTE7XV43hXuZV4lPQsEJlPvNoykiQ7dBGkoHVTw')
    
    #Download a survey as csv file to the location that you specified
    #q1.downloadSurvey('your path', 'csv', 'your survey id')

    #Get the survey that you want as a data frame
    #print(q1.getSurvey('csv', 'your survey id'))

    #Get the survey's questions
    print(q1.getSurveyQuestions('csv', 'your survey id'))

