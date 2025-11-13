import os

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
            try:
                current_tune_lines['tune'] = line[2:].strip()
            except:
                if line.startswith("R:"):
                    try:
                        current_tune_lines['tune'] = line[2:].strip()
                    except:
                        print("Oh no")
        
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

            