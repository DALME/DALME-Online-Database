<template>
  <q-dialog
    v-model="auth.unauthorized"
    persistent
    transition-show="scale"
    transition-hide="scale"
    class="frosted-background login-dialog"
    v-if="pageBackdropLoaded"
  >
    <q-card class="login-modal">
      <q-card-section class="login-card-header">
        <img class="ida-logo-gif" src="~assets/ida_logo_anim.gif" />
      </q-card-section>
      <q-separator />
      <q-card-section class="login-card-body">
        <template v-if="auth.reauthenticate || auth.authenticate">
          <div class="login-card-text">
            <span v-if="auth.reauthenticate">Please re-authenticate</span>
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
              <span v-if="auth.reauthenticate" class="text-grey-7 q-mx-sm">|</span>
              <a v-if="auth.reauthenticate" @click="logout" class="text-link cursor-pointer">
                Log out
              </a>
            </div>
          </q-form>
        </template>
        <AdaptiveSpinner
          v-else
          type="facebook"
          color="indigo-3"
          size="100px"
          :container-height="240"
          :container-width="250"
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { any, isEmpty } from "ramda";
import { computed, defineComponent, inject, ref } from "vue";
import { requests } from "@/api";
import { useAPI, useEventHandling, useStores } from "@/use";
import { useRoute } from "vue-router";
import { AdaptiveSpinner } from "@/components";

export default defineComponent({
  name: "LoginModal",
  components: { AdaptiveSpinner },
  setup() {
    const { auth } = useStores();
    const { notifier } = useEventHandling();
    const $route = useRoute();
    const { apiInterface } = useAPI();
    const { fetchAPI, status } = apiInterface();

    const pageBackdropLoaded = inject("pageBackdropLoaded");

    const username = ref("");
    const password = ref("");
    const isPassword = ref(true);
    const submitting = ref(false);

    const show = computed(() => auth.reauthenticate || auth.authenticate);
    const disabled = computed(() => any(isEmpty)([username.value, password.value]));

    const usernameRules = [(val) => (val && !isEmpty(val)) || "Username is required"];
    const passwordRules = [(val) => (val && !isEmpty(val)) || "Password is required"];

    const logout = () => {
      auth.send({ type: "LOGOUT" });
    };

    const onSubmit = async () => {
      submitting.value = true;
      await fetchAPI(
        requests.auth.login({
          username: username.value,
          password: password.value,
        }),
      );
      if (status.value == 202) {
        auth.send({ type: "LOGIN" });
        if ($route.query.next) {
          username.value = "";
          password.value = "";
          window.location.href = $route.query.next;
        }
      } else {
        notifier.auth.authFailed();
        auth.send({ type: "LOGIN_FAILED" });
      }
      submitting.value = false;
    };

    return {
      auth,
      disabled,
      isPassword,
      logout,
      onSubmit,
      pageBackdropLoaded,
      password,
      passwordRules,
      submitting,
      username,
      usernameRules,
      show,
    };
  },
});
</script>

<style lang="scss">
.login-modal {
  min-width: 400px;
  box-shadow: 0px 0px 20px 3px #212f3a8c;
  margin-top: 10%;
  margin-bottom: auto;
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
.ida-logo-image {
  align-self: center;
  width: 100%;
  filter: drop-shadow(1px 0px 1px white);
  transform: rotate(339deg);
  opacity: 0.5;
  position: relative;
  top: -30px;
}
.ida-logo-gif {
  width: 120%;
  position: absolute;
  top: -30px;
  left: -30px;
}
.login-card-header {
  display: flex;
  flex-direction: column;
  padding: 0;
  min-width: 300px;
  text-align: center;
  height: 200px;
  background-color: #343e72;
  background-image: linear-gradient(22deg, #343e72 34.62%, #151c3e);
  overflow: hidden;
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
  min-height: 266px;
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
.login-dialog .q-dialog__inner {
  align-items: unset;
}
</style>
