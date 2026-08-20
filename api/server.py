import subprocess
from pathlib import Path

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from brain.jarvis_brain import think
from brain.tools import execute

# ---------- AI ----------

# ---------- Socket ----------
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
    return {"status":"online"}

@sio.event
async def connect(sid,environ):
    print("CONNECTED:",sid)

@sio.event
async def disconnect(sid):
    print("DISCONNECTED:",sid)

@sio.event
async def ask(sid,text):
    print("TEXT:",text)

    d=think(text)

    if d["type"]=="tool":
        r=execute(d)
    elif d["type"]=="tools":
        r=execute(d)
    else:
        r=d["text"]

    await sio.emit("reply",str(r),to=sid)

@sio.event
async def audio(sid,data):

    print("AUDIO RECEIVED")

    Path("api/uploads").mkdir(parents=True,exist_ok=True)

    webm="api/uploads/input.webm"
    wav="api/uploads/input.wav"

    with open(webm,"wb") as f:
        f.write(bytes(data))

    subprocess.run(
        [
            "ffmpeg","-y",
            "-i",webm,
            "-ar","16000",
            "-ac","1",
            wav
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    txt="api/uploads/transcript"

    subprocess.run([
        "python","-m","mlx_audio.stt.generate",
        "--model","mlx-community/parakeet-tdt-0.6b-v3",
        "--audio",wav,
        "--output-path",txt
    ],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

    text=Path(txt+".txt").read_text().strip()

    print("TRANSCRIPT:",text)

    d=think(text)

    if d["type"]=="tool":
        r=execute(d)
    elif d["type"]=="tools":
        r=execute(d)
    else:
        r=d["text"]

    await sio.emit("reply",str(r),to=sid)

socket_app=socketio.ASGIApp(sio,other_asgi_app=app)


from fastapi import Body

@app.post("/ask")
async def ask_http(data: dict = Body(...)):
    text=data["text"]

    d=think(text)

    if d["type"]=="tool":
        r=execute(d)
    elif d["type"]=="tools":
        r=execute(d)
    else:
        r=d["text"]

    return {"reply": str(r)}
