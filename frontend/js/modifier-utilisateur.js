
//ID recuperation
const urlParams = new URLSearchParams(window.location.search);
const userId = urlParams.get("id");

if (!userId) {
    alert("Aucun utilisateur sélectionné");
}

//Admin token connection control
const token = sessionStorage.getItem("token");
if (!token) {
  alert("Session expirée ou accès interdit. Veuillez vous reconnecter.");
  window.location.href = "login.html";
}

//User id recuperation
window.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get("id");
  if (!userId) {
    alert("Aucun utilisateur sélectionné");
    window.location.href = "admin.html";
    return;
  }

  // User infos recuperation for the form
  fetch(`${API_URL}/lock-users/${userId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Utilisateur non trouvé");
      return res.json();
    })
    .then((user) => {
      document.getElementById("lastname").value = user.lastname;
      document.getElementById("firstname").value = user.firstname;
      const photoStatus = document.getElementById("photoStatus");
      const empreinteStatus = document.getElementById("empreinteStatus");

      if (photoStatus) {
        photoStatus.textContent = user.face_data_path ? "✔️ Présente" : "❌ Absente";
      }
      if (empreinteStatus) {
        empreinteStatus.textContent = user.fingerprint_path ? "✔️ Présente" : "❌ Absente";
      }
    })
    .catch((err) => {
      alert(err.message);
      window.location.href = "admin.html";
    });

  document.getElementById("modifierUserForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const lastname = document.getElementById("lastname").value.trim();
    const firstname = document.getElementById("firstname").value.trim();
    const face_data = document.getElementById("face_data").files[0];
    const fingerprint = document.getElementById("fingerprint").files[0];

  
    const formData = new FormData();
    formData.append("lastname", lastname);
    formData.append("firstname", firstname);
    formData.append("role", "user");

    if (face_data) {
      formData.append("face_data", face_data);
    }

    if (fingerprint) {
      formData.append("fingerprint", fingerprint);
    }

    try {
      
      const response = await fetch(`${API_URL}/lock-users/${userId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}` 
        },
        body: formData,
      });

      if (response.ok) {
        document.getElementById("modifierUserForm").reset();
        window.location.href = "admin.html";
      } else {
        const result = await response.json();
        alert(result.message || "Erreur lors de la modification.");
      }
    } catch (error) {
      console.error("Erreur API :", error);
      alert("Une erreur est survenue lors de l'envoi.");
    }
  });
});

const btn = document.querySelector(".return-btn");
if (btn) {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    window.location.href = "admin.html";
  });
}
