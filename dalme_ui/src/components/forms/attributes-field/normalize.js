import moment from "moment";

import { attributeValidators } from "@/schemas";

export const empty = () => ({ attribute: null, value: null });

// Transform initial attributes data to the correct shape expected by the form.
// NOTE: I've tried to capture the most general patterns here but due to
// disrepancies in the API/serializing I've had to add case-by-case transforms
// to certain editSchemas to shim around data issues. Hopefully future dev will
// ameliorate these complexities and we will be able to delete plentifully.
export const normalizeAttributesInput = (attributeTypes, attributes) => {
  const normalized = attributeTypes.map((attributeType) => {
    const data = attributes[attributeType.shortName];

    // NOTE: Until we can refactor the API properly we'll have to capture all
    // the complextity in this switch statement.
    /* eslint-disable */
    switch (attributeType.dataType) {
      case "Options":
        const validator = attributeValidators[attributeType.shortName];

        // It's been parsed by another schema into the expected options format.
        if (data.hasOwnProperty("value") && data.hasOwnProperty("label")) {
          return { attribute: attributeType, value: data };
        }

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

        // It just needs to be transformed into a value/label payload while
        // parsing the JSONified ID field.
        if (data.hasOwnProperty("id") && data.hasOwnProperty("name")) {
          try {
            return {
              attribute: attributeType,
              value: { value: JSON.parse(data.id).id, label: data.name },
            };
          } catch {
            return {
              attribute: attributeType,
              value: { value: data.id, label: data.name },
            };
          }
        }

        // It just needs to be transformed into a value/label payload, but it
        // comes down from the API wrapped in a list so we need to unpack it
        // and parse the JSONified ID field.
        if (Array.isArray(data)) {
          const { name, id } = data[0];
          return {
            attribute: attributeType,
            value: { label: name, value: JSON.parse(id).id },
          };
        }

        // It's a non-ID driven select value, probably just a (string, string)
        // tuple making up a simple set of non-FK choices.
        return {
          attribute: attributeType,
          value: { label: data, value: data },
        };

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

export const normalizeOutputSchema = (attributes) => attributes;
// export const normalizeOutputSchema = yup
//   .array()
//   .nullable()
//   .compact((value) => value === empty())
//   .of(outputSchema)
//   .transform((final) => (isEmpty(final) ? null : final));
