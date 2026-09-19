function Parametres() {
  return (
    <div style={{ padding: "40px", maxWidth: "700px", margin: "0 auto", fontFamily: "'Segoe UI', Arial, sans-serif" }}>
      <h1 style={{ marginBottom: "30px" }}>Paramètres</h1>

      <div style={{ backgroundColor: "#f5f7fa", borderRadius: "10px", padding: "25px", boxShadow: "0 2px 10px rgba(0,0,0,0.06)" }}>
        <h3 style={{ marginTop: 0 }}>À propos</h3>
        <p>Dashboard KPI - Support Jira</p>
        <p>Ce tableau de bord affiche les indicateurs de performance du support (statuts, types, priorités, volume, temps de résolution, SLA) extraits automatiquement depuis Jira.</p>

        <h3>Connexion</h3>
        <p>Connecté en tant qu'administrateur.</p>
      </div>
    </div>
  );
}

export default Parametres;