

import { useState, useEffect, useRef } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendRequest = async () => {
    if (!message.trim()) return;

    setChat((prev) => [...prev, { type: "user", text: message }]);
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("http://127.0.0.1:8000/agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: message })
      });

      const data = await res.json();

      if (data.error) {
        throw new Error("Backend error");
      }

      if (!data.recipes) {
        throw new Error("No recipes returned");
      }

      const recipes = data.recipes;

      let text = "";

      if (recipes) {
        text += "🍽 Starter:\n";
        recipes.starter.forEach((r) => {
          text += "• " + r.strMeal + "\n";
        });

        text += "\n🍛 Main:\n";
        recipes.main.forEach((r) => {
          text += "• " + r.strMeal + "\n";
        });

        text += "\n🍰 Dessert:\n";
        if (recipes.dessert.length === 0) {
          text += "• No dessert\n";
        } else {
          recipes.dessert.forEach((r) => {
            text += "• " + r.strMeal + "\n";
          });
        }
      }

      setChat((prev) => [
        ...prev,
        { type: "bot", text }
      ]);

    } catch (error) {
      setChat((prev) => [
        ...prev,
        { type: "bot", text: "❌ Backend not running or error" }
      ]);
      console.log(error);
    }

    setLoading(false);
  };

  return (
    <div className="container mt-4">

      <h2 className="text-center mb-3">ChefBot Assistant</h2>

      <div className="card shadow" style={{ height: "380px", overflowY: "auto" }}>
        <div className="card-body">

          {chat.map((msg, i) => (
            <div key={i} className={`d-flex mb-2 ${msg.type === "user" ? "justify-content-end" : "justify-content-start"}`}>
              
              <div
                className={`p-3 rounded ${
                  msg.type === "user" ? "bg-success text-white" : "bg-light"
                }`}
                style={{
                  maxWidth: "75%",
                  whiteSpace: "pre-wrap"
                }}
              >
                {msg.text}
              </div>

            </div>
          ))}

          {loading && (
            <p className="text-center text-muted">👨‍🍳 Cooking...</p>
          )}

          <div ref={bottomRef}></div>

        </div>
      </div>

      <div className="input-group mt-3">
        <input
          type="text"
          className="form-control"
          placeholder="Try: indian dinner, american lunch..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendRequest();
            }
          }}
        />
        <button className="btn btn-dark" onClick={sendRequest}>
          Send
        </button>
      </div>

      <footer className="text-center mt-3 text-muted">
        Built by Vaishnavi | ChefBot 🍳
      </footer>

    </div>
  );
}

export default App;