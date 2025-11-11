def loadabcFiles(filename):
    with open(filename, "r", encoding='latin-1') as f:
        lines = f.readlines()  
    return lines


def cleanFiles(lines):
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
                "alt_title": None,
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



tunes = []

lines = loadabcFiles("abc_books/2/00.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/01.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/02.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/03.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/04.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/05.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/06.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/07.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/08.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/09.abc")
tunes.append(cleanFiles(lines))

lines = loadabcFiles("abc_books/2/10.abc")
tunes.append(cleanFiles(lines))

#parses the sublists in the tunes list
tunes = [item for sublist in tunes for item in sublist]

i = 1

tunes_index = []
for tune in tunes:
    x = {
        "index": None,
        "id": None    
    }
    x['id'] = tune['id']
    x['id'] = tune['id']
    x["index"] = i
    i += 1
    tunes_index.append(x)
    print(x)
    



print(tunes[228])
print(tunes[227])

#print(tunes)

#print(len(tunes))
