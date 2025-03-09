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
      <q-card class="workflow-card">
        <q-card-section horizontal>
          <q-card-section class="q-pr-none">
            <div class="status-section">
              <div v-if="data.wfStatus === 1">
                <span>This record is currenlty under </span>
                <q-badge
                  class="status-badge"
                  color="orange-1"
                  text-color="orange-9"
                  label="assessment"
                />
                <span>.</span>
              </div>
              <div v-if="data.wfStatus === 3 || (data.stage === 5 && data.parsingDone)">
                <span>The processing workflow for this record has been </span>
                <q-badge
                  class="status-badge"
                  color="green-1"
                  text-color="green-10"
                  label="completed"
                />
                <span>.</span>
              </div>
              <template v-else>
                <div
                  v-if="
                    (data.stage === 5 && !data.parsingDone) || (data.stage === 4 && data.reviewDone)
                  "
                >
                  <span>The record is awaiting automated </span>
                  <q-badge
                    class="status-badge"
                    color="deep-purple-1"
                    text-color="deep-purple-8"
                    label="parsing"
                  />
                  <span>.</span>
                </div>
                <template v-else>
                  <div v-if="currentStageDone">
                    <span>The record is awaiting </span>
                    <q-badge
                      class="status-badge"
                      color="deep-purple-1"
                      text-color="deep-purple-8"
                      :label="nextStage"
                    />
                    <span>.</span>
                  </div>
                  <div v-else>
                    <q-badge
                      class="status-badge plus-text"
                      color="blue-1"
                      text-color="blue-9"
                      :label="currentStage"
                    />
                    <span>is in progress.</span>
                  </div>
                </template>
              </template>
              <div v-if="data.helpFlag">
                <span>The </span>
                <q-badge
                  class="status-badge plus-text"
                  color="red-1"
                  text-color="red-10"
                  label="help flag"
                />
                <span>requesting assistance is currently set on this record.</span>
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <q-list dense separator class="status-menu text-grey-9">
              <q-item
                v-if="stageMenu.show"
                clickable
                v-close-popup
                :disable="stageMenu.disabled"
                @click="stageMenu.handler"
              >
                <q-item-section avatar>
                  <q-icon :name="stageMenu.icon" size="xs" color="grey-6" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ stageMenu.label }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="toggleHelp">
                <q-item-section avatar>
                  <q-icon :name="helpFlagMenu.icon" size="xs" color="grey-6" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ helpFlagMenu.label }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item v-if="assessmentMenu.show" clickable v-close-popup @click="toggleAssessment">
                <q-item-section avatar>
                  <q-icon :name="assessmentMenu.icon" size="xs" color="grey-6" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ assessmentMenu.label }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item
                clickable
                v-close-popup
                :disable="publicationMenu.disabled"
                @click="togglePublic"
              >
                <q-item-section avatar>
                  <q-icon :name="publicationMenu.icon" size="xs" color="grey-6" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ publicationMenu.label }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card-section>
        <q-card-section v-if="data.wfStatus === 1" class="q-pt-none status-detail text-grey-7">
          <span>
            While under assessment, records are temporarily placed outside of the normal processing
            workflow. Certain functions may not be available as a result.
          </span>
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
  emits: ["stateChanged"],
  setup(props, context) {
    const { workflowTagColours, workflowIconbyStage, workflowStagesById } = useConstants();
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

    const currentStage = computed(() => workflowStagesById[props.data.stage]);
    const nextStage = computed(() =>
      props.data.stage === 5 ? "parsing" : workflowStagesById[props.data.stage + 1],
    );
    const currentStageDone = computed(() => props.data[`${currentStage.value}Done`]);

    const markStageDone = () => {
      context.emit("stateChanged", {
        action: "stage_done",
        code: props.data.stage,
      });
    };

    const startStage = () => {
      context.emit("stateChanged", {
        action: "begin_stage",
        code: props.data.stage + 1,
      });
    };

    const togglePublic = () => {
      context.emit("stateChanged", {
        action: "toggle_public",
      });
    };

    const toggleHelp = () => {
      context.emit("stateChanged", {
        action: "toggle_help",
      });
    };

    const toggleAssessment = () => {
      const isDone = props.data.stage === 5 && props.data.parsingDone;
      const code = props.data.wfStatus === 1 ? (isDone ? 3 : 2) : 1;
      context.emit("stateChanged", {
        action: "change_status",
        code: code,
      });
    };

    const stageMenu = computed(() => {
      if (
        (props.data.stage === 4 && props.data.reviewDone) ||
        props.data.stage === 5 ||
        props.data.wfStatus === 3
      )
        return { show: false };
      const label = currentStageDone.value
        ? `Start ${nextStage.value}`
        : `Mark ${currentStage.value} as done`;
      const icon = currentStageDone.value ? "mdi-circle-edit-outline" : "mdi-check";
      const disabled = props.data.wfStatus === 1;
      const handler = currentStageDone.value ? startStage : markStageDone;
      return { label, icon, disabled, show: true, handler };
    });

    const publicationMenu = computed(() => ({
      disabled: props.data.wfStatus === 1 || !props.data.reviewDone,
      label: props.data.isPublic ? "Unpublish this record" : "Publish this record",
      icon: props.data.isPublic ? "mdi-earth-off" : "mdi-earth",
    }));

    const helpFlagMenu = computed(() => ({
      label: props.data.helpFlag ? "Unset help flag" : "Flag for help",
      icon: props.data.helpFlag ? "mdi-flag-off" : "mdi-flag",
    }));

    const assessmentMenu = computed(() => ({
      show: props.data.wfStatus !== 3 && !(props.data.stage === 5 && props.data.parsingDone),
      label: props.data.wfStatus === 1 ? "Return to processing" : "Place under assessment",
      icon: props.data.wfStatus === 1 ? "mdi-eye-off" : "mdi-eye",
    }));

    return {
      colours,
      icon,
      stageMenu,
      helpFlagMenu,
      publicationMenu,
      assessmentMenu,
      currentStage,
      nextStage,
      currentStageDone,
      togglePublic,
      toggleHelp,
      toggleAssessment,
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
.workflow-card {
  max-width: 450px;
}
.status-badge {
  text-transform: uppercase;
  font-weight: 600;
  font-size: 10px;
  border: 1px solid;
  margin-right: 1px;
}
.status-section {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 10px;
  font-size: 12px;
}
.status-detail {
  font-size: 10px;
}
.status-menu .q-item__label {
  text-wrap: nowrap;
}
.plus-text {
  margin-right: 3px;
}
</style>
