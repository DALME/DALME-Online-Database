<template>
  <Spinner v-if="loading" />
  <div v-else class="full-width full-height">
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
          <div class="row q-my-xs">
            <div class="col-2 text-weight-medium text-right q-mr-lg">ID</div>
            <div class="col-8">{{ set.id }}</div>
          </div>

          <div class="row q-my-xs">
            <div class="col-2 text-weight-medium text-right q-mr-lg">Name</div>
            <div class="col-8">{{ set.name }}</div>
          </div>

          <div class="row q-my-xs">
            <div class="col-2 text-weight-medium text-right q-mr-lg">Type</div>
            <div class="col-8">{{ set.setType.name }}</div>
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.isPublic)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Public
            </div>
            <q-icon :name="set.isPublic ? 'done' : 'close'" size="xs" />
          </div>

          <div class="row q-my-xs" v-if="!isNil(set.hasLanding)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Landing
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

          <div class="row q-my-xs">
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

          <div class="row q-my-xs">
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

          <div class="row q-my-xs" v-if="!isNil(set.progress)">
            <div class="col-2 text-weight-medium text-right q-mr-lg">
              Progress
            </div>
            <!-- TODO: progress bar -->
            <div class="col-8">{{ set.progress }}%</div>
          </div>
        </q-card-section>
      </q-card>

      <q-card v-if="hasMembers" class="q-ma-md">
        <SetMembers
          :members="set.members"
          :memberCount="set.memberCount"
          :publicMemberCount="set.publicMemberCount"
        />
      </q-card>

      <Comments />
    </q-tab-panel>
  </div>
</template>

<script>
import { isNil } from "ramda";
import { useMeta } from "quasar";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { requests } from "@/api";
import { Comments } from "@/components";
import { Spinner } from "@/components/utils";
import { setDetailSchema } from "@/schemas";
import { useAPI } from "@/use";

import SetMembers from "./SetMembers.vue";

export default defineComponent({
  name: "SetDetail",
  components: {
    Comments,
    SetMembers,
    Spinner,
  },
  async setup() {
    const $route = useRoute();
    const { loading, success, data, fetchAPI } = useAPI();

    const set = ref({});
    const objId = ref($route.params.objId);
    const hasMembers = computed(
      () => set.value.memberCount !== undefined && set.value.memberCount > 0,
    );

    provide("model", "Set");
    provide("objId", objId);

    useMeta(() => ({
      title: set.value ? set.value.name : `Set ${objId.value}`,
    }));

    const fetchData = async () => {
      await fetchAPI(requests.sets.getSet(objId.value), true);
      if (success.value)
        await setDetailSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => (set.value = value))
          .finally(() => (loading.value = false));
    };

    watch(
      () => $route.params.objId,
      async (to) => {
        objId.value = to;
        await fetchData();
      },
      { immediate: true },
    );

    await fetchData();

    return {
      hasMembers,
      isNil,
      loading,
      set,
    };
  },
});
</script>
