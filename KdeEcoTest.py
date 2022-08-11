import re
import argparse
import os
from pynput.mouse import Listener
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key
from xdo import Xdo
import time
import signal
from datetime import datetime as dt
import os.path
from dataclasses import dataclass

windowDefined = False
writeMousePosToFile = False
testIsRunning = True
windowResized = False
writeLineToFunctionsDict = False
commentActionStr = ""

#declare the dictionnary where the functions will be stored
functionsDict = {}
global functionDict
mainArray = []

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key))
        if key == Key.f1:
            global testIsRunning
            if testIsRunning == True:
                testIsRunning = False
                print("The testing program is on pause.")
            else:
                testIsRunning = True
                print("The testing program is running.")
        if key == Key.f2:
            print("Program aborted.")
            os.kill(os.getpid(), signal.SIGTERM)

    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def writeToLog(logFileName, logStr):
    file1 = open(logFileName, 'a')
    file1.write(logStr)
    file1.write("\n")
    file1.close()


def defineWindow():
    ## get application origin coordinates
    global xdo
    xdo = Xdo()
    global win_id
    win_id = xdo.select_window_with_click()

    global win_location
    win_location = xdo.get_window_location(win_id)
    print(win_location.x)

    print(win_location.y)
    global windowDefined
    windowDefined = True

    global win_size
    win_size = xdo.get_window_size(win_id)
    print(win_size.width)
    print(win_size.height)


def executeFunction(functionNameStr):
    #print(functionsDict)
    if functionNameStr not in functionsDict:
        print("The function {} has not been defined.".format(functionNameStr))
    else:
        for line in functionsDict[functionNameStr]:
            print(line.lineStr)
            readAndExecuteAction(line)

def readAndExecuteAction(line):


        if line.lineStr:
            commentTestStr = line.lineStr.strip()
            if len(commentTestStr) > 0:
                if commentTestStr[0] == "#":
                    global commentActionStr
                    commentActionStr = commentTestStr
                    return


        strMatch = re.search('click (-?\d*),(-?\d*)',line.lineStr.lower())
        if strMatch:
            x = strMatch.group(1)
            y = strMatch.group(2)
            xdo.move_mouse(win_location.x + int(x), win_location.y + int(y))
            xdo.click_window(win_id, 1)

        strMatch = re.search('scrolldown',line.lineStr.lower())
        if strMatch:
            print("test scrolldown")
            os.system('xdotool click 5')

        strMatch = re.search('scrollup',line.lineStr.lower())
        if strMatch:
            print("test scrollup")
            os.system('xdotool click 4')

        strMatch = re.search('sleep ([\d\.]*)',line.lineStr.lower())
        if strMatch:
            sleep_time = strMatch.group(1)
            time.sleep(float(sleep_time))

        strMatch = re.search('write "([^\"]*)",(\d*),(\d*)',line.lineStr.lower())
        if strMatch:
            stringToWriteToScreen = strMatch.group(1)
            string_x = strMatch.group(2)
            string_y = strMatch.group(3)
            xdo.move_mouse(win_location.x + int(string_x), win_location.x + int(string_y))

            xdo.focus_window(win_id)
            #xdo.wait_for_window_focus(win_id, 1)
            os.system('xdotool type --window {0} --delay [500] \"{1}\" '.format(win_id,stringToWriteToScreen))

        strMatch = re.search('moveWindowToOriginalLocation (\d*),(\d*)',line.lineStr)
        if strMatch:
            print("Move tested window to original location.")
            origWin_x = strMatch.group(1)
            origWin_y = strMatch.group(2)
            os.system('xdotool windowmove {0} {1} {2}'.format(win_id,origWin_x,origWin_y))
            #xdo.move_window(win_id, origWin_x, origWin_y)

        strMatch = re.search('setWindowToOriginalSize (\d*),(\d*)',line.lineStr)
        if strMatch:
            print("Set tested window to original size.")
            origWin_width = strMatch.group(1)
            origWin_height = strMatch.group(2)
            os.system('xdotool windowsize {0} {1} {2}'.format(win_id,origWin_width,origWin_height))
            global windowResized
            windowResized = True


        strMatch = re.search('key (.*)',line.lineStr)
        if strMatch:
            print("Send key.")
            keyStr = strMatch.group(1)
            print(keyStr)
            os.system('xdotool key {0}'.format(keyStr))

        strMatch = re.search('writeTimestampToLog "([^\"]*)"',line.lineStr)
        if strMatch:
            print("Write timestamp to log.")
            now = dt.now()
            timestampStr = now.strftime("%a %m %y")
            print('Timestamp:', timestampStr)
            f2 = open(outputFilename, 'a')
            f2.write("# Write message to the log.\n")
            f2.write("writeMessageToLog \"" + textInput + "\"\n")
            f2.write("\n")
            f2.close()

        strMatch = re.search('execFunction ([\w_]*$)',line.lineStr)
        if strMatch:
            functionNameStr = strMatch.group(1)
            print("Execute function {}".format(functionNameStr))
            executeFunction(functionNameStr)



        lineStr = "Line{:0>3d}; {}".format(line.lineIndex, line.lineStr.strip())
        print(lineStr)
        commentActionStr = commentActionStr.lstrip('#')
        if line.lineStr.strip() != "":
            now = dt.now()
            writeToLog(testLogFilename,now.strftime("%Y-%m-%d_%H-%M-%S " + ";" + lineStr + ";" + commentActionStr))
            commentActionStr = ' '




