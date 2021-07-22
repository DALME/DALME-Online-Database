<template>
  <div class="q-ma-md full-width full-height">
    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="bookmark" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Source</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="assignment" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Attributes</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="info" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Metadata</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <!-- Don't show if not source.description -->
    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="subject" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Description</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="menu_book" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Pages</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="people" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Agents</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <q-card class="q-ma-md">
      <q-item>
        <q-item-section avatar>
          <q-avatar>
            <q-icon name="share" style="transform: rotate(90deg)" />
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>Children</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-card-section> </q-card-section>
    </q-card>

    <Comments />
  </div>
</template>

<script>
import { defineComponent, inject, provide, ref } from "vue";

import { requests } from "@/api";
import { Comments } from "@/components";
import { sourceDetailSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "SourceDetail",
  components: {
    Comments,
  },
  async setup() {
    const { success, data, fetchAPI } = useAPI();
    // const {
    //   success: childrenSuccess,
    //   fetchAPI: childrenFetchAPI,
    //   status: childrenStatus,
    // } = useAPI();

    const source = ref(null);
    const objId = inject("objId");
    provide("model", "Source");

    await fetchAPI(requests.sources.getSource(objId));
    if (success.value)
      await sourceDetailSchema
        .validate(data.value, { stripUnknown: true })
        .then((value) => {
          source.value = value;
        });

    return { source };
  },
});
</script>
