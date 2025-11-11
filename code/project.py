def loadabcFiles(filename):
    with open(filename, "r", encoding='latin-1') as f:
        lines = f.readlines()  
    return lines

tunes = []

lines = loadabcFiles("abc_books/2/00.abc")
title_check = False

for line in lines:
    # Check if this starts a new tune
    line = line.strip()

    if line.startswith("X:"):
        current_tune_lines = {
            "id": int(line[2:]),
            "title": None,
            "alt_title": None,
            "tune": None,
            "Key": None,
            
        }
        title_check = False

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


print(lines[:20])

print(tunes)
