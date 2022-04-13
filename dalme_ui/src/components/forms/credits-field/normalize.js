import { isEmpty } from "ramda";
import * as yup from "yup";

// IN: [{
//   id: "00000000-0000-0000-0000-000000000000",
//   standard_name: "foo",
//   type: {
//     id: 1,
//     name: "bar",
//    },
//    note: "baz",
// }]
// OUT: [{
//   "id": "00000000-0000-0000-0000-000000000000",
//   "type": "1",
//   "note": "baz"
// }]

export const empty = () => ({ agent: null, role: null, note: null });

export const creditsNormalizeInputSchema = yup.array().of(
  yup
    .object()
    .shape({
      agent: yup.object().shape({
        value: yup.string().uuid().required(),
        label: yup.string().required(),
      }),
      role: yup.object().shape({
        value: yup.number().required(),
        label: yup.string().required(),
      }),
      note: yup.string().default(null).nullable(),
    })
    .camelCase()
    .transform((data) => ({
      agent: { value: data.id, label: data.standardName },
      role: { value: data.type.id, label: data.type.name },
      note: data.note,
    })),
);

export const creditsNormalizeOutputSchema = yup
  .array()
  .nullable()
  .compact((value) => value === empty())
  .of(
    yup
      .object()
      .shape({
        agent: yup.string().uuid().required(),
        type: yup.number().required(),
        note: yup.string().default(null).nullable(),
      })
      .transform((data) => ({
        agent: data.agent.value,
        type: data.role.value,
        note: data.note,
      })),
  )
  .transform((final) => (isEmpty(final) ? null : final));
