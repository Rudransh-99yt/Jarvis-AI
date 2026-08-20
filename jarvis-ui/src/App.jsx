import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";

const socket = io("http://127.0.0.1:8000",{transports:["websocket"]});

export default function App(){

  const [text,setText]=useState("");
  const [thinking,setThinking]=useState(false);
  const [messages,setMessages]=useState([
    {role:"assistant",text:"Jarvis online."}
  ]);

  const endRef=useRef(null);

  useEffect(()=>{
    socket.on("reply",(msg)=>{
      setMessages(m=>[...m,{role:"assistant",text:String(msg)}]);
      setThinking(false);
    });

    return()=>socket.off("reply");
  },[]);

  useEffect(()=>{
    endRef.current?.scrollIntoView({behavior:"smooth"});
  },[messages]);

  function ask(){

    if(!text.trim()) return;

    setMessages(m=>[...m,{role:"user",text}]);
    socket.emit("ask",text);
    setThinking(true);
    setText("");
  }

  return(
    <div className="jarvis">

      <h1>JARVIS</h1>

      <div className="chat">

        {messages.map((m,i)=>(
          <div key={i} className={`bubble ${m.role}`}>
            {m.text}
          </div>
        ))}

        {thinking&&<div className="bubble assistant">Thinking...</div>}

        <div ref={endRef}/>

      </div>

      <div className="inputBar">

        <input
          value={text}
          onChange={e=>setText(e.target.value)}
          onKeyDown={e=>e.key==="Enter"&&ask()}
          placeholder="Ask Jarvis..."
        />

        <button onClick={ask}>Send</button>

      </div>

    </div>
  );
}
