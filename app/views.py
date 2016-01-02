from .app import app
from .models import get_albums, get_album_by_id, get_some_albums_by_artist, SearchForm, get_results_of_search, get_all_artists, get_artist, get_albums_by_artist, LoginForm, are_ids_ok, InscriptionForm, login_exists, Utilisateur
from .commands import newuser
from flask import render_template, g, redirect, url_for
from flask.ext.login import login_user, logout_user


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
    ids_ok = True
    if loginForm.login.data != None and loginForm.password.data != None:
        ids_ok = are_ids_ok(loginForm.login.data, loginForm.password.data)
    return render_template(
        "login_page.html",
        form = loginForm,
        ids_ok = ids_ok)

@app.route("/nouvel-utilisateur", methods=("POST", "GET"))
def nouvel_utilisateur():
    form = InscriptionForm()
    if form.validate_on_submit():
        if form.login.data != None and form.password.data != None:
            new_user = Utilisateur(login=form.login.data, password=form.password.data)
            if login_exists(new_user.login): # si l'utilisateur existe, on affiche un message d'erreur
                return render_template("inscription_page.html",
                                       form = form,
                                       user_exists = True)
            else: # sinon on ajoute l'utilisateur et on retourne sur la page home
                newuser(new_user.login, new_user.password)
                login_user(new_user) # après inscription, on se connecte directement au site
                return redirect(url_for("home"))
    return render_template(
        "inscription_page.html",
        form = form,
        user_exists = False)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
