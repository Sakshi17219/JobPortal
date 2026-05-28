from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from datetime import datetime

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app, async_mode='threading', cors_allowed_origins='*')

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        join_room(f'user_{current_user.id}')
        emit('activity', {
            'type': 'system',
            'message': f'Connected as {current_user.username}',
            'timestamp': datetime.utcnow().isoformat()
        })

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        leave_room(f'user_{current_user.id}')

@socketio.on('join_admin')
def handle_join_admin():
    if current_user.is_authenticated and current_user.role == 'admin':
        join_room('admin_room')

def broadcast_activity(event_type: str, message: str, data: dict = None):
    """Broadcast a real-time activity event to all admin users."""
    payload = {
        'type': event_type,
        'message': message,
        'timestamp': datetime.utcnow().isoformat(),
        'data': data or {}
    }
    socketio.emit('activity', payload, to='admin_room')

def notify_user(user_id: int, message: str, status: str = None):
    """Send a real-time notification to a specific user."""
    payload = {
        'type': 'notification',
        'message': message,
        'status': status,
        'timestamp': datetime.utcnow().isoformat()
    }
    socketio.emit('notification', payload, to=f'user_{user_id}')
