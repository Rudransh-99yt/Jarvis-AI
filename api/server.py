import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from brain.jarvis_brain import think
from brain.tools import execute

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["http://localhost:5173"],
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "online"}

@sio.event
async def connect(sid, environ):
    print(f"✅ Connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"❌ Disconnected: {sid}")

@sio.event
async def ask(sid, text):
    decision = think(text)

    if decision["type"] == "tool":
        reply = execute(decision)
    elif decision["type"] == "tools":
        reply = execute(decision)
    else:
        reply = decision["text"]

    if isinstance(reply, list):
        reply = "\n".join(map(str, reply))
    elif isinstance(reply, dict):
        reply = reply.get("text", str(reply))
    else:
        reply = str(reply)

    await sio.emit("reply", reply, to=sid)

socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
