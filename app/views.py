from .app import app
from .models import get_albums
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
