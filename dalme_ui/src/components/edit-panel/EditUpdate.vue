<template>
  <q-btn
    fab
    icon="edit"
    text-color="black"
    :color="!isDetail ? 'grey' : 'amber'"
    :disable="!isDetail"
    :loading="loading"
    :onclick="handleClick"
  >
    <template v-slot:loading>
      <q-spinner-facebook />
    </template>
  </q-btn>
</template>

<script>
import cuid from "cuid";
import { keys } from "ramda";
import { computed, defineComponent } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { normalizeAttributesInput } from "@/components/forms/attributes-field/normalize";
import forms from "@/forms";
import { attributeTypesSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "EditUpdate",
  setup() {
    const mode = "update";

    const { apiInterface } = useAPI();
    const {
      isDetail,
      resource,
      machine: { send },
    } = useEditing();
    const $route = useRoute();

    const { success, data, fetchAPI, loading } = apiInterface();

    const id = computed(() => $route.params.id);

    const spawnForm = (initialData) =>
      send("SPAWN_FORM", {
        cuid: cuid(),
        initialData,
        kind: resource.value,
        mode,
      });

    // NOTE: This is not very pleasing.
    const handleClick = async () => {
      loading.value = true;
      const {
        edit: editSchema,
        requests: { get },
      } = forms[resource.value];
      await fetchAPI(get(id.value));
      if (success.value) {
        await editSchema
          .validate(data.value, { stripUnknown: true })
          .then(async (value) => {
            // We only need to transform the attributes if they are there,
            // otherwise the schema has taken care of everything already.
            if (!value.attributes) {
              spawnForm(value);
            } else {
              const { success, data, fetchAPI } = apiInterface();
              const { attributes } = value;
              const shortNames = keys(attributes).join(",");
              const request =
                requests.attributeTypes.getAttributeTypesByShortName(
                  shortNames,
                );
              await fetchAPI(request);
              if (success.value)
                await attributeTypesSchema
                  .validate(data.value, { stripUnknown: true })
                  .then((attributeTypes) => {
                    const normalized = {
                      ...value,
                      attributes: normalizeAttributesInput(
                        attributeTypes,
                        attributes,
                      ),
                    };
                    spawnForm(normalized);
                  });
            }
          });
      }
      loading.value = false;
    };

    return {
      handleClick,
      isDetail,
      loading,
      resource,
    };
  },
});
</script>
