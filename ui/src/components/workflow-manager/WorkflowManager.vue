<template>
  <div class="column">
    <q-btn-dropdown
      dense
      outline
      split
      size="sm"
      :icon="icon"
      :text-color="colours.text"
      :class="`workflow-button bg-grey-2`"
      :label="data.status.text"
    >
      <q-card>
        <q-card-section horizontal>
          <q-card-section>somthing</q-card-section>
          <q-card-section>
            <q-list dense separator class="text-grey-9">
              <q-item clickable v-close-popup>
                <q-item-section>
                  <q-item-label> Mark stage as done/Start stage </q-item-label>
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
  </div>
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
    // const colours = computed(() => workflowTagColours[props.data.status.tag]);
    const colours = computed(() => {
      let type = props.data.status;
      type = ["ingestion", "transcription", "markup", "review", "parsing"].reduce(
        (result, word) => result.replace(word, ""),
        type,
      );
      type = type.trim().replace(" ", "_");
      return workflowTagColours[type];
    });
    const icon = computed(() => workflowIconbyStage[props.data.stage]);

    return {
      colours,
      icon,
    };
  },
});
</script>

<style lang="scss">
.workflow-button > button {
  padding-right: 10px;
}
.workflow-button > button span {
  font-weight: 600;
  font-size: 12px;
  text-transform: capitalize;
}
.workflow-button button:not(.q-btn-dropdown__arrow-container) i:first-of-type {
  font-size: 18px;
  font-weight: 200;
  margin-left: 5px;
}
</style>
