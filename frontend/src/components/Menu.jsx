import { Link, useNavigate, useLocation } from "react-router-dom";

function Menu({ setIsLoggedIn }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    navigate("/login");
  };

  const links = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/tickets", label: "Tickets" },
    { path: "/parametres", label: "Paramètres" },
  ];

  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "16px 40px",
        background: "linear-gradient(90deg, #0D47A1 0%, #1565C0 100%)",
        fontFamily: "'Segoe UI', Arial, sans-serif",
        boxShadow: "0 2px 10px rgba(0,0,0,0.15)",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "40px" }}>
        <span style={{ color: "white", fontWeight: "800", fontSize: "20px", letterSpacing: "1px" }}>
          VERMEG
        </span>

        <div style={{ display: "flex", gap: "8px" }}>
          {links.map((link) => {
            const active = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                style={{
                  color: "white",
                  textDecoration: "none",
                  fontWeight: active ? "700" : "400",
                  fontSize: "14.5px",
                  padding: "8px 16px",
                  borderRadius: "8px",
                  backgroundColor: active ? "rgba(255,255,255,0.18)" : "transparent",
                  transition: "background-color 0.2s",
                }}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      </div>

      <button
        onClick={handleLogout}
        style={{
          padding: "9px 20px",
          backgroundColor: "white",
          color: "#0D47A1",
          border: "none",
          borderRadius: "8px",
          fontWeight: "600",
          fontSize: "14px",
          cursor: "pointer",
        }}
      >
        Déconnexion
      </button>
    </nav>
  );
}

export default Menu;