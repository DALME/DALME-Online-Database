<template>
  <q-uploader
    @rejected="handleRejected"
    :url="url"
    label="Upload attachment"
    style="max-width: 300px"
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
