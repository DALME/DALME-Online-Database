const languageTypes = [
  {
    label: "Dialect",
    value: true,
    class: "text-grey-8",
    classSelected: "text-weight-bold bg-indigo-1 text-indigo-5",
  },
  {
    label: "Language",
    value: false,
    class: "text-grey-8",
    classSelected: "text-weight-bold bg-indigo-1 text-indigo-5",
  },
];
export const filterList = {
  filters: [
    {
      label: "Type",
      selection: "single",
      type: "generic",
      field: "is_dialect",
      items: languageTypes,
      isolation: false,
    },
  ],
};
