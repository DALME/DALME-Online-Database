<template>
  <q-btn
    fab
    icon="edit"
    text-color="black"
    :disable="!isDetail"
    :color="!isDetail ? 'grey' : 'amber'"
    :onclick="handleClick"
  />
</template>

<script>
import cuid from "cuid";
import { computed, defineComponent } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { taskSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "EditUpdate",
  setup(_, context) {
    const mode = "update";

    const { success, data, fetchAPI } = useAPI(context);
    const {
      isDetail,
      machine: { send },
    } = useEditing();
    const $route = useRoute();

    const id = computed(() => $route.params.id);
    const kind = computed(() => $route.name.toLowerCase());

    const getRequest = () => requests.tasks.getTask(id.value);

    const fetchData = async () => {
      await fetchAPI(getRequest());
      if (success.value)
        // TODO: Stubbed for now, will become dynamic.
        // const { submitSchema } = useDynamicForm();
        await taskSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            send("SPAWN_FORM", {
              cuid: cuid(),
              initialData: value,
              kind: kind.value,
              mode,
            });
          });
    };

    const handleClick = async () => {
      // TODO: Disable if obj already open.
      await fetchData();
    };

    return {
      handleClick,
      isDetail,
    };
  },
});
</script>
