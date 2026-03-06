from flask import Flask, render_template, request

from hw5.main import load_tf_idf, get_inverted_index, vector_search

app = Flask(__name__)

lemma_vectors, lemma_idf = load_tf_idf()
index = get_inverted_index()


@app.route("/", methods=["GET", "POST"])
def search_page():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form["query"]
        results = vector_search(query, lemma_vectors, lemma_idf, index)

    return render_template(
        "index.html",
        query=query,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)