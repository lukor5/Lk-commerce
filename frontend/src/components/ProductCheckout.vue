<template>
  <div>
    <div class="products-container">
      <div class="rows">
        <h2 class="heading">Products</h2>
        <div class="labels">
          <label>Name</label>
          <label>Size</label>
          <label>Color</label>
          <label>Quantity</label>
        </div>
        <div
          v-for="(basketItem, index) in basket.basketItems"
          :key="index"
          class="product"
        >
          <b>{{ basketItem.product.name }}</b>
          <p>{{ basketItem.variant.size }}</p>
          <p>{{ basketItem.variant.color }}</p>
          <p>x{{ basketItem.quantity }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "ProductCheckout",
  computed: {
    ...mapGetters(["user", "basket"]),
  },
  props: {
    basketContent: Object,
  },
  data() {},
  mounted() {},
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.products-container {
  display: grid;
  text-align: left;
  .rows {
    display: grid;
    grid-template-rows: auto repeat;
    .heading {
      text-align: center;
    }
    .labels {
      display: grid;
      gap: 10px;
      grid-template-columns: 2fr 1fr 1fr 1fr;
      @include small-text;
    }
    .product {
      display: grid;
      gap: 10px;
      grid-template-columns: 2fr 1fr 1fr 1fr;
    }
  }
}
</style>