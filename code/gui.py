from collections import Counter

import tkinter as tk
from tkinter import ttk

import pandas as pd
import sqlite3

#code to work tkinter as a gui


id_search_results = None
search_tttt = None
str_search =None


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

def build_table(values):
    global table_frame

    if table_frame is not None:
        table_frame.destroy()

    table_frame = tk.Frame(page_search)
    table_frame.pack(fill="both", expand=True)

    columns = ('id', 'title', 'alt_title', 'tune', 'key','book')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

    for col in columns:
        tree.heading(col, text=col)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    

   
    for row in values:
        tree.insert("", tk.END, values=row) 

    return tree
    


def search_query(column_name, looking_For):
    #made it global so no error on first go around, it deletes each time a new input is made
    global str_search
    if str_search is not None:
        str_search.destroy()
    results = []
    alt_title_checker = (column_name == 'title')

    for index, row in df.iterrows():
        match = False

        value = str(row[column_name])
        alt   = str(row['alt_title'])

        if len(looking_For) >3 :
            # contains reson why is that i feel as if words are 4 or more characters wrong they are searching for a certain word 
            if looking_For.lower() in value.lower():
                match = True
            if alt_title_checker and looking_For.lower() in alt.lower() and alt != 'None':
                match = True
        else:
            # startswith for 3 or less word as i feel that thats when people are wondering the begining of a song
            if value.lower().startswith(looking_For.lower()):
                match = True
            if alt_title_checker and alt.lower().startswith(looking_For.lower()) and alt != 'None':
                match = True

        if match:
            results.append([
                row['id'],
                row['title'],
                row['alt_title'],
                row['tune'],
                row['key'],
                row['book']
            ])

    # shows results if they are found if not says no matches found
    if results:
        str_search = build_table(results)
    else:
        str_search = tk.Label(page_search, text="No matches found")
        str_search.pack()
                    
        
    
def search_query_id(query):
    global id_search_results
    store_results = []
    values = []
    row = df[df["id"] == int(query)]

    # you *can* skip this if you're 100% sure ids are 1..len(df)
    if row.empty:
        tk.Label(page_search, text="No tune found with that ID").pack()
        return

    values = [row[col].iloc[0] for col in row.columns]
    store_results.append(values)
    id_search_results = build_table(store_results)
    
    
    
        
    
def get_input_search(type,entry_widget):
    global search_tttt
    global df

    if search_tttt is not None:
        search_tttt.destroy()
    query = entry_widget.get()
    if type == 'id':
        if id_search_results is not None:
            id_search_results.destroy()
        if not query.isdigit():
            search_tttt = tk.Label(page_search, text = f"Your searched {query} from the {type}, you need to enter an integer")
            search_tttt.pack()
            #return to end the function imdtially as number isnt valid
            return
        elif int(query) <= 0 or int(query) > df.shape[0]:
            search_tttt = tk.Label(page_search, text = f"Your search needs to be between 1 and {df.shape[0]}")
            search_tttt.pack()
        
        else:
            search_tttt = tk.Label(page_search, text = f"Your searched {query} from the {type},\n that is correct")
            search_tttt.pack()
            search_query_id(query)
    else:  
        search_tttt = tk.Label(page_search, text = f"Your searched {query} from the {type}")
        search_tttt.pack()
        search_query(type,query)
    


def click_search(type):
    
    for widget in page_search.winfo_children():
        widget.destroy()
    
    label = tk.Label(page_search, text=f"You selected: {type}", font=("Comic Sans", 30))
    label.pack(padx=40, pady=40)
    
    back_button =  tk.Button(page_search,
                             text = 'back',
                             font=("Comic Sans", 20),
                             command=lambda: show_frame(page_menu))
    back_button.pack()
    
    
    label = tk.Label(page_search, text = f"Search by {type}:")
    label.pack(pady = 10)
    
    enter = tk.Entry(page_search,width = 30)
    enter.pack(pady = 10)
    
    button = tk.Button(page_search, text="Submit",command= lambda : get_input_search(type,enter))
    button.pack(pady = 10)
    show_frame(page_search)
    
    
    
    
root = tk.Tk()
root.title("DCP-assignment")


# ---------- helper to switch pages ----------
def show_frame(frame):
    frame.tkraise()  
    
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# ---------- create two "pages" ---------- will create or 4 to veiw the stats
page_menu = tk.Frame(container)
page_search = tk.Frame(container)
page_visuals = tk.Frame(container)

for page in (page_menu, page_search):
    page.grid(row=0, column=0, sticky="nsew")

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)


#-----------Main Menu Code-----------

#function to make search type buttons on the main menu
def make_button(names):
    return tk.Button(
        page_menu,
        text= names,
        font=("Comic Sans", 30),
        command=lambda: click_search(names),
        width = 10,
        height = 1
    )

tk.Label(page_menu,
         text="Select what you want to search by").pack()
make_button("id").pack()
make_button("title").pack()
make_button('tune').pack()
make_button('key').pack()
make_button('book').pack()

#----------End Main Menu Code -----------
table_frame = tk.Frame(page_search)


table_frame.pack(fill="both", expand=True)

columns = ('id','title','alt_title','tune','key')
tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

for col in columns:
    tree.heading(col, text=col)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.grid(row=0, column=0, sticky='nsew')
scrollbar.grid(row=0, column=1, sticky='ns')

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)


show_frame(page_menu)
root.mainloop()
  






            


    



