from .app import app
from .models import get_albums, get_album_by_id, get_some_albums_by_artist, SearchForm, get_results_of_search, get_all_artists, get_artist, get_albums_by_artist, LoginForm
from flask import render_template, g, redirect, url_for
from flask.ext.login import login_user


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
                               resultats=get_albums(page),
                               nom_resultat='albums')


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
                           resultats=results,
                           nom_resultat='recherche_resultats',
                           page=page)



@app.route("/artistes")
@app.route("/artistes/<int:page>")
def artistes(page=1):
    return render_template("artistes.html",
                           page=page,
                           resultats=get_all_artists(page),
                           nom_resultat='artistes')


@app.route("/artistes/albums")
@app.route("/artistes/albums/<int:id>")
@app.route("/artistes/albums/<int:id>/<int:page>")
def albums_artiste(id=1, page=1):
    return render_template("albums_artiste.html",
                           page=page,
                           resultats=get_albums_by_artist(id, page),
                           artiste = get_artist(id))



@app.route("/login/", methods=("GET", "POST"))
def login():
    loginForm = LoginForm() # the login form
    if loginForm.validate_on_submit():
        user = loginForm.get_authentificated_user()
        if user:
            # si un utilisateur est déjà authentifié et va à l'URL "/login" on le redirige vers la page "/home"
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "login_page.html",
        form = loginForm)
