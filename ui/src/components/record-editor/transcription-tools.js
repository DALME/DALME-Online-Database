import { API, requests } from "@/api";
import { completionListSchema } from "@/schemas";

const { loading, success, data, fetchAPI } = API();

export const getCompletions = (context) => {
  return new Promise((resolve) => {
    console.log("getCompletions", context);
    const language = "618";
    let word = context.matchBefore(/\w*/);
    console.log("completion", word);
    if (word.from == word.to && !context.explicit) {
      resolve(null);
    }
    const request = requests.languages.getCompletions(language, { word: word.text });
    fetchAPI(request).then(() => {
      if (success.value) {
        completionListSchema.validate(data.value, { stripUnknown: false }).then((value) => {
          loading.value = false;
          console.log("completions returning", value);
          resolve({
            from: word.from,
            options: value,
          });
        });
      }
    });
  });
};
