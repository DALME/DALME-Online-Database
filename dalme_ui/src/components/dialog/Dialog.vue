<template>
  <q-dialog
    ref="dialogRef"
    :persistent="isPersistent"
    :position="position"
    :seamless="seamless"
    transition-show="scale"
    transition-hide="scale"
    @hide="onDialogHide"
  >
    <q-card class="q-dialog-plugin">
      <q-card-section v-if="title" class="row items-center q-pb-none q-mb-md">
        <div class="text-h6">{{ title }}</div>
        <q-space v-if="closeIcon" />
        <q-btn v-if="closeIcon" icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section :class="message ? 'row items-center' : null">
        <q-avatar
          v-if="message && icon"
          :icon="icon"
          :color="iconColour"
          text-color="black"
        />
        <span v-if="message" class="q-ml-sm">{{ message }}</span>
        <div v-if="prompt" class="text-h6">{{ prompt }}</div>
      </q-card-section>

      <q-card-section v-if="prompt" class="q-pt-none">
        <q-input dense v-model="promptValue" autofocus />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          unelevated
          no-caps
          :color="CancelButtonColour"
          :label="CancelButtonLabel"
          @click="onCancelClick"
        />
        <q-btn
          unelevated
          no-caps
          :color="OkayButtonColour"
          :label="OkayButtonLabel"
          @click="onOkayClick"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from "quasar";
import { ref } from "vue";

export default {
  props: {
    isPersistent: {
      type: Boolean,
      default: false,
    },
    seamless: {
      type: Boolean,
      default: false,
    },
    position: {
      type: String,
      default: "standard",
    },
    title: {
      type: String,
      default: "",
    },
    closeIcon: {
      type: Boolean,
      default: false,
    },
    message: {
      type: String,
      default: "If you see this, something's gone terribly wrong",
    },
    icon: {
      type: String,
      default: "",
    },
    iconColour: {
      type: String,
      default: "white",
    },
    CancelButtonLabel: {
      type: String,
      default: "Cancel",
    },
    OkayButtonLabel: {
      type: String,
      default: "Okay",
    },
    CancelButtonColour: {
      type: String,
      default: "primary",
    },
    OkayButtonColour: {
      type: String,
      default: "primary",
    },
    prompt: {
      type: String,
      default: "",
    },
  },
  emits: [...useDialogPluginComponent.emits],
  setup(props) { // eslint-disable-line
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const promptValue = ref("");

    return {
      dialogRef,
      onDialogHide,
      promptValue,
      onCancelClick: onDialogCancel,
      onOkayClick: onDialogOK,
    };
  },
};
</script>
