<template>
  <div class="orders-wrapper">
    <div class="order-nav">
      <ul>
        <li>
          <button
            @click="getOrdersByStatus('All')"
            class="dark-button"
            :class="{ 'primary-button': activeStatus === 'All' }"
          >
            All
          </button>
        </li>
        <li v-for="(status, index) in deliveryStatusArray" :key="index">
          <button
            @click="getOrdersByStatus(status.status)"
            class="dark-button"
            :class="{ 'primary-button ': activeStatus === status.status }"
          >
            {{ status.status }} <b>({{ status.count }})</b>
          </button>
        </li>
      </ul>
    </div>
    <AdminSearchBar
      @search-input="handleSearchInput"
      :placeholder="'Search orders ...'"
      :userToSearch="this.username"
    />
    <div class="grid-container">
      <div class="orders">
        <div
          v-for="(order, index) in paginatedOrders"
          @click="handleOrderClicked(order)"
          class="order-preview"
          :key="index"
        >
          <div class="top-row">
            <h2>Order ID: {{ order.id }}</h2>
            <div
              class="status"
              :style="'background: blue; color: white;'"
              v-if="order.status == 'Ordered'"
            >
              <b>Ordered</b>
              <font-awesome-icon :icon="['fas', 'cart-shopping']" />
            </div>
            <div
              class="status"
              :style="'background: green; color: white;'"
              v-if="order.status == 'Paid'"
            >
              <b>Paid</b>
              <font-awesome-icon :icon="['fas', 'money-check-dollar']" />
            </div>
            <div
              class="status"
              :style="'background: orange; color: white;'"
              v-if="order.status == 'Sent'"
            >
              <b>Sent</b>
              <font-awesome-icon :icon="['fas', 'envelope-circle-check']" />
            </div>
            <div
              class="status"
              :style="'background: purple; color: white;'"
              v-if="order.status == 'Delivered'"
            >
              <b>Delivered</b> <font-awesome-icon :icon="['fas', 'check']" />
            </div>
          </div>
          <div class="row">
            <div class="column">
              <label> Ordered on </label>
              {{ order.date }}
            </div>
          </div>
          <div class="row">
            <b>User: </b> <b v-if="order.user">{{ order.user.username }}</b>
            <b v-else>None</b>
          </div>
          <div class="row">
            <div class="column">
              <label>City</label>
              <span>{{ order.delivery.city }}</span>
            </div>
            <div class="column">
              <label>Zip code</label>
              <span>{{ order.delivery.zip_code }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <AdminPagination
      @page-clicked="handlePageClicked"
      :perPage="12"
      :length="this.foundOrders.length"
    />
  </div>
</template>
<script>
import axios from "axios";
import AdminSearchBar from "./AdminSearchBar.vue";
import AdminPagination from "./AdminPagination.vue";
export default {
  name: "OrderList",
  components: {
    AdminSearchBar,
    AdminPagination,
  },
  props: ["username"],
  computed: {
    formattedOrders() {
      return this.filteredOrders.map((order) => ({
        ...order,
        date: new Date(order.created_at).toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        }),
      }));
    },
    foundOrders() {
      let searchPhrase = this.searchPhrase || "";
      return this.formattedOrders.filter((order) => {
        if (order.user) {
          return (
            order.id.toString().includes(searchPhrase) ||
            order.delivery.city
              .toLowerCase()
              .includes(searchPhrase.toLowerCase()) ||
            order.user.username
              .toLowerCase()
              .includes(searchPhrase.toLowerCase())
          );
        } else {
          return (
            order.id.toString().includes(searchPhrase) ||
            order.delivery.city
              .toLowerCase()
              .includes(searchPhrase.toLowerCase())
          );
        }
      });
    },
    paginatedOrders() {
      const start = this.currentPage * 12;
      const end = start + 12;
      return this.foundOrders.slice(start, end);
    },
  },
  data() {
    return {
      orders: [],
      filteredOrders: [],
      deliveryStatusArray: [],
      baseUrl: this.$baseUrl,
      activeStatus: "All",
      searchPhrase: "",
      currentPage: 0,
    };
  },
  methods: {
    getOrders() {
      axios
        .get(this.baseUrl + "/orders")
        .then((response) => {
          this.orders = response.data;
          if (this.username) {
            this.filteredOrders = this.orders.filter(
              (order) => order.user && order.user.username === this.username
            );
          } else {
            this.filteredOrders = this.orders;
          }
          this.sortOrdersByDate();
          this.getDeliveryStatuses();
        })
        .catch((error) => {
          console.log("error: ", error);
        });
    },
    handleOrderClicked(order) {
      this.$emit("order-clicked", order);
    },
    getDeliveryStatuses() {
      const statuses = {};
      this.orders.forEach((order) => {
        const status = order.status;
        if (statuses[status]) {
          statuses[status]++;
        } else {
          statuses[status] = 1;
        }
      });
      for (const status in statuses) {
        this.deliveryStatusArray.push({
          status: status,
          count: statuses[status],
        });
      }
    },
    handlePageClicked(pageIndex) {
      this.currentPage = pageIndex;
    },
    sortOrdersByDate() {
      this.orders.sort((a, b) => {
        const dateA = new Date(a.created_at);
        const dateB = new Date(b.created_at);
        if (dateB - dateA !== 0) {
          return dateB - dateA;
        } else {
          return a.id - b.id;
        }
      });
    },

    getOrdersByStatus(status) {
      if (status == "All") {
        this.activeStatus = "All";
        this.filteredOrders = this.orders;
      } else {
        this.activeStatus = status;
        this.filteredOrders = this.orders.filter(
          (order) => order.status == status
        );
      }
    },
    handleSearchInput(string) {
      this.searchPhrase = string;
    },
  },
  mounted() {
    this.getOrders();
  },
};
</script>

<style lang="scss">
@import "../../assets/styles/main.scss";

.orders-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-inline: 5vw;
  gap: 20px;

  .order-nav {
    display: flex;
    flex-direction: row;
    justify-content: center;
    background-color: var(--lighter-dark-color);
    color: white;

    ul {
      padding: 10px;
      display: flex;
      flex-direction: row;
      gap: 10px;
      li {
        list-style: none;
        padding: 0;
      }
    }
  }

  .grid-container {
    .orders {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      grid-template-rows: auto auto auto auto;
      gap: 10px;

      .order-preview {
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
          .status {
            padding: 5px;
            border-radius: 15px;
          }
        }
        .row {
          display: flex;
          flex-direction: row;
          gap: 20px;
          align-items: center;
          .column {
            display: flex;
            flex-direction: column;
            label {
              @include small-text;
            }
          }
        }
      }

      .order-preview:hover {
        cursor: pointer;
        background-color: var(--primary-color);
        color: white;
      }
    }
  }
}
@media (max-width: 1000px) {
  .orders-wrapper {
    .grid-container {
      .orders {
        grid-template-columns: 1fr 1fr 1fr;
      }
    }
  }
}
@media (max-width: 700px) {
  .orders-wrapper {
    .grid-container {
      .orders {
        grid-template-columns: 1fr 1fr;
      }
    }
  }
}
</style>
