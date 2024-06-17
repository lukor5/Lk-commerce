<template>
  <div class="register-form-wrapper">
    <form @submit.prevent="submitForm">
      <div class="input-wrapper">
        <span v-if="!isUsernameValid && username !== ''" class="invalid-icon"
          >!</span
        >
        <span v-if="isUsernameValid && username !== ''" class="valid-icon"
          >✓</span
        >
        <div class="input-title-wrapper">
          <b>Username</b>
          <div class="input-row">
            <span
              v-if="!isUsernameValid && username !== ''"
              class="invalid-icon"
              >!</span
            >
            <span v-if="isUsernameValid && username !== ''" class="valid-icon"
              >✓</span
            >
            <input
              type="text"
              v-model="username"
              placeholder="Username"
              minlength="5"
              maxlength="15"
              :class="{ invalid: !isUsernameValid }"
            />
          </div>
        </div>
      </div>
      <div class="input-wrapper">
        <div class="input-title-wrapper">
          <b>Password</b>
          <div class="input-row">
            <span
              v-if="!isPasswordValid && password !== ''"
              class="invalid-icon"
              >!</span
            >
            <span
              v-if="!isPasswordMatch && repeatPassword !== ''"
              class="invalid-icon"
              >!</span
            >
            <span
              v-if="
                isPasswordMatch &&
                repeatPassword !== '' &&
                isPasswordValid &&
                password !== ''
              "
              class="valid-icon"
              >✓</span
            >
            <input
              type="password"
              v-model="password"
              placeholder="Password"
              min-length="7"
              max-length="20"
              :class="{ invalid: !isPasswordValid }"
            />
            <input
              type="password"
              v-model="repeatPassword"
              placeholder="Repeat your password..."
              :class="{ invalid: !isPasswordMatch }"
            />
          </div>
        </div>
      </div>
      <div class="input-wrapper">
        <div class="input-title-wrapper">
          <b>Your name</b>
          <div class="input-row">
            <span
              v-if="!isFirstNameValid && firstName !== ''"
              class="invalid-icon"
              >!</span
            >
            <span
              v-if="!isLastNameValid && lastName !== ''"
              class="invalid-icon"
              >!</span
            >
            <span
              v-if="
                isFirstNameValid &&
                firstName !== '' &&
                isLastNameValid &&
                lastName !== ''
              "
              class="valid-icon"
              >✓</span
            >
            <input
              type="text"
              v-model="firstName"
              placeholder="First name"
              minlength="1"
              max-length="20"
              :class="{ invalid: !isFirstNameValid }"
            />

            <input
              type="text"
              v-model="lastName"
              placeholder="Last name"
              minlength="1"
              max-length="20"
              :class="{ invalid: !isLastNameValid }"
            />
          </div>
        </div>
      </div>
      <div class="input-wrapper">
        <div class="input-title-wrapper">
          <b>Email</b>
          <div class="input-row">
            <span v-if="!isEmailValid && email !== ''" class="invalid-icon"
              >!</span
            >
            <span v-if="isEmailValid && email !== ''" class="valid-icon"
              >✓</span
            >
            <input
              type="email"
              v-model="email"
              placeholder="Email"
              :class="{ invalid: !isEmailValid }"
            />
          </div>
        </div>
      </div>
      <button class="register-button">Register</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { mapState, mapActions } from "vuex";

export default {
  name: "RegisterForm",
  data() {
    return {
      username: "",
      password: "",
      repeatPassword: "",
      firstName: "",
      lastName: "",
      email: "",
      baseUrl: this.$baseUrl,
    };
  },
  computed: {
    ...mapState(["user_id", "username"]),
    userId() {
      return this.user.id;
    },
    isUsernameValid() {
      return this.username.length >= 5 && this.username.length <= 15;
    },
    isPasswordValid() {
      return this.password.length >= 7 && this.password.length <= 20;
    },
    isPasswordMatch() {
      return this.password === this.repeatPassword;
    },
    isFirstNameValid() {
      return this.firstName.length > 0 && this.firstName.length <= 20;
    },
    isLastNameValid() {
      return this.lastName.length > 0 && this.lastName.length <= 20;
    },
    isEmailValid() {
      // Simple email validation, can be improved based on requirements
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(this.email);
    },
  },
  methods: {
    ...mapActions(["updateUser"]),
    submitForm() {
      if (
        this.isUsernameValid &&
        this.isPasswordValid &&
        this.isPasswordMatch &&
        this.isFirstNameValid &&
        this.isLastNameValid &&
        this.isEmailValid
      ) {
        const formData = {
          username: this.username,
          password: this.password,
          email: this.email,
          first_name: this.firstName,
          last_name: this.lastName,
        };
        axios
          .post(this.baseUrl + "/register", formData)
          .then(() => {
            this.$emit("result", "Registration succesful!");
            this.login();
          })
          .catch((error) => {
            const errorMessage = error.response.data.error;
            if (errorMessage === "Email already exists.") {
              this.$emit(
                "result",
                "Registration failed. Email already exists."
              );
            } else if (errorMessage === "Username already exists.") {
              this.$emit(
                "result",
                "Registration failed. Username already exists."
              );
            } else {
              this.$emit(
                "result",
                "Registration failed. Please check for mistakes."
              );
            }
          });
      } else {
        this.$emit("result", "Register form invalid");
      }
    },
    login() {
      const data = {
        username: this.username,
        password: this.password,
      };
      axios
        .post(this.baseUrl + "/login", data)
        .then((response) => {
          const tokens = response.data;
          this.updateUser({ id: tokens.user_id, username: this.username });
          this.mergeBaskets(tokens.user_id, this.$store.state.sessionKey);
          this.$emit("logged-in");
          this.$router.push("/");
        })
        .catch((error) => {
          console.error("login error:", error);
        });
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
};
</script>

<style lang=scss scoped>
@import "../assets/styles/main.scss";

.register-form-wrapper {
  display: flex;
  height: 100vh;
  flex-direction: column;
  align-items: center;
  text-align: left;
  padding: 50px;

  form {
    .input-wrapper {
      display: flex;
      flex-direction: column;

      justify-content: center;

      .input-title-wrapper {
        display: flex;
        flex-direction: column;
      }

      .input-row {
        display: flex;
        position: relative;
        flex-direction: row;
        align-items: center;
      }
    }

    input {
      margin: 10px;
      border: none;
      border-bottom: 1px solid lightgray;
      padding: 10px;
      width: 100%;
    }

    .invalid-icon {
      position: absolute;
      top: 50%;
      left: -20px;
      transform: translateY(-50%);
      color: red;
      font-weight: bold;
    }

    .valid-icon {
      position: absolute;
      top: 50%;
      left: -20px;
      transform: translateY(-50%);
      color: green;
      font-weight: bold;
    }

    input:invalid {
      border-bottom: 1px solid red;
    }

    input:valid {
    }
  }

  .register-button {
    width: 100%;
    height: 40px;
    border: 2px solid var(--secondary-color);
    background-color: var(--background-color);
    border-radius: 10px;
  }

  .register-button:hover {
    @include secondary-button;
    font-weight: bold;
    cursor: pointer;
  }
}
</style>