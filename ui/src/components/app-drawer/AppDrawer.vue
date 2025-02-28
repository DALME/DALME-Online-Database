<template>
  <div
    class="fullscreen frosted-background custom-drawer app-drawer"
    :class="appDrawerOpen ? '' : 'hide-modal'"
  >
    <div class="q-dialog__backdrop fixed-full" tabindex="-1" />
    <q-drawer overlay v-model="appDrawerOpen" side="left" :width="320">
      <q-list padding class="drawer-menu-list full-height col q-pb-none">
        <q-item dense class="no-shrink">
          <q-item-section avatar>
            <q-avatar square color="white" size="34px">
              <img src="~assets/dalme_logo.svg" alt="IDA" />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-bold">IDA DB</q-item-label>
            <q-item-label caption>App Menu</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-btn
              flat
              class="drawer-close-button"
              icon="mdi-close"
              size="10px"
              @click="appDrawerOpen = !appDrawerOpen"
            >
              <ToolTip>Close app drawer.</ToolTip>
            </q-btn>
          </q-item-section>
        </q-item>
        <EditPanel />
        <CollectionsManager
          userCollectionsOnly
          inDrawer
          :scrollHeight="minScrollHeight"
          width="319"
          :defaultOpened="true"
          label="Your collections"
        />
        <template v-for="(route, idx) in appRoutes" :key="idx">
          <q-expansion-item
            :label="route.name"
            header-class="drawer_expansion_header"
            expand-icon="mdi-plus-box-outline"
            expanded-icon="mdi-minus-box-outline"
            group="app-drawer"
          >
            <q-item
              v-for="(child, i) in route.children"
              dense
              clickable
              v-close-popup
              :key="i"
              :to="{ name: child.children ? child.children[0].name : child.name }"
              :active="
                child.children
                  ? ui.currentSubsection === child.children[0].name
                  : ui.currentSubsection === child.name
              "
              class="q-my-xs"
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon :name="child.meta.icon" size="xs" />
              </q-item-section>
              <q-item-section>
                {{ child.children ? child.children[0].name : child.name }}
              </q-item-section>
            </q-item>
          </q-expansion-item>
        </template>
      </q-list>
    </q-drawer>
  </div>
</template>

<script>
import { computed, defineComponent } from "vue";
import { useStores } from "@/use";
import { navRoutes } from "@/router";
import { CollectionsManager, EditPanel, ToolTip } from "@/components";

export default defineComponent({
  name: "AppDrawer",
  components: {
    CollectionsManager,
    EditPanel,
    ToolTip,
  },
  setup() {
    const { appDrawerOpen, ui, windowHeight } = useStores();
    const minScrollHeight = computed(() => windowHeight.value - 450);
    const appRoutes = navRoutes("app");

    return {
      appDrawerOpen,
      minScrollHeight,
      ui,
      appRoutes,
    };
  },
});
</script>

<style lang="scss">
.custom-drawer.app-drawer .q-drawer {
  border-top-right-radius: 18px;
  border-bottom-right-radius: 18px;
}
.custom-drawer.app-drawer .scroll-area {
  margin: 0;
  border: none;
}
.custom-drawer.app-drawer .q-list .q-expansion-item:nth-child(2) {
  margin-top: 8px;
}
.custom-drawer.app-drawer .q-expansion-item:last-of-type .q-item:last-of-type {
  margin-bottom: 12px;
}
.text-off-blue {
  color: #6a90b2;
}
.custom-drawer.app-drawer .collection-name {
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}
.q-item.collection-tile .q-item__label {
  display: flex;
}
</style>
