import { kebabCase, snakeCase } from "change-case";
import { Repository, useRepo } from "pinia-orm";
import { isEmpty, isNil } from "ramda";

import { API as apiInterface, requestOptions } from "@/api";
import { Field, Metadata } from "@/models";
import notifier from "@/notifier";
import { contentTypeSchema, optionListSchema } from "@/schemas";

import CustomQuery from "./query";

const FieldRepo = useRepo(Field);
const MetadataRepo = useRepo(Metadata);

window.testFieldRepo = FieldRepo;

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
      // console.log("called save on", this, records);
      if (this.autoFields) {
        let [data, entities] = this.query().normalize(records);
        if (!Array.isArray(data)) data = [data];
        Promise.all(data.map((x) => this.processAutoFields(x)))
          .then(() => {
            this.query().saveEntities(entities);
            resolve(this.revive(data));
          })
          .catch((error) => {
            notifier.ORM.error(`Unable to save ${this.entity}: ${error}`);
            resolve(null);
          });
      } else {
        // console.log("no autoFields, saving", this.entity);
        resolve(this.query().save(records));
      }
    });
  }

  create(records) {
    console.log("called create on", this.entity);
    return this.remoteCreate(records).catch((error) => {
      notifier.ORM.error(`Unable to create ${this.entity}: ${error}`);
    });
  }

  update(id, payload) {
    console.log("called update on", this.entity);
    return this.remoteUpdate(id, payload).catch((error) => {
      notifier.ORM.error(`Unable to update ${this.entity}: ${error}`);
    });
  }

  destroy(ids) {
    console.log("called destroy on", this.entity);
    return this.remoteDestroy(ids).catch((error) => {
      notifier.ORM.error(`Unable to delete ${this.entity}: ${error}`);
    });
  }

  processAutoFields(record) {
    // console.log("starting autoFields", this.entity, record.id);
    return Promise.all(
      Object.keys(this.autoFields).map((property) => {
        // console.log("autoField", this.entity, record.id, property);
        return this.autoFields[property].ensure(record[property]);
      }),
    ).catch((error) => {
      notifier.ORM.error(`Unable to process autoFields for ${this.entity}: ${error}`);
    });
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

  options(field, originator = this.entity) {
    if (!field) return Promise.resolve(null);
    return new Promise((resolve) => {
      const stored = FieldRepo.withAll().where("field", field).where("model", originator).get();
      if (stored.length > 0) {
        resolve(stored[0].options);
      } else {
        this.retrieveOptions(field, originator)
          .then((response) => resolve(response))
          .catch((error) => {
            notifier.CRUD.failure(`Unable to retrieve options for ${this.entity}: ${error}`);
            resolve(null);
          });
      }
    });
  }

  meta() {
    return new Promise((resolve) => {
      const stored = MetadataRepo.withAll().where("entity", this.entity).get();
      if (stored.length > 0) {
        resolve(stored[0]);
      } else {
        this.retrieveMetadata()
          .then((data) => resolve(data))
          .catch((error) => {
            notifier.CRUD.failure(`Unable to retrieve metadata for ${this.entity}: ${error}`);
            resolve(null);
          });
      }
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
    return new Promise((resolve, reject) => {
      const { success, data, error, fetchAPI } = apiInterface();
      fetchAPI(request).then(() => {
        if (success.value) {
          // console.log("validating...", data.value, schema, action);
          schema.validate(this.processResponse(data.value)).then((validated) => {
            action(validated).then((result) => {
              resolve(result);
            });
          });
        } else {
          reject(error.value);
        }
      });
    });
  }

  remoteRetrieve(id = null) {
    console.log("REMOTE RETRIEVE", this.entity);
    if (isNil(id)) return this.remoteCall(this.requests.list(), this.schema.list);
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
    return this.remoteCall(this.requests.destroy(id), this.schema.instance, (ids) =>
      this.query().destroy(ids),
    );
  }

  retrieveOptions(field, originator) {
    console.log("retrieve options", this.entity, field);
    return this.remoteCall(
      requestOptions(snakeCase(field), true, this.entity),
      optionListSchema,
      (data) =>
        new Promise((resolve) => {
          const fieldRecord = FieldRepo.save({ field: field, model: originator, options: data });
          resolve(fieldRecord.options);
        }),
    );
  }

  retrieveMetadata() {
    console.log("retrieveMetadata", this.entity);
    return this.remoteCall(
      this.requests.metadata(),
      contentTypeSchema,
      (data) =>
        new Promise((resolve) => {
          resolve(
            MetadataRepo.save({
              contentType: data.id,
              entity: kebabCase(data.name),
              attributeTypes: data.attributeTypes,
            }),
          );
        }),
    );
  }

  // compatibility methods so that CustomRepository instances
  // can be used in lieu of Model instances
  newRawInstance() {
    return this.use.newRawInstance();
  }
}
