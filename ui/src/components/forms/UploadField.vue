<template>
  <q-uploader
    style="max-width: 300px"
    label="Upload attachment"
    :url="url"
    @rejected="handleRejected"
  />
</template>

<script>
export default {
  name: "UploadField",
  setup() {
    const url = "";
    const handleRejected = (rejected) => console.log(rejected);

    return { handleRejected, url };
  },
};
</script>
