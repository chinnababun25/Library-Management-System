// app.js

document.addEventListener("DOMContentLoaded", function() {
    const bookForm = document.getElementById("bookForm");
    const bookList = document.querySelector("#bookList tbody");
    let editingBookId = null;

    // Fetch and render books
    function fetchBooks() {
        fetch('/books')
            .then(response => response.json())
            .then(data => {
                bookList.innerHTML = '';
                data.forEach(book => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${book[0]}</td>
                        <td>${book[1]}</td>
                        <td>${book[2]}</td>
                        <td>${book[3]}</td>
                        <td>${book[4]}</td>
                        <td class="actions">
                            <button onclick="editBook(${book[0]})">Edit</button>
                            <button onclick="deleteBook(${book[0]})">Delete</button>
                        </td>
                    `;
                    bookList.appendChild(row);
                });
            });
    }

    fetchBooks();

    // Add or update a book
    bookForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const title = document.getElementById("title").value;
        const author = document.getElementById("author").value;
        const year = document.getElementById("year").value;
        const isbn = document.getElementById("isbn").value;

        const data = { title, author, year, isbn };

        if (editingBookId) {
            fetch(`/books/${editingBookId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON
