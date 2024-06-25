<template>
  <ResultPopup v-if="showResultPopup" :messages="messages" />
  <LoginPopup
    v-if="!this.user.id || !isAdmin"
    @logged-in="handleSuccesfulLogin, handleResultMessage"
    :userToLogIn="'Admin'"
  />
  <div class="admin-panel-wrapper" v-if="this.user.id && isAdmin">
    <div
      :class="{
        'dark-overlay':
          showCreateBundle ||
          showOrderPopup ||
          showProductPopup ||
          showEmailPopup,
      }"
    ></div>
    <AdminNavBar
      @add-product-clicked="handleAddProductClicked"
      @product-clicked="handleProductClicked"
      @show-orders="handleShowOrders"
      @show-create-bundle="handleShowCreateBundle"
      @go-home="handleGoHome"
    />
    <div class="main">
      <router-view
        v-if="isRouterView"
        @send-email-clicked="handleEmailClicked"
        @order-clicked="handleOrderClicked"
        @bundle-clicked="handleBundleClicked"
      ></router-view>
      <div class="admin-content" v-else>
        <div class="warning-container">
          <font-awesome-icon
            :icon="['fas', 'triangle-exclamation']"
            class="fa-lg"
          />
          <b>Warning!</b>
          <p>{{ lowStockCount }} product variants on low stock!</p>
        </div>
        <div class="chart-grid-wrapper">
          <div class="charts">
            <SalesChart />
            <CategoryChart />
          </div>
          <div class="grid-container">
            <h1>Administrator Panel</h1>
            <div class="nav-grid">
              <div class="column">
                <button @click="redirectTo('Bundles')" class="button-big">
                  <h2>Bundles</h2>
                </button>
                <button @click="redirectTo('Orders')" class="button-big">
                  <h2>Orders</h2>
                </button>
              </div>
              <div class="column">
                <button @click="redirectTo('Users')" class="button-big">
                  <h2>Users</h2>
                </button>
                <button @click="redirectTo('Payments')" class="button-big">
                  <h2>Payments</h2>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AddProductPopup
    v-if="showProductPopup"
    @result="handleResultMessage"
    @close-popup="handleClosePopup('AddProductPopup')"
    :productId="productId"
  />
  <EditOrderPopup
    v-if="showOrderPopup"
    :order="selectedOrder"
    @close-popup="handleClosePopup('EditOrderPopup')"
  />
  <CreateBundlePopup
    v-if="showCreateBundle"
    @close-popup="handleClosePopup('CreateBundlePopup')"
    @result="handleResultMessage"
    :promotion="promotion"
  />
  <SendEmailPopup
    v-if="showEmailPopup"
    @close-popup="handleClosePopup('SendEmailPopup')"
    :userToEmail="userToEmail"
  />
</template>

<script>
import LoginPopup from "../LoginPopup.vue";
import ResultPopup from "../ResultPopup.vue";
import AdminNavBar from "./AdminNavBar.vue";
import AddProductPopup from "./AddProductPopup.vue";
import SendEmailPopup from "./SendEmailPopup.vue";
import EditOrderPopup from "./EditOrderPopup.vue";
import CreateBundlePopup from "./CreateBundlePopup.vue";
import SalesChart from "./SalesChart.vue";
import CategoryChart from "./CategoryChart.vue";
import { mapState } from "vuex";
import { useRoute } from "vue-router";
import axios from "axios";

export default {
  name: "AdminPanel",
  setup() {
    const route = useRoute();
    return { route };
  },
  components: {
    LoginPopup,
    ResultPopup,
    AdminNavBar,
    AddProductPopup,
    SendEmailPopup,
    EditOrderPopup,
    CreateBundlePopup,
    SalesChart,
    CategoryChart,
  },
  computed: {
    ...mapState(["user"]),
    isAdmin() {
      return this.user.isAdmin;
    },
    isRouterView() {
      let path = this.route.path;
      return path.startsWith("/admin") && path.length > "/admin".length;
    },
    lowStockCount() {
      return this.lowStockVariants.length;
    },
  },
  data() {
    return {
      showResultPopup: false,
      showProductPopup: false,
      showOrderPopup: false,
      selectedOrder: null,
      showOrders: false,
      showCreateBundle: false,
      showEmailPopup: false,
      productId: null,
      promotion: null,
      messages: [],
      userToEmail: null,
      lowStockVariants: [],
      baseUrl: this.$baseUrl,
    };
  },
  methods: {
    handleSuccesfulLogin() {
      this.showResultPopup = !this.showResultPopup;
      this.messages.push("Admin logged in succesfully");
      setTimeout(() => {
        this.showResultPopup = !this.showResultPopup;
      }, 4000);
    },
    handleClosePopup(popupName) {
      switch (popupName) {
        case "EditOrderPopup":
          this.showOrderPopup = false;
          break;

        case "AddProductPopup":
          this.showProductPopup = false;
          this.productId = null;
          break;
        case "CreateBundlePopup":
          this.showCreateBundle = false;
          break;
        case "SendEmailPopup":
          this.showEmailPopup = false;
          break;
      }
    },
    handleAddProductClicked() {
      this.showProductPopup = true;
    },
    handleProductClicked(id) {
      this.productId = id;
      this.showProductPopup = true;
    },
    handleEmailClicked(user) {
      this.userToEmail = user;
      this.showEmailPopup = !this.showEmailPopup;
    },
    handleOrderClicked(order) {
      this.selectedOrder = order;
      this.showOrderPopup = !this.showOrderPopup;
    },
    handleBundleClicked(promotion) {
      this.promotion = promotion;
      this.showCreateBundle = !this.showCreateBundle;
    },
    handleResultMessage(result) {
      this.showResultPopup = false;
      this.$nextTick(() => {
        if (Array.isArray(result)) {
          this.messages = result;
        } else {
          this.messages = [result];
        }
        this.showResultPopup = true;
      });
    },
    handleGoHome() {
      this.showCreateBundle = false;
      this.showOrderPopup = false;
      this.showOrders = false;
      this.showProductPopup = false;
    },
    handleShowOrders() {
      this.showOrders = true;
    },
    handleShowCreateBundle() {
      this.showCreateBundle = true;
    },
    handleWarningClicked() {
      this.$router.push("/");
    },
    getLowOnStock() {
      axios
        .get(`${this.baseUrl}/low-stock`)
        .then((response) => {
          this.lowStockVariants = response.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    redirectTo(name) {
      switch (name) {
        case "Orders":
          this.$router.push("/admin/orders");
          break;
        case "Bundles":
          this.$router.push("/admin/bundles");
          break;
        case "Users":
          this.$router.push("/admin/users");
          break;
        case "Payments":
          this.$router.push("/admin/payments");
          break;
        default:
          break;
      }
    },
  },
  mounted() {
    this.getLowOnStock();
  },
};
</script>

<style lang="scss" scoped >
@import "../../assets/styles/main.scss";

.admin-panel-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-color);
  .main {
    display: flex;
    flex: 1;
    width: 100vw;
    justify-content: center;
    height: 100%;
    flex-wrap: wrap;
    overflow-y: scroll;
    .admin-content {
      display: flex;
      flex-direction: column;
      margin-inline: 5vw;
      width: 100%;
      height: 100%;
      gap: 10px;
      .warning-container {
        display: inline-flex;
        width: fit-content;
        gap: 10px;
        padding: 5px;
        padding-inline: 10px;
        border-radius: 15px;
        border: 1px solid var(--secondary-color);
        background-color: var(--secondary-color);
        color: white;
      }
      .chart-grid-wrapper {
        display: flex;
        flex-direction: row;
        flex: 1;
        width: 100%;
        gap: 20px;
        justify-content: center;
        .charts {
          display: flex;
          flex-direction: column;
          gap: 20px;
          width: 35%;
        }
        .grid-container {
          display: flex;
          flex-direction: column;
          flex: 1;
          margin-bottom: 15px;
        }

        .nav-grid {
          display: grid;
          grid-template-columns: auto auto;
          gap: 10px;
          height: 100%;
          .column {
            display: grid;
            grid-template-rows: auto auto;
            gap: 10px;
            .button-big {
              border: 1px solid var(--border-color);
              text-align: center;
              h2 {
                font-size: 30px;
                letter-spacing: 3px;
              }
            }
            .button-big:hover {
              background-color: var(--primary-color);
              color: white;
            }
          }
        }
      }
    }
  }
}
@media (max-width: 1200px) {
  .admin-panel-wrapper {
    .main {
      .admin-content {
        .chart-grid-wrapper {
          flex-direction: column-reverse;
          gap: 0px;
          .charts {
            flex-direction: row;
            width: 100%;
            justify-content: center;
            .canvas-wrapper {
              width: 40vw;
              max-height: 50vh;
            }
          }
        }
      }
    }
  }
}
@media (max-width: 800px) {
  .admin-panel-wrapper {
    .main {
      .admin-content {
        .chart-grid-wrapper {
          .charts {
            flex-direction: column;
            justify-content: center;
            align-items: center;
            .canvas-wrapper {
              flex: 0;
              width: 70%;
              max-height: 50vh;
            }
          }
        }
      }
    }
  }
}
</style>