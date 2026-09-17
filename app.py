from flask import Flask, render_template, request

from database import (
    create_database,
    get_all_books,
    search_books
)

from bfs import bfs_search


app = Flask(__name__)


# Create database automatically when the application starts
create_database()


def create_library_graph(books):

    graph = {
        "Library": []
    }

    categories = {}

    for book in books:

        category = book["category"]
        title = book["title"]

        if category not in categories:

            categories[category] = []

            graph[category] = []

            graph["Library"].append(category)

        graph[category].append(title)

        graph[title] = []

    return graph


@app.route("/")
def index():

    books = get_all_books()

    categories = sorted(
        list(set(book["category"] for book in books))
    )

    return render_template(
        "index.html",
        books=books,
        categories=categories
    )


@app.route("/search", methods=["POST"])
def search():

    keyword = request.form.get(
        "keyword",
        ""
    ).strip()

    books = get_all_books()

    if not keyword:

        return render_template(
            "result.html",
            found=False,
            message="Please enter a book name.",
            visited=[],
            path=[],
            results=[],
            keyword="",
            nodes_visited=0,
            path_length=0,
            execution_time=0
        )

    graph = create_library_graph(books)

    matching_books = search_books(keyword)

    if matching_books:

        # Select the first matching book as the BFS target
        target = matching_books[0]["title"]

        result = bfs_search(
            graph,
            "Library",
            target
        )

        return render_template(
            "result.html",
            found=result["found"],
            message="Book Found!",
            visited=result["visited"],
            path=result["path"],
            results=matching_books,
            keyword=keyword,
            nodes_visited=result["nodes_visited"],
            path_length=result["path_length"],
            execution_time=result["execution_time"]
        )

    else:

        return render_template(
            "result.html",
            found=False,
            message="Book Not Found",
            visited=[],
            path=[],
            results=[],
            keyword=keyword,
            nodes_visited=0,
            path_length=0,
            execution_time=0
        )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )