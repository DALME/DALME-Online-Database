<template>
  <mq-layout mq="sm" class="nav-mobile">
    <el-menu mode="horizontal">
      <el-button icon="el-icon-menu" @click="drawer = true"></el-button>
    </el-menu>
  </mq-layout>

  <mq-layout mq="sm">
    <el-drawer
      v-model="drawer"
      :direction="direction"
      :show-close="false"
      :with-header="false"
      :size="'50%'"
    >
      <el-menu router class="mobile" :default-active="$route.path">
        <router-link exact to="/">
          <h1>DALME</h1>
        </router-link>
        <template v-for="(route, idx) in $router.options.routes" :key="idx">
          <el-menu-item :index="route.path" :route="route">
            {{ route.name }}
          </el-menu-item>
        </template>
        <el-menu-item class="logout">
          <button @click="logout">Logout</button>
        </el-menu-item>
      </el-menu>
    </el-drawer>
  </mq-layout>

  <mq-layout mq="md+" class="nav">
    <el-aside :width="menuWidth">
      <router-link exact to="/">
        <h1>DALME</h1>
      </router-link>
      <el-menu router class="desktop" :default-active="$route.path">
        <template v-for="(route, idx) in $router.options.routes" :key="idx">
          <el-menu-item :index="route.path" :route="route">
            {{ route.name }}
          </el-menu-item>
        </template>
        <el-menu-item class="logout">
          <button @click="logout">Logout</button>
        </el-menu-item>
      </el-menu>
    </el-aside>
  </mq-layout>
</template>

<script>
import { computed, inject, ref } from "vue";
import { useStore } from "vuex";

export default {
  name: "Nav",
  setup() {
    const store = useStore();
    const $mq = inject("mq");
    const direction = "ltr";
    const drawer = ref(false);
    const menuWidth = computed(() => ($mq.value === "lg" ? "18rem" : "12rem"));
    return { direction, drawer, menuWidth, store };
  },
  methods: {
    logout() {
      this.$message({ message: "Logging out", type: "success" });
      setTimeout(() => {
        this.store.dispatch("logout");
      }, 500);
    },
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
h1 {
  color: #000;
  font-size: 27px;
  margin: 0;
  padding: 1rem 1rem 1rem 1.15rem;
  text-align: left;
}
ul {
  align-items: flex-start;
  text-align: left;
  width: 100%;
}
ul li {
  width: 100%;
  font-size: 16px;
  text-transform: capitalize;
}
ul li i {
  vertical-align: text-bottom;
  text-align: left;
}
.el-aside {
  height: 100%;
  width: 20rem;
}
.el-menu {
  border-right: 0;
  display: flex;
  flex-direction: column;
}
.el-menu.desktop {
  height: 93%;
}
.el-menu.mobile {
  height: 100%;
}
.el-menu.desktop {
  height: 93%;
}
.logout {
  margin-top: auto;
}
.nav {
  border-right: solid 1px #e6e6e6;
}
.nav-mobile {
  align-items: center;
  display: flex;
  flex-direction: row;
}
.nav-mobile > ul {
  display: flex;
  flex-direction: row;
}
.nav-mobile > ul > button {
  color: #000;
  background-color: #fff;
  border-color: #fff;
  font-size: 21px;
  margin-left: auto;
}
</style>
