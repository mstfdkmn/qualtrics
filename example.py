from qualtrics.qualtrics import Qualtrics


if __name__== "__main__":

    #Instantiate an object of Qualtrics
    q1 = Qualtrics('TOKEN')

    #Download a survey as csv file to the location that you specified
    q1.downloadSurvey('your path', 'csv', 'yourPath.csv')

    #Get the survey that you want as a data frame
    #print(q1.getSurvey('csv', 'yourPath.csv'))

    #Get the survey's questions
    #print(q1.getSurveyQuestion('csv', 'yourPath.csv'))

