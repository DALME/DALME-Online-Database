<template>
  <q-chip
    clickable="clickable"
    dense
    :square="inline"
    :class="`${inline ? 'inline' : ''} ${dark ? 'dark' : ''}`"
    :color="color"
    @click="router.push({ name: 'User', params: { username: user.username } })"
  >
    <template v-if="showAvatar">
      <q-avatar v-if="!nully(user.avatar)" :size="avatarSize">
        <img :src="user.avatar" fit="cover" ratio="1" />
      </q-avatar>
      <q-icon
        class="avatar-icon no-padding text-grey-6"
        v-else
        name="mdi-account-circle"
        :size="avatarIconSize"
      />
    </template>
    <div :class="`${inline ? '' : 'q-pr-xs'}`" :style="style">{{ user.fullName }}</div>
  </q-chip>
</template>

<script>
import { computed, defineComponent } from "vue";
import { nully } from "@/utils";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "UserPill",
  props: {
    user: {
      type: Object,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    bold: {
      type: Boolean,
      default: true,
    },
    color: {
      type: String,
      default: "transparent",
    },
    clickable: {
      type: Boolean,
      default: true,
    },
    showAvatar: {
      type: Boolean,
      default: true,
    },
    avatarSize: {
      type: String,
      default: "18px",
    },
    textSize: {
      type: String,
      default: "14px",
    },
    inline: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const router = useRouter();
    const style = props.bold
      ? `font-size: ${props.textSize}; font-weight: 600;`
      : `font-size: ${props.textSize};`;

    const avatarIconSize = computed(() => {
      let val = parseInt(props.avatarSize.replace("px", ""));
      return `${val - 4}px`;
    });

    return {
      nully,
      router,
      style,
      avatarIconSize,
    };
  },
});
</script>

<style lang="scss" scoped>
.transparent {
  background: none;
}
.q-avatar {
  margin-right: 6px;
}
.q-chip.inline {
  margin: 0;
  padding: 0;
}
.q-chip .q-avatar {
  margin-left: 0 !important;
}
</style>
