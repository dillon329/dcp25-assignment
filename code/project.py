def loadabcFiles(filename):
    with open(filename, "r", encoding='latin-1') as f:
        lines = f.readlines()  
    return lines




df = loadabcFiles("abc_books/2/00.abc")


print(df[:20])
