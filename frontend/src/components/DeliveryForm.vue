<template>
  <form class="form">
    <div class="row">
      <h2 class="form-heading">Name</h2>
      <div class="inputs-row name">
        <input
          class="primary-input"
          type="text"
          v-model="firstName"
          placeholder="First name"
        />
        <input
          class="primary-input"
          type="text"
          v-model="lastName"
          placeholder="Last name"
        />
      </div>
    </div>
    <div class="row">
      <h2 class="form-heading">Address</h2>
      <div class="inputs-row address">
        <input
          class="primary-input"
          type="text"
          v-model="street"
          placeholder="Street"
        />
        <input
          class="primary-input"
          type="text"
          v-model="apartmentNumber"
          placeholder="Apartment number"
        />
        <input
          class="primary-input"
          type="text"
          v-model="city"
          placeholder="City"
        />
        <input
          class="primary-input"
          type="text"
          v-model="zipCode"
          placeholder="Zip code"
        />
      </div>
    </div>
    <div class="row">
      <h2 class="form-heading">Contact info</h2>
      <div class="inputs-row details">
        <div class="phone-input">
          <div class="country-code">
            <b>+</b>
            <input type="tel" v-model="countryCode" placeholder="48" />
          </div>
          <input
            class="primary-input"
            type="tel"
            v-model="phone"
            placeholder="Phone number"
          />
        </div>
        <input
          class="primary-input"
          type="text"
          v-model="email"
          placeholder="Email"
        />
      </div>
    </div>
    <div class="bottom">
      <button
        @click="setDelivery"
        class="primary-button"
        v-if="mode == 'changeDelivery'"
      >
        Update
      </button>
    </div>
  </form>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";
export default {
  name: "DeliveryForm",
  props: {
    orderClicked: Boolean,
    mode: String,
  },
  computed: {
    ...mapGetters(["user"]),
    isNameValid() {
      return this.firstName.length > 0 && this.lastName.length > 0;
    },
    isEmailValid() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(this.email);
    },
    isStreetValid() {
      return this.street.length > 0;
    },
    isApartmentNumberValid() {
      const aptRegex = /^\d+\s*(\/\s*\d+)?$/;
      return aptRegex.test(this.apartmentNumber);
    },
    isZipCodeValid() {
      const zipRegex = /^\d{2,5}(-\d{1,4})?$/;
      return zipRegex.test(this.zipCode);
    },
    isCityValid() {
      return this.city.length > 0;
    },
    isPhoneValid() {
      if (this.phone.length === 0) {
        return false;
      }
      const regex = /^\d{9}$/;
      return regex.test(this.phone);
    },
  },
  data() {
    return {
      firstName: "",
      lastName: "",
      city: "",
      street: "",
      phone: "",
      email: "",
      zipCode: "",
      apartmentNumber: "",
      messages: [],
      deliveryData: {},
      baseUrl: this.$baseUrl,
    };
  },
  methods: {
    checkDeliveryValidity() {
      this.messages = [];
      if (!this.isNameValid) {
        this.messages.push("Error: Name invalid");
      }
      if (!this.isEmailValid) {
        this.messages.push("Error: Email invalid");
      }
      if (!this.isStreetValid) {
        this.messages.push("Error: Street invalid");
      }
      if (!this.isApartmentNumberValid) {
        this.messages.push("Error: Apartment number invalid");
      }
      if (!this.isZipCodeValid) {
        this.messages.push("Error: Zip code invalid");
      }
      if (!this.isCityValid) {
        this.messages.push("Error: City invalid");
      }
      if (!this.isPhoneValid) {
        this.messages.push("Error: Phone invalid");
      }
      this.emitDeliveryValidity();
    },
    async emitDeliveryValidity() {
      try {
        if (this.messages.length === 0) {
          await this.setDeliveryData();
          this.$emit("result", "success");
        } else {
          this.$emit("result", this.messages);
        }
      } catch (error) {
        console.error("Error emitting delivery validity:", error);
        this.$emit("result", "error");
      }
    },
    async setDeliveryData() {
      this.deliveryData = {
        first_name: this.firstName,
        last_name: this.lastName,
        city: this.city,
        street: this.street,
        phone: this.phone,
        email: this.email,
        zip_code: this.zipCode,
        apartment_number: this.apartmentNumber,
      };
      this.$emit("deliveryData", this.deliveryData);
    },
    setDelivery() {
      this.checkDeliveryValidity();
      if (this.messages.length === 0) {
        this.setDeliveryData();
        this.deliveryData["user_id"] = this.user.id;
        axios
          .post(this.$baseUrl + "/set-default-delivery", this.deliveryData)
          .then(() => {
            this.$emit("result", "Delivery defaults changed successfully");
          })
          .catch((error) => {
            console.log("error", error);
          });
      } else {
        this.$emit("result", this.messages);
      }
    },
    getDelivery() {
      axios
        .get(`${this.$baseUrl}/get-default-delivery/${this.user.id}`)
        .then((response) => {
          let data = response.data;

          this.firstName = data.first_name;
          this.lastName = data.last_name;
          this.street = data.street;
          this.apartmentNumber = data.apartment_number;
          this.city = data.city;
          this.zipCode = data.zip_code;
          this.phone = data.phone;
          this.email = data.email;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
  mounted() {
    this.getDelivery();
  },
  watch: {
    orderClicked(newVal) {
      if (newVal == true) {
        this.checkDeliveryValidity();
      }
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.form {
  display: grid;
  gap: 20px;

  .bottom {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 10px;
  }
  .row {
    display: grid;
    width: 100%;
    align-items: start;

    .form-heading {
      grid-column: span 1;
    }

    .inputs-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .address {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
    }
    .phone-input {
      display: grid;
      grid-template-columns: min-content 1fr;
      .country-code {
        display: flex;
        flex-direction: row;
        align-items: center;
        padding: 5px;
        border: 1px solid var(--border-color);
        border-right: none;
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
        input {
          max-width: 40px;
          text-align: center;
          height: 100%;
        }
      }
      .primary-input {
        width: auto;
      }
    }
  }
}
</style>