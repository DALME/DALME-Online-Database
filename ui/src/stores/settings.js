// Define the settings store
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { API as apiInterface, requests } from "@/api";
import notifier from "@/notifier";
import { nully } from "@/utils";
import { preferenceListSchema, TeiUserElementSetsSchema } from "@/schemas";
import { filter as rFilter, forEach } from "ramda";

export const useSettingsStore = defineStore(
  "settings",
  () => {
    // state
    const preferenceData = ref({});
    const teiElementSetData = ref({});
    const teiElementData = ref({});

    // getters
    const preferences = computed(() =>
      Object.fromEntries(preferenceData.value.map((x) => [x.name, x.value])),
    );

    const sets = computed(() => {
      if (!nully(teiElementSetData.value)) {
        return Array.from(teiElementSetData.value, (x) =>
          Object.assign(x, {
            members: forEach(
              (y) =>
                Object.assign(
                  y,
                  teiElementData.value.find((z) => z.id == y.element),
                ),
              x.members,
            ),
          }),
        );
      } else {
        return [];
      }
    });

    const userSets = computed(() => {
      if (!nully(sets.value)) {
        return rFilter((x) => nully(x.project), sets);
      } else {
        return [];
      }
    });

    // actions
    const get = (key, defaultValue = null) => {
      if (key in preferences.value) {
        return preferences.value[key];
      } else if (defaultValue !== null) {
        return defaultValue;
      } else {
        return null;
      }
    };

    const update = (key, value) => {
      if (key && (value || value === false)) {
        preferenceData.value.find((x) => x.name == key).value = value;
        updateServer(key, value);
      }
    };

    const updateServer = async (key, value) => {
      const { fetchAPI, success } = apiInterface();
      await fetchAPI(requests.preferences.updatePreferences(key, value));
      if (!success.value) {
        notifier.users.prefUpdateFailed();
      }
    };

    const fetchPreferences = async () => {
      const { data, fetchAPI, success } = apiInterface();
      await fetchAPI(requests.preferences.getPreferences());
      if (success.value) {
        await preferenceListSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          preferenceData.value = value;
        });
      } else {
        notifier.settings.prefRetrievalFailed();
      }
    };

    const fetchTeiElements = async () => {
      console.log("called fetchTeiElements with"), nully(teiElementSetData.value);
      if (nully(teiElementSetData.value)) {
        const { data, fetchAPI, success } = apiInterface();
        await fetchAPI(requests.teiElements.getElementSets());
        if (success.value) {
          await TeiUserElementSetsSchema.validate(data.value, { stripUnknown: true }).then(
            (value) => {
              teiElementSetData.value = value.sets;
              teiElementData.value = value.elements;
            },
          );
        } else {
          notifier.settings.teiElementSetsRetrievalFailed();
        }
      }
    };

    return {
      preferenceData,
      teiElementSetData,
      teiElementData,
      get,
      update,
      sets,
      userSets,
      fetchPreferences,
      fetchTeiElements,
    };
  },
  {
    persist: true,
  },
);
