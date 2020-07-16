from flask import Flask, jsonify, request, abort
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# ini adalah pertemuan 3
#@app.route('/')
#def hello_world():
#    return 'Hello World!'


#@app.route("/admin")
#def admin_page():
#    return 'ini adalah halaman admin!'


# pertemuan 3 berakhir disini

# ini pertemuan 4
#class HelloWorld(Resource):
#    def get(self):
#        return {'hello': 'world'}


#api.add_resource(HelloWorld, '/helloworld')


# pertemuan 4 berakhir disini

# ini pertemuan 5
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(10), unique=False)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @staticmethod
    def get_all_users():
        return User.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','username', 'password', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


#@app.route("/user/", methods=["GET"])
#def get_user():
#    all_users = User.get_all_users()
#    result = users_schema.dump(all_users)
#    return jsonify(result)

# pertemuan 5 berakhir disini

# materi pertemuan 7
#@app.route("/user/<int:id>", methods=["GET"])
#def one_user(id):
#    user = User.query.get(id)
#    result = user_schema.dump(user)
#    return jsonify(result)


#@app.route("/user/", methods=["POST"])
#def create_user():
#    if not request.json or not 'username' in request.json and not 'email' in request.json:
#        abort(400)

#    user = User(request.json['username'], request.json['email'])
#    db.session.add(user)
#    db.session.commit()

#    result = user_schema.dump(user)
#    return jsonify(result)


#@app.route("/user/<int:id>/", methods=["PUT"])
#def update_user(id):
#    if not request.json or not 'username' in request.json and not 'email' in request.json:
#        abort(400)

#    user = User.query.get(id)
#    user.username = request.json['username']
#    user.email = request.json['email']
#    db.session.commit()

#    result = user_schema.dump(user)
#    return jsonify(result)


#@app.route("/user/<int:id>", methods=["DELETE"])
#def delete_user(id):
#    user = User.query.get(id)
#    db.session.delete(user)
#    db.session.commit()

#    return jsonify()

# pertemuan 7 berakhir disini

# Materi Pertemuan 8

class UserApi(Resource):
    def get(self, id=None):
        if id is not None:
            user = User.query.get(id)
            result = user_schema.dump(user)
            return jsonify(result)
        else:
            all_users = User.get_all_users()
            result = users_schema.dump(all_users)
            return jsonify(result)

    def post(self):
        if not request.json or not 'username ' in request.json and not 'password' in request.json and not 'email' in request.json:
            abort(400)

        user = User(request.json['username'], request.json['password'], request.json['email'])
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)
        return jsonify(result)

    def put(self, id):
        if not request.json or not 'username' in request.json and not 'password' in request.json and not 'email' in request.json:
            abort(400)

        user = User.query.get(id)
        user.username = request.json['username']
        user.password = request.json['password']
        user.email = request.json['email']
        db.session.commit()

        result = user_schema.dump(user)
        return jsonify(result)

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify()


api.add_resource(UserApi, '/user/', '/user/<int:id>/', endpoint='user_ep')

# Materi Pertemuan 8 berakhir di sini

# Materi Pertemuan 12

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    login_user = User.query.filter_by(username=username).first()
    print(login_user.username + " " + username)
    print(login_user.password + " " + password)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != login_user.username or password != login_user.password:   # 1 or 0 = 1 1 and 1 = 1
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Materi Pertemuan 12 berakhir di sini

# materi pertemuan 13 dan 14
@app.route('/getuser', methods=['GET'])
@jwt_required
def getuser():
    all_users = User.get_all_users()
    result = users_schema.dump(all_users)

    return jsonify(result), 200


# materi pertemuan 13 dan 14 berakhir di sini


if __name__ == '__main__':
    app.run()
