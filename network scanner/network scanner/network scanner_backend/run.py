import eventlet
eventlet.monkey_patch()

from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)  # This will run the Flask app with SocketIO support

