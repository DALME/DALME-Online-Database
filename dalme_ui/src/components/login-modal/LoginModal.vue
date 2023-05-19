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
      </q-card-section>
      <q-separator />
      <q-card-section class="login-card-body">
        <div class="login-card-text">
          <span v-if="reAuthenticate">Please re-authenticate</span>
          <span v-else>Please log in</span>
        </div>
        <q-form @submit="onSubmit" class="q-gutter-sm">
          <q-input
            placeholder="Username"
            v-model="username"
            dense
            outlined
            color="indigo-6"
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
            placeholder="Password"
            dense
            outlined
            color="indigo-6"
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

          <div class="row justify-center q-mt-sm q-pt-md">
            <q-btn
              unelevated
              no-caps
              label="Log in"
              type="submit"
              class="login-modal-button"
              color="indigo-6"
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
          <div class="row justify-center text-indigo-6 login-modal-link">
            <a href="" class="text-link">Recover password</a>
            <span v-if="reAuthenticate" class="text-grey-7 q-mx-sm">|</span>
            <a
              v-if="reAuthenticate"
              @click="logout"
              class="text-link cursor-pointer"
            >
              Log out
            </a>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { any, isEmpty } from "ramda";
import { computed, defineComponent, inject, ref } from "vue";
import { authSchema, preferenceSchema } from "@/schemas";
import { requests, publicUrl } from "@/api";
import { useAPI, useEventHandling, useStores } from "@/use";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "LoginModal",
  setup() {
    const { auth, prefs, reAuthenticate } = useStores();
    const { notifier } = useEventHandling();
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { data, fetchAPI, success } = apiInterface();
    const { showLogin, updateShowLogin } = inject("showLogin");
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

    const logout = () => {
      prefSubscription();
      auth.logout();
    };

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
            auth.login(value.user).then(async () => {
              await fetchAPI(requests.users.getUserPreferences(auth.userId));
              if (success.value) {
                await preferenceSchema
                  .validate(data.value, { stripUnknown: false })
                  .then(async (value) => {
                    await prefs.loadPreferences(value);
                    prefSubscription("subscribe");
                  });
              } else {
                notifier.users.prefRetrievalFailed();
              }
              updateShowLogin(false);
              if ($route.query.next) {
                window.location.href = `${publicUrl}${$route.query.next}`;
              }
            });
          });
      } else {
        notifier.auth.authFailed();
        submitting.value = false;
      }
    };

    return {
      disabled,
      isPassword,
      logout,
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

<style lang="scss">
.login-modal {
  min-width: 400px;
}
.dalme-logo-image {
  align-self: center;
  width: 16rem;
  filter: grayscale(1) invert(1);
  transform: rotate(-35deg);
  opacity: 0.4;
  position: relative;
  top: -10%;
}
.login-card-header {
  display: flex;
  flex-direction: column;
  padding: 0;
  min-width: 300px;
  text-align: center;
  height: 200px;
  background-color: #343e72;
  background-image: linear-gradient(59deg, #343e72 54.62%, #1b1b1b);
}
.login-card-logo {
  align-self: center;
  margin-top: auto;
  margin-bottom: auto;
}
.login-card-text {
  font-size: 16px;
  font-weight: 300;
  text-align: center;
  padding-top: 20px;
  padding-bottom: 20px;
}
.login-card-body {
  background-color: #fcfcfc;
  padding: 0px 60px 20px;
}
.login-card-body .text-negative {
  color: #c3747c !important;
}
.login-card-body .q-field--error .q-field__bottom {
  color: #9a4f57 !important;
  margin-bottom: 0;
}
.login-card-body .q-field__bottom {
  padding: 6px 12px 0;
  display: none;
}
.login-card-body .q-field__marginal {
  font-size: 18px;
}
.login-modal-link {
  font-size: 12px;
  margin-top: 10px;
  margin-bottom: 10px;
}
.login-modal-button {
  font-weight: 400;
  padding: 4px 4rem !important;
}
.frosted-background > .q-dialog__backdrop {
  backdrop-filter: blur(5px) grayscale(70%);
}
</style>
