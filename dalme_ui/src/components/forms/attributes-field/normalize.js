import moment from "moment";

import { attributeValidators } from "@/schemas";

export const empty = () => ({ attribute: null, value: null });

// Transform initial attributes data to the correct shape expected by the form.
export const normalizeAttributesInput = (attributeTypes, attributes) => {
  const normalized = attributeTypes.map((attributeType) => {
    const data = attributes[attributeType.shortName];

    // NOTE: Until we can refactor the API properly we'll have to capture all
    // the complextity in this switch statement.
    /* eslint-disable */
    switch (attributeType.dataType) {
      case "Options":
        const validator = attributeValidators[attributeType.shortName];
        // It's a MultipleSelect value.
        if (validator.type === "array") {
          return {
            attribute: attributeType,
            value: data.map((item) => {
              const { id } = JSON.parse(item.id);
              return { label: item.name, value: id };
            }),
          };
        }
        // It's just a Select value but it comes down from the API wrapped in a
        // list so we need to unpack it before it's rendered.
        if (Array.isArray(data)) {
          const { name, id } = data[0];
          return {
            attribute: attributeType,
            value: { label: name, value: JSON.parse(id).id },
          };
        }
        // It's a non-ID driven Select value, probably just a string from a
        // simple set of options choices.
        return { attribute: attributeType, value: data };
      case "Date":
        return {
          attribute: attributeType,
          value: moment(new Date(data.name)).format("YYYY-MM-DD"),
        };
      default:
        return { attribute: attributeType, value: data };
    }
    /* eslint-enable */
  });

  return normalized;
};

// TODO: Eliminate empties.
export const normalizeAttributesOutput = (attributes) => attributes;

// export const normalizeOutputSchema = yup
//   .array()
//   .nullable()
//   .compact((value) => value === empty())
//   .of(outputSchema)
//   .transform((final) => (isEmpty(final) ? null : final));