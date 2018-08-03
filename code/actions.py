
import os
import re
import xlsxwriter


"""navigate to Downloads folder on Mac"""

def moveToDownloads():
    initialD = os.getcwd()
    rootRegex = re.compile(r"(/Users/.+?)/.+")
    rootDir = rootRegex.search(initialD)
    os.chdir(rootDir.group(1) + "/Downloads")


"""check if labels exist in entry"""

def populateLabelNames(labelArray):
    if len(labelArray) > 0:
        labelString = ""
        for each in labelArray:
            labelString += "{}, ".format(each)

        return labelString.rstrip(", ")
    else:
        return "None"


"""search body for image tags and extract urls if needed"""

def imageSearch(body):
    looker = re.compile('<img.+?src="(.+?)".+?>')
    imageList = looker.findall(body)

    if len(imageList) == 0:
        return "None"
    else:
        return str(imageList)

"""prepares a new sheet's column names based on desired group"""

def writeHeaders(freshSheet, headers):
    for columnName in headers:
        freshSheet.sheet.write(freshSheet.row, freshSheet.column, columnName)

        freshSheet.columnPlus()

    return freshSheet

"""write entry to specified worksheet"""

def writeToRow(entry, worksheet):
    worksheet.rowPlus()

    worksheet.sheet.write(worksheet.row, 0, str(entry["id"]))
    worksheet.sheet.write(worksheet.row, 1, entry["title"])
    worksheet.sheet.write(worksheet.row, 2, entry["locale"])
    worksheet.sheet.write(worksheet.row, 3, str(entry["author_id"]))
    worksheet.sheet.write(worksheet.row, 4, populateLabelNames(entry["label_names"]))
    worksheet.sheet.write(worksheet.row, 5, entry["draft"])
    worksheet.sheet.write(worksheet.row, 6, entry["promoted"])
    worksheet.sheet.write(worksheet.row, 7, str(entry["section_id"]))
    worksheet.sheet.write(worksheet.row, 8, entry["position"])
    worksheet.sheet.write(worksheet.row, 9, entry["created_at"])
    worksheet.sheet.write(worksheet.row, 10, entry["edited_at"])
    worksheet.sheet.write(worksheet.row, 11, entry["updated_at"])
    worksheet.sheet.write(worksheet.row, 12, imageSearch(str(entry["body"])))
    worksheet.sheet.write(worksheet.row, 13, entry["url"])