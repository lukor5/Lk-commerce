<template>
  <div class="result-wrapper">
    <div
      v-if="this.messages"
      class="result-popup"
      @animationend="emitAnimationEnded"
    >
      <h2 v-for="(message, index) in this.messages" :key="index">
        {{ message }}
      </h2>
    </div>
    <div v-else class="result-popup" @animationend="emitAnimationEnded">
      <h2>{{ message }}</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "ResultPopup",
  props: {
    messages: Array,
    message: String,
  },
  methods: {
    emitAnimationEnded() {
      this.$emit("animation-ended");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.result-wrapper {
  width: 100vw;
  display: flex;
  justify-content: center;
}
.result-popup {
  position: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  width: auto;
  padding: 10px;
  height: auto;
  margin-inline: auto;
  top: -300px;
  z-index: 9999;
  animation: move 4s;
  backdrop-filter: blur(5px);
  background-color: var(--secondary-color);
  opacity: 0.9;
  color: white;
}

@keyframes move {
  0% {
    top: -300px;
  }
  25% {
    top: 0px;
  }
  50% {
    top: 0px;
  }
  75% {
    top: 0px;
  }
  100% {
    top: -300px;
  }
}
</style>