from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
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
    pass

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
