from flask import Flask, render_template,redirect,request
import csv
from datetime import datetime

# Cria a aplicação Flask
app = Flask(__name__)

@app.post("/add-review")
def add_review():

    with open("books.csv", mode="r", encoding="utf-8") as csv_file:
        reader = list(csv.reader(csv_file))
        last_id = 0

        if len(reader) > 1:
            last_row = reader[-1]
            if last_row:
                last_id = int(last_row[0])

        next_id = last_id + 1

    # 2. Converte a data para o formato esperado
    realesed_date_raw = request.form.get("realese_date")
    date_object = datetime.strptime(realesed_date_raw, "%Y-%m-%d")

    formatted_date = date_object.strftime("%m/%d/%Y")

    # 3. Coleta os dados do formulário usando o atributo 'name' de cada campo
    new_book_data = [
        next_id,
        request.form.get("title"),
        request.form.get("image_url"),
        request.form.get("rating"),
        formatted_date,
        request.form.get("review"),
    ]

    # 3. Anexa os novos dados ao arquivo CSV
    with open("books.csv", mode="a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(new_book_data)

    # 4. Redireciona para a página principal
    return redirect(url_for("index"))

@app.get("/add-review")
def show_add_form():
    return render_template("add-review.html")

@app.get("/book/<int:book_id>")
def book_details(book_id):
    found_book = None

    with open('books.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for book in csv_reader:
            # Compara o ID da linha (convertido para int) com o ID da URL
            if int(book['id']) == book_id:
                found_book = book
                break # Encontramos o filme, podemos parar o loop
    
    # Se um filme foi encontrado, renderiza a página de detalhes com seus dados
    if found_book:
        return render_template("book-details.html", book=found_book)

    # Se não, retorna uma página de erro 404
    else:
        return "Book not found!", 404


# Define a rota principal, que irá renderizar o index.html
@app.get("/")
def index():
    books = []
    with open('books.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            books.append(row)
    
    return render_template("index.html", books=books)



if __name__ == "__main__":
    app.run(debug=True)