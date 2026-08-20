import { useEffect, useState, useRef } from "react";
import { io } from "socket.io-client";
import { Mic, Cpu, Sparkles, Activity } from "lucide-react";
import { motion } from "framer-motion";
import "./App.css";

const socket = io("http://127.0.0.1:8000",{transports:["websocket"]});

export default function App(){

  const [reply,setReply]=useState("Jarvis online.");
  const [transcript,setTranscript]=useState("");
  const [thinking,setThinking]=useState(false);
  const [listening,setListening]=useState(false);

  const recognitionRef=useRef(null);

  useEffect(()=>{
    socket.on("reply",(msg)=>{
      setReply(msg);
      setThinking(false);
    });

    const SpeechRecognition=
      window.SpeechRecognition||window.webkitSpeechRecognition;

    if(SpeechRecognition){

      const r=new SpeechRecognition();

      r.continuous=false;
      r.interimResults=true;
      r.lang="en-US";

      r.onstart=()=>setListening(true);

      r.onresult=(e)=>{
        const text=Array.from(e.results)
          .map(r=>r[0].transcript)
          .join("");

        setTranscript(text);

        if(e.results[e.results.length-1].isFinal){
          setThinking(true);
          socket.emit("ask",text);
        }
      };

      r.onend=()=>setListening(false);

      recognitionRef.current=r;
    }

    return()=>socket.off("reply");

  },[]);

  function toggleMic(){

    if(!recognitionRef.current){
      alert("Speech recognition not supported.");
      return;
    }

    if(listening)
      recognitionRef.current.stop();
    else{
      setTranscript("");
      recognitionRef.current.start();
    }
  }

  return(
    <div className="jarvis">

      <motion.div
        className="orb"
        animate={{scale:[1,1.05,1],opacity:[0.8,1,0.8]}}
        transition={{duration:2,repeat:Infinity}}
      />

      <h1>JARVIS</h1>
      <p className="subtitle">Local AI Operating System</p>

      <div className="grid">

        <div className="card">
          <Mic/>
          <h3>Voice</h3>
          <p>{listening?"Listening...":"Ready"}</p>
        </div>

        <div className="card">
          <Cpu/>
          <h3>Brain</h3>
          <p>Qwen</p>
        </div>

        <div className="card">
          <Sparkles/>
          <h3>Tools</h3>
          <p>macOS</p>
        </div>

        <div className="card">
          <Activity/>
          <h3>Status</h3>
          <p>{thinking?"Thinking":"Online"}</p>
        </div>

      </div>

      <div className="listen">
        <div className="ring"></div>
        <div className="ring delay"></div>

        <button onClick={toggleMic}>
          {listening?"🔴":"🎙️"}
        </button>
      </div>

      <div className="card reply-card">
        <h3>You</h3>
        <pre>{transcript||"Press the mic."}</pre>
      </div>

      <div className="card reply-card">
        <h3>Jarvis</h3>
        <pre>{reply}</pre>
      </div>

    </div>
  );
}
