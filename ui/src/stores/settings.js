// Define the settings store
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { API as apiInterface, requests } from "@/api";
import notifier from "@/notifier";
import { nully } from "@/utils";
import { preferenceListSchema, UserElementSetsSchema } from "@/schemas";
import { filter as rFilter, sortBy, prop } from "ramda";

export const useSettingsStore = defineStore(
  "settings",
  () => {
    // state
    const preferenceData = ref([]);
    const teiElementSetData = ref([]);
    const teiElementData = ref([]);
    const teiTagData = ref([]);
    const currentSetId = ref("");
    const loaded = computed(() => preferenceData.value.length > 0);
    const teiReady = computed(() => teiElementData.value.length > 0);
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

    // #region getters
    // #region getters - preferences
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
    // #endregion
    // #region getter - sets
    const sets = computed(() => ({
      all: teiElementSetData.value,
      user: rFilter((x) => nully(x.project), teiElementSetData.value),
      current:
        teiReady.value && currentSetId.value
          ? teiElementSetData.value.find((x) => x.id == currentSetId.value)
          : [],
      filter: filterSets,
    }));
    // #endregion
    // #region getters - elements
    const elements = computed(() => ({
      all: teiElementData.value.map((x) => Object.assign(x, getElement(x.element))),
      current: sets.value.current.members?.map((x) => Object.assign(x, getElement(x.element))),
      menu: rFilter((x) => x.inContextMenu == true, sets.value.current.members),
      toolbar: rFilter((x) => x.inToolbar == true, sets.value.current.members),
      filter: filterElements,
      get: getElement,
    }));
    // #endregion
    // #region getters - tags
    const tags = computed(() => ({
      all: teiTagData.value,
      current: rFilter(
        (x) => elements.value.current.flatMap((x) => getElement(x.element).tags).includes(x.id),
        teiTagData.value,
      ),
      names: teiTagData.value.map((x) => x.name),
      filter: filterTags,
      get: getTag,
    }));
    // #endregion
    // #endregion
    // #region actions - getters
    const getOptions = (target) => {
      return options[`${target}Options`] || [];
    };

    const getElement = (id) => {
      return rFilter((x) => x.id == id, teiElementData.value)[0];
    };

    const getTag = (id) => {
      return rFilter((x) => x.id == id, teiTagData.value)[0];
    };
    // #endregion
    // #region actions - filters
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
      return rFilter(filter, sets.value.all);
    };

    const filterElements = (value, attribute = "all", sort = "label", target = "current") => {
      if (nully(value)) {
        return sortBy(prop(sort), elements.value[target]);
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
        return rFilter(filter, sortBy(prop(sort), elements.value[target]));
      }
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
    // #endregion
    // #region actions - fetchers
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

    const fetchTeiElements = () => {
      return new Promise((resolve) => {
        const { data, fetchAPI, success } = apiInterface();
        fetchAPI(requests.teiElements.getElementSets()).then(() => {
          if (success.value) {
            UserElementSetsSchema.validate(data.value, { stripUnknown: true }).then((value) => {
              return resolve(value);
            });
          } else {
            notifier.settings.teiElementSetsRetrievalFailed();
            return resolve(false);
          }
        });
      });
    };
    // #endregion
    // #region actions - utilities
    const getElementAttributes = (el, actual = []) => {
      if ("element" in el) el = getElement(el.element);
      const editing = actual.length > 0;
      const results = {};
      const tags = el.tags.map((x) => getTag(x));
      for (const tag of tags) {
        let attributes = [];
        const actualAttrs = actual.length > 0 ? actual.find((x) => x.name === tag.name) : false;
        for (const attr of tag.attributes) {
          if (editing && el.kind === "supplied" && attr.value === "text") continue;
          let cValue;
          if (attr.value in actualAttrs) {
            cValue = structuredClone(actualAttrs[attr.value]);
          } else if (attr.default) {
            cValue = structuredClone(attr.default);
          } else {
            cValue = attr.kind === "multichoice" ? [] : "";
          }
          attributes.push({
            default: attr.label || null,
            description: attr.description,
            editable: attr.editable,
            required: attr.required,
            kind: attr.kind,
            label: attr.label,
            value: attr.value,
            options: attr.options || [],
            currentValue: cValue,
          });
        }
        results[tag.name] = attributes;
      }
      return results;
    };
    // #endregion

    return {
      sets,
      fetchPreferences,
      fetchTeiElements,
      currentSetId,
      elements,
      teiReady,
      tags,
      preferences,
      getOptions,
      preferenceData,
      teiElementSetData,
      teiElementData,
      teiTagData,
      getElementAttributes,
      loaded,
    };
  },
  {
    persist: true,
  },
);
