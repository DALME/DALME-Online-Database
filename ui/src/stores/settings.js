// Define the settings store
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { API as apiInterface, requests } from "@/api";
import notifier from "@/notifier";
import { preferenceListSchema } from "@/schemas";

export const useSettingsStore = defineStore(
  "settings",
  () => {
    // state
    const preferenceData = ref([]);
    const ready = computed(() => preferenceData.value.length > 0);
    const options = {
      themeOptions: [
        { value: "atomone", label: "AtomOne (dark)", bg: "#272C35" },
        { value: "bbedit", label: "BBEdit (light)", bg: "#ffffff" },
        { value: "duotoneDark", label: "Duotone (dark)", bg: "#2a2734" },
        { value: "duotoneLight", label: "Duotone (light)", bg: "#faf8f5" },
        { value: "githubDark", label: "GitHub (dark)", bg: "#0d1117" },
        { value: "githubLight", label: "GitHub (light)", bg: "#ffffff" },
        { value: "oneDark", label: "OneDark (dark)", bg: "#282c34" },
        { value: "vscodeDark", label: "VSCode (dark)", bg: "#1e1e1e" },
        { value: "vscodeLight", label: "VSCode (light)", bg: "#ffffff" },
      ],
      fontSizeOptions: { min: 10, max: 18 },
    };

    // getters
    const preferences = computed(() => {
      return preferenceData.value
        ? Object.fromEntries(
            preferenceData.value.map((x) => [
              x.name,
              new Proxy(x, {
                get(target, prop) {
                  return prop === "value" ? target.value : Reflect.get(...arguments);
                },
                set(obj, prop, val) {
                  if (prop === "value") {
                    obj.value = Object.prototype.hasOwnProperty.call(val, "value")
                      ? val.value
                      : val;
                    updateServer(obj.name, obj.value);
                    return true;
                  } else {
                    return Reflect.get(...arguments);
                  }
                },
              }),
            ]),
          )
        : false;
    });

    // actions
    const getOptions = (target) => {
      return options[`${target}Options`] || [];
    };

    const updateServer = async (key, value) => {
      const { fetchAPI, success } = apiInterface();
      await fetchAPI(requests.preferences.updatePreferences(key, value));
      if (!success.value) {
        notifier.settings.prefUpdateFailed();
      }
    };

    const fetchPreferences = async () => {
      const { data, fetchAPI, success } = apiInterface();
      await fetchAPI(requests.preferences.getPreferences());
      if (success.value) {
        preferenceListSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          preferenceData.value = value;
        });
      } else {
        notifier.settings.prefRetrievalFailed();
      }
    };

    return {
      fetchPreferences,
      preferences,
      getOptions,
      preferenceData,
      ready,
    };
  },
  {
    persist: true,
  },
);
