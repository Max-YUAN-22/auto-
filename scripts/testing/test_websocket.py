import websockets
import asyncio

async def test_websocket():
    try:
        async with websockets.connect('ws://localhost:8000/ws') as ws:
            print("WebSocket connection established")
            await ws.send('{"type":"simulation_step"}')
            while True:
                response = await ws.recv()
                print(f"Received response: {response}")
    except Exception as e:
        print(f"WebSocket connection failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.get_event_loop().run_until_complete(test_websocket())
    print("Test result:", "Success" if result else "Failed")
