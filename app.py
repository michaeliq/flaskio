from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
import datetime
import config

app = Flask(__name__)
app.config.from_object(config)
app.debug = True
app.config['SECRET_KEY'] = 'clavesecreta'
socketio = SocketIO(app, async_mode="gevent")
db = SQLAlchemy(app)

from models import Room

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def client_connected():
    id_cli = str(request.sid)
    print('client is connected ')

@socketio.on('disconnect')
def client_disconnected():
    id_cli = request.sid
    print('client is disconnected ' + str(id_cli))

#@socketio.on('create_room')
def create_room(data):
    newRoom = Room(name=data['name'+" room"],created_at=datetime.datetime.now(),created_by=data['name'])
    db.session.add(newRoom)
    db.session.commit()

def view_room(room_id):
    pass

def edit_room(room_id,room_name,members):
    pass

@socketio.on_error()
def error_handler(e):
    app.logger.info(e)

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast = True)




if __name__ == "__main__":
    socketio.run(app)
