import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login({ setIsLoggedIn }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();

      if (data.success) {
        localStorage.setItem("token", data.token);
        setIsLoggedIn(true);
        navigate("/dashboard");
      } else {
        setError("Email ou mot de passe incorrect");
      }
    } catch (err) {
      setError("Impossible de contacter le serveur");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #1565C0 0%, #0D47A1 100%)",
        fontFamily: "'Segoe UI', Arial, sans-serif",
      }}
    >
      <div
        style={{
          backgroundColor: "white",
          borderRadius: "16px",
          padding: "50px 40px",
          width: "100%",
          maxWidth: "380px",
          boxShadow: "0 20px 50px rgba(0,0,0,0.25)",
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontSize: "32px",
            fontWeight: "800",
            letterSpacing: "1px",
            color: "#0D47A1",
            marginBottom: "6px",
          }}
        >
          VERMEG
        </div>
        <p style={{ color: "#777", marginBottom: "35px", fontSize: "14px" }}>
          Dashboard KPI - Support Jira
        </p>

        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={inputStyle}
            required
          />
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputStyle}
            required
          />

          {error && (
            <p style={{ color: "#E53935", fontSize: "13px", marginTop: "-6px", marginBottom: "16px" }}>
              {error}
            </p>
          )}

          <button type="submit" style={buttonStyle}>
            Se connecter
          </button>
        </form>

        <p style={{ marginTop: "25px", fontSize: "12px", color: "#aaa" }}>
          © {new Date().getFullYear()} Vermeg — Tous droits réservés
        </p>
      </div>
    </div>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  padding: "13px 15px",
  marginBottom: "16px",
  border: "1px solid #ddd",
  borderRadius: "8px",
  fontSize: "14px",
  outline: "none",
  boxSizing: "border-box",
  transition: "border-color 0.2s",
};

const buttonStyle = {
  width: "100%",
  padding: "13px",
  backgroundColor: "#0D47A1",
  color: "white",
  border: "none",
  borderRadius: "8px",
  fontSize: "15px",
  fontWeight: "600",
  cursor: "pointer",
  marginTop: "6px",
};

export default Login;