import { date as qDate } from "quasar";
import { format as timeagoFormat } from "timeago.js";

export const formatDate = (
  string,
  withTime = true,
  type = null,
  prefixes = ["on ", ""],
  suffixes = null,
) => {
  const format = withTime ? "D MMM YYYY @ H:mm" : "D MMM YYYY";
  let output = null;
  if (qDate.isValid(string)) {
    if (!type) {
      type = qDate.getDateDiff(Date.now(), string, "days") > 7 ? "d" : "h";
    } else {
      prefixes = null;
    }
    if (type == "d") {
      output = qDate.formatDate(string, format);
      if (prefixes) output = `${prefixes[0]}${output}`;
      if (suffixes) output = `${output}${suffixes[0]}`;
    } else {
      output = timeagoFormat(string);
      if (prefixes) output = `${prefixes[1]}${output}`;
      if (suffixes) output = `${output}${suffixes[1]}`;
    }
  }
  return output;
};
