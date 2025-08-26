<div align="center">
    <img src="https://res.cloudinary.com/it-akademy/image/upload/f_auto,q_auto,h_60/logo_2x_feoygs.png" alt="IT-Akademy logo" title="IT-Akademy"  height="60" />  
</div>
</br> 

<div align="center">
  
![Project](https://img.shields.io/badge/Projet_type-IoT-blue.svg)
![Project](https://img.shields.io/badge/Projet_mode-Hackathon/sprint-orange.svg)
![Session](https://img.shields.io/badge/Session-DFS33-brightgreen.svg)
</div>



<div align="center">
  <h1> Open Project IoT </h1>
</div>
</br> 
<div align="center"> <img src="https://i.imgur.com/ybnN7dy.png" width="500"/>  </div>


</br> 
</br> 
<div align="center"> <h1> Pitch  </h1> 
</br> 
  
### SentinelPi est une solution d'accès et de contrôle d’accès nouvelle génération, alliant sécurité renforcée, simplicité et confidentialité.
</br> 

### Basé sur un Raspberry Pi, le système permet l'ouverture de la serrure connectée par reconnaissance d'empreintes digitales, ainsi qu'un contrôle à distance par un administrateur qui a la possibilité de modifier les accès, gérer les utilisateurs mais aussi de suivre les entrées ou tentatives via un historique.
</div>
</br>
</br> 


<div align="center">
  <img src="https://www.raspberrypi.org/app/uploads/2017/09/fingerprint2.gif" width="500"/>
</div>

</br> 

#### 🌍  Interface web accessible de partout : grâce à un tableau de bord administrateur déployé dans le cloud, le superviseur peut consulter l’historique, gérer les utilisateurs et surveiller les accès depuis n’importe où.

#### 👥  Gestion des utilisateurs : ajout de personnes, modification ou suppression des autorisations à l'accès depuis le dashboard de l'administrateur.

#### 📊  Suivi intelligent en temps réel : chaque tentative d’accès (acceptée ou refusée) sur la serrure est horodatée, tracée et immédiatement visible à distance par le superviseur. Lorsqu’un accès est validé, la personne est identifiée clairement sur le dashboard, garantissant une traçabilité sans transit des données biométriques.

#### 🔒  Confidentialité et sécurité : les données biométriques restent strictement locales et ne quittent jamais l’appareil. Les informations utilisateurs, elles, sont stockées sur le cloud sans les empreintes, garantissant une séparation totale entre identité et biométrie.



<div align="center">
    
### En combinant fiabilité matérielle, sécurité logicielle et ergonomie web, SentinelPi propose une solution "clé" en main pour un contrôle d’accès moderne et robuste.
</div>

</br> 
</br> 
</br> 


<div align="center"> <h1> Infos  </h1> </div>

- Accès pour Login à l'interface Admin sur **[https://www.sentinelpi.tech](https://www.sentinelpi.tech/)**  .

- Interface et Dashboard Admin consultables dans la vidéo de Démonstration en bas de page (ou accès fournis sur demande).

- Code du Raspberry ajouté dans la **[branche "raspberry"](https://github.com/it-akademy-students/sentinelPi-it/tree/raspberry)** du repo.

</br>
</br>
</br> 
<div align="center"> <h1> Features  </h1> </div>

- Interface web admin sécurisé accessible depuis n'importe où.
- Gestion des utilisateurs à distance (ajout / suppression / modification).
- Suivi des accès en temps réel et historiques des accès ou tentatives d'accès avec horodatage.
- Sécurité renforcée par la séparation des données : données biométriques locales sans données utilisateurs / Données utilisateurs cloud sans images biométriques.

- Accès sécurisés par reconnaissance d'empreintes digitales.
- Système polyvalent adaptable à plusieurs supports d'accès (portes, casiers, coffres...).
- Jusqu'à 300 utilisateurs reconnus par serrure.
  
</br>
</br>
</br>

<div align="center"> <h1> Stack  </h1> </div>
</br> 
</br>


### Frontend  - Interface web admin pour la gestion des utilisateurs et la visualisation des accès
<div float="left">
  
![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
  </br> 
  
</div>

- **Langages :** Pour la Verison 1 HTML, CSS, JavaScript 
- **Communication :** Requêtes HTTPS pour interagir avec le backend (REST API)  

</br> 
</br> 
</br> 


### Raspberry Pi 4 / Dispositif embarqué
<div float="left">
  
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=flat&logo=raspberrypi&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-wss-blue?logo=websocket&logoColor=white)
</br> 
</div>

- **Système :** Linux  
- **Langage :** Python 3  
- **Gestion du capteur d’empreintes digitales :** pyfingerprint  
- **Contrôle matériel :** RPi.GPIO  
- **Communication avec le backend :** WebSocket sécurisé (WSS, protocole chiffré)  

</br> 
</br> 
</br> 

###  Backend / API Server
<div float="left">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/5697b1e4c4a9790ece607654e6c02a160620c7e1/docs/badge/v2.json)](https://pydantic.dev)

![API](https://img.shields.io/badge/API-FF6F00?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-blue?logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-4169E1?logo=sqlite&logoColor=fff&style=plastic)
![WebSocket](https://img.shields.io/badge/WebSocket-wss-blue?logo=websocket&logoColor=white)
![DigitalOcean](https://img.shields.io/badge/DigitalOcean-0080FF?logo=digitalocean&logoColor=white)

![OAuth2](https://img.shields.io/badge/OAuth2-308D46?logo=oauth2&logoColor=white)
![bcrypt](https://img.shields.io/badge/bcrypt-4.3.0-black?logo=bcrypt&logoColor=white)
![Passlib](https://img.shields.io/badge/Passlib-abcdef?logo=python&logoColor=white)

</div>

- **Langage :** Python 3  
- **Framework web :** FastAPI + Starlette  
- **Base de données relationnelle :** PostgreSQL via SQLAlchemy (V1). Migration possible vers la base PostgreSQL de l’hébergeur.  
- **Validation et modélisation des données :** Pydantic  
- **Authentification et sécurité :** JWT (python-jose), hashage (bcrypt, passlib), OAuth2  
- **Déploiement :** Serveur cloud Ubuntu (DigitalOcean) – 2 vCPUs, 8 GB RAM, 25 GB stockage, 4 TB trafic  
- **Gestion du domaine :** Tech Domain (.tech) avec DNS management  

</br> 
</br> 

### 📦 Installer facilement l'ensemble des dépendances nécessaires au projet 

**Le fichier requirements.txt inclus à la racine du projet sert à lister toutes les dépendances Python du projet afin que n’importe qui puisse les installer facilement avec pip (pip estinclus dans Python).**

**Etapes et commandes Bash:**
#### 1. Créer un environnement virtuel

</br>

#### 2. Installer les dépendances

##### pip install -r requirements.txt

</br>

#### 3. Ajouter un package

##### pip install nom_du_package
##### pip freeze > requirements.txt

</br>

#### 4. Ne pas pas upgrade requirement.txt

##### Le fichier requirement.txt sert aussi à figer les dépendance pour éviter une mise à jour des dépendances cassant le code en créant des incompatibilités (pip freeze > requirements.txt). 

</br> 
</br> 
</br>

<div align="center"> <h1> Documentation  </h1> </div>

<div align="center"> En cours ... </div>

</br> 
</br> 
</br>

<div align="center"> <h1> Team & organisation  </h1> </div>

<div align="center">
  
</br> 

### Jawad LAMHAOURKI

### Ludivine THINET

### Robin ZAFRANI

### Baptiste SALAZAR

</div>
</br> 

### Méthodes et outils d'organisation:
- Méthode Agile Kanban
- Trello : [VOIR LE TABLEAU KANBAN sur trello](https://trello.com/invite/b/68811583cc402617a1afd28c/ATTI062f1ae5625cd26227a6296db04c04db56DD964E/tableau-kanban-taches)
  
### Travail en commun, partages de documents:
- Google Drive , Google Doc
- Contrôle de versions: git
- Bonnes pratiques communes GitHub dans le repo: fichier CONTRIBUTING.md


</br> 
<div align="center"> <h1> Demo  </h1> </div> 

<div align="center">
  <h3>Lien vers vidéo de démonstration fonctionnelle:</h3>

<img src="https://cdn1.thesculptedvegan.com/wp-content/uploads/2020/05/07151301/Arrows-3-pointing-down-arrow-down-animated.gif" height="100" /> 
 
## <a> [VOIR LA VIDEO](https://drive.google.com/file/d/1O45TUK8ZJpJpfTdv8lTNmULktiQystbF/view?usp=sharing) <a/> 

<div/>

