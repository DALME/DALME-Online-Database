import { Model } from "pinia-orm";

export default class CustomModel extends Model {
  static hidden = [];
  static autoFields = null;

  static piniaExtend = {
    persist: true,
  };

  get isStale() {
    const now = Math.floor(Date.now() / 1000);
    return now - this._meta.updatedAt > 3600;
  }

  get entity() {
    return this.$entity();
  }
}
