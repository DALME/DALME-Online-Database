<template>
  <div v-if="scope.pagesNumber" class="row full-width q-py-xs q-px-sm">
    <q-item-section class="q-pl-xs q-pr-sm">
      <q-item-label class="text-subtitle text-grey-8">
        {{ status }}
      </q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-btn-group unelevated class="list-footer-button-group">
        <q-btn
          v-if="scope.pagesNumber > 2"
          flat
          icon="skip_previous"
          :text-color="scope.isFirstPage ? 'grey-8' : 'indigo-5'"
          size="sm"
          class="list-footer-button"
          :disable="scope.isFirstPage"
          @click="scope.firstPage"
        />
        <q-separator vertical class="bg-grey-4" />
        <q-btn
          flat
          icon="fast_rewind"
          :text-color="scope.isFirstPage ? 'grey-8' : 'indigo-5'"
          size="sm"
          class="list-footer-button"
          :disable="scope.isFirstPage"
          @click="scope.prevPage"
        />
        <div class="row justify-center">
          <q-input
            :model-value="newPage"
            type="number"
            :min="1"
            :max="scope.pagesNumber"
            :placeholder="placeHolder"
            stack-label
            borderless
            class="inline page-input"
            :style="`width: ${placeHolder.length / 1.5}em`"
            @update:modelValue="onUpdateModelValue"
            @keyup="onKeyup"
            @blur="updateCurrentPageModel"
          >
          </q-input>
        </div>
        <q-btn
          flat
          icon="fast_forward"
          :text-color="scope.isLastPage ? 'grey-8' : 'indigo-5'"
          size="sm"
          class="list-footer-button"
          :disable="scope.isLastPage"
          @click="scope.nextPage"
        />
        <q-separator vertical class="bg-grey-4" />
        <q-btn
          v-if="scope.pagesNumber > 2"
          flat
          icon="skip_next"
          :text-color="scope.isLastPage ? 'grey-8' : 'indigo-5'"
          size="sm"
          class="list-footer-button"
          :disable="scope.isLastPage"
          @click="scope.lastPage"
        />
      </q-btn-group>
    </q-item-section>
  </div>
</template>

<script>
import { computed, defineComponent, ref } from "vue";
import { format } from "quasar";

export default defineComponent({
  name: "BasicTablePager",
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

    const status = computed(() => {
      return `Showing ${props.scope.pagination.rowsNumber.toLocaleString(
        "en-US",
      )} out of ${props.scope.pagination.rowsTotal.toLocaleString(
        "en-US",
      )} records.`;
    });

    return {
      newPage,
      placeHolder,
      onUpdateModelValue,
      onKeyup,
      status,
      updateCurrentPageModel,
    };
  },
});
</script>
