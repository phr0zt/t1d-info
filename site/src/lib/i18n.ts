export type Lang = "en" | "fr";
export const LANGS: Lang[] = ["en", "fr"];

export type TopicKey =
  | "start" | "emergencies" | "food" | "movement" | "medications"
  | "drugs-alcohol" | "complications" | "manual-therapy" | "people" | "help";

// Topic folder names per language, and which source deck feeds each download bundle.
export const TOPICS: Record<TopicKey, { en: string; fr: string; label: Record<Lang, string>; blurb: Record<Lang, string>; deck: string }> = {
  start: {
    en: "start", fr: "commencer", deck: "00-master",
    label: { en: "Start here", fr: "Commencer ici" },
    blurb: { en: "The whole picture in one pass: what type 1 is and what the daily work actually is.", fr: "Le portrait complet, en une seule lecture : ce qu'est le type 1 et ce que le travail quotidien demande vraiment." },
  },
  emergencies: {
    en: "emergencies", fr: "urgences", deck: "00-master",
    label: { en: "Emergencies", fr: "Urgences" },
    blurb: { en: "Low blood sugar, glucagon, DKA and sick days. Learn these first.", fr: "Hypoglycémie, glucagon, acidocétose et jours de maladie. À apprendre en premier." },
  },
  food: {
    en: "food", fr: "alimentation", deck: "01-food",
    label: { en: "Food", fr: "Alimentation" },
    blurb: { en: "There is no diabetic diet. Carbs, timing, labels, celiac, parties.", fr: "Il n'existe pas de « diète pour diabétiques ». Glucides, moment des repas, étiquettes, maladie cœliaque, fêtes." },
  },
  movement: {
    en: "movement", fr: "activite-physique", deck: "02-movement",
    label: { en: "Movement", fr: "Activité physique" },
    blurb: { en: "Why exercise moves glucose both ways, and how to plan around it.", fr: "Pourquoi l'exercice fait bouger la glycémie dans les deux sens, et comment s'y préparer." },
  },
  medications: {
    en: "medications", fr: "medicaments", deck: "03-medications",
    label: { en: "Medications", fr: "Médicaments" },
    blurb: { en: "Other medicines that move blood sugar, sick-day holds, and what to ask first.", fr: "Les autres médicaments qui influencent la glycémie, les pauses en cas de maladie et les questions à poser." },
  },
  "drugs-alcohol": {
    en: "drugs-alcohol", fr: "drogues-alcool", deck: "04-drugs-alcohol",
    label: { en: "Drugs & alcohol", fr: "Drogues et alcool" },
    blurb: { en: "Harm reduction, not a lecture.", fr: "De la réduction des méfaits, pas un sermon." },
  },
  complications: {
    en: "complications", fr: "complications", deck: "05-complications",
    label: { en: "Complications", fr: "Complications" },
    blurb: { en: "What the evidence says, how far the rates have fallen, and screening.", fr: "Ce que disent les données, à quel point les taux ont diminué, et le dépistage." },
  },
  "manual-therapy": {
    en: "manual-therapy", fr: "therapies-manuelles", deck: "07-manual-therapy",
    label: { en: "Massage & manual therapy", fr: "Massothérapie et orthothérapie" },
    blurb: { en: "Massage, orthotherapy and physio with type 1: what helps, insulin sites, sensors, and what to tell the therapist.", fr: "Massothérapie, orthothérapie et physio avec le type 1 : ce qui aide, les sites d'insuline, les capteurs et quoi dire au thérapeute." },
  },
  people: {
    en: "people", fr: "entourage", deck: "00-master",
    label: { en: "The people around you", fr: "Votre entourage" },
    blurb: { en: "Family, friends, coaches, teachers, and the words that help.", fr: "Famille, amis, entraîneurs, personnel enseignant, et les mots qui aident." },
  },
  help: {
    en: "help", fr: "aide", deck: "00-master",
    label: { en: "Help & resources", fr: "Aide et ressources" },
    blurb: { en: "Québec and Canadian helplines, organisations and coverage.", fr: "Lignes d'aide, organismes et couverture au Québec et au Canada." },
  },
};

export const TOPIC_ORDER: TopicKey[] = ["start", "emergencies", "food", "movement", "medications", "drugs-alcohol", "complications", "manual-therapy", "people", "help"];

export function topicFromFolder(lang: Lang, folder: string): TopicKey | undefined {
  return TOPIC_ORDER.find((k) => TOPICS[k][lang] === folder);
}

