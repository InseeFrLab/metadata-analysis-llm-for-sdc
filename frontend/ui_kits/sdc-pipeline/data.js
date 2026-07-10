/* Fake data for the SDC pipeline UI kit. Mirrors the real product domain:
   a metadata workbook → serialized Markdown → questions → validated JSON table.
   Only used for the standalone kit preview; the live app fetches from the backend. */
(function () {
  // Serialized Markdown the model would receive (what the producer previews)
  const SAMPLE_MARKDOWN = `## Feuille « Demande_CA »  (feuille de demande)

| N° tableau | Champ              | Indicateur   | Activité (NAF) | Taille |
|------------|--------------------|--------------|----------------|--------|
| T1         | entreprises FR     | ca_total     | A88            | TREFF  |
| T2         | entreprises FR     | ca_salades   | niveau division| —      |
| T3         | entreprises FR     | ca_batavia   | niveau division| —      |

> Note : ca_salades et ca_batavia sont deux types de chiffre d'affaires « salades ».
> Tous les tableaux portent sur les entreprises françaises.

## Feuille « Nomenclature_TREFF »  (feuille de référence)

| Code | Libellé             |
|------|---------------------|
| 0    | 0 salarié           |
| 1    | 1 à 9 salariés      |
| 2    | 10 à 49 salariés    |
| 3    | 50 salariés et plus |`;

  // Phase 1 questions the model asks the producer
  const QUESTIONS = [
    {
      id: 1,
      category: "Indicateurs et hiérarchies",
      text: "Pour T2 et T3, « ca_batavia » est-il un composant de « ca_salades », ou une variable indépendante ?",
      ref: "Feuille Demande_CA · note ligne 5",
      options: ["Composant de ca_salades", "Variable indépendante"],
    },
    {
      id: 2,
      category: "Variables de croisement et nomenclatures",
      text: "La colonne « Taille » de T1 (TREFF) renvoie-t-elle à la nomenclature « Nomenclature_TREFF » fournie dans le classeur ?",
      ref: "Feuille Demande_CA · colonne Taille",
      options: ["Oui, la nomenclature fournie", "Non, variable non structurée"],
    },
    {
      id: 3,
      category: "Champ et population",
      text: "Le champ « entreprises françaises » s'applique-t-il bien aux trois tableaux, y compris ceux dont la cellule Champ est vide ?",
      ref: "Feuille Demande_CA · note finale",
      options: ["Oui, à tous les tableaux", "Non, préciser par tableau"],
    },
  ];

  // Phase 2 — validated records (the deliverable)
  const RECORDS = [
    { table_name: "T1", field: "entreprises_francaises", hrc_field: "NA", indicator: "ca_total", hrc_indicator: "NA", spanning: "A88 · TREFF" },
    { table_name: "T2", field: "entreprises_francaises", hrc_field: "NA", indicator: "ca_salades", hrc_indicator: "hrc_salades", spanning: "naf_code" },
    { table_name: "T3", field: "entreprises_francaises", hrc_field: "NA", indicator: "ca_batavia", hrc_indicator: "hrc_salades", spanning: "naf_code" },
  ];

  window.SDC_DATA = { SAMPLE_MARKDOWN, QUESTIONS, RECORDS };
})();
