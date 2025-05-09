from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_secreta"  # config chave de acesso ao bando
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # caminho do arquivo, o endereço do banco

login_manager = LoginManager() 
db.init_app(app)
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(user_id)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        #longin
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
                login_user(user)
                print(current_user.is_authenticated)
                return jsonify({"message": " Autenticação realizada com sucesso"})

    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required  # Essa anotação verifica se o usuario esta logado, protegendo a rota
def logout():
     logout_user()
     return jsonify({"message": "Logout realizado com sucesso!"})


@app.route('/user', methods=["POST"])
def create_user():
     data = request.json
     username = data.get("username")
     password = data.get("password")

     if username and password:
          user = User(username=username, password=password)
          db.session.add(user)
          db.session.commit()
          return jsonify({"message": "Usuario cadastrado com sucesso!"})
     
     return jsonify({"message": "Dados invalidos."}), 400


@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
     user = User.query.get(id_user)

     if user:
          return jsonify({"username": user.username})
     
     return jsonify({"message": "Usuario não encontrado!"}), 404


@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
     data = request.json
     user = User.query.get(id_user)

     if user and data.get("password"):
          user.password = data.get("password")
          db.session.commit()
          return jsonify({"message": f"Usuário {id_user} atualizado com sucesso!"})
     
     return jsonify({"message": "Usuário não encontrado!"}), 400


@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
     user = User.query.get(id_user)

     if user and id_user != current_user.id:  # "id_user != current_user.id" verificador se é o mesmo id logado, para nao fazer a deleção do proprio usuario.
          db.session.delete(user)
          db.session.commit()
          return jsonify({"username": f"Usuário {id_user} deletado com sucesso!"})
     
     return jsonify({"message": "Usuario não encontrado!"}), 404


if __name__ == '__main__':
    app.run(debug=True)

