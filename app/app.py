import os
import json
import redis
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/flask_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

cache = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'phone': self.phone}

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], phone=data.get('phone'))
    db.session.add(user)
    db.session.commit()
    cache.delete('users_list')
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    cached = cache.get('users_list')
    if cached:
        return jsonify(json.loads(cached)), 200
    users = User.query.all()
    result = [u.to_dict() for u in users]
    cache.setex('users_list', 60, json.dumps(result))
    return jsonify(result), 200

@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    cache_key = f'user_{uid}'
    cached = cache.get(cache_key)
    if cached:
        return jsonify(json.loads(cached)), 200
    user = User.query.get_or_404(uid)
    result = user.to_dict()
    cache.setex(cache_key, 60, json.dumps(result))
    return jsonify(result), 200

@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    data = request.get_json()
    user = User.query.get_or_404(uid)
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    db.session.commit()
    cache.delete('users_list')
    cache.delete(f'user_{uid}')
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    cache.delete('users_list')
    cache.delete(f'user_{uid}')
    return '', 204

# Создание таблиц базы данных при старте приложения (для Gunicorn)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Для локального запуска (опционально, но оставляем)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)