from collections import Counter
import tkinter as tk
import pandas as pd
import sqlite3




def get_input():
    user_text = entry.get()
    label.config(text=f"You entered:{user_text}")

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



def do_databasse_stuff():
    global df 
    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()
    
    df = pd.read_sql("SELECT * FROM tunes", conn)
    print(df.head())
    conn.close()
do_databasse_stuff()
print(df)

"""
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
"""

def click(type):
    print(f"You clicked the button {type}")
    
    
    
root = tk.Tk()
root.title
root.geometry("800x400")

label = tk.Label(root, text = "Select a mode to search by")
label.pack(pady=10)

button_index = tk.Button(root,
               text = "Index",
               command = lambda: click('id'),
               font = ("Comic Sans",30),
               width=10,   
               height=1 )

button_index.pack()


button_titles = tk.Button(root,
               text = "Titles",
               command = lambda: click('title'),
               font = ("Comic Sans",30),
               width=10,   
               height=1)
button_titles.pack()

button_tune = tk.Button(root,
               text = "Tune",
               command = lambda : click('tune'),
               font = ("Comic Sans",30),
               width=10,   
               height=1)
button_tune.pack()

button_key = tk.Button(root,
               text = "Key",
               command = lambda: click('key'),
               font = ("Comic Sans",30),
               width=10,   
               height=1)
button_key.pack()

button = tk.Button(root, text='Submit', command=get_input)
button.pack(pady=10)




root.mainloop()
  




"""
checker = []

for tune in tunes:
    checker.append(tune['title'])

counts = Counter(checker)
duplicates = [checker for checker, count in counts.items() if count >= 2]

duplicates = {title: count for title, count in counts.items() if count >= 2}
"""

            


    



