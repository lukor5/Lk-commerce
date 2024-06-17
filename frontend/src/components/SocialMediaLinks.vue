<template>
  <div class="links-container">
    <div class="links">
      <img src="../assets/icons/facebook.png" />
      <img src="../assets/icons/instagram.png" />
      <img src="../assets/icons/tiktok.png" />
      <img src="../assets/icons/twitter.png" />
      <img src="../assets/icons/linkedin.png" />
    </div>
  </div>
</template>

<script>
export default {
  name: "SocialMediaLinks",
  data() {},
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.links-container {
  display: flex;
  flex: 0;
  justify-content: right;
  .links {
    display: flex;
    margin-right: 10vw;
    flex-direction: row;
    border-bottom-right-radius: 25px;
    border-top-left-radius: 25px;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 5px;
    img {
      transform: scale(0.6);
      transition: transform 0.3s;
      cursor: pointer;
    }
    img:hover {
      transform: scale(0.7);
    }
  }
}
</style>