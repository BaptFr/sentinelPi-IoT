//Config API
window.addEventListener("configLoaded", () => {
  const firstnameCheck = document.getElementById("prenom")
  const lastnameCheck = document.getElementById("nom")
  const photoInput = document.getElementById("photoInput");
  const addUserSubmitBtn = document.getElementById("addUserSubmitBtn");
  const enrollmentSubmitBtn = document.getElementById("enrollmentSubmitBtn");

  function checkInputs() {
    if (firstnameCheck.value.trim() !=="" && lastnameCheck.value.trim() !=="") {
      enrollmentSubmitBtn.disabled = false;
    } else {
      enrollmentSubmitBtn.disabled = true;
    }
  }

  function checkPhotoInput () {
    if (firstnameCheck.value.trim() !=="" && lastnameCheck.value.trim() !=="" & photoInput.files.length > 0 ) {
      addUserSubmitBtn.disabled = false;
    } else {
      addUserSubmitBtn.disabled = true;
    }
  }


    photoInput.addEventListener("change", checkPhotoInput);
    firstnameCheck.addEventListener("input", checkInputs);
    lastnameCheck.addEventListener("input", checkInputs);

  //******Enrollment procedur click button******
    enrollmentSubmitBtn.addEventListener("click", async () => {
      const firstname = document.getElementById("prenom").value.trim();
      const lastname = document.getElementById("nom").value.trim();
      const role = "user";

      if (!firstname || !lastname) {
        alert("Veuillez remplir tous les champs obligatoires.");
        return;
      }

      const token = sessionStorage.getItem("token");
      if (!token) {
        alert("Session expirée. Veuillez vous reconnecter.");
        window.location.href = "login.html";
        return;
      }

      //POST to enrollment process
      try {
      const response = await fetch(API_URL + "/enrollment/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({firstname, lastname, role})
      });

      if (response.status === 401 || response.status === 403) {
        alert("Session expirée. Veuillez vous reconnecter.");
        sessionStorage.removeItem("token");
        window.location.href = "login.html";
        return;
      }

      if (response.ok) {
        const result = await response.json();
        console.log(result);
        alert("Enrôlement d'empreinte initié.");
      } else {
        const result = await response.json();
        alert(result.detail || result.message || "Erreur lors de la procédure l'enrôlement.");
      }
    } catch (error) {
      console.error("API Error:", error);
      alert("Une erreur est survenue.");
    }
  });

    /****** A DEFINIR ??  ******/       
  //Add user with face_data click button
  addUserSubmitBtn.addEventListener("click", async () => {
    const firstname = document.getElementById("prenom").value.trim();
    const lastname = document.getElementById("nom").value.trim();
    const face_data =  photoInput.files[0];
    const role = "user";



    if (!firstname || !lastname) {
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
        addUserSubmitBtn.disabled = true;
        window.location.href = "admin.html";
      } else {
        console.error("Erreur backend :", result); 
        alert(result.detail || result.message || "Erreur lors de l'ajout.");
      }
    } catch (error) {
      console.error("Erreur API :", error);
      alert("Une erreur est survenue.");
    }
  });
  
  const btn = document.querySelector(".return-btn");
  if (btn) {
    btn.addEventListener("click", () => {
      window.location.href = "admin.html";
    });
  }
})
