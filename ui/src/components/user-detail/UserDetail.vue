<template>
  <div v-if="!loading && user">
    <div class="row q-pa-md">
      <div class="col-12 col-md-9 q-pr-md">
        <q-card class="detail-card" bordered flat>
          <q-item class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5" dense>
            <q-item-section class="q-pr-sm" side>
              <q-icon color="indigo-5" name="person" size="xs" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-subtitle2">
                {{ user.fullName || "Profile" }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator class="bg-indigo-3" />
          <q-card-section>
            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">First Name</div>
              <div class="col-8">{{ user.firstName }}</div>
            </div>
            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Last Name</div>
              <div class="col-8">{{ user.lastName }}</div>
            </div>
            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">User ID</div>
              <div class="col-8">{{ user.id }}</div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Staff</div>
              <div class="col-8">
                <BooleanValue :value="user.isStaff" size="20px" />
              </div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Superuser</div>
              <div class="col-8">
                <BooleanValue :value="user.isSuperuser" size="20px" />
              </div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Active</div>
              <div class="col-8">
                <BooleanValue :value="user.isActive" size="20px" />
              </div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Joined</div>
              <div class="col-6">{{ user.dateJoined }}</div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Last login</div>
              <div class="col-8">{{ user.lastLogin }}</div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Groups</div>
              <div v-html="formatGroups(user.groups)" class="col-8"></div>
            </div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card class="detail-card full-height bg-grey-2" bordered flat>
          <q-card-section class="justify-center content-center q-pa-none full-height">
            <q-img
              v-if="user.avatar"
              :src="user.avatar"
              class="q-mx-auto q-my-auto full-height avatar-image"
              fit="cover"
            />
            <q-icon
              v-else
              class="column q-mx-auto q-my-auto full-height"
              color="grey-4"
              name="no_accounts"
              size="15rem"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>
    <div v-if="showPrefs" class="row q-pl-md q-pr-md q-pb-md">
      <UserPreferences />
    </div>
  </div>
  <OpaqueSpinner :showing="loading" />
</template>

<script>
import { useMeta } from "quasar";
import { map } from "ramda";
import { computed, defineComponent, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { BooleanValue, OpaqueSpinner } from "@/components";
import { userSchema } from "@/schemas";
import { useAuthStore } from "@/stores/auth";
import { useAPI } from "@/use";

import UserPreferences from "./UserPreferences.vue";

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
    BooleanValue,
    OpaqueSpinner,
    UserPreferences,
  },
  setup() {
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const $authStore = useAuthStore();

    const user = ref(null);
    const username = $route.params.username;
    const tab = ref("general");
    const showPrefs = computed(() => username === $authStore.user.username);

    useMeta({ title: `User | ${username}` });

    const formatGroups = (groups) => map((group) => group.name, groups).join("<br>");

    const fetchData = async () => {
      await fetchAPI(requests.users.getUser(username));
      if (success.value)
        await userSchema.validate(data.value, { stripUnknown: true }).then((value) => {
          user.value = value;
          loading.value = false;
        });
    };

    onMounted(async () => await fetchData());

    return { formatGroups, loading, getAttributeLabel, tab, showPrefs, user };
  },
});
</script>

<style scoped lang="scss">
.avatar-image {
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}
</style>
