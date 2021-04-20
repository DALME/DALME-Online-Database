<template>
  <el-container class="container">
    <Nav />
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script>
import { Nav } from "@/components";

export default {
  name: "App",
  components: {
    Nav,
  },
  setup() {
    return {};
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
  text-align: center;
}
body {
  height: 100vh;
  margin: 0;
}
a {
  text-decoration: none;
}
section.container {
  flex-direction: column;
  height: 100%;
}
@media screen and (min-width: 600px) {
  section.container {
    flex-direction: row;
  }
}
</style>
