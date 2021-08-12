<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      {{ user }}
    </q-card>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { userSchema } from "@/schemas";
import { useAPI } from "@/use";

const getAttributeLabel = (attribute) => {
  return {
    id: "User ID",
    firstName: "First Name",
    lastName: "Last Name",
    email: "Email",
    isStaff: "Staff",
    isSuperuser: "Superuser",
    isActive: "Active",
    dateJoined: "Date Joined",
    lastLogin: "Last Login",
    groups: "Groups",
  }[attribute];
};

export default defineComponent({
  name: "UserDetail",
  async setup() {
    const $route = useRoute();
    const { success, data, fetchAPI } = useAPI();

    const user = ref(null);
    const username = $route.params.username;

    const fetchData = async () => {
      await fetchAPI(requests.users.getUser(username));
      if (success.value)
        await userSchema
          .validate(data.value[0], { stripUnknown: true })
          .then((value) => {
            user.value = value;
          });
    };

    await fetchData();

    return { getAttributeLabel, user };
  },
});
</script>
