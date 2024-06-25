<template>
  <ul class="quick-access-list">
    <li @click="redirectToCategories('Men')">Men</li>
    <li @click="redirectToCategories('Women')">Women</li>
    <li @click="redirectToCategories('Kids')">Kids</li>
    <li @click="scrollToPromotions()">Promotions</li>
    <li @click="redirectToCategories('New')">New</li>
  </ul>
</template>

<script>
export default {
  name: "QuickList",
  data() {},
  methods: {
    redirectToCategories(category) {
      this.$router.push({
        name: "productList",
        params: {
          category: category,
          type: "All",
        },
      });
    },
    scrollToPromotions() {
      this.$emit('scroll-to-promotions')
    }
  },
  mounted() {
    this.$emit('quick-access-height', this.$el.clientHeight);
  }
};
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";

.quick-access-list {
  display: flex;
  list-style: none;
  justify-content: space-around;
  margin-inline: 30px;
  padding: 10px;

  li {
    text-transform: uppercase;
    color: gray;
    font-family: $secondary-font-stack;
    border-bottom: 1px solid transparent;
    padding-bottom: 2px;
    position: relative;
    cursor: pointer;
    transition: 0.3s ease;
  }

  li::before {
    content: "";
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 100%;
    height: 1px;
    background-color: gray;
    transform: scaleX(0);
    transition: transform 0.3s ease;
    box-shadow: 0px 2px 2px rgba(var(--shadow-color-rgb), var(--shadow-opacity));
  }

  li:hover::before {
    transform: scaleX(1);
  }

  li:hover {
    color: var(--text-color);
  }
}
</style>