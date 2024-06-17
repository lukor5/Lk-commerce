<template>
  <div class="login-popup">
    <div class="form-wrapper">
      <button class="exit-button" @click="closeLoginPopup">
        <font-awesome-icon :icon="['fas', 'x']" />
      </button>
      <h1 v-if="showForm == 'forgot' || showForm == 'recover'">
        Recover password
      </h1>
      <h1 v-else>Log in</h1>
      <form v-if="showForm == 'login'" @submit.prevent="login">
        <div class="login-inputs">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Username"
          />
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Password"
          />
        </div>
        <div class="row">
          <div class="remember-me-wrapper">
            <input type="checkbox" /> <b>Remember me</b>
          </div>
          <button @click.prevent="handleForgotPassword" class="forgot-password">
            Forgot password
          </button>
        </div>
        <button type="submit" ref="signInButton">Sign in</button>
      </form>
      <form v-if="showForm == 'forgot'" @submit.prevent="handleRecoverPassword">
        <div class="login-inputs">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" placeholder="Email" />
          <p>If email exists, recovery code will be mailed to you.</p>
        </div>
        <button @click.prevent="handleRecoverPassword">Recover password</button>
      </form>
      <form v-if="showForm == 'recover'" @submit.prevent="submitRecoveryCode">
        <div class="login-inputs">
          <label for="recoveryCode">Recovery code</label>
          <input
            type="text"
            id="recoveryCode"
            v-model="recoveryCode"
            placeholder="Recovery code"
          />
          <p>Please type in your recovery code.</p>
        </div>
        <button @click.prevent="submitRecoveryCode">Recover password</button>
      </form>
      <form v-if="showForm == 'set-new-password'" @submit.prevent="submitNewPassword">
        <div class="login-inputs">
          <label for="newPassword">New password</label>
          <input
            type="password"
            id="newPassword"
            v-model="newPassword"
            placeholder="New password"
          />
          <label for="newPasswordRepeat">Repeat password</label>
          <input
            type="password"
            id="newPasswordRepeat"
            v-model="newPasswordRepeat"
            placeholder="Repeat new password"
          />
        </div>
        <button @click.prevent="submitNewPassword">Set password</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { mapActions } from "vuex";
export default {
  name: "LoginPopup",
  props: {
    userToLogIn: null,
  },
  data() {
    return {
      username: "",
      password: "",
      baseUrl: this.$baseUrl,
      showForm: "login",
      email: "",
      recoveryCode: "",
      newPassword: "",
      newPasswordRepeat: "",
    };
  },
  methods: {
    ...mapActions(["updateUser"]),
    setTokens(tokens) {
      Cookies.set("JWToken", tokens.token, { path: "/" });
      Cookies.set("CSRFToken", tokens.csrf_token, { path: "/" });
    },
    login() {
      const formData = {
        username: this.username,
        password: this.password,
      };
      axios
        .post(this.baseUrl + "/login", formData)
        .then((response) => {
          const tokens = response.data;
          this.setTokens(tokens);
          if (tokens.superuser !== true) {
            this.mergeBaskets(tokens.user_id, this.$store.state.sessionKey)
              .then(() => {
                this.$emit("result", "Logged in successfully!");

                if (tokens.superuser === true && this.userToLogIn === "Admin") {
                  this.updateUser({
                    id: tokens.user_id,
                    username: this.username,
                    isAdmin: true,
                  });

                  this.$emit("logged-in", "Logged in successfully");
                } else {
                  this.updateUser({
                    id: tokens.user_id,
                    username: this.username,
                    isAdmin: false,
                  });
                  this.$emit("logged-in", "Logged in successfully");
                  this.$router.push("/");
                }
              })
              .catch((error) => {
                console.error("merge error:", error);
              });
          } else {
            if (this.userToLogIn === "Admin") {
              this.updateUser({
                id: tokens.user_id,
                username: this.username,
                isAdmin: true,
              });
              this.$emit("logged-in", "Logged in successfully");
            }
          }
        })
        .catch((error) => {
          console.error("Login error:", error);
          this.$emit(
            "result",
            "Login failed - either user does not exist, or password is incorrect"
          );
        });
    },
    closeLoginPopup() {
      this.$emit("close-popup");
    },
    handleForgotPassword() {
      this.showForm = "forgot";
    },
    handleRecoverPassword() {
      const data = {
        email: this.email,
      };
      axios
        .post(this.baseUrl + "/send-recovery-code", data)
        .then((response) => {
          if (response.status == 200) {
            this.showForm = "recover";
          }
        })
        .catch((error) => {
          console.log("error", error);
          this.$emit("result", "Email not found");
        });
    },
    submitRecoveryCode() {
      const data = {
        recovery_code: this.recoveryCode,
        email: this.email,
      };
      axios
        .post(this.baseUrl + "/recover-password", data)
        .then((response) => {
          if (response.status == 200) {
            this.showForm = "set-new-password";
          }
        })
        .catch((error) => {
          this.$emit("result", "Recovery code invalid");
          console.log("error", error);
        });
    },
    submitNewPassword() {
      const data = {
        new_password: this.newPassword,
        email: this.email,
      };
      axios
        .post(this.baseUrl + "/set-password", data)
        .then((response) => {
          if (response.status == 200) {
            this.$emit("result", "Password set succesfully");
            this.showForm = "login";
          }
        })
        .catch((error) => {
          console.log("error", error);
          this.$emit("result", "Error setting new password");
        });
    },
    handleKeyDown(event) {
      if (event.key === "Enter") {
        event.preventDefault(); 
        if (this.showForm === "login") {
          this.login();
        } else if (this.showForm === "forgot") {
          this.handleRecoverPassword();
        } else if (this.showForm === "recover") {
          this.submitRecoveryCode();
        } else if (this.showForm === "set-new-password") {
          this.submitNewPassword();
        }
      }
    },
    mergeBaskets(id, sessionKey) {
      return new Promise((resolve, reject) => {
        const formData = {
          user_id: id,
          session_key: sessionKey,
        };
        axios
          .post(this.baseUrl + "/merge-baskets", formData)
          .then(() => {
            resolve();
          })
          .catch((error) => {
            console.error("merge error:", error);
            reject(error);
          });
      });
    },
  },
  mounted() {
    document.addEventListener("keydown", this.handleKeyDown);
  },
};
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";

.login-popup {
  position: absolute;
  display: flex;
  width: 100%;
  height: 100vh;
  justify-content: center;
  align-items: center;
  z-index: 9999;

  .form-wrapper {
    background-color: var(--background-color);
    border-radius: 5px;
    position: relative;
    padding: 20px;

    .exit-button {
      position: absolute;
      top: 10px;
      right: 10px;
    }

    form {
      display: flex;
      flex-direction: column;
      min-height: 30vh;
      min-width: 20vw;
      justify-content: space-around;
      .row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        .remember-me-wrapper {
          display: flex;
          flex-direction: row;
          align-items: center;
          gap: 10px;
          text-align: left;
        }
      }

      .login-inputs {
        display: flex;
        flex-direction: column;

        p {
          @include small-text;
        }

        input {
          padding: 5px;
          margin-inline: 20px;
          margin-top: 5px;
          margin-bottom: 5px;
          border: none;
          border-bottom: 1px solid lightgray;
        }
      }

      label {
        text-align: left;
        font-size: 0.8em;
      }

      button {
        @include secondary-button;
        padding: 10px;
        border-radius: 10px;
      }
    }
  }
}
</style>