<template>
  <div class="shopping-basket">
    <div class="basket-top">
      <h3>Basket contents</h3>
      <font-awesome-icon
        @click="closeShoppingBasket"
        :icon="['fas', 'x']"
        id="escapeIcon"
      />
    </div>
    <div class="product-list">
      <div class="product-column">
        <div class="row">
          <div class="single-detail"><p>Name</p></div>
          <div class="single-detail">Size</div>
          <div class="single-detail">Color</div>
          <div class="single-detail-count">Count</div>
        </div>
      </div>
      <div
        class="product-column"
        v-for="(basketItem, index) in sortedBasket"
        :key="index"
      >
        <div class="row">
          <div class="single-detail">
            <b>{{ basketItem.product.name }}</b>
          </div>
          <div class="single-detail">
            <b>{{ basketItem.variant.size }}</b>
          </div>
          <div class="single-detail">
            <b>{{ basketItem.variant.color }}</b>
          </div>
          <div class="single-detail-count">
            <font-awesome-icon
              :icon="['fas', 'angle-left']"
              class="fa-lg"
              @click="counter(basketItem, 'decrease')"
            />
            <b>{{ basketItem.quantity }}</b>
            <font-awesome-icon
              :icon="['fas', 'angle-right']"
              class="fa-lg"
              @click="counter(basketItem, 'increase')"
            />
          </div>
        </div>
        <div class="row-bottom">
          <div class="single-detail">
            <font-awesome-icon
              :icon="['far', 'trash-can']"
              class="fa-lg"
              @click="
                updateBasketProduct(basketItem, 'delete');
                counter(basketItem, 'delete');
              "
            />
          </div>
          <div class="single-detail">
            <b>{{ formatTotalPrice(basketItem) }} </b>
          </div>
        </div>
      </div>
      <div class="basket-summary">
        <b>Total price: {{ this.totalPrice }} $</b>
      </div>
    </div>
    <button
      class="primary-button"
      @click="
        redirectToOrder();
        closeShoppingBasket();
        $emit('total-price-emitted', totalPrice);
      "
    >
      Order
    </button>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions, mapGetters } from "vuex";
export default {
  name: "ShoppingBasket",
  data() {
    return {
      baseUrl: this.$baseUrl,
      basket: [],
      removeClicked: false,
      totalPrice: null,
    };
  },
  computed: {
    ...mapGetters(["user"]),
    userId() {
      return this.user.id;
    },
    basketQuantity() {
      return this.basket.reduce((quantity, basketItem) => {
        return quantity + basketItem.quantity;
      }, 0);
    },
    sortedBasket() {
      return this.basket.slice().sort((a, b) => {
        if (a.variant.id < b.variant.id) return -1;
        if (a.variant.id > b.variant.id) return 1;
        return 0;
      });
    },
  },
  methods: {
    ...mapActions(["updateBasket", "addBasketItem"]),
    getBasketProducts() {
      axios
        .get(`${this.baseUrl}/basket${this.userId ? "/" + this.userId : ""}`, {
          headers: {
            "X-Session-Key": this.$store.state.sessionKey,
          },
        })
        .then((response) => {
          this.basket = response.data;
          this.totalPrice = this.basket[0].total_price;
          this.updateBasket({
            basketItems: this.basket,
            quantity: this.basketQuantity,
            totalPrice: response.data[0].total_price,
          });
        })
        .catch((error) => {
          console.log("error fetching basket", error);
          this.$store.state.basket.quantity = 0;
          this.closeShoppingBasket();
        });
    },
    counter(basketItem, action) {
      const previousQuantity = basketItem.quantity;
      if (action === "decrease") {
        if (basketItem.quantity > 1) {
          basketItem.quantity--;
          this.updateBasketProduct(basketItem, "decrease", previousQuantity);
        }
      } else if (action === "increase") {
        basketItem.quantity++;
        this.updateBasketProduct(basketItem, "increase", previousQuantity);
      } else if (action === "delete") {
        this.updateBasket({
          quantity: this.basketQuantity - basketItem.quantity,
        });
      }
    },
    updateBasketProduct(basketItem, action, previousQuantity) {
      if (this.user.id) {
        const data = {
          basket_id: basketItem.basket,
          product_id: basketItem.product.id,
          variant: basketItem.variant,
          action: action,
        };

        axios
          .post(this.baseUrl + "/update_basket", data)
          .then((response) => {
            this.totalPrice = response.data.total_price;
            this.getBasketProducts();
          })
          .catch((error) => {
            console.log("error updating basket", error);
            basketItem.quantity = previousQuantity;
          });
      } else {
        const data = {
          basket_id: basketItem.basket,
          product_id: basketItem.product.id,
          variant: basketItem.variant,
          action: action,
          session_key: this.$store.state.sessionKey,
        };

        axios
          .post(this.baseUrl + "/update_basket", data)
          .then((response) => {
            this.totalPrice = response.data.total_price;
            this.getBasketProducts();
          })
          .catch((error) => {
            console.log("error updating basket", error);
            basketItem.quantity = previousQuantity;
          });
      }
    },
    calculateTotalPrice(basketItem) {
      return (
        (Math.round(
          basketItem.product.price * basketItem.product.discount * 100
        ) /
          100) *
        basketItem.quantity
      ).toFixed(2);
    },
    formatTotalPrice(basketItem) {
      const totalPrice = this.calculateTotalPrice(basketItem);
      return totalPrice + " $";
    },
    redirectToOrder() {
      if (this.userId) {
        this.$router.push({ name: "orderForm" });
      } else {
        this.$emit("user-not-logged-in");
        // You can handle this case further as needed
      }
    },
    closeShoppingBasket() {
      this.$emit("close-basket-clicked");
    },
  },
  mounted() {
    this.getBasketProducts();
  },
  watch: {
    basketQuantity() {
      this.$emit("basket-quantity-changed", this.basketQuantity);
    },
  },
};
</script>

<style lang=scss>
@import "../assets/styles/main.scss";
.shopping-basket {
  display: grid;
  grid-template-rows: 10vh 30vh 10vh;

  position: fixed;
  height: 100vh;
  z-index: 9999;
  max-width: 25vw;
  padding: 20px;
  background-color: var(--background-color);
  text-align: left;
  animation: slideIn 0.3s ease-in forwards;
  box-shadow: -5px 3px 17px 1px
    rgba(var(--shadow-color-rgb), var(--shadow-opacity));
  .basket-top {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: baseline;

    #escapeIcon:hover {
      cursor: pointer;
    }
  }
  .product-list {
    display: grid;

    overflow-y: auto; // Enables scrolling for overflow content
  }

  .product-column {
    display: grid;
    grid-template-rows: 1fr 1fr; // Adjust based on your design preference
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    .row {
      display: grid;
      grid-template-columns: 1.5fr 1fr 1fr 1fr;
      .single-detail-count {
        display: grid;
        grid-template-columns: auto auto auto;
        align-items: center;
        justify-content: center;
        gap: 5px;
      }
    }
    .row-bottom {
      display: grid;
      grid-template-columns: 1fr auto;
    }

    .fa-lg {
    }
    .fa-lg:hover {
      color: var(--secondary-color);

      cursor: pointer;
    }
  }
}

@media (max-width: 1400px) {
  .shopping-basket {
    max-width: 60vw;
  }
}
@media (max-width: 600px) {
  .shopping-basket {
    max-width: 70vw;
    .product-row {
    }
  }
}

@keyframes slideIn {
  0% {
    right: -300px;
  }

  100% {
    right: 0px;
  }
}
</style>