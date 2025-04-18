<template>
  <div
    :class="userDrawerOpen ? '' : 'hide-modal'"
    class="fullscreen frosted-background custom-drawer user-drawer"
  >
    <div class="q-dialog__backdrop fixed-full" tabindex="-1" />
    <q-drawer v-model="userDrawerOpen" :width="320" side="right" overlay>
      <q-list class="drawer-menu-list full-height col" padding>
        <q-item class="no-shrink" dense>
          <q-item-section avatar>
            <q-avatar class="greyscale-50" size="40px">
              <q-img
                v-if="!nully(auth.user.avatar)"
                :src="auth.user.avatar"
                fit="cover"
                ratio="1"
              />
              <q-icon v-else name="mdi-account-circle" size="40px" />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-bold">{{ auth.user.fullName }}</q-item-label>
            <q-item-label caption>{{ auth.user.username }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-btn
              @click="userDrawerOpen = !userDrawerOpen"
              class="drawer-close-button"
              icon="mdi-close"
              size="10px"
              flat
            >
              <ToolTip>Close user drawer.</ToolTip>
            </q-btn>
          </q-item-section>
        </q-item>
        <q-separator spaced />
        <q-item
          v-close-popup
          :to="{ name: 'User', params: { username: auth.user.username } }"
          clickable
          dense
        >
          <q-item-section class="col-auto q-mr-xs">
            <q-icon class="menu-icon" name="mdi-account-details-outline" size="xs" />
          </q-item-section>
          <q-item-section>Your profile</q-item-section>
        </q-item>
        <q-item
          v-close-popup
          :to="{ name: 'User', params: { username: auth.user.username } }"
          clickable
          dense
        >
          <q-item-section class="col-auto q-mr-xs">
            <q-icon class="menu-icon" name="mdi-account-cog-outline" size="xs" />
          </q-item-section>
          <q-item-section>Your preferences</q-item-section>
        </q-item>

        <q-scroll-area :style="`height: ${scrollHeight}px;`" class="scroll-area" dark>
          <TaskManager />
        </q-scroll-area>

        <q-item
          v-close-popup
          @click="logout"
          :loading="submitting"
          class="q-mt-auto"
          clickable
          dense
        >
          <q-item-section class="col-auto q-mr-xs">
            <q-icon class="menu-icon" name="mdi-logout" size="xs" />
            <template #loading>
              <q-spinner-oval size="sm" />
            </template>
          </q-item-section>
          <q-item-section>Log out</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>
  </div>
</template>

<script>
import { useQuasar } from "quasar";
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, onBeforeMount, ref } from "vue";

import { CustomDialog, TaskManager, ToolTip } from "@/components";
import { useStores } from "@/use";
import { nully } from "@/utils";

export default defineComponent({
  name: "UserDrawer",
  components: {
    ToolTip,
    TaskManager,
  },
  setup() {
    const $q = useQuasar();
    const { auth, userDrawerOpen, windowHeight, taskStore } = useStores();
    const submitting = ref(false);
    const scrollHeight = computed(() => windowHeight.value - 181);

    const logout = () => {
      $q.dialog({
        component: CustomDialog,
        componentProps: {
          isPersistent: true,
          title: "Log out",
          closeIcon: false,
          message: "Do you want to end your current session?",
          icon: "exit_to_app",
          okayButtonLabel: "Log out",
        },
      }).onOk(() => {
        auth.logout();
      });
    };

    onBeforeMount(() => {
      if (!taskStore.ready || taskStore.isStale) {
        taskStore.initialize();
      }
    });

    return {
      auth,
      isEmpty,
      isNil,
      userDrawerOpen,
      submitting,
      logout,
      nully,
      scrollHeight,
    };
  },
});
</script>
