import { useState } from "react";

export function useVoiceButton(){
  const [listening,setListening]=useState(false);

  function toggle(){
    setListening(v=>!v);
  }

  return {listening,toggle};
}
