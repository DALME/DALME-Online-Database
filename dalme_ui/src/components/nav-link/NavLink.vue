<template>
  <q-item
    dense
    :to="{ name: to }"
    exact
    clickable
    :class="
      active
        ? 'icon-adj bg-blue-1 text-light-blue-10 text-weight-600'
        : 'icon-adj'
    "
    active-class="bg-blue-1 text-light-blue-10 text-weight-600"
    exact-active-class="bg-blue-1 text-light-blue-10 text-weight-600"
    :active="active"
  >
    <q-item-section side class="q-pr-sm">
      <q-icon :name="icon" size="16px" />
    </q-item-section>

    <q-item-section class="q-pr-sm">{{ to }}</q-item-section>
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
<style lang="scss">
.icon-adj {
  padding: 8px 18px;
}
</style>
