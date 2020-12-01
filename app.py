import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clavesecreta'


socketio = SocketIO(app, async_mode='eventlet', message_queue = "redis://", logger=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def client_connected():
    id_cli = str(request.sid)
    socketio.emit('connect', id_cli)
    print('client is connected ')

@socketio.on('disconnect')
def client_disconnected():
    id_cli = request.sid
    print('client is disconnected ' + str(id_cli))

@socketio.on('join_personal_room')
def join_personal_room(data):
    id_cli = request.sid
    room = id_cli
    msg = data['msg']
    send(msg, room = room)

@socketio.on_error()
def error_handler(e):
    app.logger.info(e)

@socketio.on('message')
def handle_message(msg):
    msg['sid'] = request.sid
    socketio.emit('message', msg, namespace='/')


if __name__ == "__main__":
    socketio.run(app, debug=True)
