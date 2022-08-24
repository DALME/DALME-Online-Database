<template>
  <q-dialog
    v-model="showLogin"
    persistent
    transition-show="scale"
    transition-hide="scale"
    class="frosted-background"
  >
    <q-card class="login-modal">
      <q-card-section class="login-card-header">
        <img class="dalme-logo-image" src="~assets/dalme_logo.svg" />
        <div v-if="reAuthenticate">Please re-authenticate.</div>
      </q-card-section>

      <q-separator />

      <q-card-section class="login-card-body">
        <q-form @submit="onSubmit" class="q-gutter-sm">
          <q-input
            label="Username"
            v-model="username"
            outlined
            bg-color="white"
            hide-bottom-space
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            lazy-rules
            :rules="usernameRules"
          />

          <q-input
            v-model="password"
            label="Password"
            outlined
            bg-color="white"
            lazy-rules
            hide-bottom-space
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            :type="isPassword ? 'password' : 'text'"
            :rules="passwordRules"
          >
            <template v-slot:append>
              <q-icon
                class="cursor-pointer"
                :name="isPassword ? 'visibility_off' : 'visibility'"
                @click.stop="isPassword = !isPassword"
              />
            </template>
          </q-input>

          <div class="row justify-center q-mt-lg q-pt-md">
            <q-btn
              align="between"
              label="Login"
              type="submit"
              color="primary"
              padding="sm 5rem"
              preventClose="true"
              :disable="disabled"
              :loading="submitting"
            >
              <template v-slot:loading>
                <q-spinner-facebook />
              </template>
            </q-btn>
          </div>
          <div class="row justify-center">
            <q-btn
              label="Forgot your password?"
              flat
              no-caps
              type="a"
              color="primary"
            >
            </q-btn>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { any, isEmpty } from "ramda";
import { computed, defineComponent, inject, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { usePrefStore } from "@/stores/preferences";

import { authSchema, preferenceSchema } from "@/schemas";

import { requests, publicUrl } from "@/api";
import { useAPI, useNotifier } from "@/use";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "LoginModal",
  setup() {
    const $authStore = useAuthStore();
    const $prefStore = usePrefStore();
    const $notifier = useNotifier();
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { data, fetchAPI, success } = apiInterface();
    const { showLogin, updateShowLogin } = inject("showLogin");
    const reAuthenticate = inject("reAuthenticate");
    const prefSubscription = inject("prefSubscription");
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

    const onSubmit = async () => {
      submitting.value = true;
      await fetchAPI(
        requests.auth.login({
          username: username.value,
          password: password.value,
        }),
      );
      if (success.value) {
        await authSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            $authStore.login(value.user).then(async () => {
              await fetchAPI(
                requests.users.getUserPreferences($authStore.userId),
              );
              if (success.value) {
                await preferenceSchema
                  .validate(data.value, { stripUnknown: true })
                  .then(async (value) => {
                    await $prefStore.loadPreferences(value);
                    prefSubscription("subscribe");
                  });
              } else {
                $notifier.users.prefRetrievalFailed();
              }
              updateShowLogin(false);
              if ($route.query.next) {
                window.location.href = `${publicUrl}${$route.query.next}`;
              }
            });
          });
      } else {
        $notifier.auth.authFailed();
        submitting.value = false;
      }
    };

    return {
      disabled,
      isPassword,
      onSubmit,
      password,
      passwordRules,
      reAuthenticate,
      showLogin,
      submitting,
      username,
      usernameRules,
    };
  },
});
</script>

<style scoped lang="scss">
.login-modal {
  min-width: 400px;
}
.dalme-logo-image {
  width: 7.5rem;
}
.login-card-header {
  padding: 50px 25px 40px 25px;
  background-color: #f5f5f5;
  min-width: 300px;
  text-align: center;
}
.login-card-body {
  background-color: #fcfcfc;
  padding: 25px 40px;
}
</style>
