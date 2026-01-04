from Website import create_app
from Backend.spotipyMain import authentication

app = create_app()

if __name__ == '__main__':
    authentication()
    app.run(debug=True)