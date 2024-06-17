<template>
  <div class="user-settings-popup">
    <div class="settings-wrapper">
      <div style="position: absolute; right: 8px; top: 8px; z-index: 9999">
        <button @click="handleClosePopup" class="exit-button">
          <font-awesome-icon :icon="['fas', 'x']" />
        </button>
      </div>

      <div class="options">
        <button
          @click="changeActiveButton('Settings')"
          class="options-button"
          :class="{ active: activeButton == 'Settings' }"
        >
          Account Settings
        </button>
        <button
          @click="changeActiveButton('Orders')"
          class="options-button"
          :class="{ active: activeButton == 'Orders' }"
        >
          My Orders
        </button>
        <button
          @click="changeActiveButton('Vouchers')"
          class="options-button"
          :class="{ active: activeButton == 'Vouchers' }"
        >
          My Vouchers
        </button>
        <div class="indicator" :style="indicatorStyle"></div>
      </div>
      <div class="option-content-wrapper">
        <div
          class="content-vouchers"
          v-if="activeButton == 'Vouchers' && hasVouchers"
        >
          <div class="column-left">
            <button
              @click="setVoucherFilter('active')"
              :class="{ active: this.voucherFilter == 'active' }"
            >
              <h3>Active</h3>
            </button>
            <button
              @click="setVoucherFilter('spent')"
              :class="{ active: this.voucherFilter == 'spent' }"
            >
              <h3>Spent</h3>
            </button>
          </div>
          <div class="vouchers">
            <div class="labels">
              <h3>Code</h3>
              <h3>Discount</h3>
              <h3>Valid until</h3>
            </div>
            <div
              class="voucher-row"
              v-for="(voucher, index) in filteredVouchers"
              :key="index"
            >
              <button
                @click="copyCodeToClipboard(voucher.code)"
                class="copy-button"
              >
                <font-awesome-icon :icon="['far', 'copy']" />
                <b>{{ voucher.code }}</b>
              </button>
              <p>{{ voucher.template.discount }} $</p>
              <b>{{ toReadableDate(voucher.valid_until) }}</b>
            </div>
          </div>
        </div>
        <button id="goBackButton" v-if="showSetting" @click="handleGoBack">
          <font-awesome-icon :icon="['fas', 'arrow-left']" />
          <span>Go back</span>
        </button>
        <div class="content-settings" v-if="activeButton == 'Settings'">
          <h2 v-if="!showSetting">Your account settings</h2>
          <div v-if="!showSetting" class="buttons-wrapper">
            <button @click="handleChangePassword" class="primary-button">
              Change password
            </button>
            <button @click="handleChangeDelivery" class="primary-button">
              Delivery details
            </button>
          </div>
          <form v-if="showSetting == 'changePassword'" class="settings-form">
            <div class="password-inputs">
              <div>
                <label>Current password</label>
                <input
                  type="password"
                  class="primary-input"
                  v-model="password"
                />
              </div>
            </div>
            <div class="password-inputs">
              <div>
                <label>New password</label>
                <div class="password-icon-wrapper">
                  <span
                    v-if="!checkPasswordsValidity && newPassword !== ''"
                    class="invalid-icon"
                    >!</span
                  >
                  <span v-if="checkPasswordsValidity" class="valid-icon"
                    >✓</span
                  >
                  <input
                    type="password"
                    class="primary-input"
                    v-model="newPassword"
                  />
                </div>
              </div>
              <div>
                <label>Repeat password</label>
                <input
                  type="password"
                  class="primary-input"
                  v-model="newPasswordRepeat"
                />
              </div>
            </div>
            <div class="password-inputs">
              <button
                @click.prevent="submitPasswordChange"
                v-if="checkPasswordsFilledIn"
                class="primary-button"
              >
                Change
              </button>
              <button
                v-else
                disabled
                class="primary-button"
                :class="'disabled'"
              >
                Change
              </button>
            </div>
          </form>
          <DeliveryForm
            v-if="showSetting == 'changeDelivery'"
            :mode="'changeDelivery'"
            @result="handleResult"
          />
        </div>
        <div
          class="content-orders"
          v-if="activeButton == 'Orders' && hasOrders"
        >
          <div class="order-list">
            <h2>Your orders</h2>
            <div v-for="order in ordersPerPage" :key="order" class="order">
              <b>Order {{ order.id }}</b>
              <p>{{ toReadableDate(order.created_at) }}</p>
              <p v-if="order.delivery.delivery_method == 2">COURIER</p>
              <p v-else>POSTAL SERVICE</p>
              <div
                v-for="(orderItem, index) in order.basket.items"
                :key="index"
                class="order-item"
              >
                <span>{{ orderItem.product.name }}</span>
                <span>{{ orderItem.product.price }} $</span>
                <span>x{{ orderItem.quantity }}</span>
              </div>
              <div class="order-bottom">
                <div class="order-status">
                  <p>Status:</p>
                  <h3>{{ order.status }}</h3>
                </div>
                <div></div>
                <button
                  @click="handlePayClicked(order.id)"
                  v-if="order.status === 'Ordered'"
                  class="primary-button"
                >
                  Pay
                </button>
              </div>
            </div>
          </div>

          <div class="pagination">
            <font-awesome-icon :icon="['fas', 'chevron-left']" />
            <button
              :class="{ active: this.currentPage == index }"
              @click="changePage(index)"
              v-for="(page, index) in numberOfPages"
              :key="index"
            >
              {{ index + 1 }}
            </button>
            <font-awesome-icon :icon="['fas', 'chevron-right']" />
          </div>
        </div>
        <div class="empty" v-if="activeButton == 'Orders' && !hasOrders">
          <h1>You have no orders yet</h1>
        </div>
        <div class="empty" v-if="activeButton == 'Vouchers' && !hasVouchers">
          <h1>You have no vouchers</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";
