<template>
  <div class="order-wrapper">
    <div class="form-wrapper">
      <div class="column-left">
        <ProductCheckout />
        <div class="delivery-wrapper">
          <h2>Choose delivery:</h2>
          <div class="delivery-options">
            <div class="option">
              <font-awesome-icon :icon="['fas', 'truck']" class="fa-xl" />
              <div class="option-label">
                <b>Courier ({{ this.deliveryOptions[0].price }} $)</b>
                <label
                  >Delivery in
                  {{ this.deliveryOptions[0].estimatedDelivery }}</label
                >
              </div>
              <div class="radio-container">
                <input type="radio" value="Courier" v-model="deliveryMethod" />
                <span class="radio"></span>
              </div>
            </div>
            <div class="option">
              <font-awesome-icon :icon="['fas', 'envelope']" class="fa-xl" />
              <div class="option-label">
                <b>Postal service ({{ this.deliveryOptions[1].price }} $)</b>
                <label
                  >Delivery in
                  {{ this.deliveryOptions[1].estimatedDelivery }}</label
                >
              </div>
              <div class="radio-container">
                <input
                  type="radio"
                  value="Postal service"
                  v-model="deliveryMethod"
                />
                <span class="radio"></span>
              </div>
            </div>
          </div>
        </div>
        <div class="payment-wrapper">
          <div class="payment">
            <h2>Payment option</h2>
            <div class="column">
              <div class="option">
                <div class="radio-container">
                  <input type="radio" value="Card" v-model="paymentMethod" />
                  <span class="radio"></span>
                </div>
                <b>Card</b>
                <div class="images">
                  <img src="../assets/icons/visa.png" />
                  <img src="../assets/icons/mastercard.png" />
                </div>
              </div>
              <div class="option">
                <div class="radio-container">
                  <input type="radio" value="Paypal" v-model="paymentMethod" />
                  <span class="radio"></span>
                </div>
                <b>PayPal</b>
                <img src="../assets/icons/paypal.png" />
              </div>
            </div>
            <div class="column">
              <div class="option">
                <div class="radio-container">
                  <input type="radio" value="Bank" v-model="paymentMethod" />
                  <span class="radio"></span>
                </div>
                <b>Bank</b>
                <img src="../assets/icons/bank.png" />
              </div>
              <div class="option">
                <div class="radio-container">
                  <input type="radio" value="Stripe" v-model="paymentMethod" />
                  <span class="radio"></span>
                </div>
                <b>Stripe</b>
                <img src="../assets/icons/stripe.png" />
              </div>
            </div>
          </div>
        </div>
        <div class="voucher-wrapper">
          <h2>Voucher</h2>
          <div class="voucher">
            <input
              class="primary-input"
              v-model="voucherCode"
              placeholder="Your voucher code"
            />
            <button @click="handleVoucherApplied" class="apply-button">
              Apply
            </button>
          </div>
        </div>
      </div>
      <div class="column-right">
        <DeliveryForm
          :orderClicked="orderClicked"
          @deliveryData="handleDeliveryData"
          @result="createOrder"
        />
        <div class="bottom">
          <div class="summary">
            <b>Subtotal: {{ this.basket.totalPrice }} </b>
            <p>Delivery: {{ this.shippingPrice }}</p>
            <h2>Total : {{ checkoutPrice }} $</h2>
          </div>
          <div class="order-button">
            <button class="primary-button" @click.prevent="handleOrderClicked">
              Order
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters, mapState, mapActions } from "vuex";
import ProductCheckout from "./ProductCheckout.vue";
import DeliveryForm from "./DeliveryForm.vue";
import axios from "axios";

