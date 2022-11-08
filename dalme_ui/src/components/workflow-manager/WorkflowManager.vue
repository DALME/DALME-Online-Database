<template>
  <q-btn-dropdown
    dense
    outline
    :icon="icon"
    :color="colours.colour"
    :text-color="colours.text"
    :class="`workflow-button bg-${colours.colour}`"
    :label="data.status.text"
  >
    <q-card>
      <q-card-section horizontal>
        <q-card-section>somthing</q-card-section>
        <q-card-section>
          <q-list dense separator class="text-grey-9">
            <q-item clickable v-close-popup>
              <q-item-section>
                <q-item-label>Mark stage as done/Start stage</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>
                <q-item-label>Flag for assistance</q-item-label>
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>
                <q-item-label>Place under assessment</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card-section>
    </q-card>
  </q-btn-dropdown>
</template>

<script>
import { computed, defineComponent } from "vue";
import { useConstants } from "@/use";

export default defineComponent({
  name: "WorkflowManager",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const { workflowTagColours, workflowIconbyStage } = useConstants();
    const colours = computed(() => workflowTagColours[props.data.status.tag]);
    const icon = computed(() => workflowIconbyStage[props.data.stage]);

    return {
      colours,
      icon,
    };
  },
});
</script>

<style lang="scss">
.workflow-button {
  font-weight: 600;
  font-size: 12px;
}
.workflow-button i:first-of-type {
  font-size: 18px;
  font-weight: 200;
  margin-left: 5px;
}
</style>
