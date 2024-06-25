<template>
  <div class="payment-list">
    <div class="search-bar">
      <AdminSearchBar
        @search-input="handleSearchInput"
        :placeholder="'Search orders ...'"
      />
    </div>
    <div class="grid-container">
      <div class="payments">
        <div
          v-for="(payment, index) in paginatedPaymentList"
          :key="index"
          class="payment"
        >
          <div class="top-row">
            <h2>Payment ID: {{ payment.id }}</h2>
            <b>{{ this.toReadableDate(payment.payment_date) }}</b>
          </div>
          <div class="row">
            <div class="column">
              <label>Card number</label>
              <div class="card-row">
                <font-awesome-icon :icon="['far', 'credit-card']" /><b>{{
                  payment.card_number_obfuscated
                }}</b>
              </div>
            </div>
            <div class="column">
              <label>Expiry date</label>
              <b>{{ payment.expiry_date }}</b>
            </div>
          </div>
          <div class="row">
            <h3>Amount:</h3>
            <span>{{ payment.amount }} $</span>
          </div>
        </div>
      </div>
    </div>
    <AdminPagination
      :page-clicked="handlePageClicked"
      :length="payments.length"
      :perPage="16"
    />
  </div>
</template>
<script>
import axios from "axios";
import AdminPagination from "./AdminPagination.vue";
import AdminSearchBar from "./AdminSearchBar.vue";
export default {
  name: "AdminPaymentList",
  components: {
    AdminPagination,
    AdminSearchBar,
  },
  computed: {
    foundPayments() {
      let searchPhrase = this.searchPhrase || "";
      return this.payments.filter((payment) => {
        let readableDate = this.toReadableDate(
          payment.payment_date
        ).toLowerCase();
        let paymentID = payment.id.toString().toLowerCase();
        let amount = payment.amount.toString().toLowerCase();
        let cardNumber = payment.card_number_obfuscated.toLowerCase();

        return (
          readableDate.includes(searchPhrase) ||
          paymentID.includes(searchPhrase) ||
          amount.includes(searchPhrase) ||
          cardNumber.includes(searchPhrase)
        );
      });
    },
    paginatedPaymentList() {
      const start = this.currentPage * 12;
      const end = start + 12;
      return this.foundPayments.slice(start, end);
    },
  },
  data() {
    return {
      payments: [],
      baseUrl: this.$baseUrl,
      currentPage: 0,
      searchPhrase: "",
    };
  },
  methods: {
    getPayments() {
      axios
        .get(`${this.baseUrl}/payments`)
        .then((response) => {
          this.payments = response.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    toReadableDate(date) {
      let formatted_date;
      formatted_date = new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
      return formatted_date;
    },
    handlePageClicked(pageIndex) {
      this.currentPage = pageIndex;
    },
    handleSearchInput(string) {
      this.searchPhrase = string;
    },
  },
  mounted() {
    this.getPayments();
  },
};
</script>
<style lang="scss" >
@import "../../assets/styles/main.scss";
.payment-list {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-inline: 5vw;
  gap: 20px;
  margin-top: 20px;
  .search-bar {
    display: flex;
    flex-direction: row;
  }
  .grid-container {
    .payments {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      grid-template-rows: 1fr 1fr 1fr auto;
      gap: 10px;
      .payment {
        border: 1px solid var(--border-color);

        padding: 10px;
        border-radius: 10px;
        gap: 15px;
        display: flex;
        flex-direction: column;
        text-align: left;
        .top-row {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: space-between;
        }
        .row {
          display: flex;
          flex-direction: row;
          gap: 20px;
          align-items: center;
          .column {
            display: flex;
            flex-direction: column;
            .card-row {
              display: flex;
              flex-direction: row;
              gap: 5px;
              align-items: center;
            }
            label {
              @include small-text;
            }
          }
        }
      }
    }
  }
}
@media (max-width: 1400px) {
  .payment-list {
    .grid-container {
      .payments {
        grid-template-columns: 1fr 1fr 1fr;
      }
    }
  }
}
@media (max-width: 1050px) {
  .payment-list {
    .grid-container {
      .payments {
        grid-template-columns: 1fr 1fr;
        .payment {
        }
      }
    }
  }
}
</style>