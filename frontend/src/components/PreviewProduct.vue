<template>
  <div
    class="single-product"
    :class="{ 'hover-effect': isHover, moveTransition: toMove }"
    @mouseover="toggleHover(true)"
    @mouseleave="toggleHover(false)"
    @click="handleProductClick"
  >
    <img class="product-image" :src="baseMediaUrl + product.product_image" />
    <div class="product-bottom">
      <div class="details-top">
        <h2>{{ product.name }}</h2>
        <div class="ratings-wrapper">
          <font-awesome-icon style="color: gold" :icon="['fas', 'star']" />

          <b>{{ this.product.total_rating }}</b>
        </div>
      </div>
      <div class="details-bottom">
        <div class="price-wrapper">
          <span v-if="hasDiscount">
            <span style="text-decoration: line-through">{{
              product.price + "$"
            }}</span
            >*</span
          >
          <span style="font-weight: bold">{{ priceAfterDiscount }}</span>
        </div>
      </div>
      <div class="small-text">
        <p>*Price before discount: {{ product.price + "$" }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PreviewProduct",
  props: {
    product: {
      type: Object,
      required: true,
    },
    index: null,
    direction: null,
  },
  data() {
    return {
      variants: [],
      baseMediaUrl: this.$baseMediaUrl,
      isHover: false,
      toMove: false,
      currentIndex: null,
    };
  },
  methods: {
    toggleHover(value) {
      this.isHover = value;
    },
    handleProductClick() {
      this.$emit("product-clicked", this.product);
    },
  },
  computed: {
    priceAfterDiscount() {
      return (
        (
          Math.round(this.product.price * this.product.discount * 100) / 100
        ).toFixed(2) + "$"
      );
    },
    sortedVariants() {
      let sortedVariants = this.product.product_variants;
      if (this.product) {
        sortedVariants.sort((a, b) => {
          return a.size.localeCompare(b.size);
        });
      }
      return sortedVariants;
    },
    hasDiscount() {
      return this.product.discount != 1
    }
  },
  mounted() {},
  watch: {
    index(newIndex) {
      this.currentIndex = newIndex; // Update currentIndex data property if needed
    },

    direction(newValue) {
      if (
        (newValue === "left" && this.index === 2) ||
        (newValue === "right" && this.index === 0)
      ) {
        this.toMove = true;
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";
.single-product {
  display: flex;
  flex-direction: column;
  position: relative;
  justify-content: space-between;

  width: 200px;

  height: 350px;

  padding: 20px;
 

  cursor: pointer;
  background-color: var(--background-color);
  transition: opacity 1s, transform 0.5s;
  &.hover-effect {
    transform: scale(1.1);
  }
  &.moveTransition {
    opacity: 0;
    transform: scale(0);
  }

  .product-image {
    width: 100%;
   height: auto;
   object-fit: cover;
    border-radius: 15px;
  }

  .product-bottom {
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .details-top {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      white-space: nowrap;
      align-items: center;
    }

    .details-bottom {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 0px;

      .sizes {
        display: flex;
        flex-direction: row;
        gap: 10px;
      }
      .price-wrapper {
        display: flex;
        gap: 10px;
      }
    }
    .small-text {
      @include small-text;
    }
  }
}

@media (max-width: 600px) {
  .single-product {
    
  }
}
</style>