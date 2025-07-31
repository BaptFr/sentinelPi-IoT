// login.js

document.getElementById("loginForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const mdp = document.getElementById("password").value;

  if (!email || !mdp) {
    alert("Veuillez remplir tous les champs.");
    return;
  }


// remplace url par l'url de l'api (sert a envoyer les identifiants a l'api de backend pour la connexion)
  try {
    const response = await fetch(API_URL + "/admin/login", {
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
      const data = await response.json();
      sessionStorage.setItem("token", data.access_token); 
      window.location.href = "admin.html";
    } else {
      alert("Email ou mot de passe incorrect.");
    }
  } catch (error) {
    console.error("Erreur réseau:", error);
    alert("Une erreur est survenue.");
  }
});
