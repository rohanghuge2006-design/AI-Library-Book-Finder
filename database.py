import sqlite3

DATABASE_NAME = "library.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            shelf TEXT NOT NULL
        )
    """)

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:

        books = [
            (
                "Artificial Intelligence",
                "Stuart Russell",
                "Computer Science",
                "A-01"
            ),
            (
                "Python Programming",
                "Mark Lutz",
                "Computer Science",
                "A-02"
            ),
            (
                "Database Management Systems",
                "Raghu Ramakrishnan",
                "Computer Science",
                "A-03"
            ),
            (
                "Computer Networks",
                "Andrew Tanenbaum",
                "Computer Science",
                "A-04"
            ),
            (
                "Operating System Concepts",
                "Silberschatz",
                "Computer Science",
                "A-05"
            ),
            (
                "Data Structures",
                "Seymour Lipschutz",
                "Computer Science",
                "B-01"
            ),
            (
                "Machine Learning",
                "Tom Mitchell",
                "Artificial Intelligence",
                "B-02"
            ),
            (
                "Deep Learning",
                "Ian Goodfellow",
                "Artificial Intelligence",
                "B-03"
            ),
            (
                "Engineering Mathematics",
                "B. S. Grewal",
                "Mathematics",
                "C-01"
            ),
            (
                "Digital Electronics",
                "Morris Mano",
                "Electronics",
                "D-01"
            ),
            (
                "Microprocessors",
                "Ramesh Gaonkar",
                "Electronics",
                "D-02"
            ),
            (
                "Software Engineering",
                "Ian Sommerville",
                "Software",
                "E-01"
            ),
            (
                "Web Technology",
                "Uttam K. Roy",
                "Web Development",
                "E-02"
            ),
            (
                "Cyber Security",
                "William Stallings",
                "Security",
                "E-03"
            )
        ]

        cursor.executemany("""
            INSERT INTO books
            (title, author, category, shelf)
            VALUES (?, ?, ?, ?)
        """, books)

        connection.commit()

    connection.close()


def get_all_books():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM books
        ORDER BY category, title
    """)

    books = cursor.fetchall()

    connection.close()

    return books


def search_books(keyword):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ?
           OR author LIKE ?
           OR category LIKE ?
        ORDER BY title
    """, (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    books = cursor.fetchall()

    connection.close()

    return books