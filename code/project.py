from collections import Counter

def loadabcFiles(filename):
    with open(filename, "r", encoding='latin-1') as f:
        lines = f.readlines()  
    return lines


def cleanFiles(lines):
    global tunes 
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
                "id": None,
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
    



tunes = []

files = ['abc_books/2/00.abc',"abc_books/2/01.abc", "abc_books/2/02.abc", "abc_books/2/03.abc",
         "abc_books/2/04.abc", "abc_books/2/05.abc", "abc_books/2/06.abc", "abc_books/2/07.abc",
         "abc_books/2/08.abc", "abc_books/2/09.abc", "abc_books/2/10.abc"]

for file in files:
    file = loadabcFiles(file)
    cleanFiles(file)

#parses the sublists in the tunes list

#checking for dupes in dataset, alter by chatGpt
seen_titles = set()
unique_tunes = []

for tune in tunes:
    title = tune['title']
    if title not in seen_titles:
        seen_titles.add(title)
        unique_tunes.append(tune)

tunes = unique_tunes

#gives ever tune a unique id
for number, tune in enumerate(tunes, start=1):
    tune['id'] = number
i = 1


  
running = False 
 
while running != True:
    search_type = input("Enter 1 to search by the index of the list \nEnter 2 to search by the name \nEnter q to quit")
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
        while True:
            user_title = input("Please enter a title of a tune you want to find \nPress ESC to quit")
            if user_title == '^[':
                break
            
        
    else:
        print("That is not valid")
  




# code to make sure no dupes
"""
checker = []

for tune in tunes:
    checker.append(tune['title'])

counts = Counter(checker)
duplicates = [checker for checker, count in counts.items() if count >= 2]

duplicates = {title: count for title, count in counts.items() if count >= 2}
"""
            


    



