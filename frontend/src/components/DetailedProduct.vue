<template>
  <div class="product-wrapper">
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
          <StarRating
            @rating-clicked="handleRatingClicked"
            :product="product"
          />
          <div
            v-if="this.product.status === true"
            class="product-availability"
            style="color: green"
          >
            <font-awesome-icon :icon="['fas', 'check']" />
            <b>Product available</b>
          </div>
          <div v-else class="product-availability" style="color: red">
            <b>Product not available</b>
          </div>

          <div class="price-wrapper">
            <span style="text-decoration: line-through"
              >{{ product.price }} $</span
            >
            <b>{{ this.priceAfterDiscount }} $</b>
          </div>
          <button v-if="id" class="primary-button" @click="addToBasket">
            Add to basket
          </button>
        </div>
      </div>
      <div class="reviews-container">
        <h2>Reviews</h2>
        <button
          v-if="!showReviews"
          class="reviews-button"
          @click="showReviews = true"
        >
          <font-awesome-icon :icon="['fas', 'angle-down']" class="fa-2xl" />
        </button>
        <button v-else @click="showReviews = false">
          <font-awesome-icon :icon="['fas', 'angle-up']" class="fa-2xl" />
        </button>
        <ReviewList v-if="showReviews" :product="product" />
      </div>
    </div>

    <div v-else>Loading...</div>
  </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";
import { mapGetters, mapActions } from "vuex";
import StarRating from "./StarRating.vue";
import ReviewList from "./ReviewList.vue";
export default {
  name: "DetailedProduct",
  props: {
    id: String,
    ids: String,
  },
  components: {
    StarRating,
    ReviewList,
  },
  data() {
    return {
      baseMediaUrl: this.$baseMediaUrl,
      baseUrl: this.$baseUrl,
      product: null,
      variants: [],
      selectedVariant: null,
      selectedSize: null,
      activeColor: null,
      selectedColor: null,
      priceAfterDiscount: null,
      colorButtons: [],
      colorsBySize: [],
      messages: [],
      showReviews: true,
    };
  },
  computed: {
    ...mapGetters(["user", "basket"]),
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
  },
  methods: {
    ...mapActions(["updateBasket", "addBasketItem"]),
    getProductDetails(bundleProductId) {
      const url = `${this.baseUrl}/products/${this.id}`;
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
          console.log("Error fetching product details", error);
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
    },
    handleRatingClicked(data) {
      this.$emit("rating-clicked", data);
    },

    getUniqueSizes() {
      this.uniqueSizes = this.variants.filter((variant, index, array) => {
        return array.findIndex((v) => v.size === variant.size) === index;
      });
    },
    filterColorsBySize(variant) {
      this.colorsBySize = this.variants.filter((v) => v.size === variant.size);
    },

    addToBasket() {
      if (this.checkVariantsSelected()) {
        let data = [];
        if (this.user.id) {
          data = {
            quantity: 1,
            user_id: this.userId,
            product_id: this.product.id,
            size: this.selectedSize,
            color: this.selectedColor,
          };
        } else {
          data = {
            quantity: 1,
            product_id: this.product.id,
            size: this.selectedSize,
            color: this.selectedColor,
          };
        }
        const csrftoken = Cookies.get("CSRFToken");
        let headers = {};
        if (csrftoken) {
          headers = {
            "X-CSRFToken": csrftoken,
            "X-Session-Key": this.$store.state.sessionKey,
          };
        } else {
          headers = {
            "X-Session-Key": this.$store.state.sessionKey,
          };
        }

        axios
          .post(this.baseUrl + "/add_to_basket", data, {
            headers,
            withCredentials: true, // Add this line to send credentials with the request
          })
          .then(() => {
            this.$emit("result", "Product added to basket");
            this.$emit("product-added");
            const newBasketQuantity = this.$store.getters.basket.quantity + 1;
            this.updateBasket({ quantity: newBasketQuantity });
          })
          .catch((error) => {
            console.error("Add to basket error:", error);
          });
      } else {
        this.$emit("result", this.messages);
        this.messages = [];
      }
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
  },
  watch: {
    "$route.params.id": function (newId) {
      this.getProductDetails(newId);
    },
  },
  mounted() {
    if (this.id) {
      this.getProductDetails();
    }
  },
};
</script>

<style scoped lang=scss>
@import "../assets/styles/main.scss";

.product-wrapper {
  flex: 1;
  height: auto;
  overflow-y: scroll;
  display: flex;
  flex-direction: column;

  .single-product {
    display: flex;
    flex-direction: column;
    text-align: left;
    flex: 1;
    max-width: 100%;
    padding-inline: 5%;
    gap: 10px;

    .product-availability {
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 5px;
    }

    .details-wrapper {
      display: flex;
      flex-direction: row;
      justify-content: center;
      gap: 40px;
    }

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
    }

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

    .price-wrapper {
      display: flex;
      flex-direction: row;
      gap: 40px;
      justify-content: flex-end;
    }

    .reviews-container {
      align-items: center;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;

      button {
        transition: all 0.3s ease;

        &:hover {
          color: var(--secondary-color);
          transform: scale(1.2);
        }
      }
    }

    .product-image {
      border-radius: 15px;
      max-width: 100%;
      max-height: 500px;
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

@media (max-width: 900px) {
  .product-wrapper {
    .single-product {
      .details-wrapper {
        flex-direction: column;
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
    }
  }
}
</style>