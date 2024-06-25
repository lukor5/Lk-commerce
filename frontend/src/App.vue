  <template>
    <template v-if="isAdminPath">
    <AdminPanel/>
  </template>
  <template v-else>
    <ShoppingBasket
      v-if="showBasket"
      @close-basket-clicked="handleToggleBasket"
      @user-not-logged-in="handleToggleOrderPopup"
    />
    <div
      :class="{
        'dark-overlay':
          showBasket ||
          showLoginPopup ||
          showOrderPopup ||
          showPaymentPopup ||
          showAddReviewPopup ||
          showUserSettingsPopup ||
          showShopReadmePopup ||
          showAddBundlePopup,
      }"
    ></div>
    <div class="hero-wrapper">
      <NavBar
        @navbar-height="navBarHeight = $event"
        @login-clicked="handleLoginClicked"
        @result="handleResult"
        @option-clicked="handleOptionClicked"
        @basket-clicked="handleToggleBasket"
        @product-clicked="handleProductClicked"
        :username="username"
      />
      <QuickList
        @scroll-to-promotions="handleScrollToPromotions" 
        @quick-access-height="quickAccessHeight = $event"
      />
      <router-view
        @product-clicked="handleProductClicked"
        @rating-clicked="handleRatingClicked"
        @result="handleResult"
        @logged-in="handleLoggedIn"
        @sessionCookieChangeRequired="setSessionCookie"
        @create-payment="handleCreatePayment"
        :paymentStatus="paymentStatus"
        @close-popup="closePopup('payment')"
        @payment-success="handlePaymentSuccess"
        @add-promotion-bundle="handleAddPromotionBundle"
        :quickAccessHeight="quickAccessHeight" :navBarHeight="navBarHeight"
      />
    </div>
    <ShopReadme v-if="showShopReadmePopup" @notice-read="handleNoticeRead" />
    <ResultPopup
      v-if="showResultPopup"
      :messages="messages"
      @animation-ended="handleAnimationEnded"
    />
    <LoginPopup
      v-if="showLoginPopup"
      @logged-in="handleLoggedIn"
      @close-popup="closePopup('login')"
      @result="handleResult"
    />
    <OrderPopup v-if="showOrderPopup" @redirected="handleRedirected" />
    <PaymentPopup
      v-if="showPaymentPopup"
      @result="handleResult"
      @payment-status="handlePaymentStatus"
      @close-popup="closePopup('payment')"
      :orderId="orderId"
    />
    <UserSettingsPopup
      v-if="showUserSettingsPopup"
      :option="optionClicked"
      @result="handleResult"
      @close-popup="closePopup('usersettings')"
      @create-payment="handleCreatePayment"
    />
    <AddReviewPopup
      v-if="showAddReviewPopup"
      @close-popup="closePopup('review')"
      @result="handleResult"
      :data="ratingData"
    />
    <AddBundlePopup
      ref="AddBundlePopup"
      v-if="showAddBundlePopup"
      @result="handleResult"
      @close-popup="closePopup('bundle')"
      :bundle="promotionBundle"
    />
    <BestSellers @product-clicked="handleProductClicked" />
    <PromotionBundleList ref="promotions" @add-bundle="handleAddBundle" />
    <PageFooter />
  </template>
</template>

  <script>
