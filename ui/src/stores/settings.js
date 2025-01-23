// Define the settings store
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { API as apiInterface, requests } from "@/api";
import notifier from "@/notifier";
import { nully } from "@/utils";
import { preferenceListSchema, UserElementSetsSchema } from "@/schemas";
import { filter as rFilter, forEach, sortBy, prop } from "ramda";

export const useSettingsStore = defineStore(
  "settings",
  () => {
    // state
    const preferenceData = ref({});
    const teiElementSetData = ref({});
    const teiElementData = ref({});
    const teiTagData = ref({});
    const currentSetId = ref("");
    const teiReady = ref(false);

    // getters
    const preferences = computed(() =>
      Object.fromEntries(preferenceData.value.map((x) => [x.name, x.value])),
    );

    const allSets = computed(() =>
      Array.from(teiElementSetData.value, (x) =>
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
      ),
    );
    const userSets = computed(() => rFilter((x) => nully(x.value.project), allSets));
    const currentSet = computed(() => allSets.value.find((x) => x.id == currentSetId.value));

    const sets = computed(() => ({
      all: allSets,
      user: userSets,
      current: currentSet,
      filter: filterSets,
    }));

    const allElements = computed(() => teiElementData.value);
    const currentSetAll = computed(() => currentSet.value.members);
    const currentSetMenu = computed(() =>
      rFilter((x) => x.inContextMenu == true, currentSetAll.value),
    );
    const currentSetToolbar = computed(() =>
      rFilter((x) => x.inToolbar == true, currentSetAll.value),
    );

    const elements = computed(() => ({
      all: allElements,
      current: currentSetAll,
      menu: currentSetMenu,
      toolbar: currentSetToolbar,
      filter: filterElements,
      get: getElement,
    }));

    const allTags = computed(() => teiTagData.value);
    const currentSetTags = computed(() =>
      rFilter((x) => currentSetAll.value.flatMap((x) => x.tags).includes(x.id), teiTagData.value),
    );
    const tagNames = computed(() => allTags.value.map((x) => x.name));

    const tags = computed(() => ({
      all: allTags,
      current: currentSetTags,
      names: tagNames,
      filter: filterTags,
      get: getTag,
    }));

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
        preferenceListSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          preferenceData.value = value;
        });
      } else {
        notifier.settings.prefRetrievalFailed();
      }
    };

    const fetchTeiElements = () => {
      return new Promise((resolve) => {
        const { data, fetchAPI, success } = apiInterface();
        fetchAPI(requests.teiElements.getElementSets()).then(() => {
          if (success.value) {
            UserElementSetsSchema.validate(data.value, { stripUnknown: true }).then((value) => {
              console.log(value.sets);
              teiElementSetData.value = value.sets;
              teiElementData.value = value.elements;
              teiTagData.value = value.tags;
              // temp workaround - this should be set by the UI
              currentSetId.value = value.sets[0].id;
              return resolve(true);
            });
          } else {
            notifier.settings.teiElementSetsRetrievalFailed();
            return resolve(false);
          }
        });
      });
    };

    const filterSets = (value, attribute = "all") => {
      let filter;
      if (attribute == "all") {
        filter = (x) =>
          x.label.toLowerCase().includes(value.toLowerCase()) ||
          x.description.toLowerCase().includes(value.toLowerCase()) ||
          x.project.toLowerCase().includes(value.toLowerCase());
      } else {
        filter = (x) => x[attribute] == value;
      }
      return rFilter(filter, allSets);
    };

    const filterElements = (value, attribute = "all", sort = "label", target = "current") => {
      if (nully(value)) {
        return sortBy(prop(sort), elements.value[target].value);
      } else {
        let filter;
        if (attribute == "all") {
          filter = (x) =>
            x.label.toLowerCase().includes(value.toLowerCase()) ||
            x.section.toLowerCase().includes(value.toLowerCase()) ||
            x.description.toLowerCase().includes(value.toLowerCase());
        } else {
          filter = (x) => x[attribute] == value;
        }
        return rFilter(filter, sortBy(prop(sort), elements.value[target].value));
      }
    };

    const getElement = (id) => {
      return rFilter((x) => x.id == id, teiElementData.value)[0];
    };

    const filterTags = (tag, attributes) => {
      // console.log("filterTags", tag, attributes);
      const filter = (x) => {
        if (x.name === tag) {
          // console.log(`${x.name} === ${tag}`);
          if (!nully(attributes)) {
            // console.log("attributes not null");
            if ("type" in attributes) {
              // console.log("type in attributes");
              const type_ref = x.attributes.find((y) => y.value === "type");
              if (nully(type_ref)) {
                return false;
              }
              if (!type_ref.editable) {
                return ["auto", attributes.type].includes(type_ref.default);
              }
            }
            for (const property in attributes) {
              const ref_attr = x.attributes.find((y) => y.value === property);
              if (nully(ref_attr)) {
                // console.log(`${property} not found in ${x.name}`);
                return false;
              } else {
                if (
                  !ref_attr.editable &&
                  !["auto", attributes[property]].includes(ref_attr.default)
                ) {
                  // console.log(`${ref_attr.default} not in auto, ${attributes[property]}`);
                  return false;
                } else {
                  if (
                    ref_attr.kind !== "multichoice" &&
                    ref_attr.options &&
                    !ref_attr.options.find((z) => z.value === attributes[property])
                  ) {
                    // console.log(
                    //   `${attributes[property]} not in ${ref_attr.options.map((z) => z.value)}`,
                    // );
                    return false;
                  }
                }
              }
            }
          }
          return true;
        }
        return false;
      };
      return rFilter(filter, teiTagData.value);
    };

    const getTag = (id) => {
      return rFilter((x) => x.id == id, teiTagData.value)[0];
    };

    return {
      preferenceData,
      teiElementSetData,
      teiElementData,
      teiTagData,
      get,
      update,
      sets,
      fetchPreferences,
      fetchTeiElements,
      currentSetId,
      elements,
      teiReady,
      tags,
    };
  },
  {
    persist: true,
  },
);
