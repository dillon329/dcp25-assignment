    id_val = row["id"].iloc[0]
    title_val = row["title"].iloc[0]

    hello = tk.Label(page_search, text=f"{id_val} — {title_val}")
    hello.pack()