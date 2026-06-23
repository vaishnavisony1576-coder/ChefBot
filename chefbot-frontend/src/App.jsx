import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [data, setData] = useState(null);
  const [status, setStatus] = useState("idle");
  const [selectedItem, setSelectedItem] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const userId =
    localStorage.getItem("user_id") ||
    "user_" + Math.random().toString(36).substring(2);

  localStorage.setItem("user_id", userId);

const showItems = (items) => {
  if (!items || items.length === 0)
    return <p className="text-muted">No items</p>;

  return items.map((item, index) => (
    <div
      key={`${item.name}-${index}`}
      className="card m-3 p-2 shadow"
      style={{
        width: "18rem",
        cursor: "pointer",
        transition: "0.3s",
      }}
      onClick={() => setSelectedItem(item)}
    >
      <img
        src={item.image || "https://via.placeholder.com/300"}
        className="card-img-top"
        style={{ borderRadius: "10px" }}
      />

      <div className="card-body">
        <h5>{item.name}</h5>
      </div>
    </div>
  ));
};

  const generate = async () => {
    try {
      setStatus("loading");

      const res = await fetch("http://127.0.0.1:8000/agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          user_id: userId,
        }),
      });

      const result = await res.json();
      if (result.error) {
        setStatus("error");
        setErrorMsg(result.error); 
        setData(null);
        return;
      }
      setData(result);
      setStatus("done");
    } catch (e) {
  console.log(e);
  setStatus("error");
  setErrorMsg("⚠️ Please try again later");
}
  };


  const plan = data?.structured_output?.plan;
  const memory = data?.memory;

  return (
    <div className="min-vh-100 d-flex flex-column justify-content-between text-center">

      {/* 🔥 HEADER */}
      <h1 className="fw-bold display-5 mt-5">🍳 ChefBot AI</h1>
      <p className="text-light">
      Your intelligent recipe planner with memory & AI suggestions
      </p>

      {/* 🔥 EXAMPLE QUERIES */}
      <div className="mb-4">
        <p className="text-light fw-bold">✨ Try these:</p>

        <div className="d-flex justify-content-center flex-wrap gap-2">
          {[
            "spicy indian dinner",
            "healthy breakfast",
            "veg lunch",
            "high protein meal",
            "quick snacks"
          ].map((q, i) => (
            <button
              key={i}
              className="btn btn-outline-light rounded-pill px-3 py-1 try-btn"
              onClick={() => setQuery(q)}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* 🔥 INPUT */}
        <div className="d-flex justify-content-center mb-4">
        <input
          className="form-control w-50 shadow"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && generate()}
          placeholder="Try: spicy indian dinner..."
        />
        <button className="btn btn-warning ms-2 shadow" onClick={generate}>
          Generate 🍽️
        </button>
      </div>


      {/* 🔥 STATUS */}
      <div className="mb-3">
        {status === "loading" && <p className="text-warning text-white">⚙️ Planning your meal...</p>}
        {status === "done" && <p className="text-success text-white">✅ Ready!</p>}
        {status === "error" && (<p className="text-warning fw-bold">{errorMsg}</p>)}
      </div>

      {/* 🔥 MEMORY */}

      {/* 🔥 OUTPUT */}
      {plan && (
        <>
          <h3 className="text-warning text-white bold">🥗 Starter</h3>
          <div className="d-flex flex-wrap justify-content-center">
            {showItems(plan.starter)}
          </div>

          <h3 className="text-warning text-white">🍛 Main Course</h3>
          <div className="d-flex flex-wrap justify-content-center">
            {showItems(plan.main)}
          </div>

          <h3 className="text-warning text-white">🍰 Dessert</h3>
          <div className="d-flex flex-wrap justify-content-center">
            {showItems(plan.dessert)}
          </div>
        </>
      )}

      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          
          <div className="modal-card text-start" onClick={(e) => e.stopPropagation()}>
            
            <img
              src={selectedItem.image || "https://via.placeholder.com/300"}
              className="modal-img"
            />

            <h3 className="text-start">{selectedItem.name}</h3>

            <p className="fw-bold mt-3" ><b>Ingredients:</b></p>
            <ul className = "ps-3">
              {Array.isArray(selectedItem.ingredients)
                ? selectedItem.ingredients.map((i, idx) => (
                    <li key={idx}>{i}</li>
                  ))
                : <li>No ingredients</li>}
            </ul>

            <p className="fw-bold mt-3" ><b>Steps:</b></p>
            <ol className = "ps-3">
              {Array.isArray(selectedItem.steps)
                ? selectedItem.steps.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))
                : <li>No steps</li>}
            </ol>

            <button
              className="btn btn-danger mt-2"
              onClick={() => setSelectedItem(null)}
            >
              Close
            </button>

          </div>
        </div>
      )}

      {/* 🔥 FOOTER */}
      <footer className="mt-5 text-center text-light">
      <p>
        Vaishnavi | Built for GENAI Internship
      </p>
    </footer>
    </div>
  );
}

export default App;
