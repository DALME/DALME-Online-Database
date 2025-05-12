<template>
  <q-btn
    :class="underEdit ? 'editing' : 'orange'"
    :disable="!isDetail || underEdit"
    :icon="underEdit ? 'edit_off' : 'edit'"
    :loading="loading"
    :onclick="handleClick"
    size="11px"
    square
  >
    <template #loading>
      <q-spinner-facebook />
    </template>
  </q-btn>
</template>

<script>
import { createId as cuid } from "@paralleldrive/cuid2";
import { useActor } from "@xstate/vue";
import { isNil, keys } from "ramda";
import { computed, defineComponent } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { normalizeAttributesInput } from "@/components/forms/attributes-field/normalize";
import forms from "@/forms";
import { attributeTypeSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "EditUpdate",
  setup() {
    const mode = "update";
    const { apiInterface } = useAPI();
    const {
      editingIndex,
      isDetail,
      modals,
      resource,
      machine: { send },
    } = useEditing();
    const $route = useRoute();

    const { success, data, fetchAPI, loading } = apiInterface();
    const id = computed(() => $route.params.id);
    const key = computed(() => `form-${resource.value}-${id.value}`);
    const underEdit = computed(() => !isNil(editingIndex.value[key.value]));

    const spawnForm = (initialData) =>
      send({
        type: "SPAWN_FORM",
        cuid: cuid(),
        key: key.value,
        kind: resource.value,
        initialData,
        mode,
      });

    // NOTE: This is not very pleasing on the eye.
    const handleClick = async () => {
      const indexed = editingIndex.value[key.value];
      if (underEdit.value) {
        const { send: actorSend } = useActor(modals.value[indexed.cuid].actor);
        send({ type: "SET_FOCUS", value: indexed.cuid });
        actorSend({ type: "SHOW" });
      } else {
        loading.value = true;
        console.log(forms[resource.value]);
        const {
          edit: editSchema,
          requests: { get },
        } = forms[resource.value];
        await fetchAPI(get(id.value));
        if (success.value) {
          await editSchema.validate(data.value, { stripUnknown: true }).then(async (value) => {
            // We only need to transform the attributes if they are there,
            // otherwise the schema has taken care of everything already.
            if (!value.attributes) {
              spawnForm(value);
            } else {
              const { success, data, fetchAPI } = apiInterface();
              const { attributes } = value;
              const shortNames = keys(attributes).join(",");
              const request = requests.attributeTypes.getByShortName(shortNames);
              await fetchAPI(request);
              if (success.value)
                await attributeTypeSchema
                  .validate(data.value.data, { stripUnknown: true })
                  .then((attributeTypes) => {
                    const normalized = {
                      ...value,
                      attributes: normalizeAttributesInput(attributeTypes, attributes),
                    };
                    spawnForm(normalized);
                  });
            }
          });
        }
        loading.value = false;
      }
    };

    return {
      underEdit,
      handleClick,
      isDetail,
      loading,
      resource,
    };
  },
});
</script>
