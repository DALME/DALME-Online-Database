<template>
  <q-dialog
    v-model="persistent"
    persistent
    transition-show="scale"
    transition-hide="scale"
  >
    <div class="auth-modal q-pa-md q-ma-md">
      <img class="dalme-logo" src="~assets/dalme_logo.svg" />
      <q-form @submit="onSubmit" class="q-gutter-md">
        <q-input
          label="Username *"
          v-model="username"
          filled
          lazy-rules
          :rules="usernameRules"
        />

        <q-input
          v-model="password"
          label="Password *"
          filled
          lazy-rules
          :type="isPassword ? 'password' : 'text'"
          :rules="passwordRules"
        >
          <template v-slot:append>
            <q-icon
              class="cursor-pointer"
              :name="isPassword ? 'visibility_off' : 'visibility'"
              @click="isPassword = !isPassword"
            />
          </template>
        </q-input>

        <div class="row justify-end">
          <q-btn
            align="between"
            label="Submit"
            type="submit"
            color="primary"
            :disable="disabled"
            :loading="submitting"
          >
            <template v-slot:loading>
              <q-spinner-facebook />
            </template>
          </q-btn>
        </div>
      </q-form>
    </div>
  </q-dialog>
</template>

<script>
import { any, isEmpty } from "ramda";
import { computed, defineComponent, ref, watch } from "vue";
import { useStore } from "vuex";

import { requests } from "@/api";
import notifier from "@/notifier";
import { sessionSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "LoginModal",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  setup(props, context) {
    const $store = useStore();
    const { data, fetchAPI, status } = useAPI(context);

    const showModal = ref(false);
    const username = ref("");
    const password = ref("");
    const isPassword = ref(true);
    const submitting = ref(false);
    const disabled = computed(() =>
      any(isEmpty)([username.value, password.value]),
    );

    const usernameRules = [
      (val) => (val && !isEmpty(val)) || "Username is required",
    ];
    const passwordRules = [
      (val) => (val && !isEmpty(val)) || "Password is required",
    ];

    const validateSession = async () => {
      await sessionSchema.validate(data.value).then((value) => {
        notifier.auth.reauthenticated();
        $store.dispatch("auth/login", value);
      });
    };

    const reset = () => {
      username.value = "";
      password.value = "";
    };

    const onSubmit = async () => {
      submitting.value = true;
      setTimeout(async () => {
        await fetchAPI(
          requests.auth.login({
            username: username.value,
            password: password.value,
          }),
        );
        status.value === 200 ? validateSession() : notifier.auth.authFailed();
        submitting.value = false;
        reset();
      }, 500);
    };

    watch(
      () => props.show,
      (show) => {
        showModal.value = show;
      },
    );

    return {
      disabled,
      isPassword,
      onSubmit,
      password,
      passwordRules,
      persistent: showModal,
      submitting,
      username,
      usernameRules,
    };
  },
});
</script>

<style scoped lang="scss">
.auth-modal {
  align-items: center;
  background: white;
  display: flex;
  flex-direction: column;
}
.dalme-logo {
  margin: 2rem 5rem;
  width: 7.5rem;
}
</style>
