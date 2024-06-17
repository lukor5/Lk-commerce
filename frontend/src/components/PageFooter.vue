<template>
  <div class="footer-wrapper">
    <SocialMediaLinks />
    <div class="columns">
      <div class="row">
        <h2>Lk Commerce</h2>
        <a href="">About us</a>
        <a href="">Our values</a>
        <a href="">Meet the Team</a>
        <a href="">Career</a>
        <a href="">Contact us</a>
        <a href="">Privacy policy</a>
      </div>
      <div class="row-break"></div>
      <div class="row">
        <h2>Help</h2>
        <a href="">FAQ</a>
        <a href="">Help center</a>
        <a href="">Order tracking</a>
        <a href="">Shipping information</a>
        <a href="">Return policy</a>
        <a href="">Troubleshooting guides</a>
      </div>
    </div>
  </div>
  <div class="developer-footer">
    <h3>@Łukasz Oleś</h3>
    <div class="links">
      <a href="https://www.linkedin.com/in/lukor5/"
        ><img src="../assets/icons/linkedin.png"
      /></a>
      <a href="https://www.github.com/lukor5"
        ><img src="../assets/icons/github.png"
      /></a>
      <a href="">Portfolio</a>
    </div>
  </div>
</template>
<script>
import SocialMediaLinks from "./SocialMediaLinks.vue";
export default {
  name: "PageFooter",
  components: {
    SocialMediaLinks,
  },
  data() {},
};
</script>

<style lang="scss">
@import "../assets/styles/main.scss";

.footer-wrapper {
  z-index: 1;
  display: flex;
  flex-direction: column;
  font-family: $secondary-font-stack;
  justify-content: center;

  background-color: var(--secondary-color);
  color: white;

  .columns {
    display: grid;
    grid-template-columns: auto 1px auto;
    grid-gap: 100px;
    justify-content: center;
    .row {
      text-align: left;
      display: grid;
      grid-template-rows: 1fr repeat;
      a {
        text-decoration: none;
        padding: 5px;
        color: white;
        border-bottom: 1px solid rgba(255, 255, 255, 0.5);
      }
    }
    .row-break {
      width: 1px;
      background-color: white;
    }
  }
}

.developer-footer {
  display: flex;
  flex-direction: row;
  justify-content: center;
  height: auto;
  align-items: center;
  width: 100%;
  background-color: var(--dark-color);
  margin-top: 20px;
  padding: 25px;
  padding-left: 0px;

  .links {
    position: absolute;
    right: 20vw;
    display: flex;
    align-items: center;
    a {
      text-decoration: underline;
      color: rgba(255, 255, 255, 0.8);
    }
    img {
      transform: scale(0.5);
    }
  }
}

@media (max-width: 800px) {
  .developer-footer .links {
    right: 5px;
  }
}
</style>