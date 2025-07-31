const photoInput = document.getElementById("photoInput");
const bioInput = document.getElementById("bioInput");
const submitBtn = document.getElementById("submitBtn");

// Activer le bouton que si les deux fichiers sont sélectionnés
function checkInputs() {
  if (photoInput.files.length > 0 && bioInput.files.length > 0) {
    submitBtn.disabled = false;
  } else {
    submitBtn.disabled = true;
  }
}

photoInput.addEventListener("change", checkInputs);
bioInput.addEventListener("change", checkInputs);

//Add user click button
submitBtn.addEventListener("click", async () => {
  const firstname = document.getElementById("prenom").value.trim();
  const lastname = document.getElementById("nom").value.trim();
  const fingerprint = photoInput.files[0];
  const face_data = bioInput.files[0];
  const role = "user";



  if (!firstname || !lastname || !face_data || !fingerprint) {
    alert("Veuillez remplir tous les champs obligatoires.");
    return;
  }

  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("Session expirée. Veuillez vous reconnecter.");
    window.location.href = "login.html";
    return;
  }

  const formData = new FormData();
  formData.append("firstname", firstname);
  formData.append("lastname", lastname);
  formData.append("role", role);
  formData.append("fingerprint", fingerprint);
  formData.append("face_data", face_data);
  for (let pair of formData.entries()) {
  console.log(`${pair[0]}:`, pair[1]);
  }
  //Add user-lock
  try {
    const response = await fetch(API_URL + "/lock-users", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    if (response.status === 401 || response.status === 403) {
      alert("Session expirée. Veuillez vous reconnecter.");
      sessionStorage.removeItem("token");
      window.location.href = "login.html";
      return;
    }

    const result = await response.json();

    if (response.ok) {
    
      document.querySelector("form").reset();
      submitBtn.disabled = true;
      window.location.href = "admin.html";
       alert("Utilisateur ajouté avec succès !");
    } else {
      console.error("Erreur backend :", result); 
      alert(result.detail || result.message || "Erreur lors de l'ajout.");
    }
  } catch (error) {
    console.error("Erreur API :", error);
    alert("Une erreur est survenue.");
  }
});
