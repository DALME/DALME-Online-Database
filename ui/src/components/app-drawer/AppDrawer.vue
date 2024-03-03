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
              <TooltipWidget>Close app drawer.</TooltipWidget>
            </q-btn>
          </q-item-section>
        </q-item>
        <q-scroll-area dark :style="`min-height: ${minScrollHeight}px;`" class="scroll-area">
          <CollectionsManager userCollectionsOnly inDrawer defaultOpened label="Your collections" />
        </q-scroll-area>

        <template v-for="(route, idx) in appRoutes" :key="idx">
          <q-expansion-item
            :label="route.name"
            default-opened
            header-class="drawer_expansion_header"
            expand-icon="mdi-plus-box-outline"
            expanded-icon="mdi-minus-box-outline"
          >
            <q-item
              v-for="(child, i) in route.children"
              dense
              clickable
              v-close-popup
              :key="i"
              :to="{ name: child.name }"
              :active="ui.currentSection === child.name"
              class="q-my-xs"
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon :name="child.meta.icon" size="xs" />
              </q-item-section>
              <q-item-section>{{ child.name }}</q-item-section>
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
import { CollectionsManager, TooltipWidget } from "@/components";

export default defineComponent({
  name: "AppDrawer",
  components: {
    CollectionsManager,
    TooltipWidget,
  },
  setup() {
    const { appDrawerOpen, ui, windowHeight, showTips } = useStores();
    const minScrollHeight = computed(() => windowHeight.value - 450);
    const appRoutes = navRoutes("app");

    return {
      showTips,
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
  margin-bottom: 0;
  border-bottom: none;
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
