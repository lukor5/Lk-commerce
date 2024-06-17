<template>
  <div class="popup-wrapper">
    <div class="popup">
      <button @click="closePopup" class="exit-button">
          <font-awesome-icon :icon="['fas', 'x']" />
        </button>
   
      <div class="row">
        <h2>Order ID: {{ this.order.id }}</h2>
        <b> {{ this.order.date }}</b>
      </div>

      <div class="row">
        <div class="column">
          <h2>User</h2>
          <h3>Contact</h3>
          <div class="row"><b>Phone: </b> {{ this.order.delivery.phone }}</div>
          <div class="row"><b>Email: </b> {{ userEmail }}</div>
        </div>
        <div class="column">
          <h2>Order details</h2>
          <div class="column">
            <h3>Address</h3>
            <div class="row"><b>City: </b> {{ this.order.delivery.city }}</div>
            <div class="row">
              <b>Zip code: </b> {{ this.order.delivery.zip_code }}
            </div>
            <div class="row">
              <b>Street: </b> {{ this.order.delivery.street }}
              {{ this.order.delivery.apartment_number }}
            </div>
            <div class="row"></div>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="row">
          <h2>Items</h2>
        </div>
        <div class="item-row" v-for="(item, index) in basketItems" :key="index">
          <div class="item-column">
            <h3>{{ item.product.name }}</h3>
          </div>
          <div class="item-column">
            <div class="row">
              <b>Size: {{ item.variant.size }}</b>
              <b>Color: {{ item.variant.color }}</b>
            </div>
          </div>
          <div class="item-column">
            <div class="row">
              <b>x {{ item.quantity }}</b>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <h2>Total Price: {{ totalPrice }} $</h2>
      </div>
      <ul>
        <li v-for="(action, index) in actions" :key="index">
          {{ action }}
          <div class="radio-container">
            <input
              v-model="selectedAction"
              :value="action"
              type="radio"
              name="actionRadio"
              id="actionRadio"
            />
            <span class="radio"></span>
          </div>
        </li>
      </ul>

      <button class="primary-button" @click="setStatus()">Submit</button>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "EditOrderPopup",
  props: {
    order: [],
  },
  computed: {
    userEmail() {
      if (this.order.user) {
        return this.order.user.email;
      } else {
        return this.order.delivery.email;
      }
    },
    basketItems() {
      if (this.order.user) {
        return this.order.basket.items;
      } else {
        return this.order.temporary_basket.items;
      }
    },
    totalPrice() {
      if (this.order.user) {
        return this.order.basket.total_price;
      } else {
        return this.order.temporary_basket.total_price;
      }
    },
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      selectedAction: this.order.status,
      actions: ["Ordered", "Paid", "Sent", "Delivered"],
    };
  },
  methods: {
    setStatus() {
      if (this.selectedAction) {
        const data = {
          status: this.selectedAction,
          order_id: this.order.id,
        };
        axios
          .post(this.baseUrl + "/update-order", data)
          .catch((error) => {
            console.log("error", error);
          });
      }
    },
    closePopup() {
      this.$emit("close-popup");
    },
  },
};
</script>
<style lang="scss" scoped>
.popup-wrapper {
  position: absolute;
  display: flex;
  width: 100%;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  .popup {
    display: flex;
    flex-direction: column;
    min-width: 30vw;
    flex-wrap: wrap;
    position: relative;
    padding: 20px;
    margin: auto;
    .exit-button {
      position: absolute;
      right: 20px;

    }
    .row,
    .item-row {
      display: flex;
      min-width: 50px;
      flex-direction: row;
      gap: 10px;
      align-items: center;
      text-align: left;
      flex-wrap: wrap;
    }
    .row * {
      display: flex;
      flex-direction: row;
    }
    .column {
      flex: 1;
      display: flex;
      flex-direction: column;
      .row {

      }
    }
    .item-column {
      flex: 1;
      .row {
        display: flex;
        flex-direction: row;
        justify-content: center;
      }
    }
    ul {
      list-style: none;
      display: flex;
      flex-direction: row;
      justify-content: center;
      gap: 5px;
      li {
        padding: 0px;
        display: flex;
        flex: 1;
        flex-direction: column;
      }
    }
  }
}
@media (max-width: 800px) {
  .popup-wrapper {
    .popup {

    }
  }
}
</style>