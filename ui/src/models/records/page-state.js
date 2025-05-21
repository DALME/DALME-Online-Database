import { Model } from "pinia-orm";

import { Transcriptions } from "./transcription";

export class PageState extends Model {
  static entity = "page-state";

  static fields() {
    return {
      id: this.attr(null),
      editorTab: this.string("preview"),
      viewerZoom: this.number(0),
      editorContent: this.attr(null),
    };
  }

  static piniaExtend = {
    persist: true,
  };

  static saving(model) {
    if (!model.editorContent) {
      const transcription = Transcriptions.where("pageId", model.id).first();
      if (transcription) model.editorContent = transcription.transcription;
    }
  }
}
