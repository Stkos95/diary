import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from tg_bot.config import load_config
import datetime

CREDENTIALS_FILE = "tg_bot\services\credentials1.json"


class SpreadsheetError(Exception):
    pass

class SpreadsheetNotSetError(SpreadsheetError):
    pass

class SheetNotSetError(SpreadsheetError):
    pass


class Table:
    def __init__(self,cred_file):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        self.httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', "v4", http=self.httpAuth)
        self.driveService = None
        self.spreadsheetId = None
        self.sheetId = None
        self.sheetTitle = None
        self.requests = []
        self.valueRanges = []
        self.dictOfSheets = {}
        self.dictOfSpreadsheets = {}



    def create_table(self,title_doc, title_sheet):
        body_to_create = {
            "properties": {
                "title": title_doc,
                "locale": "ru_RU"
            },
            "sheets": [{
                "properties": {
                    "sheetId": 0,
                    "title": title_sheet,
                    "sheetType": "GRID"}
            }]
        }
        create = self.service.spreadsheets().create(body=body_to_create).execute()
        self.spreadsheetId = create["spreadsheetId"]
        self.sheetId = create['sheets'][0]['properties']['sheetId']
        self.sheetTitle = create['sheets'][0]['properties']['title']
        self.dictOfSheets[self.sheetTitle] = self.sheetId
        self.dictOfSpreadsheets[self.spreadsheetId] = title_doc


    def runPreparedRequests(self):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()
        updRes1 = {}
        try:
            if len(self.requests) > 0:
                updRes1 = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                   body={"requests": self.requests}).execute()

        finally:
            self.requests = []

        return updRes1["replies"]



    def addSheetToDoc(self, sheetTitle,rows = 1000, cols= 31):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()
        self.prepare_addSheet(sheetTitle, rows, cols)
        addedSheet = self.runPreparedRequests()[0]['addSheet']['properties']
        self.sheetId = addedSheet["sheetId"]
        self.sheetTitle = addedSheet["title"]
        self.dictOfSheets[addedSheet["title"]] = addedSheet["sheetId"]



    def prepare_addSheet(self, sheetTitle, rows = 1000, cols= 31):
        self.requests.append({"addSheet": {"properties": {"title": sheetTitle, 'gridProperties': {'rowCount': rows, 'columnCount': cols}}}})

    def listOfSheets(self):

        show = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        result = show.get("sheets")
        for sheet in result:
            self.dictOfSheets[sheet['properties']['title']] = sheet['properties']['sheetId']
        return self.dictOfSheets


    def setActiveSheet(self,sheetTitle):
        self.sheetId = self.dictOfSheets["sheetTitle"]
        self.sheetTitle = sheetTitle


    def addDocbyHands(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        id = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()
        self.dictOfSpreadsheets[id["spreadsheetId"]] = id['properties']['title']
        self.sheetId = id["sheets"][0]["properties"]["sheetId"]
        self.sheetTitle = id["sheets"][0]["properties"]["title"]




    def getSheetLink(self):
        if self.spreadsheetId is None:
            raise SpreadsheetNotSetError()
        if self.sheetId is None:
            raise SheetNotSetError()
        return f'https://docs.google.com/spreadsheets/d/{self.spreadsheetId}/edit#gid={str(self.sheetId)}'


    def mergeCells(self,row_start,row_end,col_start,col_end):
        range = self.toGridRange()
        requests = [{
            "mergeCells":{
                "range":range,
                "mergeType":"MERGE_ALL"}}]
        # edit_merge = service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={"requests":}).execute()





    def shareToWritingMode(self,email, spreadsheetId = None):
        driveService = apiclient.discovery.build('drive', 'v3', http=self.httpAuth)
        idToShare = self.spreadsheetId if spreadsheetId == None else spreadsheetId
        shareRes = driveService.permissions().create(
            fileId=idToShare,
            body={'type': 'user', "role": "writer", "emailAddress": email},
            fields="id"
        ).execute()

    def toGridRange(rangeCell: str):
        cellsRange = {}

        start, end = rangeCell.split(":")[0:2]
        rangeAZ = range(ord("A"), ord("Z"))

        if ord(start[0]) in rangeAZ:
            cellsRange["startColumnIndex"] = ord(start[0]) - ord("A")
            start = start[1:]
        if ord(end[0]) in rangeAZ:
            cellsRange["endColumnIndex"] = ord(end[0]) - ord("A") + 1
            end = end[1:]
        if len(start) > 0:
            cellsRange["startRowIndex"] = int(start) - 1
        if len(end) > 0:
            cellsRange["endRowIndex"] = int(end)
        return cellsRange

    def addExercice(self, values, range="A3"):
        self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId, range=range, valueInputOption="USER_ENTERED", body={
            "range": range, # ИСПРАВИТЬ
            "majorDimension": "ROWS",
            "values": values
        }).execute()


    def addTraining(self, values, ranges):
        # self.addExercice(values, ranges)
        getupdate = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                body={
                                                                    "valueInputOption": "USER_ENTERED",
                                                                    "data": [[
                                                                        {
                                                                            "range": ranges,
                                                                            "majorDimension": "ROWS",
                                                                            "values": [[
                                                                                values
                                                                            ]]
                                                                        }
                                                                    ]]
                                                                }).execute()



    def findValueInCell(self,spreadsheetId) ->str:
        my_value = datetime.date.today().day
        ranges = ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1', 'S1',
         'T1', 'U1', 'V1', 'W1', 'X1', 'Y1', 'Z1', 'AA1', 'AB1', 'AC1', 'AD1', 'AE1', 'AF1', 'AG1', 'AH1', 'AI1', 'AJ1',
         'AK1', 'AL1', 'AM1', 'AN1', 'AO1', 'AP1', 'AQ1', 'AR1', 'AS1', 'AT1', 'AU1', 'AV1', 'AW1', 'AX1', 'AY1', 'AZ1']

        getData = self.service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range="B1:AG1").execute().get("values")[0]
        resultDict = dict(zip(ranges,getData))
        for key, value in resultDict.items():
            if str(my_value) == value:
                return key



    def getListOfExercises(self):
        getData = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range="A:A").execute()
        list_of_exercises = getData['values']
        list_with_cells = [i+1 for i in range(len(list_of_exercises))]
        return dict(zip(list_with_cells,list_of_exercises))

    def findCellExercise(self, spreadsheetId):
        getData = self.service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range="A").execute()



