//Config API loading
window.addEventListener("configLoaded", () => {

  document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const mdp = document.getElementById("password").value;

    if (!email || !mdp) {
      alert("Veuillez remplir tous les champs.");
      return;
    }


    try {
      const response = await fetch(API_URL + "/api/admin/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
          email, 
          password: mdp 
        })
      });

      if (response.ok) {
        //DEBUG
        console.log("API_URL utilisé :", API_URL);
        const data = await response.json();
        sessionStorage.setItem("token", data.access_token);
        window.dispatchEvent(new Event("configLoaded"));
        window.location.replace("admin.html");
      } else {
        alert("Email ou mot de passe incorrect.");
      }
    } catch (error) {
      console.error("Erreur réseau:", error);
      alert("Une erreur est survenue.");
    }
  });
});
