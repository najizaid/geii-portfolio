---
title: "TP — Montages à AOP"
ue: UE 5.1 — Électronique de puissance
matiere: Électronique analogique
type: tp
statut: a-relire
---

## Objectif

Caractériser un montage amplificateur non-inverseur à AOP et vérifier le gain théorique.

## Montage

Gain théorique d'un amplificateur non-inverseur :

$$
G = 1 + \frac{R_2}{R_1}
$$

## Mesures

| R1 (kΩ) | R2 (kΩ) | Gain théorique | Gain mesuré | Écart (%) |
| ------- | ------- | --------------- | ----------- | --------- |
| 1       | 9       | 10              | 9.8         | 2.0       |
| 2.2     | 10      | 5.5             | 5.4         | 1.8       |

## Analyse

Écart attribué à la tolérance des résistances (±5%) et au gain en boucle ouverte fini de l'AOP.

## Fichier joint

<a href="/fiches/tp-aop-mesures.pdf" download>Télécharger la fiche de mesures (PDF)</a>

> Placez le PDF réel dans `public/fiches/tp-aop-mesures.pdf` pour que ce lien fonctionne.
