import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

#code for stats and matplotLIB

def do_databasse_stuff():
    global df
    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()
    
    df = pd.read_sql("SELECT * FROM tunes", conn)
    print(df.head())
    conn.close()

do_databasse_stuff()

# Tune pie chart-

counts_list = list(df["tune"].value_counts().items())
print(counts_list)

# Group small slices into "Other"
total = sum(size for _, size in counts_list)
threshold = 3  # this is so that all the little stuff under 3% gets put together otherwise looks really cluttered

new_labels = []
new_sizes = []
other_total = 0

for label, size in counts_list:
    pct = (size / total) * 100
    if pct < threshold:
        other_total += size
    else:
        new_labels.append(label)
        new_sizes.append(size)

if other_total > 0:
    new_labels.append("Other")
    new_sizes.append(other_total)

plt.figure()
plt.pie(new_sizes, labels=new_labels, autopct='%1.1f%%')
plt.title("Tunes: grouped <3% as Other")
plt.savefig("images/Tune_Chart.png")

#Book bar chart

book_counts_list = list(df["book"].value_counts().items())

labels = [item[0] for item in book_counts_list]
counts = [item[1] for item in book_counts_list]
plt.figure()
plt.bar(labels, counts)
plt.xlabel("Book Number")
plt.ylabel("Count")
plt.title("Books Bar Chart")

plt.savefig("images/book_chart.png")


#Key Pie chart
key_counts_list = list(df["key"].value_counts().items())

total = sum(size for _, size in key_counts_list)
threshold = 3  # this is so that all the little stuff under 3% gets put together otherwise looks really cluttered

new_labels = []
new_sizes = []
other_total = 0

for label, size in key_counts_list:
    pct = (size / total) * 100
    if pct < threshold:
        other_total += size
    else:
        new_labels.append(label)
        new_sizes.append(size)

if other_total > 0:
    new_labels.append("Other")
    new_sizes.append(other_total)

plt.figure()
plt.pie(new_sizes, labels=new_labels, autopct='%1.1f%%')
plt.title("Key: grouped <3% as Other")
plt.savefig("images/key_chart.png")


alt_counts = (
    df[df["alt_title"].notna()]
    .groupby("book")["alt_title"]
    .count()
)




alt_labels = alt_counts.index
alt_values = alt_counts.values
plt.figure()
plt.bar(alt_labels, alt_values)
plt.xlabel("Book Number")
plt.ylabel("Count alt titles")
plt.title("Alt_titles per Book Number")
plt.savefig("images/Alt_title_chart.png")