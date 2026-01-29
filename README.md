# MPVRP-CC Solver 

**Multi-Product Vehicle Routing Problem with Changeover Cost**

> Projet académique & ingénierie logicielle — Solveur modulaire en Python respectant les spécifications officielles MPVRP-CC

---

##  Présentation

Ce projet implémente un **solveur modulaire et extensible** pour le problème **MPVRP-CC (Multi-Product Vehicle Routing Problem with Changeover Cost)**.

Le MPVRP-CC est une généralisation du VRP classique qui prend en compte :

* La distribution de **plusieurs types de produits**
* La contrainte **un seul produit transporté à la fois par véhicule**
* Un **coût de nettoyage (changeover cost)** lors du changement de produit

Ce projet est conçu pour :

*  Projets académiques (Master, recherche opérationnelle, data science)
*  Expérimentation algorithmique
*  Cas industriels (logistique pétrolière, chimique, alimentaire)

---

##  Objectifs

* Parser des fichiers d’instances `.dat` conformes à la spécification MPVRP-CC
* Construire des routes valides respectant toutes les contraintes
* Minimiser :

  * La **distance totale parcourue**
  * Le **coût total de changement de produit**
* Exporter une solution valide au **format officiel MPVRP-CC**
* Fournir une base pour intégrer des **métaheuristiques avancées**

---

##  Fonctionnalités

* Parser officiel des instances `.dat`
* Modèles de données (véhicules, dépôts, garages, stations, produits)
* Calcul des distances euclidiennes
* Heuristique gloutonne (baseline)
* Gestion du coût de changement de produit
* Validation des contraintes
* Export du fichier solution `.dat`
* Visualisation des routes (optionnel)
* Architecture prête pour :

  * Tabu Search
  * Algorithmes génétiques
  * Large Neighborhood Search (LNS)

---

## Architecture du projet

```
mpvrp-cc-solver/
│
├── src/
│   ├── parser.py        # Lecture des fichiers d’instance
│   ├── models.py       # Structures de données principales
│   ├── distance.py    # Calcul des distances
│   ├── heuristics.py  # Heuristiques de construction
│   ├── cost.py        # Gestion des coûts de changement
│   ├── validator.py  # Vérification des contraintes
│   ├── exporter.py   # Génération du fichier solution
│   └── visualizer.py # Affichage graphique des routes
│
├── data/
│   ├── instances/     # Fichiers .dat d’instances
│   └── solutions/    # Solutions générées
│
├── main.py            # Point d’entrée du solveur
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/lagbessi/mpvrp-cc-solver.git
cd mpvrp-cc-solver
```

### 2. Environnement Python

Recommandé : Python 3.9+

Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Utilisation

Placer une instance MPVRP-CC dans :

```
data/instances/
```

Lancer le solveur :

```bash
python main.py data/instances/MPVRP_S_001.dat
```

La solution sera générée dans :

```
data/solutions/
```

---

## Exemple de workflow

1. Charger une instance
2. Parser les données
3. Générer une solution initiale (heuristique gloutonne)
4. Vérifier les contraintes
5. Calculer les coûts
6. Exporter la solution
7. Visualiser les routes

---

## Contraintes respectées

* Satisfaction complète des demandes
* Capacité maximale des véhicules
* Un seul produit par mini-route
* Retour obligatoire au garage
* Alignement parfait entre trajet et produits

---

## Roadmap

* [x] Structure du projet
* [x] Parser officiel `.dat`
* [ ] Heuristique gloutonne complète
* [ ] Validation avancée
* [ ] Recherche locale
* [ ] Algorithme génétique
* [ ] Interface Web de visualisation

---

## Références

* Laporte, G. (2009). *Fifty Years of Vehicle Routing*
* Archetti et al. (2014). *Multi-Product Vehicle Routing Problem*
* Vidal et al. (2013). *Heuristics for Multi-Commodity VRP*

---

## Auteur

**Laurence Agbessi**
Développeur & Étudiant en Informatique / Optimisation / Data Science

---

## Licence

Ce projet est distribué à des fins académiques et de recherche.
Libre d’utilisation avec citation de l’auteur.

---

## Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`feature/ma-fonctionnalite`)
3. Commit (`git commit -m "Ajout d’une nouvelle fonctionnalité"`)
4. Push (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

---

> *"Optimiser, ce n’est pas seulement aller plus vite — c’est comprendre le problème en profondeur."* 

