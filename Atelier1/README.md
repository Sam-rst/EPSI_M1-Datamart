Voici **5 propositions de jeux de données** qui répondent parfaitement à tes contraintes (volume, interactions, statistiques *in-game*) et qui permettent de construire des modèles relationnels intéressants.

---

### 1. Le "Classique" riche en données : League of Legends (LoL)

C'est probablement le jeu le plus analysé au monde, mais pour une bonne raison : la granularité des données est incroyable.

* **Pourquoi ce choix ?** Le jeu est basé sur des équipes, des rôles, des objets et des objectifs temporels. Cela force à créer un modèle relationnel solide (3ème forme normale).
* **Les Stats "In-Game" :** Gold par minute, KDA (Kill/Death/Assist), dégâts aux tours, nombre de *wards* posées, premier sang, dragons tués.
* **Idée de Modélisation (ERD) :**
* Tables : `Matches`, `Participants`, `Champions`, `Items`, `Spells`, `Teams`.
* Relation : Un `Match` a plusieurs `Participants`, chaque `Participant` joue un `Champion` et achète plusieurs `Items`.


* **Où le trouver :**
* [Kaggle - League of Legends Ranked Matches](https://www.kaggle.com/datasets/datasnaek/league-of-legends) (Plus de 50k parties).



### 2. Le Tactique précis : Counter-Strike: Global Offensive (CS:GO)

Ici, on quitte la gestion de ressources pour la précision et l'économie par manche (round).

* **Pourquoi ce choix ?** La structure est très hiérarchique : Une partie contient des manches (rounds), qui contiennent des événements de joueurs. C'est parfait pour l'agrégation SQL.
* **Les Stats "In-Game" :** Type d'arme utilisée, argent dépensé par round, position (CT vs T), désamorçage de bombe, *headshot percentage*.
* **Idée de Modélisation (ERD) :**
* Tables : `Matches`, `Rounds`, `Players`, `Weapons`, `Maps`.
* Relation : Un `Match` a plusieurs `Rounds`. Dans un `Round`, un `Player` a un équipement spécifique (Weapon).


* **Où le trouver :**
* [Kaggle - CS:GO Round Winner Classification](https://www.kaggle.com/datasets/christianlillelund/csgo-round-winner-classification) (Contient des snapshots de rounds, très volumineux).



### 3. La "Battle Royale" : PUBG (PlayerUnknown's Battlegrounds)

Ce jeu offre un défi intéressant : gérer un grand nombre de joueurs (jusqu'à 100) par partie unique.

* **Pourquoi ce choix ?** Il permet d'analyser des données spatiales (distances parcourues) et de survie. Le volume de données grimpe très vite.
* **Les Stats "In-Game" :** Distance de marche, distance en véhicule, dégâts infligés, nombre de soins utilisés, rang final, temps de survie.
* **Idée de Modélisation (ERD) :**
* Tables : `Matches`, `PlayerStats`, `GameModes`.
* Challenge : La table `PlayerStats` sera très longue (100 lignes par match). Optimisation des requêtes nécessaire.


* **Où le trouver :**
* [Kaggle - PUBG Finish Placement Prediction](https://www.kaggle.com/c/pubg-finish-placement-prediction/data) (Attention, c'est un dataset énorme, il faudra peut-être en prendre un échantillon pour l'atelier).



### 4. Le Sport Mécanique : Rocket League

Un mélange de football et de voitures. Les interactions sont physiques et très rapides.

* **Pourquoi ce choix ?** Contrairement aux autres, il y a moins d'objets/inventaires, mais plus de statistiques d'action pure. C'est plus simple à modéliser mais très fun à analyser (ex: corrélation entre utilisation du boost et victoire).
* **Les Stats "In-Game" :** Buts, arrêts, tirs, démolitions, quantité de boost utilisée, vitesse moyenne.
* **Idée de Modélisation (ERD) :**
* Tables : `Matches`, `Teams`, `Players`, `Seasons`.
* Focus : Analyser les performances par `Team` (2v2, 3v3).


* **Où le trouver :**
* [Kaggle - Rocket League Matches](https://www.google.com/search?q=https://www.kaggle.com/datasets/dwt1337/rocket-league-matches-dataset) (Souvent issu de Ballchasing.com).



### 5. La Stratégie Complexe (RTS) : StarCraft II

C'est le choix "Hardcore" pour les étudiants qui veulent du défi.

* **Pourquoi ce choix ?** StarCraft génère des données extrêmement complexes. Il ne s'agit pas seulement de qui a gagné, mais de l'ordre de construction (*build order*), de l'économie (minerais/gaz) et des unités produites à la seconde.
* **Les Stats "In-Game" :** APM (Actions Per Minute), temps de production des unités, taille de l'armée, ressources collectées.
* **Idée de Modélisation (ERD) :**
* Tables : `Matches`, `Races` (Terran, Zerg, Protoss), `Units`, `Buildings`, `TechTree`.
* Relation : Très complexe car les unités dépendent des bâtiments.


* **Où le trouver :**
* [Kaggle - StarCraft II Replay Analysis](https://www.google.com/search?q=https://www.kaggle.com/datasets/dylanl/starcraft-ii-replay-analysis).



---

### Résumé technique pour le choix

| Jeu | Complexité du Modèle Relationnel | Difficulté de nettoyage | Intérêt Analytique |
| --- | --- | --- | --- |
| **League of Legends** | ⭐⭐⭐ (Élevée - beaucoup d'objets/champions) | ⭐ (Faible - souvent propre) | Méta-game, équilibrage |
| **CS:GO** | ⭐⭐ (Moyenne) | ⭐⭐ (Moyenne) | Économie, précision |
| **PUBG** | ⭐ (Faible - table unique large) | ⭐ (Faible) | Survie, spatial |
| **StarCraft II** | ⭐⭐⭐⭐ (Très Élevée) | ⭐⭐⭐ (Haute) | Optimisation, APM |

### Conseil pour l'atelier

Pour un "Atelier 1", je recommanderais **League of Legends** ou **CS:GO**.
Ils offrent le meilleur équilibre : les données sont faciles à trouver en CSV (pour chargement facile dans DuckDB/Pandas) et le modèle relationnel est évident à construire (Normalisation facile à justifier), ce qui permet de se concentrer sur la mise en place de la stack technique sans être noyé par la complexité du jeu.

**Souhaites-tu que je détaille le schéma relationnel (MCD) prévisionnel pour l'un de ces jeux pour t'aider à lancer le groupe ?**