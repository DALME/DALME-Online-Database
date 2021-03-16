<template>
  <h1>DALME</h1>

  <h2>{{ user }}</h2>
  <button @click="logout">Logout</button>

  <ul v-if="!loading">
    <li v-for="source in sources" :key="source.id">
      {{ source }}
    </li>
  </ul>
  <div v-else>Loading...</div>
</template>

<script>
import { onBeforeMount, onMounted, ref } from "vue";
import { API, dbUrl } from "../api";

export default {
  setup() {
    const user = ref(null);
    const loading = ref(true);
    const sources = ref(null);
    const logout = API.auth.logout;

    onBeforeMount(async () => {
      const response = await API.auth.session();
      response.ok
        ? (user.value = await response.json())
        : (window.location.href = dbUrl);
    });

    onMounted(async () => {
      const response = await API.sources.archives();
      response.ok
        ? (sources.value = await response.json())
        : console.error(response.json());
      loading.value = false;
    });

    return {
      loading,
      logout,
      sources,
      user,
    };
  },
};
</script>

<style scoped>
a {
  color: #42b983;
}
button {
  margin: 0 0 2rem 0;
}
ul {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
  width: 50rem;
}
li {
  list-style: none;
  margin: 0 0 1rem 0;
}
</style>
