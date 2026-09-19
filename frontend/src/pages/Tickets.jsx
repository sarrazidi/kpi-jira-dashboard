import { useState, useEffect } from "react";

function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/tickets")
      .then((res) => res.json())
      .then((data) => {
        setTickets(data);
        setLoading(false);
      });
  }, []);

  const badgeColor = (statut) => {
    if (statut === "Done" || statut === "Résolu") return "#4CAF50";
    if (statut === "In Progress" || statut === "En cours") return "#2196F3";
    if (statut === "To Do" || statut === "A faire") return "#FFC107";
    return "#9E9E9E";
  };

  return (
    <div style={{ padding: "40px", maxWidth: "1100px", margin: "0 auto", fontFamily: "'Segoe UI', Arial, sans-serif" }}>
      <h1 style={{ marginBottom: "30px" }}>Liste des tickets</h1>

      {loading ? (
        <p>Chargement...</p>
      ) : (
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", boxShadow: "0 2px 10px rgba(0,0,0,0.08)", borderRadius: "10px", overflow: "hidden" }}>
            <thead>
              <tr style={{ backgroundColor: "#0D47A1", color: "white", textAlign: "left" }}>
                <th style={{ padding: "14px" }}>Clé</th>
                <th style={{ padding: "14px" }}>Résumé</th>
                <th style={{ padding: "14px" }}>Type</th>
                <th style={{ padding: "14px" }}>Statut</th>
                <th style={{ padding: "14px" }}>Priorité</th>
                <th style={{ padding: "14px" }}>Assigné</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((t, i) => (
                <tr key={t.cle} style={{ backgroundColor: i % 2 === 0 ? "#fafafa" : "white" }}>
                  <td style={{ padding: "12px", fontWeight: "bold" }}>{t.cle}</td>
                  <td style={{ padding: "12px" }}>{t.resume}</td>
                  <td style={{ padding: "12px" }}>{t.type}</td>
                  <td style={{ padding: "12px" }}>
                    <span style={{
                      backgroundColor: badgeColor(t.statut),
                      color: "white",
                      padding: "4px 10px",
                      borderRadius: "12px",
                      fontSize: "13px"
                    }}>
                      {t.statut}
                    </span>
                  </td>
                  <td style={{ padding: "12px" }}>{t.priorite}</td>
                  <td style={{ padding: "12px" }}>{t.assigne}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Tickets;