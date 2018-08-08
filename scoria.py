#!/usr/bin/env python3

# TODO Safety Mechanisms (and code cleanup)

import os
import json
import signal
from subprocess import call

notes = dict()
version = 0.1

notepadfolder = 'notepads'
currentPad = ''
notefolder = 'notes'


def loadJSON(notepadName):
    found = False
    for f in os.listdir(notepadfolder):
        note = dict()
        f = open(notepadfolder + '/' + f, 'r')
        jsonFile = json.load(f)

        if jsonFile['name'] == notepadName:
            found = True
            global currentPad
            currentPad = f.name
            for i in range(len(jsonFile.keys()) - 1):
                note['title'] = jsonFile.get(str(i)).get('title')
                note['category'] = jsonFile.get(str(i)).get('category').lower()

                tags = jsonFile.get(str(i)).get('tags')

                for tag in tags:
                    tag = tag.lower()

                note['tags'] = tags

                notes[note['title']] = note

    if not found:
        print('Invalid notepad')
        exit(1)


def listNoteTitles():
    for noteKey in notes.keys():
        print(noteKey)


def listNoteTitlesInCategory(category):
    for noteKey in notes.keys():
        if notes.get(noteKey)['category'].lower() == category:
            print(noteKey)


def listNoteTitlesWithTag(tag):
    for noteKey in notes.keys():
        if tag in notes.get(noteKey)['tags']:
            print(noteKey)


def listCategories():
    categories = []

    for noteKey in notes.keys():
        category = notes.get(noteKey)['category']
        if category not in categories:
            print(category)
            categories.append(categories)


def listTags():
    allTags = []

    for noteKey in notes.keys():
        currentTags = notes.get(noteKey)['tags']

        for tag in currentTags:
            if tag not in allTags:
                print(tag)
                allTags.append(tag)


def newNote():
    global noteTitle, noteCategory, noteTags
    noteTitle = input('Note name: ').strip()
    noteCategory = input('Note category: ').strip()
    noteTags = input('Note tags (space-separated): ').strip()

    noteTags = noteTags.strip().split()
    updateNotes()


def updateNotes():
    noteDict = dict()
    noteDict[str(len(notes))] = dict()
    noteDict[str(len(notes))]['title'] = noteTitle
    noteDict[str(len(notes))]['category'] = noteCategory
    noteDict[str(len(notes))]['tags'] = noteTags
    f = open(currentPad)

    data = json.load(f)
    f.close()
    data.update(noteDict)
    data.update(notes)
    f = open(currentPad, 'w')
    json.dump(data, f)
    notes[noteDict[str(len(notes))]['title']] = noteDict[str(len(notes))]
    f.close()


def readNote():
    title = input("Note name: ")

    if title in notes.keys():
        print(notes.get(title)['title'] + ':')
        f = open('notes/' + notes.get(title)['title'] + '.txt')
        for line in f.readlines():
            print(line)
        f.close()
    else:
        print('That note doesn\'t exist or the notepad it is in is not loaded.')


def newNotepad():
    notepadName = input('Notepad name: ')
    f = open(notepadfolder + '/' + notepadName + '.json', 'w')
    data = dict()
    data['name'] = notepadName
    json.dump(data, f)
    f.close()


def loadNotepad():
    notepadName = input('Notepad name: ')
    loadJSON(notepadName)


def editNote():
    notetxt = input('Note name: ')
    call(["/bin/nano", notefolder + '/' + notetxt + '.txt'])


def listNotepads():
    notepadNames = os.listdir(notepadfolder)
    i = 0
    for n in notepadNames:
        print(str(i) + ': ' + n)
        i += 1


def renameNotepad():
    global currentPad
    if currentPad is not None:
        newName = input('New name: ')
        os.rename(currentPad, notepadfolder + '/' + newName + '.json')
        currentPad = newName
        f = open(currentPad, 'r')
        padJSON = f.readlines()
        f.writelines(padJSON)
        f.close()


def deleteNote():
    note = input('Note: ')
    if notes[note] is not None:
        notes[note] = None
        os.remove(notefolder + '/' + note + '.txt')
    else:
        print("Note doesn't exist!")


def deleteNotepad():
    global currentPad
    os.remove(currentPad)
    currentPad = ''


def moveNote():
    global currentPad, notes
    noteToMove = input('Note: ')
    newNotepad = input('New Notepad: ')
    found = False
    note = notes[noteToMove]

    for f in os.listdir(notepadfolder):
        f = open(notepadfolder + '/' + f, 'r')
        data = json.load(f)

        if data.get('name').lower() == newNotepad.lower():
            found = True
            data[str(len(data.keys()) - 1)] = note
            f = open(f.name, 'w')
            json.dump(data, f)
    if found:
        notes['name'] = currentPad.split('/')[-1].replace('.json', '', 1)
        del notes[noteToMove]
        f = open(currentPad, 'w')
        json.dump(notes, f)
        del notes['name']
    else:
        print('Invalid new notepad')
        exit(1)


def parse(string):
    edited = string.lower().strip()
    if string == 'new note':
        newNote()
    elif string == 'new notepad':
        newNotepad()
    elif string == 'load notepad':
        loadNotepad()
    elif edited.startswith('read note'):
        readNote()
    elif edited == 'list notes':
        listNoteTitles()
    elif edited == 'list notepads':
        listNotepads()
    elif edited == 'edit note':
        editNote()
    elif edited == 'rename notepad':
        renameNotepad()
    elif edited == 'delete note':
        deleteNote()
    elif edited == 'delete notepad':
        deleteNotepad()
    elif edited == 'move note':
        moveNote()
    elif edited.startswith('list notes in category '):
        listNoteTitlesInCategory(string.strip().split()[-1])
    elif edited.startswith('list notes with tag '):
        listNoteTitlesWithTag(string.strip().split()[-1])
    elif edited == 'exit' or edited == 'quit':
        exit(0)
    else:
        print('Unknown command!')

def clean_exit(a, b):
    global orig_sigint
    signal.signal(signal.SIGINT, orig_sigint)
    
    print()
    exit(0)

def launch_scoria():
    global orig_sigint
    orig_sigint = signal.getsignal(signal.SIGINT)

    signal.signal(signal.SIGINT, clean_exit)
    print('Scoria Version ' + str(version))
    print()
    print("By Benjamin O'Neill")
    print()
    print()

    while True:
        parse(input("> "))
    
    clean_exit(0, 0)

if __name__ == '__main__':
    launch_scoria()
