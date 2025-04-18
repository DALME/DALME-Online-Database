<template>
  <div v-if="scope.pagesNumber" class="row full-width flex-center q-py-xs q-px-sm table-pager">
    <q-btn-group class="list-footer-button-group" unelevated>
      <q-btn
        v-if="scope.pagesNumber > 2"
        @click="scope.firstPage"
        :disable="scope.isFirstPage"
        :text-color="scope.isFirstPage ? 'grey-8' : 'indigo-5'"
        class="list-footer-button strong-focus"
        icon="skip_previous"
        size="sm"
        flat
      />
      <q-separator class="bg-grey-4" vertical />
      <q-btn
        @click="scope.prevPage"
        :disable="scope.isFirstPage"
        :text-color="scope.isFirstPage ? 'grey-8' : 'indigo-5'"
        class="list-footer-button strong-focus"
        icon="fast_rewind"
        size="sm"
        flat
      />
      <div class="row justify-center">
        <q-input
          @blur="updateCurrentPageModel"
          @keyup="onKeyup"
          @update:model-value="onUpdateModelValue"
          :max="scope.pagesNumber"
          :min="1"
          :model-value="newPage"
          :placeholder="placeHolder"
          :style="`width: ${placeHolder.length / 1.5}em`"
          class="inline page-input strong-focus"
          type="number"
          borderless
          stack-label
        >
        </q-input>
      </div>
      <q-btn
        @click="scope.nextPage"
        :disable="scope.isLastPage"
        :text-color="scope.isLastPage ? 'grey-8' : 'indigo-5'"
        class="list-footer-button strong-focus"
        icon="fast_forward"
        size="sm"
        flat
      />
      <q-separator class="bg-grey-4" vertical />
      <q-btn
        v-if="scope.pagesNumber > 2"
        @click="scope.lastPage"
        :disable="scope.isLastPage"
        :text-color="scope.isLastPage ? 'grey-8' : 'indigo-5'"
        class="list-footer-button strong-focus"
        icon="skip_next"
        size="sm"
        flat
      />
    </q-btn-group>
  </div>
</template>

<script>
import { format } from "quasar";
import { computed, defineComponent, ref } from "vue";

export default defineComponent({
  name: "TablePager",
  props: {
    scope: {
      type: Object,
      required: true,
    },
  },
  emits: ["changePage"],
  setup(props, context) {
    const { between } = format;
    const newPage = ref(null);

    const isKeyCode = (evt, keyCodes) => {
      if (evt.isComposing === true || evt.qKeyEvent === true) {
        return false;
      } else {
        return [].concat(keyCodes).includes(evt.keyCode);
      }
    };

    const onKeyup = (e) => {
      isKeyCode(e, 13) === true && updateCurrentPageModel();
    };

    const onUpdateModelValue = (value) => {
      newPage.value = value;
    };

    const currentPageModel = computed({
      get: () => props.scope.pagination.page,
      set: (val) => {
        val = parseInt(val, 10);
        if (isNaN(val)) return;
        const value = between(val, 1, props.scope.pagesNumber);
        if (props.scope.pagination.page !== value) {
          context.emit("changePage", value);
        }
      },
    });

    const updateCurrentPageModel = () => {
      currentPageModel.value = newPage.value;
      newPage.value = null;
    };

    const placeHolder = computed(() => {
      return `${currentPageModel.value} / ${props.scope.pagesNumber}`;
    });

    return {
      newPage,
      placeHolder,
      onUpdateModelValue,
      onKeyup,
      updateCurrentPageModel,
    };
  },
});
</script>

<style lang="scss" scoped>
.table-pager {
  border-top: 1px solid rgb(209, 209, 209);
}
.list-footer-button {
  min-height: 2em;
  padding: 4px 10px;
}
.list-footer-button-group {
  height: 30px;
  background: white;
  border: 1px solid rgb(209, 209, 209);
}
.page-input input {
  padding: 0;
  font-weight: 500;
  user-select: auto;
  text-align: center;
  appearance: textfield;
  -moz-appearance: textfield;
  color: #616161;
}
.page-input input::-webkit-outer-spin-button,
.page-input input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.page-input .q-field__control {
  height: 28px;
  background-color: #fff;
  border-right: 1px solid rgb(209, 209, 209);
  border-left: 1px solid rgb(209, 209, 209);
}
</style>
