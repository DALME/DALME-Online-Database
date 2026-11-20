import { API, requests } from "@/api";
import { completionListSchema } from "@/schemas";

const { loading, success, data, fetchAPI } = API();

export const getCompletions = (context) => {
  return new Promise((resolve) => {
    const language = "618";
    let word = context.matchBefore(/\w*/);
    if (word.from == word.to && !context.explicit) {
      resolve(null);
    }
    const request = requests.languages.getCompletions(language, { word: word.text });
    fetchAPI(request).then(() => {
      if (success.value) {
        completionListSchema.validate(data.value, { stripUnknown: false }).then((value) => {
          loading.value = false;
          resolve({
            from: word.from,
            options: value,
          });
        });
      }
    });
  });
};
