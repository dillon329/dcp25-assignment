from collections import Counter
import os
import re



def search(tunes):
     while True:
            user_title_search_libray = []
            user_title = input("Please enter a title of a tune you want to find \nPress Q to quit\n")
            if user_title.lower() == 'q':
                break
            elif len(user_title) > 0:
                if len(user_title) >= 5:
                    for tune in tunes:
                        if user_title.lower() in tune['title'].lower() or user_title.lower() in tune['alt_title'].lower():
                            user_title_search_libray.append(tune)
                else:
                    for tune in tunes:
                        if tune['title'].lower().startswith(user_title.lower()) or tune['alt_title'].lower().startswith(user_title.lower()):
                            user_title_search_libray.append(tune)
                            
                if user_title_search_libray == []:
                    print(f"Could not find {user_title}")
                else:
                    for number, tune in enumerate(user_title_search_libray, start=1):
                        tune['id'] = number
                        if tune['alt_title'] == '':
                            print(f"{tune['id']}:{tune['title']} is the title ")
                        else:
                            print((f"{tune['id']}:{tune['title']} is the title, also goes by {tune["alt_title"]}"))
                    while True:
                        search_index = input("Please select the index of the title you are searching for and I'll display the information to you\nPress Q to quit")
                        if search_index.lower() == 'q':
                            break
                        elif not search_index.isdigit() or int(search_index) > len(user_title_search_libray) or int(search_index) < len(user_title_search_libray):
                            print("That is not a valid option")
                        else:
                            print(tune[search_index-1])
                        
            else:
                print("That is not valid")

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
    for foldername in os.listdir(folder):
        for filename in os.listdir(folder+"/"+foldername):
            if filename.endswith(".abc"):
                path = os.path.join(folder, foldername, filename)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    tunes.append(cleanFiles(lines))

tunes = []

folder = "abc_books"
                
loadabcFiles(folder)

print(tunes)
#parses the sublists in the tunes list
tunes = [item for sublist in tunes for item in sublist]

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

  
running = False 
 
while running != True:
    search_type = input("Enter 1 to search by the index of the list \nEnter 2 to search by the name\n Press 3 to see tune types \nEnter q to quit")
    if search_type == 'q':
        running = True
    elif not search_type.isdigit():
        print("That is not a valid option")
        print("That is not valid")
    elif int(search_type) == 1:
        while True:
            print(f"\nThere are {len(tunes)} in this database, select a number between 1 and {len(tunes)} and it will show you information about that tune \nPress q to go back to search type")
            database_index = input("")
            if not database_index.isdigit():
                if database_index.lower() == 'q':
                    break
                else:
                    print("That is not a valid entry")
            else:
                index = int(database_index) - 1
                if index > len(tunes) or index < 0:
                    print("That number is not valid")
                else:
                    if tunes[index]['alt_title'] == '':
                        print(f"{tunes[index]['title']} is the title of the track you have slected \nIt is an {tunes[index]['tune']} tune \nIt is written in {tunes[index]['title']} key")
                    else:
                        print(f"{tunes[index]['title']} is the title of the track you have selected\nIt has an alt title of {tunes[index['alt_title']]} \nIt is an {tunes[index]['tune']} tune \n it is written in {tunes[index]['title']} key")
    elif int(search_type) == 2:
        search(tunes)
    elif int(search_type) == 3:
        for tune in tune_list:
            print(tune)  
    else:
        print("That is not valid")
  


print(tunes[1])

"""
checker = []

for tune in tunes:
    checker.append(tune['title'])

counts = Counter(checker)
duplicates = [checker for checker, count in counts.items() if count >= 2]

duplicates = {title: count for title, count in counts.items() if count >= 2}
"""

            


    



