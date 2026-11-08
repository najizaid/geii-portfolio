# GEII Portfolio

Site de documentation personnel (BUT GEII) basé sur **Astro + Starlight**.

Fonctionnalités : recherche full-text (Pagefind), dark/light mode, sidebar hiérarchique repliable, breadcrumbs, LaTeX ($...$ / $$...$$), diagrammes Mermaid, blocs de code avec bouton copier, pièces jointes PDF.

## Démarrage

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # génère dist/
npm run preview   # prévisualise le build
```

## Ajouter une note

1. Copier `src/content/docs/ressources/modele-de-page.md`.
2. La placer dans le bon dossier : `src/content/docs/annee-X/semestre-Y/`.
3. Remplir le frontmatter (`title`, `ue`, `matiere`, `type`, `statut`).
4. `npm run dev` pour vérifier le rendu.

La sidebar se génère automatiquement (`autogenerate`) à partir des dossiers — aucune config à toucher pour ajouter une page.

## Déploiement — GitHub Pages

1. Créer un repo GitHub (ex. `geii-portfolio`) et y pousser ce projet :
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<ton-compte>/geii-portfolio.git
   git push -u origin main
   ```
2. Dans **Settings → Pages** du repo : Source = **GitHub Actions**.
3. Le workflow `.github/workflows/deploy.yml` build et déploie automatiquement à chaque push sur `main` (il calcule `site`/`base` depuis le nom du repo — aucune modif nécessaire).
4. Le site sera disponible sur `https://<ton-compte>.github.io/<nom-du-repo>/`.

### Alternative — Vercel / Netlify

- **Vercel** : importer le repo GitHub sur vercel.com, framework détecté automatiquement (Astro), build command `npm run build`, output `dist`.
- **Netlify** : build command `npm run build`, publish directory `dist`.
- Dans ces deux cas, supprimer/adapter `base` dans `astro.config.mjs` (mettre `base: '/'`) car il n'y a pas de sous-dossier de repo.

## Import des notes Notion

Voir [`NOTION-EXPORT.md`](./NOTION-EXPORT.md) pour la procédure complète d'export et d'injection.
