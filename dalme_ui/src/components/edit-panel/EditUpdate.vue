<template>
  <q-btn
    fab
    icon="edit"
    text-color="black"
    :disable="!isDetail"
    :color="!isDetail ? 'grey' : 'amber'"
    :onclick="() => handleClick(resource)"
  />
</template>

<script>
import cuid from "cuid";
import { computed, defineComponent } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import forms from "@/forms";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "EditUpdate",
  setup() {
    const mode = "update";

    const { apiInterface } = useAPI();
    const {
      isDetail,
      machine: { send },
    } = useEditing();
    const $route = useRoute();

    const { success, data, fetchAPI } = apiInterface();

    const id = computed(() => $route.params.id);
    // TODO: resourceKind (to handle Source/Set polymorphism)
    const resource = computed(() => $route.name.toLowerCase());

    const handleClick = async (kind) => {
      const { edit: editSchema } = forms[kind];
      await fetchAPI(requests.tasks.getTask(id.value));
      if (success.value) {
        await editSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            send("SPAWN_FORM", {
              cuid: cuid(),
              initialData: value,
              kind,
              mode,
            });
          });
      }
    };

    return {
      handleClick,
      isDetail,
      resource,
    };
  },
});
</script>
