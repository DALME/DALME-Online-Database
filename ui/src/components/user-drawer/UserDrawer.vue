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
              <TooltipWidget>Close user drawer.</TooltipWidget>
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
import { computed, defineComponent, inject, ref } from "vue";
import { isEmpty, isNil } from "ramda";
import { useStores } from "@/use";
import { CustomDialog, TooltipWidget, TaskManager } from "@/components";
import { nully } from "@/utils";

export default defineComponent({
  name: "UserDrawer",
  components: {
    TooltipWidget,
    TaskManager,
  },
  setup() {
    const $q = useQuasar();
    const { auth, userDrawerOpen, windowHeight, showTips } = useStores();
    const submitting = ref(false);
    const prefSubscription = inject("prefSubscription");
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
        prefSubscription();
        auth.logout();
      });
    };

    return {
      auth,
      isEmpty,
      isNil,
      showTips,
      userDrawerOpen,
      submitting,
      logout,
      nully,
      scrollHeight,
    };
  },
});
</script>

<style lang="scss">
.q-drawer > .q-drawer__content {
  overflow: hidden;
}
.hide-modal,
.hide-modal .q-dialog__backdrop {
  left: auto;
}
.custom-drawer .q-drawer {
  box-shadow:
    rgb(48, 54, 61) 0px 0px 0px 1px,
    rgba(1, 4, 9, 0.85) 0px 16px 32px 0px;
  background: var(--dark-bg-base-colour);
  border-left: 1px solid var(--dark-border-base-colour);
  overflow: hidden;
}
.custom-drawer.user-drawer .q-drawer {
  border-top-left-radius: 18px;
  border-bottom-left-radius: 18px;
}
.drawer-close-button {
  width: 28px;
  height: 28px;
  color: #5b5e66;
  border-radius: 8px;
  padding: 0;
  border: 1px solid var(--dark-border-base-colour);
}
.drawer-close-button:hover {
  color: var(--dark-menu-text-colour);
}
.drawer-close-button:hover .q-focus-helper {
  opacity: 0 !important;
}
.custom-drawer .q-separator {
  background: var(--dark-border-base-colour);
}
.custom-drawer .q-item__section--main + .q-item__section--main {
  margin-left: 4px;
}
.custom-drawer .scroll-area {
  border-top: 1px solid var(--dark-border-base-colour);
  border-bottom: 1px solid var(--dark-border-base-colour);
  margin: 8px 0;
  background: #0b161b;
}
.custom-drawer .q-expansion-item {
  width: 319px;
}
.custom-drawer .q-expansion-item .q-item.drawer_expansion_header {
  font-size: 12px;
  font-weight: 700;
  color: #677c8b;
  padding: 2px 16px;
  margin: 0;
  border-radius: 0;
  border-bottom: 1px solid var(--dark-border-base-colour);
  background-color: #16242e;
}
.custom-drawer .q-expansion-item .q-item.drawer_expansion_header:hover {
  color: #75838d;
}
.custom-drawer .q-expansion-item .q-item.drawer_expansion_header:hover .q-icon {
  color: #75838d;
}
.custom-drawer .q-expansion-item .q-item.drawer_expansion_header:hover > .q-focus-helper {
  opacity: 0.2;
  border: none;
}
.custom-drawer .q-expansion-item:not(:first-of-type) {
  border-top: 1px solid var(--dark-border-base-colour);
}
.custom-drawer .q-expansion-item .q-item.drawer_expansion_header:hover > .q-focus-helper {
  background: #215aa0;
  opacity: 0.3;
}
.custom-drawer .q-expansion-item .q-item.drawer_expansion_header .q-expansion-item__toggle-icon {
  font-size: 16px;
  color: #42505b;
}
.task-list-actions {
  display: flex;
  font-weight: 600;
  color: grey;
  border-top: 1px solid var(--dark-border-base-colour);
}
.task-list-actions .q-btn {
  font-size: 12px;
  padding: 4px 16px;
  width: 50%;
}
.task-list-actions .q-btn:last-of-type {
  margin-left: auto;
  margin-right: auto;
  // border-left: 1px solid var(--dark-border-base-colour);
}
.task-list-actions .q-btn:last-of-type .q-icon {
  font-size: 14px;
  color: var(--dark-menu-icon-colour);
}
.micro-icon-comment-count {
  color: #aec4e2;
}
.micro-icon-comment-count::before {
  color: #5a7ea0;
  opacity: 0.5;
}
</style>
