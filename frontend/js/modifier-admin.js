

//Admin token connection control
const token = sessionStorage.getItem("token");
if (!token) {
  alert("Session expirée ou accès interdit. Veuillez vous reconnecter.");
  window.location.href = "login.html";
}

document.getElementById("modifierAdminForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const lastname = document.getElementById("lastname").value.trim();
  const firstname = document.getElementById("firstname").value.trim();
  const email = document.getElementById("email").value.trim();
  const fingerprint = document.getElementById("photo").files[0];
  const face_data = document.getElementById("empreinte").files[0];

  const notifConnexionReussie = document.getElementById("notifConnexionReussie").checked;
  const notifConnexionErreur = document.getElementById("notifConnexionErreur").checked;
  const mailConnexionReussie = document.getElementById("mailConnexionReussie").checked;
  const mailConnexionErreur = document.getElementById("mailConnexionErreur").checked;

  const formData = new FormData();
  formData.append("lastname", lastname);
  formData.append("firstname", firstname);
  formData.append("email", email);
  formData.append("notifConnexionReussie", notifConnexionReussie);
  formData.append("notifConnexionErreur", notifConnexionErreur);
  formData.append("mailConnexionReussie", mailConnexionReussie);
  formData.append("mailConnexionErreur", mailConnexionErreur);

  if (photo) {
    formData.append("face_data", face_data);
  }

  if (empreinte) {
    formData.append("fingerprint", fingerprint);
  }

  try {
    
    const response = await fetch(URL + "/admin/:id", {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}` 
      },
      body: formData,
    });

    const result = await response.json();

    if (response.ok) {
      document.getElementById("modifierAdminForm").reset();
      window.location.href = "admin.html";
      alert("Modification enregistrée avec succès !");
    } else {
      alert(result.message || "Erreur lors de la modification.");
    }
  } catch (error) {
    console.error("Erreur API :", error);
    alert("Une erreur est survenue lors de l'envoi.");
  }
});
