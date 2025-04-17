import { filter as rFilter, isNil, pipe, reduce } from "ramda";
import * as yup from "yup";

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
    // the complexity in this switch statement.
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
          value: new Date(data.name).toISOString(),
        };

      default:
        return { attribute: attributeType, value: data };
    }
    /* eslint-enable */
  });

  return normalized;
};

// Transforms attributes data from the form component to the correct shape as
// expected by the API during POST/PUT operations.
export const normalizeAttributesOutput = ({ attributes }) => {
  const normalize = (dataType, value) => {
    /* eslint-disable */
    switch (dataType) {
      case "Boolean":
        return Boolean(value.value);
      case "Date":
        const date = new Date(value);
        return {
          value: {
            y: date.getFullYear(),
            m: date.getMonth() + 1,
            d: date.getDate(),
          },
        };
      case "Options":
        const handleOption = ({ value }) => {
          try {
            return { id: yup.string().uuid().validateSync(value) };
          } catch {
            try {
              return { id: yup.number().validateSync(value) };
            } catch {
              return value;
            }
          }
        };
        return Array.isArray(value)
          ? value.map((option) => handleOption(option))
          : handleOption(value);
      default:
        return value;
    }
    /* eslint-enable */
  };

  const reducer = (acc, { attribute, value }) => {
    const { shortName, dataType } = attribute;
    return { ...acc, [shortName]: normalize(dataType, value) };
  };

  const normalized = pipe(
    rFilter(({ attribute, value }) => !(isNil(attribute) && isNil(value))),
    reduce(reducer, {}),
  )(attributes);

  return normalized;
};

// NOTE: Used for sets where we present optional attributes to the user to
// maintain similarity with other CRUD instances but where what look like
// attributes map to actual fields on the model itself. So, here we just need
// to unpack the attribtutes data structure into a kwargs-like pattern. Also,
// we only need to handle options and the default here due to the limited
// 'attribute' fields permitted on sets but if we need to expand it then we can
// do so in the future.
export const unpackPseudoAttributes = ({ attributes }) => {
  const reducer = (acc, { attribute, value }) => {
    /* eslint-disable */
    switch (attribute.dataType) {
      case "Boolean":
        return { ...acc, [attribute.shortName]: value.value };
      case "Options":
        return { ...acc, [attribute.shortName]: value.value };
      default:
        return { ...acc, [attribute.shortName]: value };
    }
    /* eslint-enable */
  };
  return attributes ? reduce(reducer, {}, attributes) : {};
};
