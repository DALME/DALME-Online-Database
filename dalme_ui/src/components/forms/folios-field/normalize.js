import * as yup from "yup";

export const empty = () => ({
  folio: null,
  damId: null,
});

export const foliosNormalizeInputSchema = yup
  .array()
  .of(
    yup
      .object()
      .shape({
        id: yup.string().uuid().required(),
        folio: yup.string().nullable().required().label("Folio"),
        damId: yup
          .object()
          .shape({
            value: yup.string().required(),
            label: yup.string().required(),
          })
          .nullable()
          .required()
          .label("DAM ID"),
        order: yup.number().required(),
        hasImage: yup.boolean().required(),
        hasTranscription: yup.boolean().required(),
      })
      .camelCase()
      .transform((data) => ({
        ...data,
        damId: { value: data.damId, label: data.damId },
        folio: data.name,
      })),
  )
  .transform((arr) =>
    arr
      .map((item, idx) => ({ ...item, order: idx }))
      .sort((x, y) => x.order - y.order),
  );

// const foliosNormalizeOutputSchema
// .compact((value) => value === empty())
// .filter((item) => !isNil(item.folio) && !isNil(item.damId))
