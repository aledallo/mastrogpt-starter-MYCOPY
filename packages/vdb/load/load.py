import vdb

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
"""

def load(args):
    collection = args.get("COLLECTION", "default")
    out = f"{USAGE}Current collection is {collection}"
    inp = str(args.get('input', ""))
    db = vdb.VectorDB(args)

    # Prima controlla se l'input è un URL
    if inp.startswith("https://"):
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(inp)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            extracted_text = soup.get_text()

            # Inserisci il testo estratto nel database
            res = db.insert(extracted_text)
            out = "Inserted from link: " + " ".join([str(x) for x in res.get("ids", [])])
        else:
            out = f"Errore nel recuperare la pagina. Status code: {response.status_code}"
    
    # Gestione della ricerca vettoriale
    elif inp.startswith("*"):
        if len(inp) == 1:
            out = "please specify a search string"
        else:
            res = db.vector_search(inp[1:])
            if len(res) > 0:
                out = "Found:\n"
                for i in res:
                    out += f"({i[0]:.2f}) {i[1]}\n"
            else:
                out = "Not found"
    
    # Gestione della rimozione per substring
    elif inp.startswith("!"):
        count = db.remove_by_substring(inp[1:])
        out = f"Deleted {count} records."
    
    # Inserimento generico di testo
    elif inp != '':
        res = db.insert(inp)
        out = "Inserted " + " ".join([str(x) for x in res.get("ids", [])])
    
    return {"output": out}
