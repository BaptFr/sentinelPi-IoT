
// API config load
window.addEventListener("configLoaded", () => {
    console.log("configLoaded started (admin) ");

    verifierConnexion();
    chargerUtilisateurs();
    chargerHistorique();


  function verifierConnexion() {
    const token = sessionStorage.getItem("token");
    if (!token) {
      alert("Session expirée. Veuillez vous reconnecter.");
      window.location.href ="login.html";
    }
  }

  function deconnexion() {
    sessionStorage.removeItem("token");
    window.location.href = "login.html";
  }

  async function chargerUtilisateurs() {
    const token = sessionStorage.getItem("token");

  //lock-users list
    try {
      const response = await fetch(API_URL + "/api/lock-users", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.status === 401 || response.status === 403) {
        deconnexion();
        return;
      }

      const utilisateurs = await response.json();
      const userList = document.getElementById("user-list");
      userList.innerHTML = "";

      if (utilisateurs.length === 0) {
        userList.innerHTML = "<tr><td colspan='6'>Aucun utilisateur trouvé.</td></tr>";
      } else {
        utilisateurs.forEach(user => {
          const tr = document.createElement("tr");
          console.log(user)
          tr.innerHTML = `
            <td>${user.lastname}</td>
            <td>${user.firstname}</td>
            <td>${user.fingerprint_id ? '✅ Accès Serrure 1' : '❌'}</td>
            <td>
              <button onclick="window.location.href='modifier-utilisateur.html?id=${user.id}'">✏️</button>
              <button onclick="supprimerUtilisateur('${user.id}')">🗑️</button>
            </td>
          `;

          userList.appendChild(tr);
        });
      }
    } catch (error) {
      console.error("Lock_users llist loading error :", error);
    }
  }

  async function modifierMediaUtilisateur(id, type, fichier) {
    const token = sessionStorage.getItem("token");

    if (!fichier || !["image/jpeg", "image/png", "image/jpg", "image/webp", "image/bmp", "image/svg+xml"].includes(fichier.type)) {
      alert("Format de fichier non supporté.");
      return;
    }

    const formData = new FormData();
    formData.append(type, fichier);

    try {
      const response = await fetch(API_URL+ "api/${id}/${type}", {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        alert(`${type} modifié avec succès.`);
        chargerUtilisateurs();
      } else {
        alert(`Erreur lors de la mise à jour de ${type}.`);
      }
    } catch (error) {
      console.error(`Erreur mise à jour ${type}:`, error);
    }
  }

  async function chargerHistorique() {
    const token = sessionStorage.getItem("token");

    try {
      const response = await fetch("https://URL_API/historique", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.status === 401 || response.status === 403) {
        deconnexion();
        return;
      }

      const historique = await response.json();
      const historyList = document.getElementById("history-list");
      historyList.innerHTML = "";

      historique.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${item.lastname}</td>
          <td>${item.firstname}</td>
          <td>${item.date}</td>
          <td>${item.heure}</td>
          <td>${item.result}</td>
        `;
        historyList.appendChild(tr);
      });
    } catch (error) {
      console.error("Erreur historique :", error);
    }
  }

  async function viderHistorique() {
    const token = sessionStorage.getItem("token");
    if (!confirm("Voulez-vous vraiment vider l’historique ?")) return;

    try {
      const response = await fetch("https://URL_API/historique", {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        alert("Historique vidé.");
        chargerHistorique();
      } else {
        alert("Erreur lors du nettoyage.");
      }
    } catch (error) {
      console.error("Erreur suppression historique :", error);
    }
  }

  function modifierUtilisateur(id) {
    window.location.href = `modifier-utilisateur.html?id=${id}`;
  }
})

function supprimerUtilisateur(id) {
  if (confirm("ÊTES VOUS SÛR DE VOULOIR SUPPRIMER CET UTILISATEUR ?")) {
    fetch(`${API_URL}/api/lock-users/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem("token")}`,
      },
    })
      .then((res) => {
        console.log("Status code:", res.status); //debug

        if (!res.ok) throw new Error("Error during supression ");
        alert("Utilisateur supprimé.");
        location.reload(); //Update realoading
      })
      .catch((err) => {
        console.error("Suppression error:", err);
        alert("Erreur lors de la suppression.");
      });
  }
}