export default {
  name: "OrderForm",
  components: {
    ProductCheckout,
    DeliveryForm,
  },
  props: {
    paymentStatus: Boolean,
  },
  computed: {
    ...mapGetters(["basket"]),
    ...mapState(["user"]),
    checkoutPrice() {
      return (
        parseFloat(this.basket.totalPrice) + parseFloat(this.shippingPrice || 0)
      ).toFixed(2);
    },
    basketHasItems() {
      return this.basket.quantity > 0;
    },
    isDeliverySelected() {
      return this.deliveryMethod;
    },
    isPaymentMethodSelected() {
      return this.paymentMethod;
    },
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      basketDetails: [],
      shippingPrice: null,
      deliveryOptions: [
        { name: "Courier", price: 13.99, estimatedDelivery: "1-3 days" },
        { name: "Postal service", price: 9.99, estimatedDelivery: "5-7 days" },
      ],

      deliveryMethod: null,
      paymentMethod: null,
      messages: [],
      voucherCode: "",
      orderClicked: false,
      data: {},
    };
  },

  methods: {
    ...mapActions(["updateBasket", "fetchBasket", "fetchOrders"]),
    createOrder(result) {
      let config = {};
      if (this.user.id) {
        this.data["user_id"] = this.user.id;
      } else {
        config.headers = {
          "X-Session-Key": this.$store.state.sessionKey,
        };
        this.data["session_key"] = this.$store.state.sessionKey;
      }
      this.data["delivery_method"] = this.deliveryMethod;
      let isFormValid = this.checkFormValidity(result);
      if (isFormValid) {
        axios
          .post(this.baseUrl + "/create-order", this.data, config)
          .then((response) => {
            if (response.status === 200) {
              this.$emit("result", "Order created succesfully");
              this.$emit("create-payment", response.data.order_id);
              this.updateBasket({ quantity: 0 });
              this.fetchOrders(this.user.id);
              this.$router.push("/");
            } else {
              this.$emit("result", "Error: Order not created");
            }
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        this.$emit("result", this.messages);
      }
      this.orderClicked = false;
    },

    getProducts() {
      if (this.user.id) {
        axios
          .get(this.baseUrl + "/basket/" + this.user.id)
          .then((response) => {
            this.basketDetails = response.data;
          })
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    getVouchers() {
      const params = {
        user: this.user.id,
      };

      if (this.user.id) {
        axios
          .get(this.baseUrl + "/get-vouchers", { params })
      }
    },
    handleVoucherApplied() {
      const data = {
        code: this.voucherCode,
        temporary_basket: this.basket.basketItems[0].temporary_basket,
        basket: this.basket.basketItems[0].basket,
      };
      axios
        .post(this.baseUrl + "/apply-voucher", data)
        .then((response) => {
          if (response.status === 200) {
            this.$emit("result", "Voucher applied succesfully!");
            this.fetchBasket(
              this.user.id ? this.user.id : this.$store.state.sessionkey
            );
          }
        })
        .catch((error) => {
          console.log("error", error);
          if (error.response.status === 500) {
            this.$emit("result", "Error: Voucher already spent");
          } else if (error.response.status === 403) {
            this.$emit("result", "Error: Can't set price below 0");
          } else {
            this.$emit("result", "Error: Voucher not found");
          }
        });
    },
    handleOrderClicked() {
      this.orderClicked = true;
    },
    handleDeliveryData(data) {
      this.data = data;
    },
    checkFormValidity(result) {
      this.messages = [];
      if (result !== "success") {
        this.messages = result;
      }
      if (!this.isDeliverySelected) {
        this.messages.push("Error: No delivery selected");
      }
      if (!this.isPaymentMethodSelected) {
        this.messages.push("Error: No payment option selected");
      }
      return this.messages.length == 0;
    },
  },
  mounted() {
    this.getProducts();
  },
  watch: {
    deliveryMethod() {
      let filteredOption = this.deliveryOptions.filter((option) => {
        return this.deliveryMethod === option.name;
      });
      this.shippingPrice = filteredOption[0].price;
    },
    paymentStatus(newValue) {
      if (newValue === true) {
        this.createOrder();
      }
    },
  },
};
</script>
<style lang="scss">
@import "../assets/styles/main.scss";

.order-wrapper {
  display: grid;
  height: 100vh;
  overflow-y: scroll;

  &::-webkit-scrollbar {
    width: 12px;
  }

  &::-webkit-scrollbar-thumb {
    background-color: var(--secondary-color);
    border-radius: 4px;
    border: 2px solid white;
  }
  &::-webkit-scrollbar-thumb:hover {
    background-color: white;
    border-radius: 4px;
    border: 2px solid var(--secondary-color);
  }
  &::-webkit-scrollbar-track {
    background: white;
  }

  .form-wrapper {
    margin-inline: 2vw;
    display: grid;
    justify-content: center;
    grid-template-columns: auto auto;
    grid-template-rows: auto;
    gap: 20px;
    text-align: left;

    .column-left {
      display: grid;
      grid-template-rows: repeat(4, min-content);
      gap: 40px;

      .delivery-options {
        display: grid;
        grid-template-rows: repeat(2, 1fr);
        gap: 10px;

        .option {
          display: grid;
          grid-template-columns: 1fr 2fr 1fr;
          align-items: center;
          .option-label {
            display: grid;
            grid-template-rows: auto auto;
            label {
              @include small-text;
            }
          }
        }
      }

      .payment {
        display: grid;
        grid-template-rows: auto auto auto;
        .column {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          .option {
            display: grid;
            grid-template-columns: auto 1fr 2fr;
            justify-content: left;
            gap: 10px;
            align-items: center;
            .images {
              display: flex;
              flex-direction: row;
            }
          }
        }
      }
      .voucher {
        display: grid;
        grid-template-columns: auto auto;
        justify-content: left;
        button {
          padding: 10px;
          border: 1px solid var(--secondary-color);
          border-left: none;
          border-top-right-radius: 15px;
          border-bottom-right-radius: 15px;
        }
        button:hover {
          @include secondary-button;
        }
      }
    }
    .column-right {
      display: grid;
      grid-template-columns: auto;
      gap: 40px;
    }
  }
}
@media (max-width: 800px) {
  .order-wrapper {
    .form-wrapper {
      grid-template-columns: 1fr;
    }
  }
}
</style>