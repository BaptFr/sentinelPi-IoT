// admin.js

document.addEventListener("DOMContentLoaded", () => {
  verifierConnexion();
  chargerUtilisateurs();
  chargerHistorique();
});

function verifierConnexion() {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Session expirée. Veuillez vous reconnecter.");
    window.location.href = "login.html";
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
    const response = await fetch(API_URL + "/lock-users", {
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

        tr.innerHTML = `
          <td>${user.lastname}</td>
          <td>${user.firstname}</td>
          <td>
            <img src="${user.photoURL}" alt="photo" width="50" />
            <input type="file" accept="image/*" onchange="modifierMediaUtilisateur('${user.id}', 'photo', this.files[0])" />
          </td>
          <td>
            <img src="${user.empreinteURL}" alt="empreinte" width="50" />
            <input type="file" accept="image/*" onchange="modifierMediaUtilisateur('${user.id}', 'empreinte', this.files[0])" />
          </td>
          <td>
            <button onclick="modifierUtilisateur('${user.id}')">✏️</button>
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
    const response = await fetch(`https://URL_API/utilisateurs/${id}/${type}`, {
      method: "PATCH",
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
        <td>${item.nom}</td>
        <td>${item.prenom}</td>
        <td>${item.date}</td>
        <td>${item.heure}</td>
        <td>${item.resultat}</td>
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

async function supprimerUtilisateur(id) {
  const token = sessionStorage.getItem("token");
  if (!confirm("Supprimer cet utilisateur ?")) return;

  try {
    const response = await fetch(API_URL + `/lock-users/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (response.ok) {
      alert("Utilisateur supprimé.");
      chargerUtilisateurs();
    } else {
      alert("Erreur lors de la suppression.");
    }
  } catch (error) {
    console.error("Erreur suppression :", error);
  }
}
