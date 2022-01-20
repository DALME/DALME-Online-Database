<template>
  <q-uploader
    style="max-width: 300px"
    label="Upload attachment"
    :url="url"
    @rejected="onRejected"
  />
</template>

<script>
export default {
  name: "UploadField",
  setup() {
    const url = "";
    const onRejected = (rejected) => console.log(rejected);

    return { onRejected, url };
  },
};
</script>
