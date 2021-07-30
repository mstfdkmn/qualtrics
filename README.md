# Qualtrics

Qualtrics is an online survey platform that allows one to build surveys, distribute surveys and analyze responses from oneconvenient online location.

This is a simple python tool that can work with the [Qualtrics API](https://www.qualtrics.com/support/integrations/api-integration/using-qualtrics-api-documentation/) to get a survey. To be able to use this tool, you need to have Qualtrics API access right. After that, this tool can be used only for the following aims:

* To download a specified survey,
* To get this survey as pandas data frame
* To get the survey's questions

```python
from qualtrics.qualtrics import Qualtrics

#Instantiate an object of Qualtrics
q1 = Qualtrics('your TOKEN')

q1.downloadSurvey('location that you want to download', 'file type', 'survey id')
q1.getSurvey('file type', 'survey id')

```

If you have a more complex use-case, you can think about this package https://github.com/Jaseibert/QualtricsAPI

## Dependencies

Python3

## Installation

Clone from GitHub
