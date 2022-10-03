<template>
  <router-link
    :class="`${linkClasses}`"
    :to="target"
    @mouseover="showPopover = true"
    @mouseleave="showPopover = false"
  >
    <span v-text="text" />
    <q-menu
      v-model="showPopover"
      no-parent-event
      anchor="top left"
      self="bottom left"
      class="q-pb-sm no-shadow"
      max-width="50%"
    >
      <q-card flat bordered class="box-down-arrow q-pa-md">
        <slot>
          <q-item v-if="userData" class="q-pa-none column flex-center">
            <q-item-label v-if="showAvatar">
              <q-avatar v-if="userData.avatar" size="50px">
                <img :src="userData.avatar" />
              </q-avatar>
              <q-avatar
                v-else
                size="50px"
                icon="account_circle"
                color="light-blue-3"
                text-color="blue-9"
              />
            </q-item-label>
            <q-item-label class="text-h8 text-condensed text-grey-9">
              {{ userData.fullName }}
            </q-item-label>
            <q-item-label class="text-detail text-weight-medium text-grey-8">
              {{ userData.username }}
            </q-item-label>
          </q-item>
        </slot>
      </q-card>
    </q-menu>
  </router-link>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "DetailPopover",
  props: {
    linkClass: {
      type: String,
      required: false,
      default: "popover-link",
    },
    linkTarget: {
      type: Object,
      required: false,
    },
    linkText: {
      type: String,
      required: false,
    },
    showAvatar: {
      type: Boolean,
      required: false,
      default: false,
    },
    spaceBefore: {
      type: Boolean,
      required: false,
      default: false,
    },
    spaceAfter: {
      type: Boolean,
      required: false,
      default: false,
    },
    userData: {
      type: Object,
      required: false,
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
    };
  },
});
</script>

<style lang="scss" scoped>
.popover-link {
  font-weight: 500;
  color: inherit;
  white-space: normal;
}
.popover-link:hover {
  color: #5c6bc0;
}
.user-link {
  font-weight: 500;
  color: inherit;
  white-space: normal;
}
.user-link:hover {
  color: #5c6bc0;
}
</style>
