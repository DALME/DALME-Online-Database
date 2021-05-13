<template>
  <el-card class="login">
    <h2>DALME</h2>
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
          :disabled="disabled"
          @click="onSubmit()"
        >
          Login
        </el-button>
      </el-form-item>
      <a class="forgot-password" href="/accounts/password_reset/">
        Forgot password ?
      </a>
    </el-form>
  </el-card>
</template>

<script>
import { any, isEmpty, values } from "ramda";
import { computed, reactive, ref, unref } from "vue";
import { API } from "@/api";
import { sessionSchema } from "@/schemas";

export default {
  name: "Login",
  setup() {
    const formRef = ref({});
    const form = reactive({ username: "", password: "" });
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

    return {
      disabled,
      form,
      formRef,
      rules,
    };
  },
  methods: {
    async onSubmit() {
      const form = unref(this.formRef);
      await form.validate(async (valid) => {
        if (valid) {
          const { success, data } = await API.auth.login(this.form);
          success
            ? await sessionSchema
                .validate(data)
                .then((value) => this.login(value))
            : this.failure(data.error);
        } else {
          this.failure();
        }
      });
    },
    login(data) {
      this.success();
      this.$store.dispatch("login", data);
    },
    success() {
      this.$message({ message: "Login successful", type: "success" });
    },
    failure(message = "Login failed") {
      this.$message({ message, type: "error" });
    },
  },
};
</script>

<style scoped>
.login {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.login-button {
  width: 100%;
}
</style>
