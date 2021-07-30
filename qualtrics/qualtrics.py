import requests
import zipfile
import json
import io
import os
import pandas as pd


class Qualtrics:

    """
    Qualtrics class is used to manage qualtrics API call

    It gathers the survey responses from Qualtrics surveys.

    ...

    Attributes
    ----------
    apiToken : str
        API Token that is required for header authentication
    dataCenter : str
        The datacenter is found in Account Settings, it is part of API hostname
        By default it is fra1 to represent the data center in Europe


    Methods
    -------
    __getRequest(fileFormat, surveyId):
        Creates data export request
        Returns baseUrl, headers, progressId.

    __sendRequest(fileFormat, surveyId):
        Sends the request and checks the data export process
        Returns fileId, url, headers

    downloadSurvey(savePath, fileFormat, surveyId):
        Downloads the survey as file

    getSurvey(fileFormat, surveyId):
        Returns a survey based on the survey id

    getSurveyQuestions(self, fileFormat, surveyId):
        Returns the survey questions
    """

    def __init__(self, apiToken, dataCenter="fra1"):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
           apiToken : str
              API Token that is required for header authentication
           dataCenter : str
              The datacenter is found in Account Settings, it is part of API hostname
              By default it is fra1 to represent the data center in Europe
        """

        self.apiToken = apiToken
        self.dataCenter = dataCenter
        assert len(apiToken) == 40, "It looks like your survey apiToken is an incorrect length."


    def __getRequest(self, fileFormat, surveyId):
        """
        Creates data export request.

        If the arguments are passed, then it construct the base url to communicate with is API.

        Parameters
        ----------
        fileFormat : str
            file format should be either csv, tsv, spss
        surveyId : str
            used to reach the requested survey

        Returns
        -------
        baseUrl, headers, progressId
        """

        progressCheck = 0.0
        progressStatus = "inProgress"
        assert surveyId[:3] == 'SV_', "Your survey id seems incorrect, it should start with SV"
        assert len(surveyId) == 18, "It looks like your survey ID is an incorrect length."
        baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(self.dataCenter, surveyId)
        headers = {
        "content-type": "application/json",
        "x-api-token": self.apiToken,
        }
        if fileFormat in ["csv", "tsv", "spss"]:
            fileFormat = fileFormat
        else:
            print('fileFormat must be either csv, tsv, or spss')
        requestPayload = '{"format":"' + fileFormat + '"}'
        try:
            requestResponse = requests.post(baseUrl, data=requestPayload, headers=headers)
            requestResponse.raise_for_status()
            print("Qualtrics: HTTP Status is " + str(requestResponse.status_code))
            progressId = requestResponse.json()["result"]["progressId"]
            return baseUrl, headers, progressId
        except requests.exceptions.HTTPError as error:
            print(error)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    def __sendRequest(self, fileFormat, surveyId):
        """
        Sends the request and checks the data export process

        If the arguments are passed, then it calls __getRequest.

        Parameters
        ----------
        fileFormat : str
            file format should be either csv, tsv, spss
        surveyId : str
            used to reach the requested survey

        Returns
        -------
        fileId, url, headers
        """

        progressCheck = 0.0
        progressStatus = "inProgress"
        url, headers, progressId  = self.__getRequest(fileFormat=fileFormat, surveyId=surveyId)
        while progressStatus != "complete" and progressStatus != "failed":
            print("progressStatus=", progressStatus)
            checkUrl = url + progressId
            try:
                checkResponse = requests.get(checkUrl, headers=headers)
                checkResponse.raise_for_status()
                checkProgress = checkResponse.json()["result"]["percentComplete"]
                print("Download is " + str(checkProgress) + " complete")
                progressStatus = checkResponse.json()["result"]["status"]
            except requests.exceptions.HTTPError as error:
                print(error)
            except requests.exceptions.ConnectionError as errc:
                print(errc)
            except requests.exceptions.Timeout as errt:
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
        if progressStatus is "failed":
            raise Exception("export failed")

        fileId = checkResponse.json()["result"]["fileId"]
        return fileId, url, headers


    def downloadSurvey(self, savePath, fileFormat, surveyId):
        """
        Downloads the survey as file

        After it downloads, it unzip and saves the file to specified place.

        Parameters
        ----------
        savePath : str
            its a place where to save the downloaded survey file
        fileFormat : str
            file format should be either csv, tsv, spss
        surveyId : str
            used to reach the requested survey

        Returns
        -------
        None
        """

        fileId, url, headers= self.__sendRequest(fileFormat=fileFormat, surveyId=surveyId)
        requestDownloadUrl = url + fileId + '/file'
        try:
            requestDownload = requests.get(requestDownloadUrl, headers=headers, stream=True)
            requestDownload.raise_for_status()
            zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall(savePath)
            print("Qualtrics survey downloading is completed")
        except requests.exceptions.HTTPError as error:
            print(error)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    def getSurvey(self, fileFormat, surveyId):
        """
        Returns a survey as pandas data frame based on the survey id

        If the arguments are passed, then it calls __sendRequest.

        Parameters
        ----------
        fileFormat : str
            file format should be either csv, tsv, spss
        surveyId : str
            used to reach the requested survey

        Returns
        -------
        df
        """

        fileId, url, headers= self.__sendRequest(fileFormat=fileFormat, surveyId=surveyId)
        requestDownloadUrl = url + fileId + '/file'
        try:
            requestDownload = requests.get(requestDownloadUrl, headers=headers, stream=True)
            requestDownload.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(error)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        with zipfile.ZipFile(io.BytesIO(requestDownload.content)) as surveyZip:
            for survey in surveyZip.infolist():
                df = pd.read_csv(surveyZip.open(survey.filename))
                return df


    def getSurveyQuestions(self, fileFormat, surveyId):
        """
        Returns the survey questions

        If the arguments are passed, then it calls __sendRequest.

        Parameters
        ----------
        fileFormat : str
            file format should be either csv, tsv, spss
        surveyId : str
            used to reach the requested survey

        Returns
        -------
        questions
        """

        df = self.getSurvey(fileFormat, surveyId)
        questions = pd.DataFrame(df[:1].T)
        questions.columns = ['Questions']
        questions = questions[17:]
        return questions

