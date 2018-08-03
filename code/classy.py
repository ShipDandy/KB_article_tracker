
import xlsxwriter

 
class Sheets:
    def __init__(self, name, id, spreadsheet):
        self.name = name
        self.id = id
        self.row = 0
        self.column = 0
        self.sheet = spreadsheet.add_worksheet(name)

    def rowPlus(self):
        self.row += 1

    def columnPlus(self):
        self.column += 1

    def resetPosition(self):
        self.row, self.column = 0

    def resetColumn(self):
        self.column = 0




