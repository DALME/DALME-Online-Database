<template>
  <div v-if="!loading && user">
    <div class="row q-pa-md">
      <div class="col-12 col-md-9 q-pr-md">
        <q-card flat bordered class="detail-card">
          <q-item dense class="q-pb-none q-px-sm bg-indigo-1 text-indigo-5">
            <q-item-section side class="q-pr-sm">
              <q-icon name="person" color="indigo-5" size="xs" />
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
                <BooleanWidget :value="user.isStaff" size="20px" />
              </div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Superuser</div>
              <div class="col-8">
                <BooleanWidget :value="user.isSuperuser" size="20px" />
              </div>
            </div>

            <div class="row q-mt-xs">
              <div class="col-3 text-weight-medium text-right q-mr-lg">Active</div>
              <div class="col-8">
                <BooleanWidget :value="user.isActive" size="20px" />
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
              <div class="col-8" v-html="formatGroups(user.groups)"></div>
            </div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card flat bordered class="detail-card full-height bg-grey-2">
          <q-card-section class="justify-center content-center q-pa-none full-height">
            <q-img
              v-if="user.avatar"
              :src="user.avatar"
              fit="cover"
              class="q-mx-auto q-my-auto full-height avatar-image"
            />
            <q-icon
              v-else
              name="no_accounts"
              color="grey-4"
              size="15rem"
              class="column q-mx-auto q-my-auto full-height"
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
import { useAuthStore } from "@/stores/auth";
import { requests } from "@/api";
import { BooleanWidget, OpaqueSpinner } from "@/components";
import { userSchema } from "@/schemas";
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
    BooleanWidget,
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
    const showPrefs = computed(() => username === $authStore.username);

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
