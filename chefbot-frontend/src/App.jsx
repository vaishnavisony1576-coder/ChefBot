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
    if (!message) return;

    setChat((prev) => [...prev, { type: "user", text: message }]);
    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("https://chefbot-2-li8u.onrender.com/generate-recipe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: message })
      });

      const data = await res.json();

      setChat((prev) => [
        ...prev,
        { type: "bot", text: data.recipe || data.error }
      ]);

    } catch {
      setChat((prev) => [
        ...prev,
        { type: "bot", text: "❌ Server error" }
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="container mt-4">

      <h2 className="text-center mb-3">🍳 ChefBot Assistant</h2>

      <p className="text-center text-muted">
  ChefBot is an AI-powered cooking assistant that suggests recipes based on ingredients you have at home.
</p>

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
    textAlign: msg.type === "user" ? "right" : "left",
    whiteSpace: "pre-wrap",
    wordWrap: "break-word",
    overflowWrap: "break-word"
  }}
>
   {msg.text.split("\n").map((line, i) => {
    
    // Recipe Name (big + bold)
    if (line.toLowerCase().includes("recipe name:")) {
      return (
        <h5 key={i} style={{ fontWeight: "bold", marginTop: "10px" }}>
          {line.replace(/^\d+\.\s*/, "")}
        </h5>
      );
    }

    // Subheadings (Ingredients / Steps)
    if (
      line.toLowerCase().includes("ingredients:") ||
      line.toLowerCase().includes("steps:")
    ) {
      return (
        <p key={i} style={{ fontWeight: "bold", marginTop: "10px" }}>
          {line}
        </p>
      );
    }

    // Normal text
    return <p key={i}>{line}</p>;
  })}
</div>

            </div>
          ))}

          {loading && (
            <p className="text-center text-muted">👨‍🍳 Cooking recipes...</p>
          )}

          <div ref={bottomRef}></div>

        </div>
      </div>

      <div className="input-group mt-3">
        <input
  type="text"
  className="form-control"
  placeholder="Try: paneer, rice, butter..."
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
        <div className="mt-3 p-3 bg-light rounded text-start">
  <h6><strong>💡 Try asking:</strong></h6>
  <ol style={{ marginBottom: 0 }}>
    <li>I have paneer and rice, suggest recipes</li>
    <li>What can I cook with chicken and butter?</li>
    <li>Give me a quick breakfast using eggs</li>
    <li>Suggest a spicy Indian recipe with potatoes</li>
    <li>Easy dinner recipe with vegetables</li>
  </ol>
</div>
      <footer className="text-center mt-3 text-muted">
        Built by Vaishnavi Gungone | Built for GenAI Internship
      </footer>

    </div>
  );
}

export default App;