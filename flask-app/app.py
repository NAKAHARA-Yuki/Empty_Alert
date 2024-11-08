from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@mysql:3306/flask_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f''

@app.route('/')
def index():
    return 'Flask App'

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    name = request.json.get('name')
    if name:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name})
    else:
        return jsonify({'error': 'Missing name'}), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')