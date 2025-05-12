// Define the editor store
import { defineStore } from "pinia";
import { useRepo } from "pinia-orm";
import { useCollect, usePluck } from "pinia-orm/helpers";
import { computed, ref } from "vue";

import { API as apiInterface, requests } from "@/api";
import { TeiElement, TeiSet, TeiSetMember, TeiTag } from "@/models";
import notifier from "@/notifier";
import { UserElementSetsSchema } from "@/schemas";
import { nully } from "@/utils";

export const useEditorStore = defineStore(
  "editor",
  () => {
    // stores and repositories
    const teiElement = useRepo(TeiElement);
    const teiTag = useRepo(TeiTag);
    const teiSet = useRepo(TeiSet);
    const teiSetMember = useRepo(TeiSetMember);

    // state
    const ready = ref(false);
    const currentSetId = ref("");

    // getters
    const tagNames = computed(() => {
      return usePluck(teiTag.all(), "name");
    });

    const toolbar = computed(() => {
      const toolbarEls = teiSetMember
        .with("elementObj", (q) => q.with("tags"))
        .where((q) => q.set === currentSetId.value && q.inToolbar)
        .get();

      return useCollect(
        toolbarEls.map((x) => {
          const { elementObj, ...el } = x;
          return Object.assign(el, elementObj.$toJson());
        }),
      ).groupBy("section");
    });

    const contextMenu = computed(() => {
      const menuEls = teiSetMember
        .with("elementObj", (q) => q.with("tags"))
        .where((q) => q.set === currentSetId.value && q.inContextMenu)
        .get();

      return menuEls.map((x) => {
        const { elementObj, ...el } = x;
        return Object.assign(el, elementObj.$toJson());
      });
    });

    // actions
    const initialize = () => {
      return new Promise((resolve) => {
        fetchTeiElements().then((data) => {
          if (data) {
            teiElement.save(data.elements);
            teiTag.save(data.tags);
            teiSet.save(data.sets);
            teiSetMember.save(data.setMembers);
            ready.value = true;
            return resolve(true);
          } else {
            return resolve(false);
          }
        });
      });
    };

    const elements = (query = null) => {
      if (!query) {
        return teiElement.all();
      } else {
        if (typeof query === "string") {
          return teiElement
            .where(
              (q) =>
                q.label.toLowerCase().includes(query.toLowerCase()) ||
                q.section.toLowerCase().includes(query.toLowerCase()) ||
                q.description.toLowerCase().includes(query.toLowerCase()),
            )
            .get();
        }
      }
    };

    const sets = () => {
      return teiSet.all();
    };

    const tags = (tag = null, attributes = null) => {
      const filter = (x) => {
        if (x.name === tag) {
          if (!nully(attributes)) {
            if ("type" in attributes) {
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
                return false;
              } else {
                if (
                  !ref_attr.editable &&
                  !["auto", attributes[property]].includes(ref_attr.default)
                ) {
                  return false;
                } else {
                  if (
                    ref_attr.kind !== "multichoice" &&
                    ref_attr.options &&
                    !ref_attr.options.find((z) => z.value === attributes[property])
                  ) {
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

      if (!tag && !attributes) {
        return teiTag.with("elementObj").all();
      } else {
        return teiTag
          .with("elementObj")
          .where((q) => filter(q))
          .get();
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
            notifier.editor.teiElementSetsRetrievalFailed();
            return resolve(false);
          }
        });
      });
    };

    return {
      initialize,
      ready,
      toolbar,
      contextMenu,
      elements,
      sets,
      tagNames,
      tags,
      currentSetId,
    };
  },
  {
    persist: true,
  },
);
