import { date as qDate } from "quasar";
import { format as timeagoFormat } from "timeago.js";

export const formatDate = (
  string,
  withTime = true,
  prefixes = ["on ", ""],
  suffixes = null,
) => {
  let date = null;
  const format = withTime ? "D MMM YYYY @ H:mm" : "D MMM YYYY";
  if (qDate.isValid(string)) {
    if (qDate.getDateDiff(Date.now(), string, "days") > 7) {
      date = qDate.formatDate(string, format);
      if (prefixes) date = `${prefixes[0]}${date}`;
      if (suffixes) date = `${date}${suffixes[0]}`;
    } else {
      date = timeagoFormat(string);
      if (prefixes) date = `${prefixes[1]}${date}`;
      if (suffixes) date = `${date}${suffixes[1]}`;
    }
  }
  return date;
};
