from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_secreta"  # config chave de acesso ao bando
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # caminho do arquivo, o endereço do banco
 
db = SQLAlchemy(app)


@app.route("/ola-mundo", methods=["GET"])
def ola_mundo():
    return "óla mundo"

if __name__ == '__main__':
    app.run(debug=True)