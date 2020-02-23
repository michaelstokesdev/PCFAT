#python character frequency analysis tool

import matplotlib.pyplot as plt
import sys, re, argparse, json, os
from tkinter import filedialog
from tkinter import *

root = Tk()
root.geometry('375x70')
root.title("Python Character Frequency Analysis Tool")

#if command line arguments are given check them, otherwise run the GUI

def main():
    if len(sys.argv) > 1:
        cliRun()
    else:
        guiRun()
    sys.exit(0)

#command line and gui main functions

def cliRun():
    args = getArgs()
    if args.m != None:
        cipherText = args.m.lower()
    else:
        cipherText = getFileContents(args.i).lower()

    if args.o != None:
        jsonOut(args, cipherText)

    if args.g:
        createGraph(cipherText)
    if args.i != None:
        args.i.close()
    return

def guiRun():
    fileGet = Button(root, text="Select input file", command=guiGetFile)
    fileGet.pack()

    graphRender = Button(root, text="Render graph", command=guiGraph)
    graphRender.pack()

    mainloop()
    return

#gui graph render operation

def guiGraph():
    try:
        cipherText = open(root.filename).read().lower()
    except:
        return
    createGraph(cipherText)
    return

#get command line arguments

def getArgs():
    parser = argparse.ArgumentParser(description="A tool for calculating letter frequencies for a text file", usage="%(prog)s [input file] [output options]")
    parser.add_argument('i', nargs='?', help="Input text file", type=argparse.FileType('r'))
    parser.add_argument('-m', nargs='?', help="Manual text input. Surround sentences with commas or quotation marks")
    parser.add_argument('-o', nargs='?', help="Output percentage values in JSON format (will not overwrite files)", type=argparse.FileType('x'))
    parser.add_argument('-g', help="Display a graph of the letter frequencies", action='store_true', default=False)
    args = parser.parse_args()

    if args.i == None and args.m == None:
        if args.o != None:
            os.remove(os.path.abspath(args.o.name)) #delete output file if invalid arguments given
        print("Please provide an input method")
        sys.exit(0)

    if args.i != None and args.m != None:
        if args.o != None:
            os.remove(os.path.abspath(args.o.name))
        print("Please only provide a single input")
        sys.exit(0)

    if args.m != None and args.m == "":
        if args.o != None:
            os.remove(os.path.abspath(args.o.name))
        print("Please enter a valid string")
        sys.exit(0)

    if args.o == None and not args.g:
        print("Please provide an output method")
        sys.exit(0)

    return args

#file handling

def getFileContents(openedFile):
    fileContents = openedFile.read()
    return fileContents

    #file dialog for gui
def guiGetFile():
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select input file",filetypes = (("txt files","*.txt"),("all files","*.*")) )
    return

    #format json and output to file
def jsonOut(args, cipherText):
    frequencies = getFrequencies(cipherText)
    jsonContent = json.dumps(frequencies)
    args.o.write(jsonContent)
    print("JSON output written to file successfully")
    return

#graph drawing

def createGraph(cipherText):
    if cipherText == None:
        return
    frequencies = getFrequencies(cipherText)
    sortedKeys, sortedVals = sortPercentages(frequencies)
    drawGraph(sortedKeys, sortedVals)
    return

def drawGraph(sortedKeys, sortedVals):
    fig, ax = plt.subplots()
    letters = sortedKeys
    freq = sortedVals
    ax.bar(letters, freq)
    plt.show()
    return

#frequency and percentage functions

def getTotals(cipherText):
    occurances = dict()
    total = 0
    for i in cipherText:
        if i not in occurances:
            occurances[i] = 0
        occurances[i] += 1
        total +=1
    return occurances, total

def getPercentage(occurances, total):
    frequencies = dict()
    for i in occurances:
        percentage = occurances[i]/total*100
        frequencies[i] = percentage
    return frequencies

def sortPercentages(frequencies):
    sorted_x = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    sortedKeys = []
    sortedVals = []

    for i in range(0, len(sorted_x)):
        sortTuple = sorted_x[i]
        sortedKeys.append(sortTuple[0])
        sortedVals.append(sortTuple[1])

    return sortedKeys, sortedVals

def getFrequencies(cipherText):
    cipherText = re.sub("\s","",cipherText)
    occurances, total = getTotals(cipherText)
    frequencies = getPercentage(occurances, total)
    return frequencies

#run main function if file not used as library
if __name__ == '__main__':
    main()