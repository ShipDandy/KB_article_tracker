
import requests
import json

import creds


def getAuthorName(authorId):
    getAuthorUrl = "https://shipstation.zendesk.com/api/v2/users/{}.json".format(authorId)

    authorCall = requests.get(getAuthorUrl, headers=creds.headers)

    return authorCall.json()["user"]["name"]


def getArticleSections():
    getSectionsUrl = "https://shipstation.zendesk.com/api/v2/help_center/sections.json"

    sectionCall = requests.get(getSectionsUrl, headers=creds.headers, params=creds.particulars)

    returnDictionary = {}

    for section in sectionCall.json()["sections"]:
        returnDictionary[section["id"]] = {"name": section["name"], "locale": section["locale"]}

    return returnDictionary


def getArticles(url):
    articleRequest = requests.get(url, headers=creds.headers, params=creds.particulars)

    return articleRequest