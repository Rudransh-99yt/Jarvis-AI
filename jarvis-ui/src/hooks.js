import { useEffect, useRef, useState } from "react";

export function useVoiceButton(onFinalText){
  const [listening,setListening]=useState(false);
  const recognitionRef=useRef(null);

  useEffect(()=>{
    const SR=window.webkitSpeechRecognition || window.SpeechRecognition;

    if(!SR){
      console.log("SpeechRecognition not supported.");
      return;
    }

    const r=new SR();
    r.lang="en-US";
    r.continuous=false;
    r.interimResults=true;

    r.onstart=()=>setListening(true);
    r.onend=()=>setListening(false);

    r.onerror=(e)=>{
      console.log("Speech error:",e.error);
      alert("Mic error: "+e.error);
      setListening(false);
    };

    r.onresult=(e)=>{
      let text="";
      for(let i=0;i<e.results.length;i++){
        text+=e.results[i][0].transcript;
      }

      if(e.results[e.results.length-1].isFinal){
        onFinalText(text);
      }
    };

    recognitionRef.current=r;
  },[onFinalText]);

  async function toggle(){

    if(!recognitionRef.current){
      alert("Speech Recognition isn't supported in this browser.");
      return;
    }

    try{
      await navigator.mediaDevices.getUserMedia({audio:true});
    }catch(err){
      alert("Please allow microphone access.");
      return;
    }

    if(listening){
      recognitionRef.current.stop();
    }else{
      recognitionRef.current.start();
    }
  }

  return {listening,toggle};
}
