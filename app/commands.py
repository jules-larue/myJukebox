from .app import manager, db


@manager.command
def loaddb(filename):
    from .models import Artiste, Genre, Album, Utilisateur

    db.create_all()

    import yaml
    print("Chargement des données yaml...")
    albums = yaml.load(open(filename))

    # ajout des artistes
    artistes = {}
    print("Début de l'ajout des artistes")
    for album in albums:
        artiste = album["by"]
        if artiste not in artistes:
            artisteDB = Artiste(nom=artiste)
            db.session.add(artisteDB)
            artistes[artiste] = artisteDB
    db.session.commit()
    print("Artistes ajoutés")

    # ajout des genres
    genres={}
    print("Debut de l'ajout des genres")
    for album in albums:
        for genre in album["genre"]:
            if genre not in genres:
                genreDB = Genre(nom=genre)
                db.session.add(genreDB)
                genres[genre] = genreDB
    db.session.commit()
    print("Genres ajoutés")

    # ajout des albums
    print("Début de l'ajout des albums")
    dejaVus = set()
    for album in albums:
        if album["entryId"] not in dejaVus:
            albumDB = Album(id=album["entryId"], titre=album["title"], imgURL=album["img"], annee=album["releaseYear"], artiste_id=artistes[album["by"]].id)
            genresAlbum = []
            for genre in album["genre"]:
                genresAlbum.append(Genre(nom=genre))
            albumDB.genres=genresAlbum
            dejaVus.add(album["entryId"])
            db.session.add(albumDB)
    db.session.commit()
    
    
    
    print("Albums ajoutés")
    print("----------------------")
    print("Travail terminé !")


"""
    # liaison des genres aux albums
    print("Début de la liaison genres <-> albums")
    apparus = set() # couples (idGenre, idAlbum) déjà apparus
    for album in albums:
        for genre in album["genre"]:
            if (genres[genre].id, album["entryId"]) not in apparus:
                lien = GenreAlbum(genre_id=genres[genre].id, album_id=album["entryId"])
                db.session.add(lien)
                apparus.add((genres[genre].id, album["entryId"]))
    db.session.commit()
"""
