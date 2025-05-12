import { snakeCase } from "change-case";
import { Repository } from "pinia-orm";
import { isEmpty, isNil } from "ramda";

import { API as apiInterface, requestOptions } from "@/api";
import { contentTypeSchema, optionListSchema } from "@/schemas";

import CustomQuery from "./query";

export default class CustomRepository extends Repository {
  queue = [];
  inProgress = [];

  get schema() {
    return this.getModel().constructor.schema || null;
  }

  get requests() {
    return this.getModel().constructor.requests || null;
  }

  get autoFields() {
    return this.getModel().constructor.autoFields || null;
  }

  get entity() {
    return this.getModel().constructor.entity;
  }

  get hasAttributes() {
    return "attributes" in this.getModel().$fields();
  }

  get store() {
    return this.piniaStore();
  }

  get keyName() {
    return this.getModel().$getKeyName();
  }

  query() {
    return new CustomQuery(
      this.database,
      this.getModel(),
      this.queryCache,
      this.hydratedDataCache,
      this.pinia,
    );
  }

  save(records) {
    return new Promise((resolve) => {
      console.log("called save on", this, records);
      if (this.autoFields) {
        let [data, entities] = this.query().normalize(records);
        if (!Array.isArray(data)) data = [data];
        Promise.all(data.map((x) => this.processAutoFields(x))).then(() => {
          this.query().saveEntities(entities);
          resolve(this.revive(data));
        });
      } else {
        // console.log("no autoFields, saving", this.entity);
        resolve(this.query().save(records));
      }
    });
  }

  create(records) {
    console.log("called create on", this.entity);
    return this.remoteCreate(records);
  }

  update(id, payload) {
    console.log("called update on", this.entity);
    return this.remoteUpdate(id, payload);
  }

  destroy(ids) {
    console.log("called destroy on", this.entity);
    return this.remoteDestroy(ids);
  }

  processAutoFields(record) {
    // console.log("starting autoFields", this.entity, record.id);
    return Promise.all(
      Object.keys(this.autoFields).map((property) => {
        // console.log("autoField", this.entity, record.id, property);
        return this.autoFields[property].ensure(record[property]);
      }),
    );
  }

  ensure(ids) {
    if (isNil(ids) || isEmpty(ids)) return Promise.resolve();
    if (!Array.isArray(ids)) ids = [ids];
    return Promise.all(ids.map((x) => this.enqueue(x)));
  }

  refresh() {
    console.log("refreshing", this.entity);
    return Promise.all(
      this.query()
        .all()
        .map((x) => this.enqueue(x[this.keyName])),
    );
  }

  options(field) {
    if (!field) return Promise.resolve(null);
    return new Promise((resolve) => {
      if (field in this.store.options) resolve(this.store.options[field]);
      this.retrieveOptions(field).then((response) => {
        this.store.options[field] = response;
        resolve(response);
      });
    });
  }

  meta() {
    return new Promise((resolve) => {
      if (!isEmpty(this.store.meta)) resolve(this.store.meta);
      this.retrieveMetadata().then(() => resolve(this.store.meta));
    });
  }

  enqueue(id) {
    return new Promise((resolve) => {
      const rec = this.find(id);
      const isInQueue = this.queue.includes(id);
      const isInProgress = this.inProgress.includes(id);
      const isLoaded = Boolean(rec);
      const isStale = isLoaded ? rec.isStale : false;
      // console.log(
      //   `ENQUEUE ${this.entity} ${id}:`,
      //   `inQ: ${isInQueue}, inP: ${isInProgress}, loaded: ${isLoaded}, stale: ${isStale}`,
      // );
      if (!isInQueue && !isInProgress && (!isLoaded || isStale)) {
        // console.log("enqueuing", this.entity, id, this.queue);
        this.queue.push({ id, resolve });
        this.dequeue();
      } else {
        resolve();
      }
    });
  }

  dequeue() {
    if (this.queue.length === 0) return false;
    const target = this.queue.shift();
    if (target && target.id) {
      this.inProgress.push(target.id);
      this.remoteRetrieve(target.id).then((record) => {
        target.resolve(record);
        this.inProgress.slice(this.inProgress.indexOf(target.id), 1);
        this.dequeue();
      });
    }
    return true;
  }

  // override hooks
  processResponse(response) {
    return response;
  }

  // remote calls
  remoteCall(request, schema, action = this.save.bind(this)) {
    return new Promise((resolve) => {
      const { success, data, fetchAPI } = apiInterface();
      fetchAPI(request).then(() => {
        if (success.value) {
          console.log("validating...", data.value);
          schema.validate(this.processResponse(data.value)).then((validated) => {
            action(validated).then((result) => {
              resolve(result);
            });
          });
        }
      });
    });
  }

  remoteRetrieve(id) {
    return this.remoteCall(this.requests.get(id), this.schema.instance);
  }

  remoteUpdate(id, payload) {
    console.log("Remote update", this.entity, id, payload);
    return this.remoteCall(this.requests.update(id, payload), this.schema.instance);
  }

  remoteCreate(payload) {
    console.log("Remote create", this.entity, payload);
    return this.remoteCall(this.requests.create(payload), this.schema.instance);
  }

  remoteDestroy(id) {
    console.log("Remote destroy", this.entity, id);
    const action = (ids) => this.query().destroy(ids);
    return this.remoteCall(this.requests.destroy(id), this.schema.instance, action);
  }

  retrieveOptions(field) {
    return new Promise((resolve) => {
      const { success, data, fetchAPI } = apiInterface();
      fetchAPI(requestOptions(snakeCase(field), true, this.entity)).then(() => {
        if (success.value) {
          optionListSchema.validate(data.value, { stripUnknown: false }).then((validated) => {
            resolve(validated);
          });
        } else {
          resolve(null);
        }
      });
    });
  }

  retrieveMetadata() {
    const action = (data) => {
      this.store.attributeTypes = data.attributeTypes;
      this.store.contentType = data.id;
    };
    return this.remoteCall(this.requests.metadata(), contentTypeSchema, action);
  }

  // compatibility methods so that CustomRepository instances
  // can be used in lieu of Model instances
  newRawInstance() {
    return this.use.newRawInstance();
  }
}
