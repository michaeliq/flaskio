from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clavesecreta'
socketio = SocketIO(app)

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

@socketio.on('join_personal_room')
def join_personal_room(data):
    id_cli = request.sid
    room = id_cli
    msg = data['msg']
    send(msg, room = room)

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast = True)


if __name__ == "__main__":
    socketio.run(app)
