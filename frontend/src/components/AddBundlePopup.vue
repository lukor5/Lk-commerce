<template>
  <div class="add-bundle-popup">
    <div class="product-wrapper">
      <button
        class="exit-button"
        @click="$emit('close-popup'), this.clearAllBundleProducts()"
      >
        <font-awesome-icon :icon="['fas', 'x']" class="fa-s" />
      </button>
      <div class="single-product" v-if="product">
        <h1>{{ product.name }}</h1>
        <div class="details-wrapper">
          <div class="details-left">
            <div id="imageContainer">
              <img
                class="product-image"
                :src="baseMediaUrl + product.product_image"
              />
            </div>
          </div>

          <div class="details-right">
            {{ product.body }}
            <div class="variants-price">
              <ul>
                <li v-for="(variant, index) in this.uniqueSizes" :key="index">
                  <span>{{ variant.size }} </span
                  ><input
                    type="checkbox"
                    :id="'variant_' + index"
                    :value="index"
                    :checked="selectedVariant === index"
                    @change="handleCheckboxChange(index, variant)"
                    :disabled="variant.stock === 0"
                  />
                </li>
              </ul>
            </div>
            <div v-if="selectedVariant !== null" class="variants-colors">
              <div
                class="button-container"
                v-for="(variant, index) in this.colorsBySize"
                :key="index"
                :class="{ 'active-color': activeColor === index }"
              >
                <button
                  @click="handleColorButtonClicked(index, variant.color)"
                  class="color-button"
                  :style="{ backgroundColor: variant.color }"
                  :value="variant.color"
                ></button>
                <label>
                  <span>
                    {{ variant.color }}
                  </span>
                </label>
              </div>
            </div>
            <div v-else class="variants-colors">
              <b>Please select size</b>
            </div>
            <button @click="handleNextProductClicked" class="primary-button">
              Next product
            </button>
            <button
              v-if="bothProductsSelected"
              @click="addBundleToBasket"
              class="primary-button"
            >
              Add to basket
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

import axios from "axios";
export default {
  name: "AddBundlePopup",

  props: {
    bundle: Object,
  },
  computed: {
    ...mapGetters(["user", "basket", "bundleProducts"]),
    userId() {
      return this.user.id;
    },
    userName() {
      return this.user.username;
    },
    isColorSelected() {
      return this.selectedColor;
    },
    isSizeSelected() {
      return this.selectedSize;
    },
    bothProductsSelected() {
      return (
        this.bundleProducts.length == 2 &&
        this.bundleProducts[1].selectedColor &&
        this.bundleProducts[1].selectedVariant &&
        this.isColorSelected &&
        this.isSizeSelected
      );
    },
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      baseMediaUrl: this.$baseMediaUrl,
      currentId: null,
      nextId: null,
      product: null,
      priceAfterDiscount: null,

      variants: [],
      selectedVariant: null,
      selectedSize: null,
      activeColor: null,
      selectedColor: null,
      messages: [],
    };
  },
  methods: {
    ...mapActions([
      "updateBasket",
      "addBasketItem",
      "addBundleProduct",
      "clearAllBundleProducts",
    ]),
    getProductDetails(bundleProductId) {
      let url = ``;
      if (bundleProductId) {
        url = `${this.baseUrl}/products/${bundleProductId}`;
      }

      axios
        .get(url)
        .then((response) => {
          this.product = response.data;

          this.priceAfterDiscount = (
            Math.round(this.product.price * this.product.discount * 100) / 100
          ).toFixed(2);
          this.sortVariants();
          this.$nextTick(() => {
            let bundleProduct = this.$store.state.bundleProducts.find(
              (product) => product.id === bundleProductId
            );
            if (bundleProduct) {
              this.setCheckboxes(bundleProduct);
            }
          });
        })
        .catch((error) => {
            console.log('error', error)
        });
    },
    addBundleToBasket() {
      let data = [];
      let headers = [];
      if (this.user.id) {
        data = {
          quantity: 1,
          user_id: this.userId,
          primary_product_id: this.product.id,
          discounted_product_id: this.bundleProducts[1].id,
          size: this.selectedSize,
          discounted_size: this.bundleProducts[1].selectedSize,
          color: this.selectedColor,
          discounted_color: this.bundleProducts[1].selectedColor,
        };
      } else {
        data = {
          quantity: 1,
          primary_product_id: this.product.id,
          discounted_product_id: this.bundleProducts[1].id,
          size: this.selectedSize,
          discounted_size: this.bundleProducts[1].selectedSize,
          color: this.selectedColor,
          discounted_color: this.bundleProducts[1].selectedColor,
        };
        headers = {
          "X-Session-Key": this.$store.state.sessionKey,
        };
      }
      console.log(data)
      axios
        .post(this.baseUrl + "/add-promotion-bundle-to-basket", data, {
          headers,
          withCredentials: true, // Add this line to send credentials with the request
        })
        .then(() => {
          this.$emit("result", "Product bundle added to basket");
          this.$emit("product-added");
          this.selectedColor = null;
          this.activeColor = null;
          this.selectedSize = null;
          this.selectedVariant = null;
          const newBasketQuantity = this.$store.getters.basket.quantity + 2;
          this.updateBasket({ quantity: newBasketQuantity });
          this.clearAllBundleProducts();
          this.$router.push("/");
          this.$emit("close-popup");
        })
        .catch((error) => {
          if (error.response.status == 400) {
            this.$emit("result", "Promotion bundle already in basket");
          }
        });
    },
    sortVariants() {
      this.variants = this.product.product_variants;
      if (this.product) {
        this.variants.sort((a, b) => {
          return a.size.localeCompare(b.size);
        });
      }
      this.getUniqueSizes();
    },
    getBundleProducts() {
      let productIds = [];
      productIds[0] = this.bundle.primary_product.id;
      productIds[1] = this.bundle.discounted_product.id;
      this.currentId = productIds[0];
      this.nextId = productIds[1];

      this.getProductDetails(this.currentId);
    },
    handleCheckboxChange(index, variant) {
      if (this.selectedVariant === index) {
        this.selectedVariant = null;
        this.selectedSize = null;
        this.selectedColor = null;
      } else {
        this.selectedColor = null;
        this.activeColor = null;
        this.selectedVariant = index;
        this.selectedSize = variant.size;
        this.filterColorsBySize(variant);
      }
    },
    handleColorButtonClicked(index, color) {
      this.activeColor = index;
      this.selectedColor = color;
      this.messages = []
    },
    handleNextProductClicked() {
        this.messages = []
      if (this.checkVariantsSelected()) {
        const bundleProduct = {
          id: this.currentId,
          selectedColor: this.selectedColor,
          activeColor: this.activeColor,
          selectedSize: this.selectedSize,
          selectedVariant: this.selectedVariant,
        };
        this.addBundleProduct(bundleProduct);

        this.selectedColor = null;
        this.activeColor = null;
        this.selectedSize = null;
        this.selectedVariant = null;

        this.$nextTick(() => {
          const tempId = this.currentId;
          this.currentId = this.nextId;
          this.nextId = tempId;

          this.getProductDetails(this.currentId);
        });
      } else {
        this.$emit("result", this.messages);
      }
    },
    setCheckboxes(bundleProduct) {
      this.selectedVariant = bundleProduct.selectedVariant;
      this.selectedSize = bundleProduct.selectedSize;
      this.filterColorsBySize(this.uniqueSizes[this.selectedVariant]);
      this.activeColor = bundleProduct.activeColor;
      this.selectedColor = bundleProduct.selectedColor;
    },
    checkVariantsSelected() {
      if (!this.isColorSelected) {
        this.messages.push("Error: No color selected");
      }
      if (!this.isSizeSelected) {
        this.messages.push("Error: No size selected");
      }
      return this.messages.length === 0;
    },
    getUniqueSizes() {
      this.uniqueSizes = this.variants.filter((variant, index, array) => {
        return array.findIndex((v) => v.size === variant.size) === index;
      });
    },
    filterColorsBySize(variant) {
      this.colorsBySize = this.variants.filter((v) => v.size === variant.size);
    },
  },
  mounted() {
    this.getBundleProducts();
  },
};
</script>