// Download bundles: one per source deck.
export const BUNDLES: { deck: string; slug: string; label: Record<Lang, string>; topics: TopicKey[] }[] = [
  { deck: "00-master", slug: "00-overview", label: { en: "The whole picture", fr: "Le portrait complet" }, topics: ["start", "emergencies", "people", "help"] },
  { deck: "01-food", slug: "01-food", label: { en: "Food", fr: "Alimentation" }, topics: ["food"] },
  { deck: "02-movement", slug: "02-movement", label: { en: "Movement", fr: "Activité physique" }, topics: ["movement"] },
  { deck: "03-medications", slug: "03-medications", label: { en: "Medications", fr: "Médicaments" }, topics: ["medications"] },
  { deck: "04-drugs-alcohol", slug: "04-drugs-alcohol", label: { en: "Drugs & alcohol", fr: "Drogues et alcool" }, topics: ["drugs-alcohol"] },
  { deck: "05-complications", slug: "05-complications", label: { en: "Complications", fr: "Complications" }, topics: ["complications"] },
  { deck: "07-manual-therapy", slug: "07-manual-therapy", label: { en: "Massage & manual therapy", fr: "Massothérapie et orthothérapie" }, topics: ["manual-therapy"] },
];

export function bundleFor(topic: TopicKey) {
  return BUNDLES.find((b) => b.topics.includes(topic))!;
}

export const STATIC_PAGES = {
  downloads: { en: "downloads", fr: "telechargements" },
  sources: { en: "sources", fr: "sources" },
  about: { en: "about", fr: "a-propos" },
  search: { en: "search", fr: "recherche" },
} as const;

export const T = {
  en: {
    siteName: "KRKT's Type 1 Diabetes Education",
    alias: "KRKT:T1DE",
    library: "KRKT Library",
    fromLibrary: "from the KRKT Library",
    tagline: "Plain-language type 1 diabetes education for people newly diagnosed, and for everyone around them.",
    disclaimer: "Education, not medical advice. Every dose, ratio and target belongs with your own diabetes team.",
    emergencyTitle: "In an emergency",
    emergencyText: "Someone with type 1 who is confused, very drowsy, can't swallow or is unconscious: call 911.",
    emergencyLinks: { hypo: "Low blood sugar", dka: "DKA", sick: "Sick days" },
    topics: "Topics",
    inThisTopic: "In this section",
    sources: "Sources",
    reviewed: "Last reviewed",
    downloads: "Downloads",
    downloadThis: "Take this section with you",
    downloadNote: "Handout (PDF), editable document (DOCX) and slide deck (PowerPoint), in English and French.",
    pdf: "Handout", docx: "Document", pptx: "Slides",
    about: "About",
    search: "Search",
    searchPlaceholder: "Search the library",
    next: "Next",
    prev: "Previous",
    switchLang: "Français",
    skip: "Skip to content",
    menu: "Menu",
    home: "Home",
    allSources: "All sources",
    footerNote: "Canadian (Québec) context throughout: mmol/L, Diabetes Canada guidance, Québec services.",
  },
  fr: {
    siteName: "L'éducation sur le diabète de type 1 de KRKT",
    alias: "KRKT:T1DE",
    library: "Bibliothèque KRKT",
    fromLibrary: "de la Bibliothèque KRKT",
    tagline: "De l'information claire sur le diabète de type 1, pour les personnes nouvellement diagnostiquées et tout leur entourage.",
    disclaimer: "De l'éducation, pas un avis médical. Chaque dose, ratio et cible se décide avec votre équipe de soins en diabète.",
    emergencyTitle: "En cas d'urgence",
    emergencyText: "Une personne vivant avec le type 1 qui est confuse, très somnolente, incapable d'avaler ou inconsciente : composez le 911.",
    emergencyLinks: { hypo: "Hypoglycémie", dka: "Acidocétose", sick: "Jours de maladie" },
    topics: "Sujets",
    inThisTopic: "Dans cette section",
    sources: "Sources",
    reviewed: "Dernière révision",
    downloads: "Téléchargements",
    downloadThis: "Emportez cette section",
    downloadNote: "Document à imprimer (PDF), document modifiable (DOCX) et présentation (PowerPoint), en français et en anglais.",
    pdf: "Document PDF", docx: "Word", pptx: "Présentation",
    about: "À propos",
    search: "Recherche",
    searchPlaceholder: "Rechercher dans la bibliothèque",
    next: "Suivant",
    prev: "Précédent",
    switchLang: "English",
    skip: "Aller au contenu",
    menu: "Menu",
    home: "Accueil",
    allSources: "Toutes les sources",
    footerNote: "Contexte canadien (québécois) : mmol/L, lignes directrices de Diabète Canada, services du Québec.",
  },
} as const;

export function formatDate(d: Date, lang: Lang) {
  return d.toLocaleDateString(lang === "fr" ? "fr-CA" : "en-CA", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
}
