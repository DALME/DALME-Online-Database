<template>
  <q-timeline layout="comfortable" class="q-pl-md workflow-timeline">
    <template v-for="(entry, idx) in workLog" :key="idx">
      <q-timeline-entry
        :subtitle="entry.subtitle"
        :icon="entry.icon"
        :color="entry.colour"
        :class="entry.isStage ? 'stage' : 'event'"
      >
        <template v-slot:title>
          {{ entry.title }}
          <DetailPopover v-if="!entry.isStage" showAvatar :userData="entry.user" />
        </template>
      </q-timeline-entry>
    </template>
  </q-timeline>
</template>

<script>
import S from "string";
import { format } from "quasar";
import { computed, defineComponent } from "vue";
import { useConstants } from "@/use";
import { DetailPopover } from "@/components";
import { formatDate, notNully } from "@/utils";

export default defineComponent({
  name: "LogViewer",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  components: {
    DetailPopover,
  },
  setup(props) {
    const {
      workflowIconbyLabel,
      workflowIconbyStage,
      workflowStagesByName,
      workflowStagesById,
      workflowTagColours,
    } = useConstants();
    const { capitalize } = format;

    const getStageState = (stageId) => {
      if (
        props.data.stage === stageId - 1 &&
        props.data[`${workflowStagesById[stageId - 1]}Done`]
      ) {
        return "Awaiting";
      } else if (
        props.data.stage === stageId &&
        !props.data[`${workflowStagesById[stageId]}Done`]
      ) {
        return "In progress";
      } else {
        return props.data[`${workflowStagesById[stageId]}Done`] ? "Completed" : "Pending";
      }
    };

    const getLogEntryMeta = (entry) => {
      let stage = null;
      let text = null;
      if (entry.event.includes(":")) {
        stage = entry.event.split(":")[0];
        text = entry.event.endsWith("commenced")
          ? `${capitalize(stage)} started by`
          : `${capitalize(stage)} marked as completed by`;
      } else if (entry.event.startsWith("Source")) {
        stage = "ingestion";
        text = "Record created by";
      } else if (entry.event.startsWith("public")) {
        stage = "publication";
        text = entry.event.endsWith("True") ? "Record published by" : "Record unpublished by";
      } else if (entry.event.startsWith("help")) {
        stage = "help";
        text = entry.event.endsWith("True") ? "Help flag raised by" : "Help flag dismissed by";
      } else if (entry.event.startsWith("status")) {
        if (entry.event.endsWith("assessing")) {
          stage = "assessing";
          text = "Placed under assessment by";
        } else if (entry.event.endsWith("processed")) {
          stage = "completed";
          text = "Record processing marked as completed by";
        } else {
          stage = "processing";
          text = "Processing resumed by";
        }
      }

      return [stage, text];
    };

    const workLog = computed(() => {
      const eventLog = props.data.workLog;
      const stageNames = Object.keys(workflowStagesByName);
      let stageControl = ["ingestion"];
      let log = [
        {
          title: "Ingestion",
          subtitle: getStageState(1),
          icon: workflowIconbyStage[1],
          timestamp: notNully(eventLog) ? new Date(eventLog[0].timestamp) : null,
          isStage: true,
          colour: workflowTagColours[S(getStageState(1)).underscore().s]["text"],
        },
      ];

      eventLog.forEach((entry) => {
        const [stage, text] = getLogEntryMeta(entry);
        if (stageNames.includes(stage)) {
          let stageId = workflowStagesByName[stage];
          if (!stageControl.includes(stage)) {
            log.push({
              title: capitalize(stage),
              subtitle: getStageState(stageId),
              icon: workflowIconbyStage[stageId],
              timestamp: new Date(entry.timestamp),
              isStage: true,
              colour: workflowTagColours[S(getStageState(stageId)).underscore().s]["text"],
            });
            stageControl.push(stage);
          }
          log.push({
            title: text,
            subtitle: formatDate(entry.timestamp, true),
            icon: "none",
            timestamp: new Date(entry.timestamp),
            isStage: false,
            user: entry.user,
            colour: workflowTagColours[S(getStageState(stageId)).underscore().s]["text"],
          });
        } else {
          log.push({
            title: text,
            subtitle: formatDate(entry.timestamp, true),
            icon: workflowIconbyLabel[stage],
            timestamp: new Date(entry.timestamp),
            isStage: false,
            user: entry.user,
            colour: workflowTagColours[stage]["text"],
          });
        }
      });

      stageNames.forEach((stageName) => {
        if (!stageControl.includes(stageName)) {
          let stageId = workflowStagesByName[stageName];
          log.push({
            title: capitalize(stageName),
            subtitle: getStageState(stageId),
            icon: workflowIconbyStage[stageId],
            isStage: true,
            colour: workflowTagColours[S(getStageState(stageId)).underscore().s]["text"],
          });
          stageControl.push(stageName);
        }
      });

      return log;
    });

    return { workLog };
  },
});
</script>

<style lang="scss">
.workflow-timeline .q-timeline__entry.event .q-timeline__content {
  padding-bottom: 15px;
  padding-top: 0;
}
.workflow-timeline .q-timeline__entry.event .q-timeline__subtitle {
  font-size: 12px;
  text-transform: capitalize;
  letter-spacing: 0;
  font-weight: 600;
  padding-top: 0;
}
.workflow-timeline .q-timeline__entry.event .q-timeline__title {
  font-size: 12px;
  letter-spacing: 0;
  font-weight: 400;
  margin-bottom: 0;
}
.workflow-timeline .q-timeline__entry--icon.event .q-timeline__dot:before {
  height: 15px;
  width: 15px;
  top: 4px;
  left: 8px;
}
.workflow-timeline .q-timeline__entry--icon.event .q-timeline__dot:after {
  top: 23px;
  left: 14px;
}

.workflow-timeline .q-timeline__entry.stage .q-timeline__content {
  padding-bottom: 20px;
  padding-top: 20px;
}
.workflow-timeline .q-timeline__entry.stage:first-of-type .q-timeline__content {
  padding-top: 0;
}
.workflow-timeline .q-timeline__entry.stage .q-timeline__subtitle {
  font-size: 14px;
  letter-spacing: 1px;
  font-weight: 700;
  padding-top: 0;
}
// .workflow-timeline .q-timeline__entry.stage .q-timeline__title {
//
// }
.workflow-timeline .q-timeline__entry--icon.event .q-timeline__dot:before {
  top: 4px;
  left: 8px;
}

// .workflow-timeline .q-timeline__subtitle {
//   font-size: 10px;
//   margin-bottom: 4px;
//   letter-spacing: 0;
//   font-weight: 700;
//   line-height: 14px;
// }
// .workflow-timeline .q-timeline__dot {
//   position: absolute;
//   top: 0;
//   bottom: 0;
// }
// .workflow-timeline .q-timeline__dot i {
//   font-size: 22px;
//   top: -1px;
//   left: -1px;
// }
// .workflow-timeline .q-timeline__dot:before {
//   height: 28px;
//   width: 28px;
// }
// .workflow-timeline .q-timeline__dot:after {
//   top: 29px;
//   left: 12px;
//   width: 5px;
// }
// .workflow-timeline .q-timeline__content {
//   padding-bottom: 5px;
// }
// .workflow-timeline .q-timeline__title {
//   font-size: 1rem;
//   font-weight: 500;
//   line-height: 1rem;
//   letter-spacing: 0.0125em;
//   margin-bottom: 0;
// }
</style>
