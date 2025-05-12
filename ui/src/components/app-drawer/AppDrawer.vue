<template>
  <div
    :class="appDrawerOpen ? '' : 'hide-modal'"
    class="fullscreen frosted-background custom-drawer app-drawer"
  >
    <div class="q-dialog__backdrop fixed-full" tabindex="-1" />
    <q-drawer v-model="appDrawerOpen" :width="320" side="left" overlay>
      <q-list class="drawer-menu-list full-height col q-pb-none" padding>
        <q-item class="no-shrink" dense>
          <q-item-section avatar>
            <IDALogo fill="#83adcb" size="60px" stroke-color="#fff" stroke-width="0px" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-bold">IDA DB</q-item-label>
            <q-item-label caption>App Menu</q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-btn
              @click="appDrawerOpen = !appDrawerOpen"
              class="drawer-close-button"
              icon="mdi-close"
              size="10px"
              flat
            >
              <ToolTip>Close app drawer.</ToolTip>
            </q-btn>
          </q-item-section>
        </q-item>
        <CollectionsManager
          :default-opened="true"
          :scroll-height="minScrollHeight"
          label="Your collections"
          width="319"
          in-drawer
          user-collections
        />
        <div class="app-drawer-nav">
          <template v-for="(route, idx) in appRoutes" :key="idx">
            <q-expansion-item
              :label="route.name"
              expand-icon="mdi-plus-box-outline"
              expanded-icon="mdi-minus-box-outline"
              group="app-drawer"
              header-class="drawer_expansion_header"
            >
              <q-item
                v-for="(child, i) in route.children"
                :key="i"
                v-close-popup
                :active="
                  child.children
                    ? ui.currentSubsection === child.children[0].name
                    : ui.currentSubsection === child.name
                "
                :to="{ name: child.children ? child.children[0].name : child.name }"
                class="q-my-xs"
                clickable
                dense
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
        </div>
      </q-list>
    </q-drawer>
  </div>
</template>

<script>
import { computed, defineComponent } from "vue";

import { CollectionsManager, IDALogo, ToolTip } from "@/components";
import { navRoutes } from "@/router";
import { useStores } from "@/use";

export default defineComponent({
  name: "AppDrawer",
  components: {
    CollectionsManager,
    IDALogo,
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

<style lang="scss" scoped>
.text-off-blue {
  color: #6a90b2;
}
.app-drawer-nav {
  border-top: 1px solid var(--dark-border-base-colour);
}
.ida-logo-path {
  fill: white !important;
}
.ida-logo-poly {
  fill: white !important;
  stroke: transparent !important;
}
</style>
