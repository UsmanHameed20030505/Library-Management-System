import sqlite3

def view_books():
    # Connect to the SQLite database
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    # Execute a SQL query to select all records from the book table
    cursor.execute("SELECT * FROM book")

    # Fetch all rows from the cursor
    rows = cursor.fetchall()

    # Print column headers
    print("Title\tAuthor\tISBN\tGenre\tPublisher\tAvailable Count\tIssue Status\tBorrowed By")

    # Print each row of the result
    for row in rows:
        print('\t'.join(map(str, row)))

    # Close the cursor and connection
    cursor.close()
    connection.close()

if __name__ == '__main__':
    view_books()
