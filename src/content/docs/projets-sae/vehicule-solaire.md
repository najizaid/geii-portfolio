---
title: "SAE 5.01 — Véhicule solaire"
type: sae
statut: brouillon
---

Projet de conception d'un véhicule à propulsion solaire : chaîne de puissance, MPPT, gestion batterie.

## Architecture système

```mermaid
flowchart TD
    PV[Panneau solaire] --> MPPT[Convertisseur MPPT]
    MPPT --> BAT[Batterie Li-ion]
    BAT --> ONDU[Onduleur / driver moteur]
    ONDU --> MOT[Moteur BLDC]
```

## Points à documenter (checklist de migration Notion)

- [ ] Cahier des charges complet
- [ ] Choix des composants (datasheets)
- [ ] Schémas KiCad (export SVG/PNG dans `src/assets/`)
- [ ] Code embarqué (firmware)
- [ ] Résultats de tests
