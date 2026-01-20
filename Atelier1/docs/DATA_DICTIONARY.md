# 📖 Dictionnaire des Données

Ce document détaille la structure des fichiers CSV utilisés dans l'entrepôt de données. Les données concernent les statistiques compétitives du jeu **Valorant**.

## 1. Fichier `players.csv` (Statistiques Joueurs)

Ce fichier recense les performances individuelles des joueurs professionnels.

| Colonne | Signification | Détails / Calcul |
| --- | --- | --- |
| **player** | Nom du joueur | Pseudonyme utilisé en compétition. |
| **country** | Pays | Pays d'origine ou de résidence du joueur. |
| **team** | Équipe | Nom de l'équipe actuelle du joueur. |
| **rounds** | Manches jouées | Nombre total de rounds enregistrés pour ce joueur. |
| **rating** | Note globale | Score de performance normalisé (souvent calculé par VLR.gg ou TheSpike). |
| **ACS** | *Average Combat Score* | **Score Moyen de Combat**. Métrique clé de Valorant prenant en compte les dégâts (1pt/dmg), les kills (sujets à bonus selon le nombre d'ennemis vivants), et les assistances. |
| **K/D** | *Kill / Death Ratio* | Ratio Tués / Morts. Supérieur à 1.0 signifie plus de kills que de morts. |
| **ADR** | *Average Damage per Round* | **Dégâts Moyens par Manche**. Mesure l'impact pur en termes de dégâts infligés, indépendamment des kills finaux. |
| **KPR** | *Kills Per Round* | Moyenne de tués par manche. |
| **DPR** | *Deaths Per Round* | Moyenne de morts par manche. |
| **APR** | *Assists Per Round* | Moyenne d'assistances par manche. |
| **FBPR** | *First Blood Per Round* | Fréquence à laquelle le joueur obtient le **premier kill** de la manche (ouverture). |
| **FDPR** | *First Death Per Round* | Fréquence à laquelle le joueur est le **premier mort** de la manche. |
| **HS%** | *Headshot %* | Pourcentage de tirs touchant la tête par rapport au nombre total de touches. |
| **FBSR%** | *First Blood Success Rate* | Taux de réussite des duels d'ouverture. (Premiers Kills / [Premiers Kills + Premières Morts]). |

---

## 2. Fichier `teams.csv` (Statistiques Équipes)

Ce fichier agrège les résultats par structure/équipe, avec un focus sur les phases de jeu (Attaque vs Défense).

| Colonne | Signification | Détails |
| --- | --- | --- |
| **team** | Nom de l'équipe | Identifiant unique de l'équipe. |
| **country** | Pays/Région | Région d'affiliation de l'équipe. |
| **maps_played** | Cartes jouées | Nombre total de cartes (maps) disputées. |
| **maps_won** | Cartes gagnées | Nombre total de victoires. |
| **maps_won%** | Taux de victoire global | Pourcentage de matchs gagnés. |
| **atk_played** | Manches en Attaque | Nombre de rounds joués côté "Attaque". |
| **atk_won** | Attaques gagnées | Nombre de rounds gagnés en attaquant. |
| **atk_won%** | Winrate Attaque | Efficacité de l'équipe en phase offensive. |
| **def_played** | Manches en Défense | Nombre de rounds joués côté "Défense". |
| **def_won** | Défenses gagnées | Nombre de rounds gagnés en défendant. |
| **def_won%** | Winrate Défense | Efficacité de l'équipe en phase défensive. |
| **pistol_played** | *Pistol Rounds* joués | Les rounds 1 et 13 où l'économie est réinitialisée (pistolets uniquement). |
| **pistol_won** | *Pistol Rounds* gagnés | Victoires sur ces rounds cruciaux pour l'économie. |
| **pistol_won%** | Winrate Pistolet | Taux de succès sur les rounds de pistolet. |

---

## 3. Fichier `agents.csv` (Méta-Jeu)

Ce fichier analyse l'efficacité de chaque personnage (Agent) à travers l'ensemble des parties.

| Colonne | Signification | Détails |
| --- | --- | --- |
| **agent** | Nom de l'Agent | Personnage jouable (ex: Jett, Sova, Omen). |
| **pick_rate** | Taux de sélection | Fréquence d'apparition de l'agent dans les parties (% de présence). |
| **rounds** | Rounds observés | Nombre total de rounds où cet agent était présent. |
| **rating** | Note moyenne | Performance moyenne des joueurs utilisant cet agent. |
| **ACS** | *Average Combat Score* | Score de combat moyen généré par cet agent. |
| **K/D** | Ratio K/D Moyen | Ratio Tués/Morts moyen pour cet agent. |
| **ADR** | Dégâts Moyens | Dégâts moyens infligés par cet agent par round. |
| **KPR** | Kills par round | Potentiel de frag moyen de l'agent. |
| **DPR** | Morts par round | Survivabilité moyenne de l'agent. |
| **APR** | Assistances par round | Potentiel de support de l'agent (ex: élevé pour Skye/Breach, faible pour Reyna). |
| **FBPR** | *First Blood* par round | Capacité de l'agent à prendre le premier kill (rôle de Duelliste). |
| **FDPR** | *First Death* par round | Risque d'être éliminé en premier. |
| **HS%** | *Headshot %* | Précision moyenne des joueurs sur cet agent. |
| **FBSR%** | *First Blood Success* | Taux de réussite des duels d'ouverture. |

---

## 4. Fichier `maps.csv` (Cartographie)

Ce fichier détaille l'équilibrage des cartes (maps) compétitives.

| Colonne | Signification | Détails |
| --- | --- | --- |
| **map** | Nom de la Carte | Ex: Ascent, Bind, Haven, Icebox... |
| **played** | Fréquence | Taux d'apparition de la carte et nombre brut de sélections. |
| **avg_spike_plant** | Temps pose du Spike | Temps moyen écoulé dans le round avant que la bombe (Spike) ne soit plantée. |
| **rounds** | Total rounds | Nombre cumulé de manches jouées sur cette carte. |
| **atk_win_rate** | Avantage Attaquant | % de victoire pour le côté Attaque (Indique si la map est "T-sided"). |
| **def_win_rate** | Avantage Défenseur | % de victoire pour le côté Défense (Indique si la map est "CT-sided"). |
| **pistol_atk_...** | Winrate Pistolet Atk | Taux de victoire en attaque lors des rounds de pistolet. |
| **pistol_def_...** | Winrate Pistolet Def | Taux de victoire en défense lors des rounds de pistolet. |
| **second_round_...** | Conversion Round 2 | **Taux de conversion**. Probabilité de gagner le 2ème round (avec achat d'armes) après avoir gagné le round de pistolet. Mesure l'effet "Snowball". |