<style lang="scss">
@import "../assets/styles/main.scss";

.add-bundle-popup {
  position: absolute;
  display: flex;
  width: 100%;
  height: 100vh;
  justify-content: center;
  align-items: center;
  z-index: 9999;

  .product-wrapper {
    background-color: var(--background-color);
    height: auto;
    max-width: 900px;
    display: flex;
    flex-direction: column;

    padding: 20px;
    border-radius: 15px;
    position: relative;

    .exit-button {
      position: absolute;
      top: 10px;
      right: 10px;
      background: transparent;
      border: none;
      font-size: 1.5em;
      cursor: pointer;
      color: var(--text-color);
    }

    .single-product {
      display: flex;
      flex-direction: column;
      text-align: left;
      flex: 1;

      .details-wrapper {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 40px;

        .details-left {
          display: flex;
          flex-direction: column;
        }

        .details-right {
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          gap: 20px;
          max-width: 20%;

          .variants-price {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            gap: 10px;

            ul {
              display: flex;
              flex-direction: row;
              gap: 20px;
              list-style: none;
              padding: 0;

              li {
                input {
                  background-color: var(--background-color);
                }
              }
            }
          }

          .variants-colors {
            display: flex;
            direction: row;
            justify-content: center;
            gap: 10px;
            margin-bottom: 10px;

            .button-container {
              display: flex;
              align-items: center;
              flex-direction: column;
              position: relative;
              transition: transform 0.5s ease;
              border: 1px solid var(--subtle-border-color);
              border-radius: 10px;

              label {
                position: absolute;
                top: 30px;

                span {
                  // Add your small-text mixin styles here
                  @include small-text;
                }
              }

              .color-button {
                width: 25px;
                height: 25px;
                margin: 5px;
              }
            }

            .active-color {
              transform: scale(1.2);
            }
          }
        }
      }

      .product-image {
        border-radius: 15px;
        max-width: 100%;
        max-height: 500px;
        width: auto;
        height: auto;
        object-fit: contain;
      }
    }
  }

  /* Scrollbar Styling */
  ::-webkit-scrollbar-track {
    background: var(--background-color);
  }

  ::-webkit-scrollbar-thumb {
    background: var(--secondary-color);
    border: 2px solid var(--background-color);
  }

  ::-webkit-scrollbar-thumb:hover {
    cursor: pointer;
    background: var(--secondary-color);
    border: 2px solid var(--secondary-color);
  }

  @media (max-width: 1000px) {
    .product-wrapper {
      .single-product {
        .details-wrapper {
          align-items: center;

          .details-left {
            align-items: center;
          }

          .details-right {
            align-items: center;
            width: 100%;
            max-width: 100%;
          }
        }

        .product-image {
          max-width: 100%;
          max-height: 400px;
          width: auto;
          height: auto;
          object-fit: contain;
        }
      }
    }
  }
}
</style>