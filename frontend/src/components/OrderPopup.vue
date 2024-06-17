<template>
  <div class="order-popup">
    <div class="popup-details">
      <h1>You are not logged in.</h1>
      <h2>Would you like to register?</h2>
      <div class="popup-buttons">
        <button @click="handleRedirect('Register')">Register</button>
        <button @click="handleRedirect('WithoutRegister')">
          No, thank you
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "OrderPopup",
  data() {},
  methods: {
    handleRedirect(option) {
      switch (option) {
        case "Register":
          this.$router.push({ name: "registerForm" });
          break;

        case "WithoutRegister":
          this.$router.push({ name: "orderForm" });
          break;
      }
      this.$emit("redirected");
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.order-popup {
  position: absolute;
  display: flex;
  width: 100%;
  height: 100vh;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  .popup-details {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 40vh;
    justify-content: space-around;
    background-color: var(--background-color);
    padding: 10px;
    border-radius: 10px;
    .popup-buttons {
      display: flex;
      flex-direction: row;
      justify-content: space-around;
      button {
        @include secondary-button;
        width: 40%;
        padding: 10px;
        border-radius: 10px;
      }
    }
  }
}
</style>