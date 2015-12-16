from app import db

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
        return "<Album %s, par %s (%d), genre : %s>" % (self.titre, self.artiste.nom, self.annee, self.genre.name)


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
    

