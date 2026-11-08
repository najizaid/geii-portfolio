import { defineCollection } from 'astro:content';
import { docsSchema } from '@astrojs/starlight/schema';
import { z } from 'astro/zod';

export const collections = {
  docs: defineCollection({
    schema: docsSchema({
      extend: z.object({
        // Champs additionnels utiles pour classer les notes BUT GEII
        ue: z.string().optional(), // ex: "UE 1.1 — Circuits et systèmes électroniques"
        matiere: z.string().optional(), // ex: "Électronique de puissance"
        type: z.enum(['cours', 'tp', 'projet', 'sae', 'rapport', 'ressource']).optional(),
        statut: z.enum(['brouillon', 'a-relire', 'complet']).optional().default('complet'),
      }),
    }),
  }),
};
