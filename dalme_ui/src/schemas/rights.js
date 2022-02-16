import { head } from "ramda";
import * as yup from "yup";

export const rightsListSchema = yup.array().of(
  yup
    .object()
    .shape({
      id: yup.string().uuid().required(),
      name: yup.string().required(),
      rights: yup.string().required(),
      rightsHolder: yup.string().required(),
      rightsStatus: yup
        .object()
        .shape({
          id: yup.number().required(),
          name: yup.string().required(),
        })
        .required(),
      publicDisplay: yup.boolean().required(),
      noticeDisplay: yup.boolean().required(),
      attachments: yup
        .object()
        .shape({
          id: yup.string().uuid().required(),
          kind: yup.string().required(),
          url: yup.string().required(),
        })
        .transform((value) => {
          if (value) {
            const node = document.createElement("html");
            node.innerHTML = value.pill;
            const link = head(node.getElementsByTagName("a"));
            const kind = link.innerText;
            const href = link.getAttribute("href");
            const [, , , year, month] = href.split("/");
            const id = value.file.file_id;
            const filename = value.file.filename;
            const url = `/download/attachments/${year}/${month}/${filename}`;
            return { id, kind, url };
          }
          return value;
        })
        .default(null)
        .nullable(),
    })
    .camelCase(),
);
