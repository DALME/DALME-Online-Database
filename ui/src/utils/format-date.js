import { useConstants } from "@/use/constants";

const { dateFormats } = useConstants();

export const formatDate = (date, fmt, tz = null) => {
  if (date instanceof Date && !isNaN(date)) {
    const format = dateFormats[fmt];
    if (Array.isArray(format)) {
      let result = format.map((f) => {
        if (f in dateFormats) {
          const sfmt = dateFormats[f];
          if (tz) sfmt.timeZone = tz;
          return new Intl.DateTimeFormat(undefined, sfmt).format(date);
        }
        return f;
      });
      return result.join(" ");
    } else if (typeof format === "object") {
      if (tz) format.timeZone = tz;
      return new Intl.DateTimeFormat(undefined, format).format(date);
    }
  }
  return date;
};
