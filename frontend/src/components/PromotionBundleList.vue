<template>
  <div class="promotions-wrapper">
    <div class="promotion-button-wrapper">
      <div
        v-if="promotion"
        class="promo"
      >
        <div class="promo-products-wrapper" :class="{ 'fade-out': fadeOut, 'fade-in': fadeIn }">
          <PreviewProduct
            @product-clicked="handleProductClicked"
            :product="promotion.primary_product"
          />
          <PreviewProduct
            @product-clicked="handleProductClicked"
            class="secondary-product"
            :product="promotion.discounted_product"
          />
        </div>
        <font-awesome-icon :icon="['fas', 'right-long']" class="fa-xl" />
        <div class="details-button-wrapper"  :class="{ 'fade-out': fadeOut, 'fade-in': fadeIn }">
          <div class="promo-details">
            <p>
              <b>Normal price: {{ getPromoBeforeDiscount(promotion) }}</b>
            </p>
            <p>
              <b>In bundle: {{ getPromoAfterDiscount(promotion) }}</b>
            </p>
            <h3>
              You save <span>{{ promotion.discount }} $ </span>
            </h3>
          </div>
          <button @click="handleAddBundleClicked(promotion)">
            Add to basket
          </button>
        </div>
        <button class="next-button" @click="handleNextPromotion"><font-awesome-icon :icon="['fas', 'chevron-right']" /></button>
      </div>
 
    

    </div>
    <div class="big-text">
      <h1>Promotions zone</h1>
      <h2>Save yourself some money</h2>
      <h2>By buying one of our bundles</h2>
      <span>*All bundles are limited to one per order</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PreviewProduct from "./PreviewProduct.vue";
import { setTimeout } from "core-js";
export default {
  name: "PromotionBundleList",
  components: {
    PreviewProduct,
  },
  computed: {
    promotionListLength() {
      return this.promotionsList.length;
    },
  },
  data() {
    return {
      promotionsList: [],
      promotion: null,
      baseUrl: this.$baseUrl,
      index: 0,
      fadeIn: false,
      fadeOut: false,
    };
  },
  methods: {
    getPromotions() {
      axios
        .get(`${this.baseUrl}/product-promotions`)
        .then((response) => {
          this.promotionsList = response.data;
          this.promotion = this.promotionsList[0];
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    getPromoBeforeDiscount(promo) {
      let primaryPrice =
        Math.round(
          promo.primary_product.price * promo.primary_product.discount * 100
        ) / 100;
      let secondaryPrice =
        Math.round(
          promo.discounted_product.price *
            promo.discounted_product.discount *
            100
        ) / 100;

      return (primaryPrice + secondaryPrice).toFixed(2);
    },
    getPromoAfterDiscount(promo) {
      let beforeDiscount = this.getPromoBeforeDiscount(promo);
      return (beforeDiscount - promo.discount).toFixed(2);
    },
    handleAddBundleClicked(promo) {
      this.$emit("add-bundle", promo);
    },
    handleNextPromotion() {
      if (this.index + 1 == this.promotionListLength) {
        this.index = 0;
      } else {
        this.index += 1;
      }
      this.fadeIn = false;
      this.fadeOut = true;
      setTimeout(() => {
        this.promotion = this.promotionsList[this.index];
        this.fadeOut = false;
        this.fadeIn = true;
      }, 500);
    },
  },
  mounted() {
    this.getPromotions();
  },
};
</script>

<style lang="scss">
@import "../assets/styles/main.scss";
.promotions-wrapper {
  display: flex;
  background: var(--promotion-color);
  z-index: 2;
  justify-content: center;
  align-items: center;
  padding: 50px;
  border-top-right-radius: 300px;
  border-bottom-right-radius: 150px;
  gap: 10px;

  .promotion-button-wrapper {
    display: flex;
    flex-direction: row;
    gap: 10px;

    .promo {
      display: flex;
      position: relative;
      flex-direction: row;
      align-items: center;
      height: min-content;
      width: 700px;
      border-radius: 15px;
      padding: 15px;
      background: var(--background-color);
      box-shadow: 4px 4px 4px 2px
        rgba(var(--shadow-color-rgb), var(--shadow-opacity));
      gap: 10px;
      
      .promo-products-wrapper {
        transition: opacity 0.5s ease;
        display: flex;
        flex-direction: row;
        align-items: center;
        border: 2px solid var(--secondary-color);
        border-radius: 15px;
        width: min-content;
        height: min-content;
        padding: 17px;

        .secondary-product {
          transform: scale(0.7);
        }
      }

      .details-button-wrapper {
        transition: opacity 0.5s ease;
        display: flex;
        flex-direction: column;
        gap: 20px;

        .promo-details {
          text-align: left;
          color: var(--text-color);
          padding: 15px;
          border-radius: 15px;
        }

        button {
          bottom: 0px;
          @include secondary-button;
          padding: 10px;
          border-radius: 5px;
        }

        button:hover {
          border: 1px solid var(--secondary-color);
          background-color: var(--background-color);
          color: var(--text-color);
        }
      }
    }

    .next-button {
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: center;
      right: -15px;
      border: 2px solid var(--background-color);
      background-color: var(--subtle-border-color);
      width: 30px;
      height: 30px;
      border-radius: 5px;
      transition: none;
    }

    .next-button:hover {
      color: var(--secondary-color);
    }
  }

  .fade-out {
    opacity: 0;
  }

  .fade-in {
    opacity: 1;
  }

  .big-text {
    margin-left: 25px;
    text-align: left;

    h1 {
      color: var(--primary-color);
      font-size: 3em;
    }

    span {
      @include small-text;
    }
  }
}

@media (max-width: 1200px) {
  .promotions-wrapper {
    flex-direction: column-reverse;

    .promotion-button-wrapper {
      .promo {
        .fa-xl {
          
        }
        .promo-products-wrapper {
        }
      }
    }
  }
}

@media (max-width: 700px) {
  .promotions-wrapper {
    .promotion-button-wrapper {
      flex-direction: column-reverse;
      
      .promo {
        flex-direction: column;
        .next-button {
          bottom: 50%;
          right: 17%;
        }

        .fa-xl {
          display: none;
        }
        .promo-products-wrapper {
        }
      }
    }
  }
  
}
</style>
