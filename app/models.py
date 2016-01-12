from app import db
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired
import sqlalchemy
from hashlib import sha256
from flask.ext.login import UserMixin
from .app import login_manager

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
    id          = db.Column(db.Integer, primary_key=True)
    titre       = db.Column(db.String(100))
    imgURL      = db.Column(db.String(250))
    annee       = db.Column(db.Integer)
    nbVues      = db.Column(db.Integer)
    nbNotes     = db.Column(db.Integer)
    noteMoyenne = db.Column(db.Float)
    artiste_id  = db.Column(db.Integer, db.ForeignKey("artiste.id"))
    artiste     = db.relationship("Artiste", backref=db.backref("artiste", lazy="dynamic"))
    genres      = db.relationship("Genre", secondary=genre_album, backref=db.backref("genres", lazy="dynamic"))
    

    def __repr__(self):
        return "<Album %s, par %s (%d)>" % (self.titre, self.artiste.nom, self.annee)


bibliotheque = db.Table("bibliotheque",
                        db.Column('album_id', db.Integer, db.ForeignKey("album.id")),
                        db.Column('login', db.String(20), db.ForeignKey("utilisateur.login"))
                        )

notes = db.Table("notes",
                        db.Column('album_id', db.Integer, db.ForeignKey("album.id")),
                        db.Column('login', db.String(20), db.ForeignKey("utilisateur.login"))
                        )

class Utilisateur(db.Model, UserMixin):
    login        = db.Column(db.String(20), primary_key=True)
    password     = db.Column(db.String(25))
    albums       = db.relationship("Album", secondary=bibliotheque, backref=db.backref("albums", lazy="dynamic"))
    albums_notes = db.relationship("Album", secondary=notes, backref=db.backref("albums_notes", lazy="dynamic"))

    def get_id(self):
        return self.login


    def __repr__(self):
        return "<User %s >" % (self.login)


class SearchForm(Form):
    search = StringField("Recherche", validators=[DataRequired()])
    

class LoginForm(Form):
    login = StringField('Login')
    password = PasswordField('Mot de passe')
    next = HiddenField()

    def get_authentificated_user(self):
        user = Utilisateur.query.get(self.login.data)
        if user is None:
            return None
        else:
            m = sha256()
            m.update(self.password.data.encode())
            passwd = m.hexdigest()
            return user if passwd == user.password else None

class InscriptionForm(Form):
    login = StringField('Choisissez un login')
    password = PasswordField('Choisissez un mot de passe', validators=[DataRequired()])


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


def are_ids_ok(login, password):
    """ renvoie si la combinaison login/password passée en paramètre existe dans la base de données """
    try:
        Utilisateur.query.filter(Utilisateur.login==login & Utilisateur.password==password).one()
        return True # si succès, on arrive ici
    except:
        return False # si échec on arrive ici

def login_exists(login):
    try:
        Utilisateur.query.filter(Utilisateur.login==login).one()
        return True
    except:
        return False

def user_has_song(loginUser, idAlbum):
    """ renvoie si un utilisateur possède un album dans sa bibliothèque """
    albums = Utilisateur.query.filter(Utilisateur.login==loginUser).one().albums # les albums de l'utilisateur
    for album in albums:
        if album.id==idAlbum:
            return True
    return False

def ajouter_album_bibliotheque(loginUser, idAlbum):
    """ ajoute un album à la bibliothèque d'un utilisateur """
    user  = Utilisateur.query.filter(Utilisateur.login==loginUser).one()
    album = Album.query.filter(Album.id==idAlbum).one()
    user.albums.append(album) # ajout de l'album à la bibliothèque de l'utilisateur
    db.session.add(user)
    db.session.commit()

def get_collection(loginUser, page):
    """ renvoie la collection paginée d'albums d'un utilisateur """
    albums = Utilisateur.query.filter(Utilisateur.login==loginUser).one().albums # liste des albums de la collection de l'utilisateur (NON PAGINEE)
    ids = [album.id for album in albums] # les ids d'albums de la bibliothèque de l'utilisateur
    albums = Album.query.filter(Album.id.in_(ids)).paginate(page, 24, False) # la liste paginée des albums de la bibliothèque de l'utilisateur
    return albums

def supp_titre_from_collection(idAlbum, loginUser):
    """ retire un album de la collection d'un utilisateur """
    print("delete from bibliotheque where login='"+loginUser+"' and album_id="+str(idAlbum))
    db.engine.execute("delete from bibliotheque where login='"+loginUser+"' and album_id="+str(idAlbum))

def inc_vues(idAlbum):
    """ incrémente de 1 le nombre de vues d'un album """
    Album.query.filter_by(id = idAlbum).update({"nbVues": Album.nbVues + 1})
    db.session.commit()

def update_rate(idAlbum, newNote, login):
    """ met à jour la moyenne des notes d'un album en y ajoutant une nouvelle note """
    album = Album.query.filter_by(id=idAlbum) # l'album dont on va modifier la moyenne
    user  = Utilisateur.query.get(login) # l'utilisateur qui a mis la note
    album.update({"nbNotes": Album.nbNotes +1}) # + 1 note
    user.albums_notes.append(album.one()) # on indique qu'il a noté cet album maintenant
    if album.one().nbNotes==1: # première note
        album.update({"noteMoyenne": newNote})
    else:
        nbNotes = album.one().nbNotes
        newMoyenne = ((album.one().noteMoyenne * (nbNotes-1)) + newNote) / nbNotes # la nouvelle moyenne de l'album
        album.update({"noteMoyenne": newMoyenne})
    db.session.commit()

def has_noted(loginUser, idAlbum):
    """ renvoie si un utilisateur a noté un album """
    user = Utilisateur.query.filter_by(login=loginUser).one() # l'utilisateur
    for album in user.albums_notes:
        if album.id==idAlbum:
            return True # l'album a été noté par l'utilisateur
    return False # album non noté par l'utilisateur
    

@login_manager.user_loader
def load_user(username):
    return Utilisateur.query.get(username)