import DeliveryForm from "./DeliveryForm.vue";

export default {
  name: "UserSettingsPopup",
  props: {
    option: String,
  },
  components: {
    DeliveryForm,
  },
  computed: {
    ...mapGetters(["vouchers", "orders", "user"]),
    hasVouchers() {
      return this.vouchers.length !== 0;
    },
    hasOrders() {
      return this.orders.length !== 0;
    },
    sortedVouchers() {
      return this.vouchers.slice().sort((a, b) => {
        return a.is_spent - b.is_spent;
      });
    },
    checkPasswordsValidity() {
      return (
        this.newPassword !== "" &&
        this.newPassword.length > 5 &&
        this.newPassword.length < 20 &&
        this.newPassword === this.newPasswordRepeat
      );
    },
    checkPasswordsFilledIn() {
      return (
        this.checkPasswordsValidity &&
        this.password.length > 5 &&
        this.password.length < 20
      );
    },
    ordersPerPage() {
      return this.orders.slice(this.firstIndex, this.secondIndex);
    },
    numberOfPages() {
      return Math.ceil(this.orders.length / 3);
    },
    filteredVouchers() {
      let filtered = [];
      if (this.voucherFilter == "active") {
        filtered = this.vouchers.filter((voucher) => voucher.is_spent == false);
      }
      if (this.voucherFilter == "spent") {
        filtered = this.vouchers.filter((voucher) => voucher.is_spent == true);
      }
      return filtered;
    },
  },
  data() {
    return {
      activeButton: "",
      indicatorStyle: {
        left: "0px",
        width: "0px",
      },
      showSetting: "",
      password: "",
      newPassword: "",
      newPasswordRepeat: "",
      baseUrl: this.$baseUrl,
      paginatedOrders: [],
      firstIndex: 0,
      secondIndex: 3,
      currentPage: 0,
      voucherFilter: "active",
    };
  },
  methods: {
    ...mapActions(["updateUser", "updateBasket"]),
    changeActiveButton(option) {
      this.showSetting = null;
      this.activeButton = option;
      this.updateIndicatorPosition();
    },
    updateIndicatorPosition() {
      this.$nextTick(() => {
        const activeBtn = this.$el.querySelector(".options-button.active");
        if (activeBtn) {
          this.indicatorStyle = {
            left: `${activeBtn.offsetLeft}px`,
            width: `${activeBtn.offsetWidth}px`,
          };
        }
      });
    },
    changePage(index) {
      if (index === 0) {
        this.firstIndex = 0;
        this.secondIndex = 3;
      } else {
        this.firstIndex = index * 3;
        this.secondIndex = this.firstIndex + 3;
      }
      this.currentPage = index;
    },
    handlePayClicked(id) {
      this.$emit("create-payment", id);
    },

    toReadableDate(dateString) {
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      return `${day}-${month}-${year}`;
    },
    copyCodeToClipboard(code) {
      navigator.clipboard
        .writeText(code)
        .then(() => {
          this.$emit("result", "Code copied to clipboard");
        })
        .catch((err) => {
          console.error("Failed to copy text: ", err);
        });
    },
    handleClosePopup() {
      this.$emit("close-popup");
    },
    handleChangePassword() {
      this.showSetting = "changePassword";
    },
    handleChangeDelivery() {
      this.showSetting = "changeDelivery";
    },
    handleGoBack() {
      this.showSetting = null;
    },
    handleResult(result) {
      this.$emit("result", result);
    },
    setVoucherFilter(filter) {
      this.voucherFilter = filter;
    },
    submitPasswordChange() {
      const data = {
        password: this.password,
        new_password: this.newPassword,
      };
      axios
        .post(`${this.baseUrl}/change-password/${this.user.id}`, data)
        .then((response) => {
          if (response.status === 200) {
            this.updateUser({ id: null, username: null });
            this.updateBasket({
              basketItems: null,
              quantity: null,
              totalPrice: null,
            });
            this.$router.push("/");
            this.$emit("result", "Password changed succesfully, logged out");
            this.$emit("close-popup");
          }
        })
        .catch((error) => {
          this.$emit("result", "Password change failed");
          console.log('error', error)
        });
    },
  },
  mounted() {
    this.activeButton = this.option;
    this.updateIndicatorPosition();
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.user-settings-popup {
  display: flex;
  position: absolute;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  z-index: 10;

  .settings-wrapper {
    background-color: var(--background-color);
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    position: relative;
    min-width: 600px;
    min-height: 300px;

    .options {
      position: relative;
      display: flex;
      flex-direction: row;
      gap: 20px;
      padding-top: 30px;

      .options-button {
        position: relative;
        flex: 1;
        padding-inline: 15px;
        padding-bottom: 5px;
      }

      .active {
        text-shadow: 1px 0 0 currentColor;
      }

      .indicator {
        position: absolute;
        bottom: 0;
        height: 4px;
        background-color: var(--secondary-color);
        transition: left 0.3s ease, width 0.3s ease;
        z-index: 0;
      }
    }

    .option-content-wrapper {
      min-height: 40vh;
      min-width: 30vw;
      display: grid;
      grid-template-columns: 1fr;
      position: relative;

      #goBackButton {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
        width: min-content;
        min-height: 43px;
        padding-inline: 10px;
        transition: color 0.3s ease;
        span {
          transition: color 0.3s ease;
          @include small-text;
          text-wrap: nowrap;
        }

        &:hover {
          color: red;
          span {
            color: var(--secondary-color);
          }
        }
      }

      .empty {
        display: flex;
        justify-content: center;
        margin-top: 10%;
      }

      .content-orders {
        .pagination {
          .active {
            background-color: var(--secondary-color);
            border-radius: 15px;
            color: white;
          }
        }

        .order-list {
          height: 60vh;
          overflow-y: scroll;

          .order {
            padding: 20px;
            text-align: left;
            border-bottom: 1px solid var(--subtle-border-color);

            p {
              @include small-text;
            }

            .order-item {
              display: grid;
              grid-template-columns: 1fr 1fr 1fr;
            }
            .order-bottom {
              display: grid;
              grid-template-columns: 1fr 1fr 1fr;
              .primary-button {
                width: min-content;
                justify-self: end;
              }
            }
          }
        }
      }

      .content-settings {
        display: flex;
        flex-direction: column;
        padding: 40px;
        padding-top: 20px;
        text-align: left;

        .buttons-wrapper {
          display: flex;
          flex-direction: row;
          height: 100%;
          justify-content: center;
          gap: 10px;
          margin-top: 20px;

          .primary-button {
            height: min-content;
            width: 35%;
            border-radius: 15px;
            border: 2px solid var(--secondary-color);
            background-color: var(--background-color);
            color: var(--text-color);
          }
          .primary-button:hover {
            background-color: var(--secondary-color);
            color: white;
          }
        }

        .settings-form {
          display: grid;
          grid-template-columns: 1fr;

          gap: 20px;

          .password-inputs {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            text-align: left;

            .primary-button.disabled {
              background-color: gray;
              color: white;
              cursor: not-allowed;
            }

            div {
              display: grid;
              grid-template-rows: auto 1fr;
              align-items: center;

              span {
                display: flex;
                position: absolute;
                left: 10px;

                font-size: 30px;
                font-weight: bold;
              }

              .invalid-icon {
                color: red;
              }

              .valid-icon {
                color: green;
              }
            }
          }
        }
      }

      .content-vouchers {
        padding: 20px;
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 50px;

        .column-left {
          display: grid;
          grid-template-rows: min-content min-content;
          gap: 20px;
          border-right: 1px solid var(--subtle-border-color);
          padding-right: 10px;

          button {
            padding: 5px;
            border-radius: 15px;
          }

          .active {
            @include secondary-button;
          }
        }

        .vouchers {
          .labels {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            padding-bottom: 20px;
            text-align: left;
            gap: 20px;
          }

          .voucher-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;

            .copy-button {
              display: flex;
              flex-direction: row;
              gap: 10px;
              align-items: center;
            }
          }
        }
      }
    }
  }
}

::-webkit-scrollbar-track {
  background: var(--background-color);
}

::-webkit-scrollbar-thumb {
  background: var(--secondary-color);
}

@media (max-width: 630px) {
  .user-settings-popup {
    .settings-wrapper {
      min-height: 0;
      min-width: 90%;
    }
  }
}
</style>