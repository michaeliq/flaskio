from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

app = Flask(__name__)
app.config.from_object(config)
app.debug = True
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///message_app.db'
socketio = SocketIO(app, async_mode="gevent")
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Room, RoomMember, User

clients = {'quality':0,'id_users':[]}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:user>')
def private_chat(user):
    join_room_()
    print(request.args)
    return render_template('index.html', user_room = user)

@socketio.on('connect')
def client_connected():
    id_cli = str(request.sid)
    clients['quality'] += 1
    clients['id_users'].append(id_cli)
    emit('connect', id_cli)
    print('client is connected ')

@socketio.on('disconnect')
def client_disconnected():
    id_cli = request.sid
    clients['quality'] -= 1
    clients['id_users'].remove(id_cli)
    print('client is disconnected ' + str(id_cli))

@socketio.on('join')
def join_room_():
    #name = request.args.get()
    #room = data['room']
    #join_room(room)
    #socketio.send(name + ' has entered the room. ', room=room)
    pass

@socketio.on_error()
def error_handler(e):
    app.logger.info(e)

@socketio.on('writing')
def is_writing(usuario):
    emit('writing',usuario, broadcast=True, include_self=False)

@socketio.on('message')
def handle_message(msg):
    msg['sid'] = request.sid
    socketio.emit('message', msg, namespace='/')




if __name__ == "__main__":
    socketio.run(app, debug=True)
