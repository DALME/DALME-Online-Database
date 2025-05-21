import { useRepo } from "pinia-orm";

import { CustomModel, CustomRepository } from "@/models";

import { PageState } from "./page-state";
import { Transcriptions } from "./transcription";

const PageStates = useRepo(PageState);

class Page extends CustomModel {
  static entity = "page";

  static fields() {
    return {
      damId: this.number(null),
      hasImage: this.boolean(false),
      hasTranscription: this.boolean(false),
      id: this.attr(null),
      manifestUrl: this.string(""),
      name: this.string(""),
      order: this.number(0),
      recordId: this.attr(null),
      thumbnailUrl: this.string(""),
      transcription: this.hasOne(Transcriptions, "pageId"),
      // state
      state: this.hasOne(PageState, "id"),
    };
  }

  static saved(model) {
    console.log("Page saved", model);
    if (!model.state) {
      PageStates.save({ id: model.id });
    }
  }

  // getters
  get transcriptionContent() {
    return this.transcription;
  }
}

class PageRepo extends CustomRepository {
  use = Page;

  // getters
  get hasChanges() {
    return this.transcription.transcription !== this.state.editorContent;
  }
}

export const Pages = useRepo(PageRepo);
