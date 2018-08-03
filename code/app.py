
import datetime
import json
import xlsxwriter
from sys import exit

import classy
import actions
import calls
import creds
import contents


"""Declare Master List and dictionaries"""

mainArticleList = []
authorDb = {}

try:
    sectionDb = calls.getArticleSections()
except Exception:
    print("Problem making list section calls.")


"""Begin article master list building call"""


articlesCallUrl = "https://shipstation.zendesk.com/api/v2/help_center/articles.json"

while True:
    try:
        call = calls.getArticles(articlesCallUrl)
    except Exception:
        print("Issue making call, make sure that you are connected to the internet or that the API credentials are current.")
        exit()

    print("Fetching master article page {}.".format(call.json()["page"]))
    
    for article in call.json()["articles"]:
        mainArticleList.append(article)

        if article["author_id"] not in authorDb:
            authorDb[article["author_id"]] = calls.getAuthorName(article["author_id"])

    if call.json()["next_page"]:
        articlesCallUrl = call.json()["next_page"]
    else:
        break

print("Compiling report.")


"""Move working directory to downloads folder on Mac"""

try:
    actions.moveToDownloads()
except Exception:
    print("There was a problem moving to your Downloads folder.")
    exit()


"""create workbook, master list and draft list counters"""

workbook = xlsxwriter.Workbook("articles-{}.xlsx".format(datetime.date.today()))
authorWorkbook = xlsxwriter.Workbook("authors-{}.xlsx".format(datetime.date.today()))
sectionWorkbook = xlsxwriter.Workbook("sections-{}.xlsx".format(datetime.date.today()))

masterList = classy.Sheets("Master List", 0, workbook)
draftList = classy.Sheets("Drafts", 1, workbook)


"""write column names to default sheets"""
actions.writeHeaders(masterList, contents.primaryHeaders)
actions.writeHeaders(draftList, contents.primaryHeaders)


"""write column names to author and section sheets"""

for author in authorDb:
    authorDb[author] = classy.Sheets(authorDb[author], author, authorWorkbook)
    actions.writeHeaders(authorDb[author], contents.primaryHeaders)

for section in sectionDb:
    sectionDb[section]["sheet"] = classy.Sheets("{}-{}-{}".format(sectionDb[section]["name"][0:10], sectionDb[section]["locale"], str(section)[-5:-1]), sectionDb[section], sectionWorkbook)

    sectionDb[section]["sheet"].sheet.merge_range("A1:E1", "{} | {} | {}".format(sectionDb[section]["name"], sectionDb[section]["locale"], str(section)))

    sectionDb[section]["sheet"].rowPlus()
    
    actions.writeHeaders(sectionDb[section]["sheet"], contents.primaryHeaders)


"""Begin writing of articles"""

for entry in mainArticleList:
    actions.writeToRow(entry, masterList)

    if entry["draft"] == True:
        actions.writeToRow(entry, draftList)

    actions.writeToRow(entry, authorDb[entry["author_id"]])

    actions.writeToRow(entry, sectionDb[entry["section_id"]]["sheet"])

workbook.close()
authorWorkbook.close()
sectionWorkbook.close()

print("Please check your Downloads folder for master, author, and section .xlsx files.")