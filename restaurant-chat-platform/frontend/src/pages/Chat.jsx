import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Chat() {
  const { roomId } = useParams();
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");
  let ws;

  useEffect(() => {
    ws = new WebSocket(`ws://localhost:8000/ws/${roomId}`);

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    return () => ws.close();
  }, [roomId]);

  const sendMessage = () => {
    if (ws && message.trim()) {
      ws.send(message);
      setMessage("");
    }
  };


  return (
    <div>
      <h1>Chat Room {roomId}</h1>
      <div>
        {messages.map((msg, i) => (
          <p key={i}>{msg}</p>
        ))}
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chat;

