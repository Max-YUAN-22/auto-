# backend/websocket.py
import asyncio
import json
import socketio
from fastapi import APIRouter
from .websocket_manager import manager
from .dsl_workflows import smart_city_simulation_workflow
from .dependencies import get_dsl_instance

router = APIRouter()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

@sio.on('*')
async def catch_all(event, sid, data):
    print(f'Received event "{event}" from {sid} with data: {data}')

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('connection_successful', {'data': 'Connected'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        print(f"Parsed message data: {data}")
        
        task_type = data.get('type')
        print(f"TASK TYPE: {task_type}")
        print(f"Is task_type == 'smart_city_simulation'? {task_type == 'smart_city_simulation'}")

        task_data = data.get('data', {})

        dsl = get_dsl_instance()

        if task_type == "smart_city_simulation":
            print("Executing smart_city_simulation_workflow")
            asyncio.create_task(smart_city_simulation_workflow(dsl, task_data))
        elif task_type == 'generate_report':
             print("Executing generate_report_workflow")
             from backend.dsl_workflows import generate_report_workflow
             asyncio.create_task(generate_report_workflow(dsl))
        else:
            print(f"Unknown message type: {task_type}")
    
    except json.JSONDecodeError as e:
        print(f"Failed to parse message data: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()

# Note: The original code had a bug where it was adding a websocket route to a router.
# This is not the correct way to do it with FastAPI and python-socketio.
# The correct way is to mount the socketio app on the FastAPI app instance.
# This is done in main.py, so we don't need to do anything here.

async def start_cleanup_task():
    """启动清理任务"""
    async def cleanup():
        while True:
            await asyncio.sleep(60)  # 每分钟清理一次
            # 这里可以添加清理逻辑
            pass
    
    asyncio.create_task(cleanup())
