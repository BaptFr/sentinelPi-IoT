//API url in config.json for modification

let API_URL = "";

fetch("config.json")
  .then(res => res.json())
  .then(config => {
    API_URL = config.API_URL;
    console.log(" configLoaded started");

    window.dispatchEvent(new Event("configLoaded"));
  })
  .catch(err => {
    console.error("Erreur chargement config.json :", err);
  });

  //Deconnexion
  function deconnexion(e) {
    if (e) e.preventDefault();  
    sessionStorage.removeItem("token");
    window.location.href = "login.html";
}