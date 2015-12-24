from .app import app
from .models import get_albums, get_album_by_id, get_some_albums_by_artist
from flask import render_template


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/albums")
@app.route("/albums/<int:page>")
def albums(page=1):
	return render_template("albums.html",
	page=page,
	albums=get_albums(page))


@app.route("/albums/album/<int:id>")
def album(id):
    return render_template("album_page.html",
                           album=get_album_by_id(id),
                           otherAlbumsFromArtist = get_some_albums_by_artist(id))

