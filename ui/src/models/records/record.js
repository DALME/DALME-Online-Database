import { useRepo } from "pinia-orm";
import { DateCast } from "pinia-orm/casts";
import { ref } from "vue";

import { requests } from "@/api";
import {
  Agents,
  Attributes,
  Collections,
  CustomModel,
  CustomRepository,
  Places,
  Users,
} from "@/models";
import { recordDetailSchema, recordListSchema } from "@/schemas";

import { Pages } from "./page";
import { PageState } from "./page-state";
import { RecordState } from "./record-state";
import { Workflows } from "./workflow";

const RecordStates = useRepo(RecordState);
const PageStates = useRepo(PageState);

class Record extends CustomModel {
  static entity = "record";
  static requests = requests.records;
  static schema = {
    instance: recordDetailSchema,
    list: recordListSchema,
  };

  static piniaOptions = {
    currentRecordId: ref(null),
  };

  static autoFields = {
    agentIds: Agents,
    attributeIds: Attributes,
    creationUserId: Users,
    modificationUserId: Users,
    ownerId: Users,
    collectionIds: Collections,
    placeIds: Places,
  };

  static fields() {
    return {
      agentIds: this.attr([]),
      attributeIds: this.attr([]),
      collectionIds: this.attr([]),
      commentCount: this.number(0),
      creationTimestamp: this.attr(null),
      creationUserId: this.attr(null),
      creditLine: this.string(""),
      id: this.attr(null),
      isPrivate: this.boolean(false),
      modificationTimestamp: this.attr(null),
      modificationUserId: this.attr(null),
      name: this.string(""),
      noFolios: this.number(0),
      noTranscriptions: this.number(0),
      ownerId: this.attr(null),
      pages: this.hasMany(Pages, "recordId"),
      parent: this.attr(null),
      permissions: this.attr(null),
      placeIds: this.attr([]),
      shortName: this.string(""),
      workflow: this.hasOne(Workflows, "record"),
      // related
      agents: this.hasManyBy(Agents, "agentIds"),
      attributes: this.hasManyBy(Attributes, "attributeIds"),
      creationUser: this.belongsTo(Users, "creationUserId"),
      modificationUser: this.belongsTo(Users, "modificationUserId"),
      owner: this.belongsTo(Users, "ownerId"),
      collections: this.hasManyBy(Collections, "collectionIds"),
      places: this.hasManyBy(Places, "placeIds"),
      // state
      state: this.hasOne(RecordState, "id"),
    };
  }

  static casts() {
    return {
      creationTimestamp: DateCast,
      modificationTimestamp: DateCast,
    };
  }

  static saving(model, record) {
    console.log("saving record", model, record);
    if (!model.state) {
      RecordStates.save({ id: model.id });
    }
  }

  attr(name) {
    const result = this.attributes.filter((x) => x.name === name);
    if (result.length > 1) return result;
    if (result.length === 1) return result[0];
    return null;
  }
}

class RecordRepo extends CustomRepository {
  use = Record;

  // getters
  get current() {
    return this.withAllRecursive().find(this.store.currentRecordId);
  }
  get currentState() {
    return RecordStates.find(this.current.id);
  }
  get currentPage() {
    if (!this.current.state.currentPageId) {
      this.updateRecordState({ currentPageId: this.current.pages[0].id });
    }
    return this.current.pages.find((p) => p.id === this.current.state.currentPageId);
  }
  get currentPageIndex() {
    return this.current.pages.indexOf(this.currentPage);
  }
  get pageCount() {
    return this.current.pages.length;
  }
  get showTagMenu() {
    return this.current.state.showTagMenu;
  }
  get pageDrawerMini() {
    return this.current.state.pageDrawerMini;
  }
  get splitterHorizontal() {
    return this.current.state.splitterHorizontal;
  }
  get editorSplitter() {
    return this.current.state.editorSplitter;
  }
  get lastSplitter() {
    return this.current.state.lastSplitter;
  }
  get editOn() {
    return this.current.state.editOn;
  }
  get hasChanges() {
    return this.current.pages.some((p) => p.hasChanges);
  }
  get editorContent() {
    return this.currentPage.state.editorContent;
  }
  get viewerZoom() {
    return this.currentPage.state.viewerZoom;
  }
  get tab() {
    return this.current?.state.tab || "info";
  }
  get showEditBtn() {
    return this.tab === "pages" && this.pageCount > 0;
  }
  get editorTab() {
    return this.currentPage.state.editorTab;
  }
  // setters
  set showTagMenu(value) {
    this.updateRecordState({ showTagMenu: value });
  }
  set pageDrawerMini(value) {
    this.updateRecordState({ pageDrawerMini: value });
  }
  set splitterHorizontal(value) {
    this.updateRecordState({ splitterHorizontal: value });
  }
  set editorSplitter(value) {
    this.updateRecordState({ editorSplitter: value });
  }
  set lastSplitter(value) {
    this.updateRecordState({ lastSplitter: value });
  }
  set editOn(value) {
    this.updateRecordState({ editOn: value });
  }
  set editorContent(value) {
    this.updatePageState({ editorContent: value });
  }
  set viewerZoom(value) {
    this.updatePageState({ viewerZoom: value });
  }
  set tab(value) {
    this.updateRecordState({ tab: value });
  }
  set editorTab(value) {
    this.updatePageState({ editorTab: value });
  }
  set currentPageId(value) {
    this.updateRecordState({ currentPageId: value });
  }

  // actions
  setCurrent(id) {
    return new Promise((resolve) => {
      this.ensure(id).then(() => {
        this.store.currentRecordId = id;
        resolve();
      });
    });
  }
  updateRecordState(payload) {
    RecordStates.save({ id: this.current.id, ...payload });
  }
  updatePageState(payload) {
    PageStates.save({ id: this.current.state.currentPageId, ...payload });
  }
}

export const Records = useRepo(RecordRepo);

window.testRecords = Records;
