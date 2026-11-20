<template>
  <q-uploader
    @rejected="handleRejected"
    :url="url"
    label="Upload attachment"
    style="max-width: 300px"
  />
</template>

<script>
import logger from "@/logger";

export default {
  name: "UploadField",
  setup() {
    const url = "";
    const handleRejected = (rejected) => logger.log("Upload rejected", rejected);

    return { handleRejected, url };
  },
};
</script>
