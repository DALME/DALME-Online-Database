<template>
  <q-btn
    v-if="linkable && !saving && !editOn"
    @click="$emit('navigate')"
    :ripple="false"
    color="grey-5"
    icon="mdi-eye-outline"
    size="sm"
    dense
    flat
  />
  <q-btn
    v-if="removable && editOn && !saving"
    :ripple="false"
    color="red-5"
    icon="mdi-trash-can-outline"
    size="sm"
    dense
    flat
  >
    <q-menu
      ref="attributes-menu"
      :offset="[0, -10]"
      anchor="top middle"
      class="inline-delete-dialogue"
      self="bottom middle"
      transition-hide="scale"
      transition-show="scale"
      persistent
    >
      <div class="wrapper-box">
        <div>Delete attribute?</div>
        <q-btn v-close-popup class="q-ml-sm" color="indigo-7" label="Cancel" no-caps outline />
        <q-btn
          v-close-popup
          @click="$emit('remove')"
          class="q-ml-xs"
          color="red-10"
          label="Delete"
          no-caps
          outline
        />
      </div>
    </q-menu>
  </q-btn>
  <q-btn
    v-if="cancellable && editOn && hasChanged"
    @click="$emit('cancel')"
    :icon="cancelIcon"
    :ripple="false"
    color="orange-6"
    size="sm"
    dense
    flat
  />
  <q-btn
    v-if="!saving"
    @click="$emit('action')"
    :color="actionColour"
    :icon="actionIcon"
    :ripple="false"
    size="sm"
    dense
    flat
  />
  <AdaptiveSpinner v-if="saving" class="q-mr-xs" color="green-6" size="14px" type="pie" />
</template>

<script>
import { computed, defineComponent } from "vue";

import { AdaptiveSpinner } from "@/components";

export default defineComponent({
  name: "EditButtons",
  components: { AdaptiveSpinner },
  props: {
    linkable: {
      type: Boolean,
      default: false,
    },
    cancellable: {
      type: Boolean,
      default: false,
    },
    removable: {
      type: Boolean,
      default: false,
    },
    hasChanged: Boolean,
    editOn: Boolean,
    saving: Boolean,
    creating: Boolean,
  },
  emits: ["action", "cancel", "navigate", "remove"],
  setup(props) {
    const actionIcon = computed(() =>
      props.editOn
        ? props.hasChanged
          ? "mdi-content-save-outline"
          : "mdi-close-circle-outline"
        : "mdi-cog-outline",
    );

    const actionColour = computed(() =>
      props.editOn ? (props.hasChanged ? "green-6" : "orange-6") : "grey-5",
    );

    const cancelIcon = computed(() =>
      props.creating ? "mdi-close-circle-outline" : "mdi-undo-variant",
    );

    return {
      actionIcon,
      actionColour,
      cancelIcon,
    };
  },
});
</script>
