from app import db
import json


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.Text, primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"USER: {self.username} - {self.password}"

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)
    author = db.Column(db.Text, nullable=False)
    creator = db.Column(db.Text, nullable=False)
    creationDate = db.Column(db.Text, nullable=False)
    uploadDate = db.Column(db.Text, nullable=False)
    filename = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Image {self.id} - {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "author": self.author,
            "creator": self.creator,
            "creationDate": self.creationDate,
            "uploadDate": self.uploadDate,
            "filename": self.filename,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
