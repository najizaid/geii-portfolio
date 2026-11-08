// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Site GitHub Pages : adapte `site` et `base` au nom réel du repo avant déploiement.
// Exemple pour https://<user>.github.io/<repo>/ :
//   site: 'https://<user>.github.io',
//   base: '/<repo>',
const SITE_URL = process.env.SITE_URL || 'https://najizaid.github.io';
const BASE_PATH = process.env.BASE_PATH || '/geii-portfolio';

export default defineConfig({
  site: SITE_URL,
  base: BASE_PATH,
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [[rehypeKatex, { throwOnError: false, strict: 'ignore' }]],
  },
  integrations: [
    starlight({
      title: 'GEII — Notes & Portfolio',
      description:
        "Notes de cours, TP, projets SAE et rapports d'alternance — BUT GEII",
      defaultLocale: 'fr',
      locales: {
        root: { label: 'Français', lang: 'fr' },
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/najizaid',
        },
      ],
      head: [
        // KaTeX CSS (rendu des formules LaTeX produites par rehype-katex)
        {
          tag: 'link',
          attrs: {
            rel: 'stylesheet',
            href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
            integrity:
              'sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+',
            crossorigin: 'anonymous',
          },
        },
      ],
      customCss: ['./src/styles/custom.css'],
      components: {
        // Composant surchargé : injecte le script client Mermaid après chaque navigation
        Head: './src/components/Head.astro',
      },
      sidebar: [
        {
          label: 'Accueil',
          link: '/',
        },
        {
          label: 'Année 1 — BUT GEII',
          collapsed: true,
          items: [
            { label: 'Semestre 1', autogenerate: { directory: 'annee-1/semestre-1' } },
            { label: 'Semestre 2', autogenerate: { directory: 'annee-1/semestre-2' } },
          ],
        },
        {
          label: 'Année 2 — BUT GEII',
          collapsed: true,
          items: [
            { label: 'Semestre 3', autogenerate: { directory: 'annee-2/semestre-3' } },
            { label: 'Semestre 4', autogenerate: { directory: 'annee-2/semestre-4' } },
          ],
        },
        {
          label: 'Année 3 — BUT GEII',
          collapsed: false,
          items: [
            { label: 'Semestre 5', autogenerate: { directory: 'annee-3/semestre-5' } },
            { label: 'Semestre 6', autogenerate: { directory: 'annee-3/semestre-6' } },
          ],
        },
        {
          label: 'Projets & SAE',
          collapsed: false,
          autogenerate: { directory: 'projets-sae' },
        },
        {
          label: "Rapports d'alternance",
          collapsed: true,
          autogenerate: { directory: 'rapports-alternance' },
        },
        {
          label: 'Ressources & documents',
          collapsed: true,
          autogenerate: { directory: 'ressources' },
        },
      ],
    }),
  ],
});
