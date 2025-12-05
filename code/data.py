
import os 
import sqlite3

#code to do through each file and upload the data to a sql database tunes.db


#done so that everything this program is run the database tunes.db is reset
conn = sqlite3.connect("tunes.db")
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Drop each table
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

conn.commit()
conn.close()

abc_encoding_LOOKUP ={
    #grave
    '\\`A': 'À', '\\`a': 'à', '\\`E': 'È', '\\`e': 'è', 
    '\\`I': 'Ì', '\\`i': 'ì', '\\`O': 'Ò', '\\`o': 'ò',
    '\\`U': 'Ù', '\\`u': 'ù',

    #acute
    "\\'A": 'Á', "\\'a": 'á', "\\'E": 'É', "\\'e": 'é',
    "\\'I": 'Í', "\\'i": 'í', "\\'O": 'Ó', "\\'o": 'ó',
    "\\'U": 'Ú', "\\'u": 'ú', "\\'Y": 'Ý', "\\'y": 'ý',

    #circumflex
    '\\^A': 'Â', '\\^a': 'â', '\\^E': 'Ê', '\\^e': 'ê',
    '\\^I': 'Î', '\\^i': 'î', '\\^O': 'Ô', '\\^o': 'ô',
    '\\^U': 'Û', '\\^u': 'û',

    #tilde
    '\\~A': 'Ã', '\\~a': 'ã', '\\~N': 'Ñ', '\\~n': 'ñ',
    '\\~O': 'Õ', '\\~o': 'õ',

    #umlauts
    '\\"A': 'Ä', '\\"a': 'ä', '\\"E': 'Ë', '\\"e': 'ë',
    '\\"I': 'Ï', '\\"i': 'ï', '\\"O': 'Ö', '\\"o': 'ö',
    '\\"U': 'Ü', '\\"u': 'ü', '\\"Y': 'Ÿ', '\\"y': 'ÿ',
    
    #cedilla
    '\\cC': 'Ç', '\\cc': 'ç',

    #ring
    '\\AA': 'Å', '\\aa': 'å',

    #slash
    '\\/O': 'Ø', '\\/o': 'ø',

    #breve
    '\\uA': 'Ă', '\\ua': 'ă', '\\uE': 'Ĕ', '\\ue': 'ĕ',

    #caron
    '\\vS': 'Š', '\\vs': 'š', '\\vZ': 'Ž', '\\vz': 'ž',
    '\\vC': 'Č', '\\vc': 'č',

    #double acute
    '\\HO': 'Ő', '\\Ho': 'ő', '\\HU': 'Ű', '\\Hu': 'ű',

    #ligatures
    '\\ss': 'ß', '\\AE': 'Æ', '\\ae': 'æ', '\\oe': 'œ', '\\OE': 'Œ',}
def decode_abc(text: str) -> str:
    if not text:
        return text

    decoded = text

    for key in sorted(abc_encoding_LOOKUP, key=len, reverse=True):
        decoded = decoded.replace(key, abc_encoding_LOOKUP[key])

    return decoded


def cleanFiles(lines,current_file_count):
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
        line = decode_abc(line)
        if line.startswith("X:"):
            if pass_through_1 != False:
                tunes.append(current_tune_lines.copy())
                
            current_tune_lines = {
                "id": int(line[2:]),
                "title": None,
                "alt_title": '',
                "tune": None,
                "Key": None,
                "Book":current_file_count
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
    current_file_count = 0
    #goes thorugh each abc file in the abc_books folder
    for foldername in os.listdir(folder):
        current_file_count += 1
        for filename in os.listdir(folder+"/"+foldername):
            if filename.endswith(".abc"):
                path = os.path.join(folder, foldername, filename)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    #prarses the line into a list
                    tunes.append(cleanFiles(lines,current_file_count))


def do_databasse_stuff():
    global tunes

    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS tunes (id INTEGER, title TEXT, alt_title TEXT, tune TEXT, key TEXT, book INTEGER)')
    
    # Insert data
    for row in tunes:
        if row['alt_title'] == '':
            row['alt_title'] = None
        cursor.execute('INSERT INTO tunes (id, title, alt_title, tune, key, book) VALUES (?, ?, ?, ?, ?, ?)', (row['id'], row['title'],row['alt_title'],row['tune'],row['Key'],row['Book']))

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
print(tunes)
do_databasse_stuff()