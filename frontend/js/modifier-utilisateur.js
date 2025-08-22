//Config Api:
window.addEventListener("configLoaded", () => {
    initPage(); 
});

function initPage() {
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
    window.location.replace("admin.html");
  }

  //User id recuperation
  if (!userId) {
    alert("Aucun utilisateur sélectionné");
    window.location.replace("admin.html");
    return;
  }

  // User infos recuperation for the form
  fetch(`${API_URL}/api/lock-users/${userId}`, {
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
      const empreinteStatus = document.getElementById("empreinteStatus");

      if (empreinteStatus) {
        empreinteStatus.textContent = user.fingerprint_path ? "✔️ Présente" : "❌ Absente";
      }
    })
    .catch((err) => {
      alert(err.message);
      window.location.replace("admin.html");
    });

  //Using form data not JSON  for  possible evolution of the application (picture, file...)
  document.getElementById("modifierUserForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const lastname = document.getElementById("lastname").value.trim();
    const firstname = document.getElementById("firstname").value.trim();

    const formData = new FormData();
    formData.append("lastname", lastname);
    formData.append("firstname", firstname);
    formData.append("role", "user");

    // if (face_data) {
    //   formData.append("face_data", face_data);
    // }

    // if (fingerprint) {
    //   formData.append("fingerprint", fingerprint);
    // }

    try {
    
      const response = await fetch(`${API_URL}/api/lock-users/${userId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}` 
        },
        body: formData,
      });

      if (response.ok) {
        document.getElementById("modifierUserForm").reset();
        window.location.replace("admin.html");
      } else {
        const result = await response.json();
        alert(result.message || "Erreur lors de la modification.");
      }
    } catch (error) {
      console.error("Erreur API complète :", error);
      alert("Une erreur est survenue lors de l'envoi : " + (error.message || JSON.stringify(error)));
    }
  });
  

  const btn = document.querySelector(".return-btn");
  if (btn) {
    btn.addEventListener("click", (e) => {
       e.preventDefault();
      window.location.replace("admin.html");
    });
  }
}
