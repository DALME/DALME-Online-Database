<template>
  <div
    class="fullscreen frosted-background custom-drawer user-drawer"
    :class="userDrawerOpen ? '' : 'hide-modal'"
  >
    <div class="q-dialog__backdrop fixed-full" tabindex="-1" />
    <q-drawer overlay v-model="userDrawerOpen" side="right" :width="320">
      <q-list padding class="drawer-menu-list full-height col">
        <q-item dense class="no-shrink">
          <q-item-section avatar>
            <q-avatar size="40px" class="greyscale-50">
              <q-img
                v-if="!nully(auth.user.avatar)"
                :src="auth.user.avatar"
                fit="cover"
                ratio="1"
              />
              <q-icon v-else size="40px" name="mdi-account-circle" />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-bold">{{ auth.user.fullName }}</q-item-label>
            <q-item-label caption>{{ auth.user.username }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-btn
              flat
              class="drawer-close-button"
              icon="mdi-close"
              size="10px"
              @click="userDrawerOpen = !userDrawerOpen"
            >
              <ToolTip>Close user drawer.</ToolTip>
            </q-btn>
          </q-item-section>
        </q-item>
        <q-separator spaced />
        <q-item
          :to="{ name: 'User', params: { username: auth.user.username } }"
          dense
          clickable
          v-close-popup
        >
          <q-item-section class="col-auto q-mr-xs">
            <q-icon name="mdi-account-details-outline" size="xs" class="menu-icon" />
          </q-item-section>
          <q-item-section>Your profile</q-item-section>
        </q-item>
        <q-item
          :to="{ name: 'User', params: { username: auth.user.username } }"
          dense
          clickable
          v-close-popup
        >
          <q-item-section class="col-auto q-mr-xs">
            <q-icon name="mdi-account-cog-outline" size="xs" class="menu-icon" />
          </q-item-section>
          <q-item-section>Your preferences</q-item-section>
        </q-item>

        <q-scroll-area dark :style="`height: ${scrollHeight}px;`" class="scroll-area">
          <TaskManager />
        </q-scroll-area>

        <q-item
          dense
          clickable
          v-close-popup
          @click="logout"
          :loading="submitting"
          class="q-mt-auto"
        >
          <q-item-section class="col-auto q-mr-xs">
            <q-icon name="mdi-logout" size="xs" class="menu-icon" />
            <template v-slot:loading>
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
import { computed, defineComponent, ref, onBeforeMount } from "vue";
import { isEmpty, isNil } from "ramda";
import { useStores } from "@/use";
import { useTasks } from "@/stores/tasks";
import { CustomDialog, ToolTip, TaskManager } from "@/components";
import { nully } from "@/utils";

export default defineComponent({
  name: "UserDrawer",
  components: {
    ToolTip,
    TaskManager,
  },
  setup() {
    const $q = useQuasar();
    const { auth, userDrawerOpen, windowHeight } = useStores();
    const submitting = ref(false);
    const tm = useTasks();
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
      if (!tm.tasksReady || !tm.listsReady) tm.init();
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
