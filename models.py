from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    title = db.Column(db.String(100), primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    available_count = db.Column(db.Integer, nullable=False, default=0)
    issue_status = db.Column(db.Boolean, nullable=False, default=False)
    borrowings = db.relationship('Borrowing', backref='book', lazy=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', '{self.genre}', '{self.publisher}', '{self.available_count}', '{self.issue_status}')"

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100), db.ForeignKey('book.title'))
    borrower_name = db.Column(db.String(100))
    return_date = db.Column(db.DateTime)
