<template>
  <q-tab-panel name="data">
    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="folder" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-weight-medium">
            Set (Collection)
          </q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section>
        <template v-if="!loading">
          <div class="row q-my-xs">
            <div class="col-2 text-weight-medium text-right q-mr-lg">ID</div>
            <div class="col-8">{{ set.id }}</div>
          </div>

          <div class="row q-my-xs">
            <div class="col-2 text-weight-medium text-right q-mr-lg">Name</div>
            <div class="col-8">{{ set.name }}</div>
          </div>

          <div class="row q-my-xs" v-if="set.setType">
            <div class="col-2 text-weight-medium text-right q-mr-lg">Type</div>
            <div class="col-8">{{ set.setType.name }}</div>
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.isPublic)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Public
            </div>
            <div class="col-8">
              <q-icon :name="set.isPublic ? 'done' : 'close'" size="xs" />
            </div>
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.hasLanding)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Has landing
            </div>
            <div class="col-8">
              <q-icon :name="set.hasLanding ? 'done' : 'close'" size="xs" />
            </div>
          </div>

          <div class="row q-my-xs">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Endpoint
            </div>
            <div class="col-8">{{ set.endpoint }}</div>
          </div>

          <div class="row q-my-xs" v-if="set.owner">
            <div class="col-2 text-weight-medium text-right q-mr-lg">Owner</div>
            <div class="col-8">
              <router-link
                :to="{
                  name: 'User',
                  params: { username: set.owner.username },
                }"
              >
                {{ set.owner.fullName }}
              </router-link>
            </div>
          </div>

          <div class="row q-my-xs" v-if="set.permissions">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Permissions
            </div>
            <div class="col-8">{{ set.permissions.name }}</div>
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.description)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Description
            </div>
            <div class="col-8">{{ set.description }}</div>
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.statTitle)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Stat Title
            </div>
            <div class="col-8">{{ set.statTitle }}</div>
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.statText)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Stat Text
            </div>
            <div class="col-8">{{ set.statText }}</div>
          </div>
        </template>
      </q-card-section>
    </q-card>

    <q-card class="q-ma-md q-pa-md" v-if="isWorkset">
      <div class="row q-my-xs" v-if="!isNil(set.worksetProgress)">
        <div class="col-2 text-weight-medium text-right q-mr-lg">Progress</div>
        <div class="col-8">
          <q-linear-progress
            size="20px"
            :value="set.worksetProgress"
            color="teal"
          >
            <div class="absolute-full flex flex-center">
              <q-badge
                color="white"
                text-color="teal"
                :label="`${set.worksetProgress * 100}%`"
              />
            </div>
          </q-linear-progress>
        </div>
      </div>
    </q-card>

    <q-card class="q-ma-md" v-if="hasMembers">
      <SetMembers
        :memberCount="set.memberCount"
        :publicMemberCount="set.publicMemberCount"
      />
    </q-card>

    <OpaqueSpinner :showing="loading" />
  </q-tab-panel>
</template>

<script>
import { isNil } from "ramda";
import { useMeta } from "quasar";
import { computed, defineComponent, inject, onMounted, ref } from "vue";

import { requests } from "@/api";
import { OpaqueSpinner } from "@/components/utils";
import { setDetailSchema } from "@/schemas";
import { useAPI, useEditing } from "@/use";

import SetMembers from "./SetMembers.vue";

export default defineComponent({
  name: "SetDetail",
  components: {
    SetMembers,
    OpaqueSpinner,
  },
  setup() {
    const { apiInterface } = useAPI();
    const { editingDetailRouteGuard, resource } = useEditing();

    const { loading, success, data, fetchAPI } = apiInterface();
    const set = ref({});
    const hasMembers = computed(
      () => set.value.memberCount !== undefined && set.value.memberCount > 0,
    );
    const isWorkset = computed(
      () => set.value.setType && set.value.setType.name === "Workset",
    );

    const id = inject("id");

    useMeta(() => ({
      title: set.value ? set.value.name : `Set ${id.value}`,
    }));

    const fetchData = async () => {
      await fetchAPI(requests.sets.getSet(id.value));
      if (success.value)
        await setDetailSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            resource.value = value.setType.name.toLowerCase();
            set.value = value;
            loading.value = false;
          });
    };

    editingDetailRouteGuard();
    onMounted(async () => await fetchData());

    return {
      hasMembers,
      isNil,
      isWorkset,
      loading,
      set,
    };
  },
});
</script>

<style lang="scss" scoped>
.q-tab-panel {
  padding: 0;
}
</style>
