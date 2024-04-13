from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Book,Borrowing
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
import datetime

app = Flask(__name__)

app.config.from_pyfile('config.py')
db.init_app(app)

def create_database():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    print("Fetching books from the database...")
    books = Book.query.all()
    print("Fetched books:", books)
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        print("Received a POST request to add a new book.")
        print("Form Data:", request.form)
        
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        genre = request.form['genre']
        publisher = request.form['publisher']
        count=request.form['Total count']
        
        new_book = Book(title=title, author=author, isbn=isbn, genre=genre, publisher=publisher,available_count=count)
        
        db.session.add(new_book)
        db.session.commit()
        
        print("New book added to the database.")
        
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit_book', methods=['GET', 'POST'])
def edit_book():
    existing_book = None  # Initialize the variable outside the if block

    if request.method == 'POST':
        # Get the title of the book to edit from the form
        title = request.form['title']

        # Query the database to find the existing book by title
        existing_book = Book.query.filter_by(title=title).first()

        if existing_book:
            # Update the attributes of the existing book with values from the form
            existing_book.author = request.form['author']
            existing_book.isbn = request.form['isbn']
            existing_book.genre = request.form['genre']
            existing_book.publisher = request.form['publisher']

            # Commit the changes to the database
            db.session.commit()

            print("Book attributes updated in the database.")

            return redirect(url_for('index'))
        else:
            return jsonify({'error': 'Book not found'})

    # Render the form for editing a book
    return render_template('edit_book.html', book=existing_book)




@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        # Form was submitted, process the data
        title = request.form['title']
        borrower_name = request.form['borrower_name']
        return_date = datetime.datetime.strptime(request.form['return_date'], '%Y-%m-%d').date()
        
        # Query the database to find the book by its title
        book = Book.query.filter_by(title=title).first()
        
        if book:
            if book.available_count > 0:
                # Create a new Borrowing object
                borrowing = Borrowing(book_title=book.title, borrower_name=borrower_name, return_date=return_date)
                # Add the borrowing to the session and commit it to the database
                db.session.add(borrowing)
                db.session.commit()
                
                # Update book availability and issue status
                book.available_count -= 1
                book.issue_status = True
                # Commit changes to the database
                db.session.commit()
                
                # Redirect to the main page
                return redirect(url_for('index'))
            else:
                # No available copies, display message
                return "No book copy available"
        else:
            # Book not found, return an appropriate response
            return "Book not found"
    
    # Return a response if the request method is not POST
    return render_template('issue_book.html')


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
