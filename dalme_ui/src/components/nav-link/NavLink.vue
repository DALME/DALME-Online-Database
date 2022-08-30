<template>
  <q-item
    :to="{ name: to }"
    exact
    clickable
    :class="active ? 'bg-blue-3 text-light-blue-10 text-weight-bold' : null"
    active-class="bg-blue-3 text-light-blue-10 text-weight-bold"
    :active="active"
  >
    <q-item-section avatar>
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ to }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent, inject, ref, watch } from "vue";
import { RouterLink, useLink } from "vue-router";

export default defineComponent({
  name: "NavLink",
  props: {
    ...RouterLink.props,
    icon: {
      type: String,
      required: true,
    },
    to: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { isActive } = useLink(props);
    const currentSubsection = inject("currentSubsection");
    const active = ref(currentSubsection.value === props.to || isActive.value);

    watch(currentSubsection, () => {
      active.value = currentSubsection.value === props.to;
    });

    return {
      active,
    };
  },
});
</script>
