import { attachmentIcons } from "./attachments";
import { dateFormats } from "./dates";
import { editorModeIcons, fontSizeOptions, teiSelectors, themeOptions } from "./editor";
import { rightsColoursById, rightsIconById } from "./rights";
import { ticketTagColours, ticketTagIcon } from "./tickets";
import {
  workflowIconbyLabel,
  workflowIconbyStage,
  workflowIconbyStatus,
  workflowStagesById,
  workflowStagesByName,
  workflowTagColours,
} from "./workflow";

export const useConstants = () => {
  return {
    workflowStagesById,
    workflowStagesByName,
    workflowTagColours,
    workflowIconbyStatus,
    workflowIconbyStage,
    workflowIconbyLabel,
    teiSelectors,
    editorModeIcons,
    ticketTagColours,
    ticketTagIcon,
    attachmentIcons,
    rightsColoursById,
    rightsIconById,
    dateFormats,
    fontSizeOptions,
    themeOptions,
  };
};
