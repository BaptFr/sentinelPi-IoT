
window.addEventListener("configLoaded", initPage);

function initPage() {
  const firstnameCheck = document.getElementById("prenom")
  const lastnameCheck = document.getElementById("nom")
  const photoInput = document.getElementById("photoInput");
  //DEBUG const addUserSubmitBtn = document.getElementById("addUserSubmitBtn");
  const enrollmentSubmitBtn = document.getElementById("enrollmentSubmitBtn");
  const status = document.getElementById("enrollment-status");
  const cancelEnrollmentBtn = document.getElementById("cancelEnrollmentBtn");

  let currentEnrollmentId = null;


  //Check functions for Submit button clickable
  function checkInputs() {
    enrollmentSubmitBtn.disabled = firstnameCheck.value.trim() === "" || lastnameCheck.value.trim() === "";
  }

  //Upgrade Device Version
  // function checkPhotoInput () {
  //   if (firstnameCheck.value.trim() !=="" && lastnameCheck.value.trim() !=="" & photoInput.files.length > 0 ) {
  //     addUserSubmitBtn.disabled = false;
  //   } else {
  //     addUserSubmitBtn.disabled = true;
  //   }
  // };

  //Event listeners
  function attachListenerOnce(element, event, handler) {
      element.removeEventListener(event, handler);
      element.addEventListener(event, handler);
  }
  attachListenerOnce(firstnameCheck, "input", checkInputs);
  attachListenerOnce(lastnameCheck, "input", checkInputs);

  checkInputs();


  //******Enrollment procedur click button******
  enrollmentSubmitBtn.addEventListener("click", async () => {
    const firstname = document.getElementById("prenom").value.trim();
    const lastname = document.getElementById("nom").value.trim();
    const role = "user";

    //Handle errors before submitting
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

    //Display for waiting process
    status.classList.remove("hidden");
    status.classList.add("visible");
    enrollmentSubmitBtn.disabled = true;
    cancelEnrollmentBtn.classList.remove("hidden");

    try {
      const response = await fetch(API_URL + "/api/enrollment/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          firstname,
          lastname,
          role
        })

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
        currentEnrollmentId = result.enrollment_id;
      } else {
        const result = await response.json();
        status.classList.add("hidden");
        alert(result.detail || result.message || "Erreur lors de la procédure");
        status.classList.remove("visible");
        status.classList.add("hidden");
        location.reload();
      }
    } catch (error) {
      console.error("API Error:", error);
      alert("Une erreur est survenue.");
      status.classList.remove("visible");
      status.classList.add("hidden");
      location.reload();
    }
  });

  //Cancel enrollment option
  cancelEnrollmentBtn.addEventListener("click", async () => {
    if (!currentEnrollmentId) return;

    alert("Enrôlement annulé.");
    status.classList.add("hidden");
    cancelEnrollmentBtn.classList.add("hidden");
    enrollmentSubmitBtn.disabled = false;
    currentEnrollmentId = null;
  });


  /****** PROJECT POSSILE CAM UPGRADE  ******/
  //Add user with face_data click button
  // addUserSubmitBtn.addEventListener("click", async () => {
  //   const firstname = document.getElementById("prenom").value.trim();
  //   const lastname = document.getElementById("nom").value.trim();
  //   const face_data =  photoInput.files[0];
  //   const role = "user";

  //   if (!firstname || !lastname) {
  //     alert("Veuillez remplir tous les champs obligatoires.");
  //     return;
  //   }

  //   const token = sessionStorage.getItem("token");
  //   if (!token) {
  //     alert("Session expirée. Veuillez vous reconnecter.");
  //     window.location.href = "login.html";
  //     return;
  //   }

  //   const formData = new FormData();
  //   formData.append("firstname", firstname);
  //   formData.append("lastname", lastname);
  //   formData.append("role", role);
  //   formData.append("face_data", face_data);

  //   for (let pair of formData.entries()) {
  //   console.log(`${pair[0]}:`, pair[1]);
  //   }
  //   //Add user-lock
  //   try {
  //     const response = await fetch(API_URL + "/lock-users", {
  //       method: "POST",
  //       headers: {
  //         Authorization: `Bearer ${token}`
  //       },
  //       body: formData
  //     });

  //     if (response.status === 401 || response.status === 403) {
  //       alert("Session expirée. Veuillez vous reconnecter.");
  //       sessionStorage.removeItem("token");
  //       window.location.href = "login.html";
  //       return;
  //     }

  //     const result = await response.json();

  //     if (response.ok) {
  //       document.querySelector("form").reset();
  //       addUserSubmitBtn.disabled = true;
  //       window.location.href = "admin.html";
  //     } else {
  //       console.error("Erreur backend :", result); 
  //       alert(result.detail || result.message || "Erreur lors de l'ajout.");
  //     }
  //   } catch (error) {
  //     console.error("Erreur API :", error);
  //     alert("Une erreur est survenue.");
  //   }
  // });

  const btn = document.querySelector(".return-btn");
  if (btn) {
    btn.addEventListener("click", () => {
      window.location.replace("admin.html");
    });
  }
}
