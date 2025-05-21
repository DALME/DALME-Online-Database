export const teiSelectors = {
  braces: "tei-seg[type=brace]",
  marginalNotes: "tei-note[type=marginal]",
  renvois: "tei-ref[target]",
  columns: "tei-ab[type=column]",
  leaders: "tei-metamark[function=leader]",
};

export const editorModeIcons = {
  update: "edit_note",
  create: "playlist_add",
};

export const fontSizeOptions = { min: 10, max: 18 };

export const themeOptions = [
  { value: "atomone", label: "AtomOne (dark)", bg: "#272C35" },
  { value: "bbedit", label: "BBEdit (light)", bg: "#ffffff" },
  { value: "duotoneDark", label: "Duotone (dark)", bg: "#2a2734" },
  { value: "duotoneLight", label: "Duotone (light)", bg: "#faf8f5" },
  { value: "githubDark", label: "GitHub (dark)", bg: "#0d1117" },
  { value: "githubLight", label: "GitHub (light)", bg: "#ffffff" },
  { value: "oneDark", label: "OneDark (dark)", bg: "#282c34" },
  { value: "vscodeDark", label: "VSCode (dark)", bg: "#1e1e1e" },
  { value: "vscodeLight", label: "VSCode (light)", bg: "#ffffff" },
];