import NavBar from "./components/NavBar.vue";
import QuickList from "./components/QuickList.vue";
import BestSellers from "./components/BestSellers.vue";
import LoginPopup from "./components/LoginPopup.vue";
import ResultPopup from "./components/ResultPopup.vue";
import PageFooter from "./components/PageFooter.vue";
import ShoppingBasket from "./components/ShoppingBasket.vue";
import OrderPopup from "./components/OrderPopup.vue";
import AdminPanel from "./components/admin/AdminPanel.vue";
import AddReviewPopup from "./components/AddReviewPopup.vue";
import UserSettingsPopup from "./components/UserSettingsPopup.vue";
import PaymentPopup from "./components/PaymentPopup.vue";
import ShopReadme from "./components/ShopReadme.vue";
import PromotionBundleList from "./components/PromotionBundleList.vue";
import AddBundlePopup from "./components/AddBundlePopup.vue";
import { mapGetters, mapActions } from "vuex";
import Cookies from "js-cookie";
import axios from "axios";
import { useRoute } from "vue-router";
export default {
  name: "App",
  setup() {
    const route = useRoute();
    return { route };
  },
  components: {
    NavBar,
    QuickList,
    BestSellers,
    LoginPopup,
    ResultPopup,
    PageFooter,
    ShoppingBasket,
    UserSettingsPopup,
    OrderPopup,
    AddReviewPopup,
    AddBundlePopup,
    PaymentPopup,
    ShopReadme,
    PromotionBundleList,
    AdminPanel
  },

  data() {
    return {
      showLoginPopup: false,
      showResultPopup: false,
      message: "",
      messages: [],
      showBasket: false,
      showOrderPopup: false,
      showAddReviewPopup: false,
      showUserSettingsPopup: false,
      showPaymentPopup: false,
      showShopReadmePopup: true,
      showAddBundlePopup: false,
      isAdmin: false,
      optionClicked: "",
      paymentStatus: false,
      ratingData: [],
      orderId: null,
      promotionBundle: [],
      quickAccessHeight: 0,
      navBarHeight: 0,
    };
  },
  
  computed: {
    ...mapGetters(["user", "basket"]),
    isAdminPath() {
      return this.route.path.includes("/admin");
    }

  },
  methods: {
    ...mapActions([
      "fetchInitialProductData",
      "fetchBasket",
      "fetchOrders",
      "fetchVouchers",
    ]),
    handleProductClicked(product) {
      this.$router.push({
        name: "detailedProduct",
        params: { id: product.id },
      });
    },
    handleLoginClicked() {
      this.showLoginPopup = true;
    },
    handleOptionClicked(option) {
      this.showUserSettingsPopup = true;
      this.optionClicked = option;
    },
    handleCreatePayment(orderId) {
      this.orderId = orderId;
      this.paymentStatus = false;
      this.showPaymentPopup = true;
    },
    handlePaymentStatus(bool) {
      this.paymentStatus = bool;
      this.fetchOrders(this.user.id);
      this.fetchVouchers(this.user.id);
    },
    handlePaymentSuccess() {
      this.paymentStatus = false;
      this.closePopup("payment");
    },
    handleLoggedIn() {
      this.$store.state.orders = [];
      this.$store.state.vouchers = [];
      this.showLoginPopup = false;
      this.fetchBasket(this.user.id);
      this.fetchOrders(this.user.id);
      this.fetchVouchers(this.user.id);
    },
    handleScrollToPromotions() {
      this.$refs.promotions.$el.scrollIntoView({ behavior: "smooth" });
    },
    handleAddPromotionBundle(promotion) {
      let productIds =
        promotion.primary_product.id + "&" + promotion.discounted_product.id;
      this.$router.push({
        name: "detailedProductBundle",
        params: { ids: productIds },
      });
    },
    handleRedirected() {
      this.showOrderPopup = !this.showOrderPopup;
    },
    handleResult(result) {
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
    handleAnimationEnded() {
      this.showResultPopup = false;
    },
    handleToggleBasket() {
      if (this.basket.quantity > 0) {
        this.showBasket = !this.showBasket;
      } else if (this.basket.quantity == 0 && this.showBasket) {
        this.showBasket = !this.showBasket;
      } else {
        this.handleResult("Your basket is empty");
      }
    },
    handleAddBundle(promo) {
      this.promotionBundle = promo;
      this.showAddBundlePopup = true;
      this.$nextTick(() => {
        this.$refs.AddBundlePopup.$el.scrollIntoView({ behavior: "smooth" });
      });
    },
    handleToggleOrderPopup() {
      this.showOrderPopup = !this.showOrderPopup;
    },
    handleRatingClicked(data) {
      this.ratingData = data;
      this.showAddReviewPopup = !this.showAddReviewPopup;
    },
    handleNoticeRead() {
      this.closePopup("readme");
      Cookies.set("isRead", true);
    },
    closePopup(popup) {
      switch (popup) {
        case "login":
          this.showLoginPopup = !this.showLoginPopup;
          break;

        case "review":
          this.showAddReviewPopup = !this.showAddReviewPopup;
          break;

        case "usersettings":
          this.showUserSettingsPopup = !this.showUserSettingsPopup;
          break;

        case "payment":
          this.showPaymentPopup = false;
          break;
        case "readme":
          this.showShopReadmePopup = false;
          break;
        case "bundle":
          this.showAddBundlePopup = false;
          break;
      }
    },
    getUserIp() {
      axios.get("https://api.ipify.org?format=json").then((response) => {
        let ip = response.data.ip;
        Cookies.set("ip", ip, { expires: 1 });
        this.$store.commit("setUserIp", ip);
      });
    },

    setSessionCookie() {
      if (!Cookies.get("sessionKey")) {
        const sessionKey = Math.random().toString(36).substring(2, 15);
        Cookies.set("sessionKey", sessionKey, {
          expires: 1,
          secure: true,
          sameSite: "Lax",
        });
        this.$store.commit("setSessionKey", sessionKey);
      } else {
        this.$store.commit("setSessionKey", Cookies.get("sessionKey"));
      }
      this.$nextTick(() => {
        this.fetchBasket(
          this.user.id ? this.user.id : this.$store.state.sessionkey
        );
      });
    },
    goBack() {
      this.$router.go(-1);
    },
    goForward() {
      this.$router.go(1);
    },
    getDarkModeCookie() {
      const isDarkMode = Cookies.get("isDarkMode") === "true";
      if (isDarkMode) {
        document.body.classList.toggle("dark-mode");
      } else {
        document.body.classList.remove("dark-mode");
      }
    },
    getReadmeCookie() {
      const isRead = Cookies.get("isRead") === "true";
      this.showShopReadmePopup = !isRead;
    },
  },
  mounted() {
    this.setSessionCookie();
    this.getUserIp();
    this.fetchOrders(this.user.id);
    this.fetchVouchers(this.user.id);
    this.getDarkModeCookie();
    this.getReadmeCookie();

  },
  created() {
    this.fetchInitialProductData();
  },
  watch: {
    $route(to) {
      // Check if the current route matches the admin route
      this.isAdmin = to.path === "/admin";
    },
  },
};
</script>

  <style lang="scss">
@import "assets/styles/main.scss";

body {
  margin: 0px;
}

#app {
  display: flex;
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  flex-direction: column;
  background-color: var(--secondary-color);
}


.hero-wrapper {
  display: flex;
  min-height: 100vh;

  margin-inline: 5%;
  flex-direction: column;
  text-align: center;
  justify-content: center;
  background-color: var(--background-color);
}

router-view {
  display: flex;
  height: 100vh;
}
::-webkit-scrollbar {
  width: 10px;
}
::-webkit-scrollbar-track {
  background: var(--secondary-color);
}

::-webkit-scrollbar-thumb {
  border: 2px solid var(--background-color);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--background-color);
  cursor: pointer;
}
::-webkit-scrollbar-button {
  display: none;
  background: var(--background-color);
}
</style>
