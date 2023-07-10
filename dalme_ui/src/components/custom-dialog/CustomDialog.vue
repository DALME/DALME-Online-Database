<template>
  <q-dialog
    ref="dialogRef"
    :persistent="isPersistent"
    :position="position"
    :seamless="seamless"
    transition-show="scale"
    transition-hide="scale"
    :class="`frosted-background ${classes} ${colourScheme}`"
    @hide="onDialogHide"
  >
    <q-card class="q-dialog-plugin">
      <q-card-section v-if="title || icon" class="hero-bg">
        <q-icon v-if="icon" :name="icon" class="hero-icon" />
        <div v-if="title" class="hero-text">{{ title }}</div>
        <q-btn v-if="closeIcon" icon="close" flat round dense v-close-popup class="hero-button" />
      </q-card-section>

      <q-card-section :class="message ? 'row items-center dialogue-body' : null">
        <div v-if="message" :class="prompt ? '' : 'text-center full-width'">
          <span v-html="message" />
        </div>
        <div v-if="prompt" class="text-h6">{{ prompt }}</div>
      </q-card-section>

      <q-card-section v-if="prompt" class="q-pt-none">
        <q-input dense v-model="promptValue" autofocus />
      </q-card-section>
      <q-separator />
      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          :outline="colourScheme !== 'warning'"
          :unelevated="colourScheme === 'warning'"
          no-caps
          class="dialogue-button cancel"
          :label="cancelButtonLabel"
          @click="onCancelClick"
        />
        <q-btn
          unelevated
          no-caps
          class="dialogue-button okay"
          :label="okayButtonLabel"
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
    cancelButtonLabel: {
      type: String,
      default: "Cancel",
    },
    okayButtonLabel: {
      type: String,
      default: "Okay",
    },
    prompt: {
      type: String,
      default: "",
    },
    classes: {
      type: String,
      default: "",
    },
    colourScheme: {
      type: String,
      default: "standard",
    },
  },
  emits: [...useDialogPluginComponent.emits],
  setup() {
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent();

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

<style lang="scss">
.hero-bg {
  height: 150px;
  overflow: hidden;
  display: flex;
}
.standard .hero-bg {
  background-color: #343e72;
  background-image: linear-gradient(59deg, #343e72 54.62%, #1b1b1b);
}
.edit-mode .hero-bg {
  background-color: #6f5423;
  background-image: linear-gradient(59deg, #6f5423 54.62%, #1b1b1b);
}
.warning .hero-bg {
  background-color: #6b2828;
  background-image: linear-gradient(59deg, #6b2828 54.62%, #1b1b1b);
}
.hero-icon {
  color: white;
  font-size: 200pt;
  transform: rotate(20deg);
  opacity: 0.1;
  position: relative;
  top: -60%;
  left: 13%;
  text-shadow: -20px -20px 7px black;
}
.hero-text {
  width: 300px;
  position: relative;
  align-self: center;
  font-size: 40px;
  font-weight: 200;
  color: white;
  text-transform: capitalize;
  text-shadow: -15px 2px 14px black;
  margin-left: -235px;
  text-align: center;
}
.hero-button {
  position: absolute;
  top: 10px;
  right: 10px;
  color: #ffffff6e;
}
.dialogue-body {
  padding: 20px 40px !important;
  font-size: 16px;
  font-weight: 300;
}
.dialogue-button {
  font-size: 14px;
  font-weight: 400;
  padding: 0 20px !important;
}
.standard .dialogue-button.cancel {
  color: #7986cb;
}
.standard .dialogue-button.okay {
  background: #3f51b5;
  color: white;
}
.edit-mode .dialogue-button.cancel {
  color: #a85e00;
}
.edit-mode .dialogue-button.okay {
  background: #c87001;
  color: white;
}
.warning .dialogue-button.cancel {
  background: #577b5c;
  color: white;
}
.warning .dialogue-button.okay {
  background: #b14747;
  color: white;
}
</style>
