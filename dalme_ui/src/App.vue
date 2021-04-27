<template>
  <el-container class="container">
    <Nav />
    <el-main>
      <SuspenseWithError>
        <template #default>
          <router-view />
        </template>
        <template #fallback>
          <Spinner />
        </template>
        <template #error>
          <strong>Failed to load</strong>
        </template>
      </SuspenseWithError>
    </el-main>
  </el-container>
</template>

<script>
import { Nav } from "@/components";
import { Spinner, SuspenseWithError } from "@/components/utils";

export default {
  name: "App",
  components: {
    Nav,
    Spinner,
    SuspenseWithError,
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
h1,
h2,
h3,
h4,
h5 {
  margin: 0;
}
</style>
