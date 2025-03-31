import os
import json
import datetime
import yfinance as yf
import shutil

symbolJSONFilePath = "./python/stock-prices/stockSymbols.json"
STOCKSYMBOLINDEX = 0
STOCKPRECISION = 3
THREEDECIMALPOINTFORMAT = "{:.3f}"

def getSymbol(symbol):
    return symbol.split(".")[STOCKSYMBOLINDEX]

def getCurrentPrice(ticker):
    return THREEDECIMALPOINTFORMAT.format(ticker.fast_info['lastPrice'])

def getCurrentTime():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def getTickerObject(symbol):
    return yf.Ticker(symbol)

def checkFolderExists(key):
    keyFolderFilePath = "./python/stock-prices/" + key 
    if not os.path.exists(keyFolderFilePath):
        os.makedirs(keyFolderFilePath)

def createSymbolDailyPriceFile(key, symbol):
    filePath = "./python/stock-prices/" + key + "/" + getSymbol(symbol) + "DailyPrices.txt"
    appendWrite = "a+" if os.path.exists(filePath) == True else "w"
    with open(filePath, appendWrite) as file:
            if appendWrite == "w":
                file.write("%-25s %-20s\n" % ("Date/Time", "Current price"))
            file.write("%-25s %-20s\n" % (getCurrentTime(), getCurrentPrice(getTickerObject(symbol))))

def loadJSONData(JSONFilePath):
    with open(JSONFilePath, 'r')  as jsonFile:
        data = json.load(jsonFile)

    for key, value in data.items():
        for symbol in value:
            checkFolderExists(key)
            createSymbolDailyPriceFile(key, symbol)

# ONLY USE THIS IF YOU WANT TO CLEAN UP THE FOLDERS OTHERWISE DON'T USE THIS METHOD
def deleteAllFolders(JSONFilePath):
    with open(JSONFilePath, 'r')  as jsonFile:
        data = json.load(jsonFile)

    for key, value in data.items():
        keyFolderFilePath = "./python/stock-prices/" + key 
        if os.path.exists(keyFolderFilePath):
            shutil.rmtree(keyFolderFilePath)

def startProgram():
    if os.path.exists(symbolJSONFilePath):
        loadJSONData(symbolJSONFilePath) 
    else:
        print("JSON file path not found. Please try again.")

startProgram()

# deleteAllFolders(symbolJSONFilePath)
