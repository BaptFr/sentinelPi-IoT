//Config API
document.addEventListener("DOMContentLoaded", () => {
  fetch("config.json")
    .then(res => res.json())
    .then(config => {
      window.API_URL = config.API_URL;
      initPage(); 
    })
    .catch(err => {
      console.error("Erreur de chargement config.json :", err);
      alert("Erreur lors du chargement de la configuration.");
    });
});

function initPage() {
  //existing form  ?
  const form = document.getElementById("modifierAdminForm");
  if (!form) {
    console.error("Formulaire 'modifierAdminForm' introuvable.");
    return;
  }
  //Admin token connection control
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Session expirée ou accès interdit. Veuillez vous reconnecter.");
    window.location.replace("admin.html");
  }


  //Previous infos recuperation for form 
  fetch(`${API_URL}/api/admin/profile`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Impossible de charger les infos admin");
      return res.json();
    })
    .then((admin) => {
      if (admin.firstname) document.getElementById("firstname").value = admin.firstname;
      if (admin.lastname) document.getElementById("lastname").value = admin.lastname;
      if (admin.email) document.getElementById("email").value = admin.email;
      if (admin.mailConnexionErreur !== undefined) {
      }
    })
    .catch((err) => {
      alert(err.message);
      window.location.href = "admin.html";
    });

  document.getElementById("modifierAdminForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const lastname = document.getElementById("lastname").value.trim();
    const firstname = document.getElementById("firstname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    //Password confirmation  if juste one is modified or modified but not the same

    if (password && confirmPassword && password !== confirmPassword) {
      alert("Les mots de passe ne correspondent pas.");
      return;
    }

    const dataToSend = {
      lastname,
      firstname,
      email,
    };
    if (password) {
      dataToSend.password = password;
    }


    try {
      
      const response = await fetch( API_URL + "/api/admin/profile", {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",

        },
        body: JSON.stringify(dataToSend),
      });

      const result = await response.json();

      if (response.ok) {
        document.getElementById("modifierAdminForm").reset();
        window.location.href = "admin.html";
      } else {
        alert(result.message || "Erreur lors de la modification.");
      }
    } catch (error) {
      console.error("Erreur API :", error);
      alert("Une erreur est survenue lors de l'envoi.");
    }
  });

  const btn = document.querySelector(".return-btn");
  if (btn) {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById("modifierAdminForm").reset();
      window.location.href = "admin.html";
    });
  }
}
