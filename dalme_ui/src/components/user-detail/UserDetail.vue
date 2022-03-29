<template>
  <div class="q-ma-md full-width full-height">
    <q-tab-panel v-if="!loading && user" name="data">
      <q-card class="q-ma-md">
        <q-item>
          <q-item-section avatar>
            <q-avatar>
              <q-icon name="person" />
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label class="text-weight-medium"> Profile </q-item-label>
          </q-item-section>
        </q-item>

        <q-separator />

        <q-card-section>
          <div class="row">
            <div class="col-xs-12 col-sm-6">
              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  First Name
                </div>
                <div class="col-6">{{ user.firstName }}</div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Last Name
                </div>
                <div class="col-6">{{ user.lastName }}</div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  User ID
                </div>
                <div class="col-6">{{ user.id }}</div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Staff
                </div>
                <div class="col-6">
                  <q-icon :name="user.isStaff ? 'done' : 'close'" size="xs" />
                </div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Superuser
                </div>
                <div class="col-6">
                  <q-icon
                    :name="user.isSuperuser ? 'done' : 'close'"
                    size="xs"
                  />
                </div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Active
                </div>
                <div class="col-6">
                  <q-icon :name="user.isActive ? 'done' : 'close'" size="xs" />
                </div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Joined
                </div>
                <div class="col-6">{{ user.dateJoined }}</div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Last login
                </div>
                <div class="col-6">{{ user.lastLogin }}</div>
              </div>

              <div class="row q-my-xs">
                <div class="col-3 text-weight-medium text-right q-mr-lg">
                  Groups
                </div>
                <div class="col-6" v-html="formatGroups(user.groups)"></div>
              </div>
            </div>

            <div
              class="col-xs-12 col-sm-6 q-pa-lg row justify-center content-center"
            >
              <q-avatar v-if="user.avatar" rounded size="15rem">
                <img :src="user.avatar" />
              </q-avatar>
              <q-avatar
                v-else
                rounded
                font-size="1rem"
                color="grey-3"
                size="15rem"
              >
                No photo
              </q-avatar>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-tab-panel>
    <OpaqueSpinner :showing="loading" />
  </div>
</template>

<script>
import { useMeta } from "quasar";
import { map } from "ramda";
import { defineComponent, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
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
  components: {
    OpaqueSpinner,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();

    const { loading, success, data, fetchAPI } = apiInterface();
    const user = ref(null);
    const username = $route.params.username;

    useMeta({ title: `User | ${username}` });

    const formatGroups = (groups) =>
      map((group) => group.name, groups).join("<br>");

    const fetchData = async () => {
      await fetchAPI(requests.users.getUser(username));
      if (success.value)
        await userSchema
          .validate(data.value[0], { stripUnknown: true })
          .then((value) => {
            user.value = value;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    return { formatGroups, loading, getAttributeLabel, user };
  },
});
</script>

<style lang="scss" scoped>
img {
  border: 1px solid #eee;
  width: 100% !important;
  height: auto !important;
}
</style>
