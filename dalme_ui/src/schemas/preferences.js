import * as yup from "yup";

export const preferenceSchema = yup.object().shape({
  ui: yup.object().shape({
    tooltipsOn: yup.boolean().required(),
    sidebarCollapsed: yup.boolean().required(),
  }),
  sourceEditor: yup.object().shape({
    fontSize: yup.string().required(),
    highlightWord: yup.boolean().required(),
    showGuides: yup.boolean().required(),
    showGutter: yup.boolean().required(),
    showInvisibles: yup.boolean().required(),
    showLineNumbers: yup.boolean().required(),
    softWrap: yup.boolean().required(),
    theme: yup.string().required(),
  }),
});
