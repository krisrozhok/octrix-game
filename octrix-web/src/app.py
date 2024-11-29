from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from game_adapter import GameAdapter
import os

app = Flask(__name__,
    template_folder='../templates',
    static_folder='../static'
)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

game_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    game = GameAdapter(socketio, session_id)
    game_sessions[session_id] = game
    game.emit_to_client('output', ' ' * 27 + 'OCTRIX\n')
    game.emit_to_client('output', ' ' * 20 + 'CREATIVE COMPUTING\n')
    game.emit_to_client('output', ' ' * 18 + 'MORRISTOWN, NEW JERSEY\n\n\n')
    game.emit_to_client('input_request', 'TEACH GAME(Y OR N)? ')

@socketio.on('input')
def handle_input(data):
    session_id = request.sid
    if session_id in game_sessions:
        game_sessions[session_id].handle_input(data)

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in game_sessions:
        del game_sessions[session_id]

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
