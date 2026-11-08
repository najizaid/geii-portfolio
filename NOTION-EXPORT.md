# Export Notion → site web (zéro perte d'information)

Le connecteur Notion de cette session n'a pas accès à ton workspace `esiee-eisc`. Solution la plus fiable de toute façon pour une exhaustivité totale : **l'export natif Notion**, qui descend récursivement toutes les sous-pages.

## 1. Export depuis Notion

Sur la page racine **Notion GEII** :

1. `•••` (en haut à droite) → **Export**
2. Format : **Markdown & CSV**
3. Cocher :
   - **Include subpages** (sinon seule la page racine sort)
   - **Create folders for subpages**
4. Lancer l'export → Notion prépare un `.zip` (peut prendre plusieurs minutes si le workspace est volumineux) → télécharger.

Pourquoi Markdown & CSV et pas HTML ou PDF :
- **Markdown** = format natif de Starlight, zéro conversion, préserve titres/listes/code/liens.
- **CSV** accompagne les éventuelles bases de données Notion (tableaux de suivi, listes de TP) → à réintégrer en tableaux Markdown ou en `content/config.ts` si tu veux les requêter.
- HTML/PDF perdent la structure (un PDF n'est pas éditable, du HTML brut demande un nettoyage lourd).

## 2. Nettoyage de l'archive

L'export Notion produit une arborescence du type :
```
Notion GEII/
├── Semestre 5/
│   ├── UE 5.1 Électronique de puissance/
│   │   ├── Cours Hacheurs abc123.md
│   │   └── TP AOP def456.md
├── Projets SAE/
└── ...
```

Notion suffixe chaque fichier/dossier par un ID hex (`abc123`). Un script de renommage/rangement :

```bash
# Depuis le dossier où tu as dézippé l'export Notion
python3 scripts/import-notion.py "/chemin/vers/Notion GEII" src/content/docs
```

Le script fourni (`scripts/import-notion.py`, ci-dessous) :
- retire les IDs hex Notion des noms de fichiers/dossiers,
- slugifie (minuscules, tirets, sans accents) pour des URLs propres,
- ajoute automatiquement le frontmatter Starlight (`title` déduit du nom de fichier),
- copie les images/fichiers joints dans `src/assets/` et corrige les liens relatifs.

## 3. Correspondance de hiérarchie

Mappe tes dossiers Notion vers la structure du site (à ajuster une fois l'export en main) :

| Notion                          | Site (`src/content/docs/...`) |
| -------------------------------- | ------------------------------ |
| Semestre 1, 2                    | `annee-1/semestre-1`, `annee-1/semestre-2` |
| Semestre 3, 4                    | `annee-2/semestre-3`, `annee-2/semestre-4` |
| Semestre 5, 6                    | `annee-3/semestre-5`, `annee-3/semestre-6` |
| Projets / SAE                    | `projets-sae/`                 |
| Rapports d'alternance            | `rapports-alternance/`         |
| Fiches, PDF, liens externes      | `ressources/`                  |

## 4. Points d'attention

- **Formules LaTeX** : Notion exporte les blocs d'équation en `$$...$$` — compatible tel quel avec `remark-math`/`rehype-katex` déjà configurés.
- **Images** : l'export les place dans un sous-dossier à côté du `.md` ; le script les déplace vers `src/assets/<slug>/` et réécrit les chemins (`![alt](./image.png)` → import Astro ou chemin public selon le volume).
- **Tableaux** : Notion exporte les tableaux Markdown nativement — aucune conversion nécessaire.
- **Bases de données Notion** (ex. suivi de notes, liste de TP) sortent en CSV séparé : à transformer en tableau Markdown avec un script ou laissées en pièce jointe téléchargeable dans `ressources/`.
- **Schémas KiCad/AutoCAD** : exporter en SVG/PNG depuis le logiciel (pas de format natif supporté nativement par Notion) puis les glisser dans `src/assets/`.

## 5. Vérification zéro-perte

Après import, lance :
```bash
npm run build
```
Le build échoue si un lien Markdown pointe vers un fichier manquant (`astro check` recommandé en plus : `npx astro check`). Compare aussi le nombre de fichiers `.md` générés au nombre de pages Notion (visible dans l'export) pour confirmer qu'aucune sous-page n'a été oubliée.
