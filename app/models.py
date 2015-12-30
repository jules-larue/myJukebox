from app import db
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
import sqlalchemy

class Artiste(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(65))

    def __repr__(self):
        return "<Artiste %s (%d)>" % (self.nom, self.id)


class Genre(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))

    def __repr__(self):

        return "<Genre %s (%d)>" % (self.nom, self.id)

    
genre_album = db.Table("genre_album",
                        db.Column('genre_id', db.Integer, db.ForeignKey("genre.id"), primary_key=True),
                        db.Column('album_id', db.Integer, db.ForeignKey("album.id"), primary_key=True)
                        )

class Album(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    titre      = db.Column(db.String(100))
    imgURL     = db.Column(db.String(250))
    annee      = db.Column(db.Integer)
    artiste_id = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    artiste    = db.relationship("Artiste", backref=db.backref("artiste", lazy="dynamic"))
    genres     = db.relationship("Genre", secondary=genre_album, backref=db.backref("genres", lazy="dynamic"))
    

    def __repr__(self):
        return "<Album %s, par %s (%d)>" % (self.titre, self.artiste.nom, self.annee)


bibliotheque = db.Table("bibliotheque",
                        db.Column('album_id', db.Integer, db.ForeignKey("album.id")),
                        db.Column('login', db.String(20), db.ForeignKey("utilisateur.login"))
                        )

class Utilisateur(db.Model):
    login    = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(25))
    albums   = db.relationship("Album", secondary=bibliotheque, backref=db.backref("albums", lazy="dynamic"))


    def __repr__(self):
        return "<User %s >" % (self.login)

class SearchForm(Form):
    search = StringField("Recherche", validators=[DataRequired()])
    

class LoginForm(Form):
    login = StringField('Login')
    password = PasswordField('Mot de passe')

    def get_authentificated_user(self):
        user = Utilisateur.query.get(self.login.data)
        if user is None:
            return None
        else:
            m = sha256()
            m.update(self.password.data.encode())
            passwd = m.hexdigest()
            return user if passwd == user.password else None


###################################
# ACCESSEURS A LA BASE DE DONNEES #
###################################

def get_albums(page):
    """ renvoie tous les albums de la base paginés """
    return Album.query.paginate(page, 12, False)


def get_album_by_id(id):
    """ renvoie l'album avec l'id passé en paramètre """
    return Album.query.filter(Album.id==id).one()


def get_some_albums_by_artist(album_id):
    """ renvoie quelques albums (4 maximums) de l'artiste associé à l'id de l'album passé en paramètre """
    idArtiste = Album.query.filter(Album.id==album_id).one().artiste_id
    return Album.query.filter((Album.artiste_id==idArtiste) & (Album.id!=album_id)).limit(4).all()


def get_results_of_search(research, page):
    """ renvoie tous les albums dont le titre contient une partie de la recherche (ou est égal à la recherche)"""
    return Album.query.filter(sqlalchemy.func.lower(Album.titre).contains(research.lower())).paginate(page, 12, False)


def get_all_artists(page):
    """ renvoie une liste paginée de tous les artistes de la base, situés au numéro de page spécifié en paramètre """
    return Artiste.query.order_by(Artiste.nom).paginate(page, 40, False)

def get_artist(id):
    """ renvoie l'artiste avec l'id spécifié en paramètre """
    return Artiste.query.filter(Artiste.id==id).one()

def get_albums_by_artist(idArtiste, page):
    """ renvoie une liste paginée de tous les albums de l'artiste passé en paramètre, et de la page spécifiée """
    artiste = get_artist(idArtiste)
    return Album.query.filter(Album.artiste_id==artiste.id).order_by(Album.titre).paginate(page, 12, False)
