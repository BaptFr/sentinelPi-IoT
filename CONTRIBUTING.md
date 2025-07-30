# CONTRIBUTING

## Objectif

Ce guide définit les règles à suivre pour collaborer efficacement sur ce projet Git, en environnement Windows, avec Git Bash ou PowerShell.

## Règles de base

- Ne jamais travailler directement sur la branche `main`.
- Toute contribution doit passer par une branche dédiée et une Pull Request (PR).
- Une PR ne doit contenir qu’un seul objectif (fonctionnalité, correction, etc.).

## Création d’une branche

Toujours créer une branche dont l'origine, la base de code vient d'abord de la branche `main`. Exécuter les commandes suivantes dans Git Bash ou PowerShell :

```bash
(basculer sur main)
git checkout 
(récupérer le code de la branche main)
git pull origin main
(Création et bascule sur une nouvelle branche créée)
git checkout -b type/nom-de-la-tache
```
Format recommandé pour les noms de BRANCHES :

```
type/nom-clair
```

Types de branche autorisés :

- `Feat` : nouvelle fonctionnalité, modifs fonctionnelles
- `Fix` : correction de bug
- `Docs` : documentation
- `Refactor` : amélioration technique de code, de dossiers etc... sans modification fonctionnelle

Exemples :
- `Feat/ajout-authentification`
- `Fix/erreur-affichage-mobile`
- `Docs/update-readme`

## Commits

Chaque commit doit être clair, concis, et suivre ce format :

```
typeducommit : description du changement
```

Types de commit valides :

- `Feat` : ajout de fonctionnalité
- `Fix` : correction de bug
- `Doc` : documentation
- `Refactor` : refactorisation


Exemples de commit:

- `Feat: ajout du formulaire de contact`
- `Fix: correction du bug de navigation`
- `Docs: mise à jour du guide de contribution`



## Pull Request

Une fois la tâche terminée :

```bash
git add .
git commit -m "typeducommit: message clair"
git push origin nom-de-la-branche
```

Puis sur GitHub :

1. Créer une Pull Request vers `main`
2. Vérifier le titre et la description
3. Attendre la revue d’un autre membre avant fusion



## Bonnes pratiques

- Toujours mettre à jour `main` avant de commencer une tâche :

```bash
git checkout main
git pull origin main
```

- Ne pas commit :
  - de code non fonctionnel
  - de fichiers temporaires ou inutiles
  - de `console.log()` ou TODO non traités

- Tester son code avant de pousser

## Liens utiles

- `README.md` — Présentation du projet
- `issues/` — Suivi des tâches et bugs


## Workflow
# 1. Cloner le repo principal (PAS de fork)
git clone (url code)
cd mon-projet

# 2. Créer une branche à partir de main
git checkout -b feat/ma-tache

# 3. Travailler et committer
git add .
git commit -m "feat: ajouter un composant navbar"

# 4. Pousser la branche vers GitHub
git push origin feat/ma-tache

# 5. Ouvrir une Pull Request vers main depuis GitHub