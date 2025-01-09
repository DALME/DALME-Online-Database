// Define the preferences store machine interface.
import { defineStore } from "pinia";
import { ref } from "vue";
import { API as apiInterface, requests } from "@/api";
import notifier from "@/notifier";
import { notNully } from "@/utils";
import { preferenceListSchema } from "@/schemas";

export const usePreferencesStore = defineStore(
  "preferences",
  () => {
    // state
    const keys = ref({});
    const preferences = ref(null);

    // actions
    const getPreferences = async () => {
      if (!notNully(keys.value)) {
        const { data, fetchAPI, success } = apiInterface();
        await fetchAPI(requests.preferences.getPreferences());
        if (success.value) {
          await preferenceListSchema.validate(data.value, { stripUnknown: true }).then((value) => {
            preferences.value = value;
            value.forEach((x) => (keys.value[x.name] = x.value));
          });
        } else {
          notifier.users.prefRetrievalFailed();
        }
      }
    };

    const updatePreferences = async (route, mutation) => {
      const { newValue, key, target } = mutation.events;
      const useKey = Array.isArray(target) ? route : key;
      const useValue = Array.isArray(target) ? keys.value[useKey] : newValue;
      const { fetchAPI, success } = apiInterface();
      await fetchAPI(requests.preferences.updatePreferences(useKey, useValue));
      if (!success.value) {
        notifier.users.prefUpdateFailed();
      }
    };

    return {
      keys,
      getPreferences,
      updatePreferences,
    };
  },
  {
    persist: { paths: ["persistable"] },
  },
);
