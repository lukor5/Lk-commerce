<template>
  <div class="popup-wrapper">
    <div class="payment-popup">
      <div class="row">
        <h2>Input card details</h2>
        <button class="exit-button" @click="closePaymentPopup">
          <font-awesome-icon :icon="['fas', 'x']" />
        </button>
      </div>
      <div class="card-number-row">
        <div class="input-wrapper">
          <label>Card Number</label>
          <div class="card-number">
            <img src="../assets/icons/visa_icon_2.png" />
            <input
              @input="handleInput"
              v-model="cardFirstFour"
              type="text"
              max="9999"
              id="firstFour"
            />
            <b>-</b>
            <input
              @input="handleInput"
              v-model="cardSecondFour"
              type="text"
              max="9999"
              id="secondFour"
            />
            <b>-</b>
            <input
              @input="handleInput"
              v-model="cardThirdFour"
              type="text"
              max="9999"
              id="thirdFour"
            />
            <b>-</b>
            <input
              @input="handleInput"
              v-model="cardFourthFour"
              type="text"
              max="9999"
              id="fourthFour"
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="input-wrapper">
          <label> Expiration date </label>
          <input
            @input="handleExpiryInput"
            @keydown="handleExpiryBackspace"
            class="primary-input"
            v-model="expirationDate"
            type="text"
            placeholder="mm/yyyy"
            maxlength="7"
          />
        </div>
        <div class="input-wrapper">
          <label> CVV </label>
          <input class="primary-input" type="text" v-model="cvv" />
          <p>Found on back of your card</p>
        </div>
      </div>
      <button @click="processPayment" class="primary-button">Pay</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  name: "PaymentPopup",
  computed: {
    ...mapGetters(["user"]),
    isExpiryDateValid() {
      const expiryRegex = /^(0[1-9]|1[0-2])\/(20\d{2}|19\d{2})$/;
      return expiryRegex.test(this.expirationDate);
    },
    isCvvValid() {
      const cvvRegex = /^\d{3,4}$/;
      return cvvRegex.test(this.cvv);
    },
  },
  props: {
    orderId: Number,
  },
  data() {
    return {
      cardFirstFour: "",
      cardSecondFour: "",
      cardThirdFour: "",
      cardFourthFour: "",
      expirationDate: "",
      cvv: "",
      baseUrl: this.$baseUrl,
      messages: [],
    };
  },
  methods: {
    handleInput(event) {
      let value = event.target.value.replace(/\D/g, "");
      if (value.length > 4) {
        value = value.slice(0, 4);
      }
      if (event.target.id === "firstFour") {
        this.cardFirstFour = value;
      } else if (event.target.id === "secondFour") {
        this.cardSecondFour = value;
      } else if (event.target.id === "thirdFour") {
        this.cardThirdFour = value;
      } else if (event.target.id === "fourthFour") {
        this.cardFourthFour = value;
      }

      if (value.length === 4 && event.target.id !== "fourthFour") {
        const nextInput = event.target.nextElementSibling.nextElementSibling;
        if (nextInput) {
          nextInput.focus();
        }
      }
    },
    handleExpiryInput() {
      if (this.expirationDate.length == 2) {
        this.expirationDate += "/";
      }
    },
    handleExpiryBackspace(event) {
      if (event.key === "Backspace" && this.expirationDate.length === 3) {
        this.expirationDate = "";
      }
    },
    processPayment() {
      let config = {};
      let cardNumber =
        this.cardFirstFour +
        this.cardSecondFour +
        this.cardThirdFour +
        this.cardFourthFour;
      let data = {
        card_number: cardNumber,
        cvv: this.cvv,
        expiry_date: this.expirationDate,
        order_id: this.orderId,
      };
      if (this.user.id) {
        data.user_id = this.user.id;
      }

      config.headers = {
        "X-Session-Key": this.$store.state.sessionKey,
      };
      if (this.checkValidity()) {
        axios
          .post(this.$baseUrl + "/create-payment", data, config)
          .then((response) => {
            if (response.status == 200) {
              this.$emit("payment-status", true);
              this.$emit("result", "Payment successful");
              this.$emit("close-popup", "payment");
            }
          })
          .catch((error) => {
            this.$emit("payment-status", false);
            this.messages.push("Card declined");
            this.$emit("result", this.messages);
            console.log("error", error);
          });
      } else {
        this.$emit("result", this.messages);
      }
    },
    checkValidity() {
      this.messages = [];
      if (!this.isExpiryDateValid) {
        this.messages.push(
          "Expiry date invalid. Please type in mm/yyyy format."
        );
      }
      if (!this.isCvvValid) {
        this.messages.push("Cvv invalid. Please input 3 numbers.");
      }
      return this.messages.length == 0;
    },
    closePaymentPopup() {
      this.$emit("close-popup", "payment");
    },
  },
  watch: {},
};
</script>

<style scoped lang="scss">
@import "../assets/styles/main.scss";

.popup-wrapper {
  z-index: 11;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;

  .payment-popup {
    background-color: var(--background-color);
    padding: 20px;
    box-shadow: 0 4px 8px rgba(var(--shadow-color-rgb), var(--shadow-opacity));
    display: flex;
    flex-direction: column;

    .card-number-row {
      text-align: left;
      margin-bottom: 20px;

      .input-wrapper {
        display: flex;
        flex-direction: column;

        .card-number {
          display: flex;
          align-items: center;
          img {
            margin-right: 10px;
          }
          input {
            width: 65px;
            text-align: center;
            margin-right: 5px;
            padding: 8px 12px;
            font-size: 16px;
            border: 1px solid var(--border-color);
            border-radius: 4px;
          }
        }
      }
    }

    .row {
      display: flex;
      justify-content: space-between; // Space out the Expiration date and CVV

      .exit-button {
        display: flex;
        width: min-content;
      }

      .input-wrapper {
        flex: 1; // Flexibly adjust based on content
        display: flex;
        flex-direction: column;

        &:not(:last-child) {
          margin-right: 20px; // Space between inputs
        }

        input.primary-input {
          width: auto; // Full width within wrapper
          padding: 8px 12px;
          font-size: 16px;
          border: 1px solid var(--border-color);
          border-radius: 4px;
        }

        p {
          font-size: 12px;
          color: #666;
          margin-top: 4px;
        }
      }
    }
    button {
      width: 50%;
    }
  }
}
</style>

