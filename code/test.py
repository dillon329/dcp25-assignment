# Starter code to load in the files into a sql database




import os 
import sqlite3
import pandas as pd
import mysql.connector
# sqlite for connecting to sqlite databases


def cleanFiles(lines):
    current_tune_lines = {
                "id": None,
                "title": None,
                "alt_title": '',
                "tune": None,
                "Key": None,
                
            }
    tunes = []
    #not all lines end with the same line, thus i added this to make it so that after the for loop has passed through once
    #that it would append when it comes up on a new X:, and for the last set just to append it when the for loop is finished
    pass_through_1 = False
    for line in lines:
        
        # Check if this starts a new tune
        line = line.strip()
        if line =='X: 228':
            pass
        if line.startswith("X:"):
            if pass_through_1 != False:
                tunes.append(current_tune_lines.copy())
                
            current_tune_lines = {
                "id": int(line[2:]),
                "title": None,
                "alt_title": '',
                "tune": None,
                "Key": None,
                
            }
            title_check = False
            pass_through_1 = True

        elif line.startswith("T:"):
            title = line[2:].strip()
            if not title_check:
                current_tune_lines['title'] = title
                title_check = True
            else:
                current_tune_lines['alt_title'] = title

        elif line.startswith("R:"):
            current_tune_lines['tune'] = line[2:].strip()
            
        elif line.startswith("K:"):
            current_tune_lines['Key'] = line[2:].strip()
    tunes.append(current_tune_lines.copy())
    return tunes


def loadabcFiles(folder):
    global tunes 
    #goes thorugh each abc file in the abc_books folder
    for foldername in os.listdir(folder):
        for filename in os.listdir(folder+"/"+foldername):
            if filename.endswith(".abc"):
                path = os.path.join(folder, foldername, filename)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    #prarses the line into a list
                    tunes.append(cleanFiles(lines))


def do_databasse_stuff():
    global tunes

    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS tunes (id INTEGER, title TEXT, alt_title TEXT, tune TEXT, key TEXT)')

    # Insert data
    for row in tunes:
        cursor.execute('INSERT INTO tunes (id, title, alt_title, tune, key) VALUES (?, ?, ?, ?, ?)', (row['id'], row['title'],row['alt_title'],row['tune'],row['Key']))

    # Save changes
    conn.commit()

    cursor.execute('SELECT * FROM tunes')
    

    # Get all results
    results = cursor.fetchall()

    # Print results
    for row in results:
        print(row)    
        print(row[0])
        print(row[4])
    # Close
    
    conn.close()

    
    



tunes = []

folder = "abc_books"
                
loadabcFiles(folder)

print(tunes)
#parses the sublists in the tunes list
tunes = [item for sublist in tunes for item in sublist]

#deletes tunes that dont have a title or id because could just be a bug in the dode
for i in range(len(tunes)):
    if tunes[i]['id'] == None or tunes[i]['title'] == None:
        del tunes[i]


#checking for dupes in dataset, alter by chatGpt
seen_titles = set()
unique_tunes = []

for tune in tunes:
    title = tune['title']
    if title not in seen_titles:
        seen_titles.add(title)
        unique_tunes.append(tune)

tunes = unique_tunes
tune_list = []

#gives ever tune a unique id
for number, tune in enumerate(tunes, start=1):
    tune['id'] = number
    tune_list.append(tune['tune']) 
i = 1

print(tunes)
tune_list = set(tune_list) 
do_databasse_stuff()