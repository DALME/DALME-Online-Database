<template>
  <BaseModal :cuid="cuid" :x-pos="xPos" :y-pos="yPos">
    <template v-slot:content>
      <Spinner :showing="!url" />
      <q-img v-if="url" :src="url">
        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-negative text-white">
            Couldn't load preview...
          </div>
        </template>
      </q-img>
    </template>
  </BaseModal>
</template>

<script>
import { defineComponent, onMounted, ref } from "vue";
import { useSelector } from "@xstate/vue";

import { requests } from "@/api";
import { BaseModal } from "@/components";
import { Spinner } from "@/components/utils";
import { useAPI, useEditing } from "@/use";

export default defineComponent({
  name: "FormModal",
  components: {
    BaseModal,
    Spinner,
  },
  props: {
    cuid: {
      type: String,
      required: true,
    },
    xPos: {
      type: Number,
      required: true,
    },
    yPos: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const { apiInterface } = useAPI();
    const { folios } = useEditing();

    const { data, fetchAPI, success } = apiInterface();

    const { actor } = folios.value[props.cuid];
    const metadata = useSelector(actor, (state) => state.context.metadata);

    const url = ref(null);
    const fetchFolio = async () => {
      await fetchAPI(requests.images.getImageUrl(metadata.value.damId));
      if (success.value) {
        url.value = data.value.url;
      }
    };

    onMounted(async () => await fetchFolio());

    return {
      url,
    };
  },
});
</script>
