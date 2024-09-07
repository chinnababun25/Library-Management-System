from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER,
                        isbn TEXT UNIQUE
                    )''')
    conn.commit()
    conn.close()

# Route for rendering the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to view all books
@app.route('/books', methods=['GET'])
def view_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)

# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    author = data['author']
    year = data['year']
    isbn = data['isbn']

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", 
                       (title, author, year, isbn))
        conn.commit()
        return jsonify({'message': 'Book added successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'ISBN already exists!'}), 400
    finally:
        conn.close()

# Route to update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json
    title = data['title']
    author = data['author']
    year = data['year']
    isbn = data['isbn']

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?", 
                   (title, author, year, isbn, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book updated successfully!'})

# Route to delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted successfully!'})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
