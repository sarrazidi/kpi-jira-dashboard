import { useState, useEffect } from "react";
import { Bar, Pie, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, PointElement, LineElement, Title, Tooltip, Legend);

function Dashboard() {
  const [statutData, setStatutData] = useState([]);
  const [typeData, setTypeData] = useState([]);
  const [prioriteData, setPrioriteData] = useState([]);
  const [tempsData, setTempsData] = useState(null);
  const [volumeData, setVolumeData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/kpi/statut").then((r) => r.json()).then(setStatutData);
    fetch("http://localhost:5000/api/kpi/type").then((r) => r.json()).then(setTypeData);
    fetch("http://localhost:5000/api/kpi/priorite").then((r) => r.json()).then(setPrioriteData);
    fetch("http://localhost:5000/api/kpi/temps").then((r) => r.json()).then(setTempsData);
    fetch("http://localhost:5000/api/kpi/volume").then((r) => r.json()).then(setVolumeData);
  }, []);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { labels: { font: { size: 13, family: "'Segoe UI', Arial" }, color: "#333" } },
    },
  };

  const statutChart = {
    labels: statutData.map((item) => item.statut),
    datasets: [{ label: "Tickets", data: statutData.map((i) => i.nombre_tickets), backgroundColor: ["#2196F3", "#4CAF50", "#FFC107", "#F44336", "#9C27B0"], borderRadius: 8 }],
  };

  const typeChart = {
    labels: typeData.map((item) => item.type),
    datasets: [{ data: typeData.map((i) => i.nombre_tickets), backgroundColor: ["#0D47A1", "#00BCD4", "#7E57C2", "#26A69A"] }],
  };

  const prioriteChart = {
    labels: prioriteData.map((item) => item.priorite),
    datasets: [{ label: "Tickets", data: prioriteData.map((i) => i.nombre_tickets), backgroundColor: ["#F44336", "#FF9800", "#FFEB3B", "#8BC34A"], borderRadius: 8 }],
  };

  const volumeChart = {
    labels: volumeData.map((item) => item.date || item.jour),
    datasets: [{ label: "Tickets créés", data: volumeData.map((i) => i.nombre_tickets), borderColor: "#0D47A1", backgroundColor: "rgba(13,71,161,0.15)", tension: 0.35, fill: true }],
  };

  const pageStyle = {
    minHeight: "100vh",
    backgroundColor: "#F0F3F8",
    fontFamily: "'Segoe UI', Arial, sans-serif",
    padding: "40px",
  };

  const containerStyle = { maxWidth: "1200px", margin: "0 auto" };

  const gridStyle = { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginTop: "30px" };

  const cardStyle = {
    backgroundColor: "white",
    borderRadius: "14px",
    padding: "24px",
    boxShadow: "0 4px 16px rgba(0,0,0,0.06)",
  };

  const kpiGridStyle = { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "16px", marginTop: "10px" };

  const kpiBoxStyle = (color) => ({
    background: `linear-gradient(135deg, ${color}15, ${color}05)`,
    borderLeft: `4px solid ${color}`,
    borderRadius: "10px",
    padding: "22px",
    textAlign: "center",
  });

  return (
    <div style={pageStyle}>
      <div style={containerStyle}>
        <h1 style={{ color: "#0D47A1", fontSize: "28px", fontWeight: "800", marginBottom: "4px" }}>
          Dashboard KPI — Support Jira
        </h1>
        <p style={{ color: "#888", marginTop: 0 }}>Vue d'ensemble des tickets et performances du support</p>

        <div style={gridStyle}>
          <div style={cardStyle}>
            <h2 style={{ fontSize: "17px", color: "#333", marginTop: 0 }}>Tickets par statut</h2>
            <Bar data={statutChart} options={chartOptions} />
          </div>

          <div style={cardStyle}>
            <h2 style={{ fontSize: "17px", color: "#333", marginTop: 0 }}>Tickets par type</h2>
            <Pie data={typeChart} options={chartOptions} />
          </div>

          <div style={cardStyle}>
            <h2 style={{ fontSize: "17px", color: "#333", marginTop: 0 }}>Tickets par priorité</h2>
            <Bar data={prioriteChart} options={chartOptions} />
          </div>

          <div style={cardStyle}>
            <h2 style={{ fontSize: "17px", color: "#333", marginTop: 0 }}>Temps de résolution & SLA</h2>
            {tempsData ? (
              <div style={kpiGridStyle}>
                <div style={kpiBoxStyle("#2196F3")}>
                  <h3 style={{ margin: 0, fontSize: "26px", color: "#2196F3" }}>{tempsData.nombre_tickets_resolus}</h3>
                  <p style={{ margin: "6px 0 0", color: "#666", fontSize: "13px" }}>Tickets résolus</p>
                </div>
                <div style={kpiBoxStyle("#FF9800")}>
                  <h3 style={{ margin: 0, fontSize: "26px", color: "#FF9800" }}>{tempsData.temps_moyen_heures ?? "N/A"}</h3>
                  <p style={{ margin: "6px 0 0", color: "#666", fontSize: "13px" }}>Temps moyen (h)</p>
                </div>
                <div style={kpiBoxStyle("#4CAF50")}>
                  <h3 style={{ margin: 0, fontSize: "26px", color: "#4CAF50" }}>{tempsData.sla_respecte_pourcentage ?? "N/A"}%</h3>
                  <p style={{ margin: "6px 0 0", color: "#666", fontSize: "13px" }}>SLA respecté</p>
                </div>
              </div>
            ) : (
              <p>Chargement...</p>
            )}
          </div>

          <div style={{ ...cardStyle, gridColumn: "1 / -1" }}>
            <h2 style={{ fontSize: "17px", color: "#333", marginTop: 0 }}>Volume de tickets par jour</h2>
            {volumeData.length > 0 ? <Line data={volumeChart} options={chartOptions} /> : <p>Aucune donnée de volume disponible.</p>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;