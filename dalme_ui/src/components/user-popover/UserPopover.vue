<template>
  <router-link
    class="user-popover-link"
    :to="{
      name: 'User',
      params: { username: username },
    }"
    :href="'/users/' + username + '/'"
    v-on:mouseover="showPopover = true"
    v-on:mouseleave="showPopover = false"
  >
    <span v-text="username" />
    <q-menu v-model="showPopover" no-parent-event>
      <q-list>
        <q-item>
          <q-item-section top avatar>
            <q-avatar v-if="avatar" size="40px">
              <img :src="avatar" />
            </q-avatar>
            <q-avatar
              v-else
              size="40px"
              icon="account_circle"
              color="light-blue-3"
              text-color="blue-9"
            />
          </q-item-section>
          <q-item-section>
            <span
              class="text-subtitle2 text-weight-bold"
              v-text="fullName"
              style="line-height: 20px"
            />
            <span class="text-caption" v-text="`${username} (${id})`" />
          </q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </router-link>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "UserPopover",
  props: {
    id: {
      type: Number,
      required: true,
    },
    username: {
      type: String,
      required: true,
    },
    fullName: {
      type: String,
      required: true,
    },
    avatar: {
      type: String,
      required: true,
    },
  },
  setup() {
    const showPopover = ref(false);

    return {
      showPopover,
    };
  },
});
</script>

<style lang="scss" scoped>
.user-popover-link {
  font-weight: 500;
}
.user-popover-link:hover {
  color: #01579b;
  text-decoration: underline;
}
</style>
