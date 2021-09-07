import boto3
import time
import json
import http.client
from pathlib import Path


conn = http.client.HTTPSConnection("twinword-text-similarity-v1.p.rapidapi.com")



def startJob2(s3BucketName, objectName2):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': objectName2
            }
        })

    return response["JobId"]


def isJobComplete2(jobId):
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


def getJobResults2(jobId):
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
documentName2 = "Attachment 1 - DSS 2.0 SOW - 4-13-2020 - Final.pdf"
s3BucketName = "caci-search-engine-s3-wlerl7hy6qeu"


jobId2 = startJob2(s3BucketName, documentName2)
print("Started job with id: {}".format(jobId2))
if (isJobComplete2(jobId2)):
    response2 = getJobResults2(jobId2)

# print(response)



# Print detected text
fulltext2 = ""
for resultPage2 in response2:
    for item2 in resultPage2["Blocks"]:
        if item2["BlockType"] == "LINE":
            abc2 = '\033[94m' + item2["Text"] + '\033[0m'
            yz2 =  item2["Text"]
            abc2
            # print(abc)
            fulltext2 += f'{yz2} '
            # print(fulltext2)

            # my_string = abc.replace(r"\n", "\t")
            # print(my_string)
# payload = f"text2={fulltext2}&""text1="f"{fulltext}.&"

# breakpoint()

# headers = {
#     'content-type': "application/x-www-form-urlencoded",
#     'content-type': "application/x-www-form-urlencoded",
#     'x-rapidapi-key': "558d90a21dmshd88e6ca5b1ffda1p162336jsnf42818f8bd09",
#     'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com"
# }
#
# conn.request("POST", "/similarity/", payload, headers)
#
# res2 = conn.getresponse()
# data2 = res2.read()
#
# print(data2.decode("utf-8"))

#
# comprehend = boto3.client('comprehend')
#
# entities = comprehend.detect_entities(LanguageCode="en", Text=yz)
# print("\nEntities\n========")
# for entity in entities["Entities"]:
#     print("{}\t=>\t{}".format(entity["Type"], entity["Text"]))

# Detect entities




