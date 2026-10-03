def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r") as f:
            i = 0
            album = dict()
            lista_anni = []
            lista_foto = []
            for line in f:
                line = line.strip("\n")
                if i == 0:
                    headers=line.split(", ")
                    i=i+1
                else:
                    foto = dict()
                    elementi=line.split(",")
                    for j in range(len(headers)):
                        if headers[j] == "anno":
                            elementi[j] = int(elementi[j])
                            if elementi[j] not in lista_anni:
                                lista_anni.append(int(elementi[j]))
                        foto[headers[j]] = elementi[j]
                    lista_foto.append(foto)

            for anno in lista_anni:
                album[anno] = []

            for fotos in lista_foto:
                album[fotos["anno"]].append(fotos)

    except FileNotFoundError:
        print("File non trovato")
        return None

    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if cerca_foto(album, codice) is not None:
        print("Codice già presente nell'album")
        return False

    if anno not in album:
        album[anno] = []
    foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }
    album[anno].append(foto)
    with open(file_path, "a") as f:
        f.write(f"{foto["codice"]},{foto["titolo"]},{foto["autore"]},{foto["mese"]},{foto["anno"]}\n")
    return True


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    risultato = None
    for anno in album:
        for i in range(len(album[anno])):
            if album[anno][i]["codice"] == codice:
                risultato=album[anno][i]
    return risultato

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    return sorted(album[anno], key = lambda foto: foto["titolo"])


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                if mese < 1 or mese > 12:
                    print("Mese non valido, operazione annullata")
                    break
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
