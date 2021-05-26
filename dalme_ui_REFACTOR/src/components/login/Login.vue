<template>
  <el-card class="login">
    <h2 class="logo">DALME</h2>
    <el-form ref="formRef" :model="form" :rules="rules" class="login-form">
      <el-form-item prop="username">
        <el-input v-model="form.username" placeholder="Username"> </el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="form.password"
          placeholder="Password"
          type="password"
        >
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button
          class="login-button"
          type="primary"
          native-type="button"
          block
          :disabled="disabled || submitting"
          @click="onSubmit()"
        >
          Login
        </el-button>
      </el-form-item>
      <a class="forgot-password" href="/accounts/password_reset/">
        Forgotten password ?
      </a>
    </el-form>
  </el-card>
</template>

<script>
import { ElMessage } from "element-plus";
import { any, isEmpty, values } from "ramda";
import { computed, reactive, ref, unref } from "vue";
import { useStore } from "vuex";

import { requests } from "@/api";
import { sessionSchema } from "@/schemas";
import { useAPI } from "@/use";

export default {
  name: "Login",
  setup() {
    const store = useStore();
    const { data, fetchAPI, status } = useAPI();

    const formRef = ref({});
    const form = reactive({ username: "", password: "" });
    const submitting = ref(false);
    const disabled = computed(() => any(isEmpty)(values(form)));
    const rules = {
      username: [
        {
          required: true,
          message: "Username is required",
          trigger: "blur",
        },
      ],
      password: [
        {
          required: true,
          message: "Password is required",
          trigger: "blur",
        },
      ],
    };

    const onSubmit = async () => {
      submitting.value = true;
      const form = unref(formRef);
      await form.validate(async (valid) => {
        if (valid) {
          await fetchAPI(requests.auth.login(form.model));
          status.value === 200
            ? await sessionSchema.validate(data.value).then((value) => {
                ElMessage.success("Login successful");
                store.dispatch("login", value);
              })
            : ElMessage.error("Login failed");
        } else {
          ElMessage.error("Login failed");
        }
      });
      submitting.value = false;
      form.resetFields();
    };

    return {
      disabled,
      form,
      formRef,
      onSubmit,
      rules,
    };
  },
};
</script>

<style scoped>
.login {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  width: 17rem;
}
@media screen and (min-width: 600px) {
  .login {
    width: 20rem;
  }
}
.login-button {
  width: 100%;
}
.logo {
  margin-bottom: 1rem;
}
</style>
