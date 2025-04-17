import { useConstants } from "@/use/constants";

const { dateFormats } = useConstants();

export const formatDate = (date, fmt) => {
  const format = dateFormats[fmt];
  if (Array.isArray(format)) {
    let result = format.map((f) => {
      if (f in dateFormats) return new Intl.DateTimeFormat(undefined, dateFormats[f]).format(date);
      return f;
    });
    return result.join(" ");
  } else if (typeof format === "object") {
    return new Intl.DateTimeFormat(undefined, format).format(date);
  }
};
