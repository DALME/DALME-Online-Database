<template>
  <Modal :show="showModal" :reauthenticate="reauthenticate">
    <Login />
  </Modal>
  <el-container class="app-container">
    <SuspenseWithError>
      <template #default>
        <Nav />
        <el-main>
          <router-view />
        </el-main>
      </template>
      <template #fallback>
        <Spinner />
      </template>
      <template #error>
        <h1 class="error">Failed to load</h1>
      </template>
    </SuspenseWithError>
  </el-container>
</template>

<script>
import { ref } from "vue";
import { Login, Modal, Nav } from "@/components";
import { Spinner, SuspenseWithError } from "@/components/utils";
import { provideAPI } from "@/use";

export default {
  name: "App",
  components: {
    Login,
    Modal,
    Nav,
    Spinner,
    SuspenseWithError,
  },
  setup() {
    const showModal = ref(false);
    const reauthenticate = (value) => (showModal.value = value);
    provideAPI(reauthenticate);
    return { reauthenticate, showModal };
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
.app-container {
  flex-direction: column;
  height: 100%;
}
@media screen and (min-width: 600px) {
  .app-container {
    flex-direction: row;
  }
}
.error {
  margin-top: 1rem;
  width: 100%;
}
</style>
