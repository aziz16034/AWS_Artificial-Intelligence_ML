import boto3
import time
import json
import http.client
from pathlib import Path
# from ttttt import fulltext2

conn = http.client.HTTPSConnection("twinword-text-similarity-v1.p.rapidapi.com")



def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName
            }
        })

    return response["JobId"]


def isJobComplete(jobId):
    time.sleep(5)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while (status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def getJobResults(jobId):
    pages = []

    time.sleep(5)

    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)

    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if ('NextToken' in response):
        nextToken = response['NextToken']

    while (nextToken):
        time.sleep(5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if ('NextToken' in response):
            nextToken = response['NextToken']

    return pages


# Document
documentName = "cover-letter-examples.png"
s3BucketName = "caci-search-engine-s3-wlerl7hy6qeu"


jobId = startJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if (isJobComplete(jobId)):
    response = getJobResults(jobId)

# print(response)



# Print detected text
fulltext = ""
for resultPage in response:
    for item in resultPage["Blocks"]:
        if item["BlockType"] == "LINE":
            abc = '\033[94m' + item["Text"] + '\033[0m'
            yz =  item["Text"]
            abc
            # print(abc)
            fulltext += f'{yz} '
            print(fulltext)
            # print(abc)

            # my_string = abc.replace(r"\n", "\t")
            # print(my_string)

# breakpoint()
# payload = f"text2={fulltext}&""text1="f"{fulltext2}.&"
#
# headers = {
#     'content-type': "application/x-www-form-urlencoded",
#     'content-type': "application/x-www-form-urlencoded",
#     'x-rapidapi-key': "558d90a21dmshd88e6ca5b1ffda1p162336jsnf42818f8bd09",
#     'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com"
# }
#
# conn.request("POST", "/similarity/", payload, headers)
#
# res = conn.getresponse()
# data = res.read()
#
# print(data.decode("utf-8"))
#
#

#
comprehend = boto3.client('comprehend')

entities = comprehend.detect_entities(LanguageCode="en", Text=fulltext)
print("\nEntities\n========")
for entity in entities["Entities"]:
    print("{}\t=>\t{}".format(entity["Type"], entity["Text"]))

# Detect KEYPHRASES

print('Calling DetectKeyPhrases')
print(json.dumps(comprehend.detect_key_phrases(Text=fulltext, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectKeyPhrases\n')





