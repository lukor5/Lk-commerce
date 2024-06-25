<template>
  <div class="nav-bar">
    <div class="admin-options">
      <button @click="goHome">
        <font-awesome-icon :icon="['fas', 'house-chimney']" class="fa-xl" />
      </button>
      <button @click="showAddProductPopup">Add Product</button>
      <button @click="showOrders">Orders</button>
      <button @click="showCreateBundlePopup">Create Bundle</button>

      <div class="search-dropdown-wrapper">
        <div class="search-bar">
          <SearchBar
            @dropdown-toggled="handleDropdownToggled"
            @product-clicked="handleProductClicked"
            :closeDropdown="this.showSearchResults"
            :admin="true"
          />
        </div>
      </div>
      <div class="notifications-button-wrapper">
        <div @click="showNotifications" class="buttons">
          <button class="notifications-button">
            <font-awesome-icon :icon="['fas', 'bell']" class="fa-xl" />
          </button>
          <span v-if="notificationsQuantity > 0" class="notifications-quantity">
            {{ notificationsQuantity }}</span
          >
        </div>
        <div
          class="dropdown-notifications"
          :class="{ 'show-dropdown': showNotificationDropdown }"
        >
          <div class="notifications-dropdown-list">
            <div class="top">
              <h3>Notifications</h3>
              <div class="top-buttons">
                <button
                  class="notification-button"
                  @click="this.active = 'Unread'"
                  :class="{ active: active == 'Unread' }"
                >
                  Unread
                </button>
                <button
                  class="notification-button"
                  @click="this.active = 'All'"
                  :class="{ active: active == 'All' }"
                >
                  All
                </button>
              </div>
            </div>
            <ul v-if="this.active == 'Unread'">
              <li
                v-for="(notification, index) in notifications.messages"
                :key="index"
              >
                {{ notification.message }}
              </li>
            </ul>
            <ul v-if="this.active == 'All'">
              <li
                v-for="(notification, index) in allNotifications"
                :key="index"
              >
                {{ notification.message }}
              </li>
            </ul>
            <div
              v-if="active == 'Unread' && notificationsQuantity > 0"
              class="bottom"
            >
              <span>Mark as read</span>
              <input type="checkbox" v-model="markAsRead" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "../SearchBar.vue";
import { mapActions, mapGetters } from "vuex";
import axios from "axios";
export default {
  name: "AdminNavBar",
  components: {
    SearchBar,
  },
  computed: {
    ...mapGetters(["notifications"]),
    notificationsQuantity() {
      return this.notifications.quantity;
    },
  },
  data() {
    return {
      showSearchResults: false,
      showNotificationDropdown: false,
      baseUrl: this.$baseUrl,
      active: "Unread",
      markAsRead: false,
      allNotifications: [],
    };
  },
  methods: {
    ...mapActions(["fetchNotifications"]),
    showAddProductPopup() {
      this.$emit("add-product-clicked");
    },
    showOrders() {
      this.$router.push("/admin/orders");
    },
    showCreateBundlePopup() {
      this.$emit("show-create-bundle");
    },
    showNotifications() {
      this.showNotificationDropdown = !this.showNotificationDropdown;
    },
    handleProductClicked(id) {
      this.$emit("product-clicked", id);
    },
    closeDropdowns(event) {
      const isSearchResults =
        event.target.closest(".dropdown-products") !== null;
      const isNotificationDropdown =
        event.target.closest(".notifications-button-wrapper") !== null;
      if (!isSearchResults) {
        this.showSearchResults = false;
      }
      if (!isNotificationDropdown) {
        this.showNotificationDropdown = false;
      }
    },
    handleDropdownToggled(dropdown, type) {
      switch (type) {
        case "category":
          this.showDropdown = dropdown;
          break;
        case "search":
          this.showSearchResults = dropdown;
          break;
        default:
          break;
      }
    },
    fetchAllNotifications() {
      axios
        .get(`${this.baseUrl}/all-notifications`)
        .then((response) => {
          this.allNotifications = response.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    handleMarkAllAsRead() {
      const data = {
        user_id: this.$store.state.user.id,
      };
      axios
        .post(`${this.baseUrl}/mark-all-as-read`, data)
        .then((response) => {
          if (response.status == 200) {
            this.fetchNotifications();
          }
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    goHome() {
      this.$router.push("/admin");
    },
  },
  mounted() {
    document.body.addEventListener("click", this.closeDropdowns);
    this.fetchNotifications();
  },
  watch: {
    notificationsQuantity(newValue) {
      if (newValue === 0) {
        this.active = "All";
      } else {
        this.active = "Unread";
      }
    },
    markAsRead(newValue) {
      if (newValue == true) {
        this.handleMarkAllAsRead();
      }
    },
    active(newValue) {
      if (newValue == "All") {
        this.fetchAllNotifications();
      }
    },
  },
};
</script>
<style lang="scss" >
@import "../../assets/styles/main.scss";

.nav-bar {
  display: flex;
  flex-direction: row;
  background-color: var(--background-color);
  color: var(--text-color);
  padding: 10px;

  .admin-options {
    display: flex;
    flex-direction: row;
    width: 100%;
    align-items: center;
    gap: 10px;
    margin-inline: 5%;
    button {
      &:hover {
        color: var(--primary-color);
      }
    }

    .search-bar {
      display: flex;
      align-items: stretch;
    }

    .search-dropdown-wrapper {
      position: relative;
      display: flex;
      flex-direction: column;
    }
  }

  .notifications-button-wrapper {
    margin-left: auto;
    position: relative;

    .buttons {
      position: relative;
      cursor: pointer;
      .notifications-button {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        margin: 0;
      }

      .fa-xl {
        color: var(--text-color);
      }

      .notifications-quantity {
        position: absolute;
        top: 15px;
        right: -10px;
        background-color: var(--secondary-color);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
      }
    }

    .dropdown-notifications {
      position: absolute;
      top: 40px;
      right: 0;
      width: 250px;
      background-color: var(--background-color);
      display: none;
      border-radius: 5px;
      z-index: 1000;
      max-height: 300px;
      overflow-y: auto;
      border: 1px solid var(--border-color);

      &.show-dropdown {
        display: block;
      }

      .notifications-dropdown-list {
        text-align: left;
        .top {
          display: flex;
          flex-direction: column;
          padding: 10px;
          .top-buttons {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
            gap: 15px;
            padding: 5px;
            .notification-button {
              font-weight: bold;
              padding: 10px;
              border-radius: 15px;
              flex: 1;

              &.active {
                background-color: var(--primary-color);
                color: white;
              }
            }
          }
        }
        ul {
          list-style: none;
          padding: 0;
          margin: 0;

          li {
            padding: 10px;
            border-bottom: 1px solid var(--subtle-border-color);

            &:last-child {
              border-bottom: none;
            }
          }
        }
        .bottom {
          display: flex;
          flex-direction: row;
          justify-content: flex-end;
          padding: 5px;
          gap: 2px;
          align-items: center;
          span {
            @include small-text;
          }
        }
      }
    }
  }
}
</style>