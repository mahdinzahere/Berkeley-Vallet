import socketio
from typing import Dict, List
from .models import User, DriverProfile, Ride, RideStatus

# Create Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode='asgi'
)

# Store connected users
connected_users: Dict[str, Dict] = {}
online_drivers: Dict[int, Dict] = {}

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")
    
    # Remove from connected users
    if sid in connected_users:
        user_data = connected_users[sid]
        user_id = user_data.get('user_id')
        role = user_data.get('role')
        
        # Remove from online drivers if applicable
        if role == 'driver' and user_id in online_drivers:
            del online_drivers[user_id]
        
        del connected_users[sid]

@sio.event
async def authenticate(sid, data):
    """Authenticate user and store connection info"""
    user_id = data.get('user_id')
    role = data.get('role')
    
    connected_users[sid] = {
        'user_id': user_id,
        'role': role,
        'sid': sid
    }
    
    await sio.emit('authenticated', {'status': 'success'}, room=sid)

@sio.event
async def driver_online(sid, data):
    """Handle driver going online"""
    user_id = data.get('user_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    online_drivers[user_id] = {
        'sid': sid,
        'latitude': latitude,
        'longitude': longitude
    }
    
    await sio.emit('driver_status', {'status': 'online'}, room=sid)

@sio.event
async def driver_offline(sid, data):
    """Handle driver going offline"""
    user_id = data.get('user_id')
    
    if user_id in online_drivers:
        del online_drivers[user_id]
    
    await sio.emit('driver_status', {'status': 'offline'}, room=sid)

@sio.event
async def update_location(sid, data):
    """Update driver location"""
    user_id = data.get('user_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if user_id in online_drivers:
        online_drivers[user_id].update({
            'latitude': latitude,
            'longitude': longitude
        })

@sio.event
async def request_ride(sid, data):
    """Handle ride request and broadcast to nearby drivers"""
    ride_id = data.get('ride_id')
    pickup_lat = data.get('pickup_latitude')
    pickup_lng = data.get('pickup_longitude')
    dropoff_lat = data.get('dropoff_latitude')
    dropoff_lng = data.get('dropoff_longitude')
    fare = data.get('fare')
    
    # Broadcast to all online drivers
    for driver_id, driver_data in online_drivers.items():
        await sio.emit('ride_request', {
            'ride_id': ride_id,
            'pickup_latitude': pickup_lat,
            'pickup_longitude': pickup_lng,
            'dropoff_latitude': dropoff_lat,
            'dropoff_longitude': dropoff_lng,
            'fare': fare
        }, room=driver_data['sid'])

@sio.event
async def accept_ride(sid, data):
    """Handle driver accepting ride"""
    ride_id = data.get('ride_id')
    driver_id = data.get('driver_id')
    
    # Find rider's sid
    rider_sid = None
    for sid, user_data in connected_users.items():
        if user_data.get('role') == 'rider':
            # In a real app, you'd check if this rider has the specific ride
            rider_sid = sid
            break
    
    if rider_sid:
        await sio.emit('ride_assigned', {
            'ride_id': ride_id,
            'driver_id': driver_id
        }, room=rider_sid)
    
    # Notify driver
    await sio.emit('ride_accepted', {
        'ride_id': ride_id,
        'status': 'accepted'
    }, room=sid)

@sio.event
async def update_ride_status(sid, data):
    """Update ride status and notify relevant parties"""
    ride_id = data.get('ride_id')
    status = data.get('status')
    driver_id = data.get('driver_id')
    
    # Find rider's sid
    rider_sid = None
    for sid, user_data in connected_users.items():
        if user_data.get('role') == 'rider':
            rider_sid = sid
            break
    
    if rider_sid:
        await sio.emit('ride_status_update', {
            'ride_id': ride_id,
            'status': status
        }, room=rider_sid)
    
    # Notify driver
    await sio.emit('ride_status_update', {
        'ride_id': ride_id,
        'status': status
    }, room=sid)

@sio.event
async def driver_location_update(sid, data):
    """Send driver location update to rider"""
    ride_id = data.get('ride_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Find rider's sid for this specific ride
    rider_sid = None
    for sid, user_data in connected_users.items():
        if user_data.get('role') == 'rider':
            rider_sid = sid
            break
    
    if rider_sid:
        await sio.emit('driver_location', {
            'ride_id': ride_id,
            'latitude': latitude,
            'longitude': longitude
        }, room=rider_sid)

def get_online_drivers() -> List[Dict]:
    """Get list of online drivers"""
    return list(online_drivers.values())

def is_driver_online(driver_id: int) -> bool:
    """Check if driver is online"""
    return driver_id in online_drivers
