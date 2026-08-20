import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";

const socket = io("http://127.0.0.1:8000",{transports:["websocket"]});

export default function App(){

  const [reply,setReply]=useState("Jarvis online.");
  const [listening,setListening]=useState(false);
  const recorder=useRef(null);

  useEffect(()=>{
    socket.on("reply",setReply);
    return()=>socket.off("reply");
  },[]);

  async function toggle(){

    if(listening){
      recorder.current.stop();
      setListening(false);
      return;
    }

    const stream=await navigator.mediaDevices.getUserMedia({audio:true});

    recorder.current=new MediaRecorder(stream);

    const chunks=[];

    recorder.current.ondataavailable=e=>chunks.push(e.data);

    recorder.current.onstop=async()=>{

      const blob=new Blob(chunks,{type:"audio/webm"});

      const buffer=await blob.arrayBuffer();
socket.emit("audio",new Uint8Array(buffer));
    };

    recorder.current.start();

    setListening(true);
  }

  return(
    <div className="jarvis">

      <h1>JARVIS</h1>

      <button className="mic" onClick={toggle}>
        {listening?"🔴 Stop":"🎙️ Speak"}
      </button>

      <div className="card">
        <pre>{reply}</pre>
      </div>

    </div>
  );
}
