<template>
  <BaseModal :cuid="cuid" :x-pos="xPos" :y-pos="yPos">
    <template #title> {{ mode }} {{ kind }} </template>

    <template #content>
      <SchemaForm :cuid="cuid" :form-model="formModel" :schema="formSchema" />
    </template>
  </BaseModal>
</template>

<script>
import { useStorage } from "@vueuse/core";
import { useActor, useSelector } from "@xstate/vue";
import { defineComponent, ref } from "vue";

import { BaseModal, SchemaForm } from "@/components";
import { useAPI, useDynamicForm, useEditing } from "@/use";

export default defineComponent({
  name: "FormModal",
  components: {
    BaseModal,
    SchemaForm,
  },
  props: {
    cuid: {
      type: String,
      required: true,
    },
    xPos: {
      type: Number,
      required: true,
    },
    yPos: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const formRequest = ref(null);
    const formSchema = ref(null);
    const submitSchema = ref(null);

    const { apiInterface } = useAPI();
    const { formWatcher } = useDynamicForm(formRequest, formSchema, submitSchema);
    const {
      forms,
      formSubmitWatcher,
      machine: { send },
    } = useEditing();

    const { status, success, fetchAPI } = apiInterface();

    const { actor } = forms.value[props.cuid];
    const { send: actorSend, state: actorState } = useActor(actor);

    const kind = useSelector(actor, (state) => state.context.kind);
    const mode = useSelector(actor, (state) => state.context.mode);
    const initialData = useSelector(actor, (state) => state.context.initialData);

    const fieldsKey = `form-fields:${props.cuid}`;
    const formModel = useStorage(fieldsKey, initialData.value || {}, localStorage);

    const handleSubmit = async (postSubmitRefresh) => {
      await submitSchema.value
        .validate(formModel.value, { stripUnknown: true })
        .then(async (value) => {
          const request = formRequest.value(value);
          await fetchAPI(request);
          if (success.value & [200, 201].includes(status.value)) {
            actorSend({ type: "RESOLVE" });
            postSubmitRefresh.value = true;
            send({ type: "DESTROY_MODAL", cuid: props.cuid });
          } else {
            actorSend({ type: "REJECT" });
          }
        });
    };

    formWatcher(kind, mode);
    formSubmitWatcher(actorState, handleSubmit);

    return {
      formModel,
      formSchema,
      mode,
      kind,
    };
  },
});
</script>
