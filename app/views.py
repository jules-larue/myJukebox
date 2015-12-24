from .app import app
from .models import get_albums, get_album_by_id, get_some_albums_by_artist, SearchForm, get_results_of_search
from flask import render_template, g, redirect, url_for

@app.before_request
def before_request():
    g.searchForm = SearchForm()


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


@app.route("/recherche/", methods=("GET", "POST"))
def recherche():
    if not g.searchForm.validate_on_submit():
        return redirect(url_for('home'))
    return redirect(url_for('recherche_resultats', query=g.searchForm.search.data))


@app.route("/recherche_resultats/<query>")
@app.route("/recherche_resultats/<query>/<int:page>")
def recherche_resultats(query, page=1):
    results = get_results_of_search(query, page)
    return render_template('search_results.html',
                           query=query,
                           albums=results,
                           page=page)
