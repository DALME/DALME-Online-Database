<template>
  <router-link
    @mouseleave="showPopover = false"
    @mouseover="showPopover = true"
    :class="`${linkClasses}`"
    :to="target"
  >
    <span v-text="text" />
    <q-menu
      v-model="showPopover"
      :class="dark ? 'dark' : ''"
      anchor="top left"
      class="popover-container"
      max-width="50%"
      self="bottom left"
      no-parent-event
    >
      <q-card :class="dark ? 'dark' : ''" class="box-small-arrow q-pa-sm" bordered>
        <slot>
          <q-item v-if="userData">
            <q-item-section v-if="showAvatar" avatar>
              <q-avatar size="32px">
                <q-img
                  v-if="!nully(userData.avatar)"
                  :src="userData.avatar"
                  fit="cover"
                  ratio="1"
                />
                <q-icon v-else name="mdi-account-circle" size="30px" />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-item-label>
                {{ userData.fullName }}
              </q-item-label>
              <q-item-label caption>
                {{ userData.email }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </slot>
      </q-card>
    </q-menu>
  </router-link>
</template>

<script>
import { defineComponent, ref } from "vue";

import { nully } from "@/utils";

export default defineComponent({
  name: "DetailPopover",
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    linkClass: {
      type: String,
      required: false,
      default: "popover-link",
    },
    linkTarget: {
      type: Object,
      required: false,
      default: null,
    },
    linkText: {
      type: String,
      required: false,
      default: null,
    },
    showAvatar: {
      type: Boolean,
      required: false,
      default: false,
    },
    userData: {
      type: Object,
      required: false,
      default: null,
    },
  },
  setup(props) {
    const showPopover = ref(false);
    const linkClasses = ref(props.userData ? "user-link" : props.linkClass);
    const target = ref(
      props.userData
        ? { name: "User", params: { username: props.userData.username } }
        : props.linkTarget,
    );
    const text = ref(props.userData ? props.userData.username : props.linkText);

    return {
      linkClasses,
      showPopover,
      target,
      text,
      nully,
    };
  },
});
</script>

<style lang="scss" scoped>
.popover-container {
  --bg-colour: var(--light-bg-base-colour);
  --border-colour: var(--ligth-border-base-colour);
  --main-colour: var(--light-default-text-colour);
  --secondary-colour: var(--light-secondary-text-colour);
}
.popover-container.dark {
  --bg-colour: var(--dark-bg-base-colour);
  --border-colour: var(--dark-border-base-colour);
  --main-colour: var(--dark-default-text-colour);
  --secondary-colour: var(--dark-secondary-text-colour);
}
.popover-container {
  padding: 8px;
  box-shadow: none !important;
  background: none !important;
}
.popover-container .q-card {
  background: var(--bg-colour);
  border-color: var(--border-colour);
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.2);
}
.popover-container .q-item {
  color: var(--main-colour);
}
.popover-container .q-item .q-item__label--caption {
  color: var(--secondary-colour);
}
.popover-link,
.user-link {
  font-weight: 700;
  color: inherit;
  white-space: normal;
}
</style>
