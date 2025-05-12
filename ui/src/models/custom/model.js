import { Model } from "pinia-orm";
import { ref } from "vue";

export default class CustomModel extends Model {
  static hidden = [];
  static autoFields = null;

  static piniaOptions = {
    options: ref({}),
    meta: ref({}),
  };

  static piniaExtend = {
    persist: true,
  };

  static saved(model) {
    console.log("saved", this.entity, model.id);
  }

  static get isStale() {
    const now = Math.floor(Date.now() / 1000);
    console.log("since created", now - this._meta.createdAt);
    console.log("since updated", now - this._meta.updatedAt);
    return now - this._meta.updatedAt > 3600;
  }
}