#get input arguments
parser = argparse.ArgumentParser()
parser.add_argument("--inputFilename", required=True, help = "Test script to be used with KdeEcoTest.")
parser.add_argument("--testLogFilename", required=False, help = "Test log filename")
args = parser.parse_args()
intputFilename = args.inputFilename

#get log filename, create a default one if none provided
now = dt.now()
testLogFilename = "KdeEcoLogFile_" + now.strftime("%Y-%m-%d_%H-%M-%S")
print(testLogFilename)
if args.testLogFilename is not None:
    testLogFilename = args.testLogFilename


#Test if intputFilename exists
if os.path.exists(intputFilename) == False:
    print("Input filename {0} has not been found.".format(intputFilename))
    os.kill(os.getpid(), signal.SIGTERM)

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

#get the location and size of the application to test
print("Click on the application you want to test.")
defineWindow()

#read KdeEcoTest input file line by line, output result in mainArray and functionsDict
class Line:
    lineIndex: int
    lineStr: str

file1 = open(intputFilename, "r")
lines = file1.readlines()
file1.close()

functionName = ""
lineIndex = 1
for lineStr in lines:
    line = Line()
    line.lineStr = lineStr
    line.lineIndex = lineIndex
    lineIndex = lineIndex + 1

    # add functions code to dictionnary functionsDict
    isFunctionDefinitionLine = False
    strMatch = re.search('^function ([\w_]*$)',line.lineStr)
    if strMatch:
        isFunctionDefinitionLine = True
        writeLineToFunctionsDict = True
        functionName = strMatch.group(1)
        functionsDict[functionName] = []
    else:
        isFunctionDefinitionLine = False

    strMatch = re.search('^end$',line.lineStr.lower())
    if strMatch:
        writeLineToFunctionsDict = False

    if writeLineToFunctionsDict == True and isFunctionDefinitionLine == False:
        if line.lineStr.find('repeatFunction') != -1:
            print("The current version of KdeEcoTest does not support use of repeatFunction within a function.")
            print("Program aborted.")
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            functionsDict[functionName].append(line)

    # add main code to mainArray
    if writeLineToFunctionsDict == False and strMatch == None:
        mainArray.append(line)


#read mainArray and functionsDict to execute the test
for line in mainArray:
    if testIsRunning == True:

        strMatch = re.search('repeatFunction ([^\"]*),(\d*)',line.lineStr)
        if strMatch:
            functionNameStr = strMatch.group(1)
            nbOfRepetition = strMatch.group(2)
            print("Execute function {0} {1} times.".format(functionNameStr, nbOfRepetition))
            for i in range(int(nbOfRepetition)):
                executeFunction(functionNameStr)

        readAndExecuteAction(line)


#display warning if the tested app window has not been tested
print(windowResized)
if windowResized == False:
    print("The tested window app has not been resized, this could result in test errors.")
