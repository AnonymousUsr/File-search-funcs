from pathlib import Path
import os
import shutil

#Depending on input given, adds either files in a directory or files in a directory and all 
#subdirectories to a list in mainFunc()
def getDir(direction: str, directory: Path, allFiles: list) -> None:
#direction - letter that tells the function what the user wants to happen
#directory - directory the function takes the files from
#allFiles - list that contains all files taken from directory
    #Adds all files in a directory
    if (directory.is_dir() == True):
        if direction == "D":
            allFiles2 = directory.iterdir()
            for file in sorted(allFiles2):
                if file.is_dir() == False:
                    allFiles.append(file)
                    print(file)
        #Adds all files in the directory and all subdirectories
        elif direction == "R":
            allFiles2 = directory.iterdir()
            allFiles3 = directory.iterdir()
            for item in sorted(allFiles2):    
                if os.path.isfile(item) == True:
                    allFiles.append(item)
                    print(item)
            for moreItems in sorted(allFiles3):
                if moreItems.is_dir():
                    sorted(list(str(item)))
                    getDir(direction, moreItems, allFiles)
        else:
            print("ERROR")
    else:
        print('ERROR')

#Using files from getDir(), depending on input marks certain files as interesting
def searchFiles(letter: str, filestoMatch: list, allFiles: list) -> list:
#letter - letter that tells the function what the user wants to happen
#filestoMatch - things used to filter out what files should be marked interesting
#allFiles - list of possible files to be marked interesting
    interestingFiles = []
    #Marks all files given as interesting
    if letter[0] == "A":
        for file in allFiles:
            interestingFiles.append(file)
        if (interestingFiles == []):
            return ['NOTHING']
    #Marks all files that match a given name as interesting
    elif letter[0] == "N":
        for file in filestoMatch:
            for currentFile in allFiles:
                if file == Path(currentFile).name:
                    interestingFiles.append(currentFile)
        if (interestingFiles == [] and (not filestoMatch[0].startswith('.')) and ('.' in filestoMatch[0])):
            return ['NOTHING']
    #Marks all files that end in a given suffix as interesting
    elif letter[0] == 'E':
        for file in allFiles:
            for otherFile in filestoMatch:
                if file.suffix == otherFile:
                    if file not in interestingFiles:
                            interestingFiles.append(file)
        if (interestingFiles == [] and str(filestoMatch[0]).startswith('.')):
            return ['NOTHING']
    #Marks all files that contain certain words as interesting
    elif letter[0] == 'T':
        combined = ' '.join(filestoMatch)
        for file in allFiles:
            try:
                openedFile = open(file)
                line = openedFile.readlines()
                for words in line:
                    if combined in words:
                        if file not in interestingFiles:
                            interestingFiles.append(file)
            except:
                openedFile.close
        if (interestingFiles == []):
            return ['NOTHING']
    #Marks all files less than a given size as interesting
    elif letter[0] == '<':
        for file in allFiles:
            if (os.path.getsize(file) < int(filestoMatch[0])) and (os.path.getsize(file) > 0):
                if file not in interestingFiles:
                    interestingFiles.append(file)
        if (len(interestingFiles) == 0):
            return ['NOTHING']
    #Marks all files greater than a given size as interesting
    elif letter[0] == '>':
        for file in allFiles:
            if os.path.getsize(file) > int(filestoMatch[0]):
                if file not in interestingFiles:
                    interestingFiles.append(file)
        if (interestingFiles == []):
            return ['NOTHING']
    return interestingFiles

#Perform an action on files marked interesting
def fileAction(letter: str, interestingFiles: list) -> str:
#letter - letter that tells the function what the user wants to happen
#interestingFiles - list of files meant to be affected
    #Reads the first line of all interesting files
    if letter == 'F':
        for file in interestingFiles:
            try:
                openedFile = open(file)
                line = openedFile.readline()
                print(line, end = '')
            except:
                openedFile.close
                print('NOT TEXT', end = '')
        return 'ended'
    #Creates a duplicate of all interesting files
    if letter == 'D':
        for file in interestingFiles:
            try:
                dupFile = shutil.copyfile(Path(file).absolute(), Path(file).parent / (Path(file).name + '.dup'))
            except:
                print('Cannot duplicate', file)
        return 'ended'
    #Modifies time of all interesting files to the most recent time
    if letter == 'T':
        for file in interestingFiles:
            os.utime(file, None)
        return 'ended'
    else:
        print('ERROR')

#Calls the three functions above according to input
def mainFunc() -> None:
    allFiles = []
    #Runs until (a) file(s) are taken from a directory
    while True:
        dirInput = input("")
        splitDir = dirInput.split(' ', -1)
        if (len(splitDir) > 1) and (len(splitDir[0]) == 1)  and (splitDir[1]):
            getDir(splitDir[0], Path(splitDir[1]), allFiles)
        else:
            print('ERROR')
        if allFiles:
            break
    
    #Runs either file(s) are marked interesting or no files are found to be interesting
    interestingFiles = []
    while True :
        fileInput = input('')
        splitFiles = fileInput.split(' ', -1)
        if (len(splitFiles) > 1) or (str(splitFiles[0])) == 'A':
            interestingFiles = searchFiles(splitFiles[0], splitFiles[1:], allFiles)
        if interestingFiles and interestingFiles != ['NOTHING']:
            for file in interestingFiles:
                print(Path(file).absolute())
            break
        elif interestingFiles != ['NOTHING']: 
            print('ERROR')
        if interestingFiles == ['NOTHING']:
            break
    
    #Runs until the interesting files are used in some way
    while True and interestingFiles != ['NOTHING']:
        endOrNot = ''
        actionInput = input("")
        if len(actionInput) < 2:
            endOrNot = fileAction(actionInput, interestingFiles)
        if endOrNot:
            break

#If project1.py is being run as a script and not imported then start 
if __name__ == '__main__':
    mainFunc()