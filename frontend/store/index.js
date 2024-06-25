import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || {
        id: null,
        username: null,
        isAdmin: false,
      },
      basket: {
        quantity: null,
        basketItems: [],
        totalPrice: null,
      },
      notifications: {
        quantity: null,
        messages: [],
      },
      productList: [],
      originalProductList: [],
      allProductList: [],
      activeFilters: [],
      categoryList: [],
      orders: [],
      vouchers: [],
      bundleProducts: [],
      sessionKey: null,
      userIp: null,

    };
  },
  mutations: {
    setUser(state, payload) {
      state.user.id = payload.id;
      state.user.username = payload.username;
      state.user.isAdmin = payload.isAdmin;
      localStorage.setItem('user', JSON.stringify(state.user));
    },
    setBasket(state, payload) {
      state.basket.quantity = payload.quantity;
      state.basket.basketItems = payload.basketItems
      state.basket.totalPrice = payload.totalPrice
    },
    setNotifications(state, payload) {
      state.notifications.quantity = payload.quantity
      state.notifications.messages = payload.messages
    },
    setOrders(state, orders) {
      state.orders = orders;
    },
    setVouchers(state, vouchers) {
      state.vouchers = vouchers;
    },
    setBundleProducts(state, bundleProducts) {
      state.bundleProducts = bundleProducts
    },
    addBundleProduct(state, bundleProduct) {
      const index = state.bundleProducts.findIndex(product => product.id === bundleProduct.id);
      if (index !== -1) {
        state.bundleProducts.splice(index, 1, bundleProduct);
      } else {
        state.bundleProducts.push(bundleProduct)
      }
    },

    clearBundleProducts(state) {
      state.bundleProducts = [];
    },

    setBasketItem(state, basketItem) {
      const index = state.basket.basketItems.findIndex(item => item.id === basketItem.id);
      if (index === -1) {
        state.basket.basketItems.push(basketItem)
      } else {
        state.basket.basketItems[index].quantity += 1
      }

    },
    setSessionKey(state, sessionKey) {
      state.sessionKey = sessionKey
    },
    setUserIp(state, ip) {
      state.userIp = ip
    },
    setProductList(state, payload) {
      state.productList = payload
    },
    setAllProductList(state, payload) {
      state.allProductList = payload
    },
    setOriginalProductList(state, payload) {
      state.originalProductList = payload
    },
    setCategoryList(state, payload) {
      state.categoryList = payload
    },
    setActiveFilters(state, activeFilter) {
      const index = state.activeFilters.findIndex(item => item.filter === activeFilter.filter);
      if (index !== -1) {
        state.activeFilters[index].option = activeFilter.option
      } else {
        state.activeFilters.push({ filter: activeFilter.filter, option: activeFilter.option })
      }
    },
    removeActiveFilter(state, index) {
      state.activeFilters.splice(index, 1)
    }
  },
  actions: {
    updateUser({ commit }, payload) {
      commit('setUser', payload);
    },
    updateBasket({ commit }, payload) {
      commit('setBasket', payload);
    },
    addBasketItem({ commit }, basketItem) {
      commit('setBasketItem', basketItem)
    },
    updateProductList({ commit }, payload) {
      commit('setProductList', payload);
    },
    setCategoryList({ commit }, payload) {
      commit('setCategoryList', payload)
    },
    updateActiveFilters({ commit }, activeFilter) {
      commit('setActiveFilters', activeFilter)
    },
    removeActiveFilter({ commit }, index) {
      commit('removeActiveFilter', index)
    },
    addBundleProduct({ commit }, bundleProduct) {
      commit('addBundleProduct', bundleProduct);
    },
    clearAllBundleProducts({ commit }) {
      commit('clearBundleProducts');
    },
    async fetchInitialProductData({ commit }) {
      try {
        const response = await axios.get('http://13.50.242.240:8000/shop/products');
        const products = response.data;
        commit('setProductList', products);
        commit('setOriginalProductList', products);
        commit('setAllProductList', products)
      } catch (error) {
        console.error('Error fetching initial product data:', error);
      }
    },
    async fetchBasket({ commit, state }, basketId) {
      if (state.hasInitialized) return;
      let url = 'http://13.50.242.240:8000/shop/basket/';
      if (basketId) {
        url += basketId;
      }
      axios.get(url, {
        headers: {
          'X-Session-Key': state.sessionKey
        }
      }).then(response => {
        const basketItems = response.data
        const totalPrice = basketItems[0].total_price
        let quantity = 0
        basketItems.forEach(product => {
          quantity += product.quantity
        });
        commit('setBasket', { basketId, basketItems, totalPrice, quantity });

      }).catch(error => {
        console.log('Error fetching basket', error)
      })
    },
    async fetchNotifications({ commit, state }) {
      if (state.hasInitialized) return;
      const url = 'http://13.50.242.240:8000/shop/notifications';
      try {
      const response = await axios.get(url);
      const messages = response.data;
      const quantity = Array.isArray(messages) ? messages.length : Object.keys(messages).length;
      commit('setNotifications', { messages, quantity });
    } catch (error) {

      console.log('Error fetching notifications:', error);
    }
    },
    async fetchOrders({ commit, state }, user_id) {
      if (state.hasInitialized) return;
      let url = 'http://13.50.242.240:8000/shop/user-orders';
      axios.get(`${url}/${user_id}`).then(response => {

        commit('setOrders', response.data)
      }).catch(error => {
        console.log('error', error)
      })
    },
    async fetchVouchers({ commit, state }, user_id) {
      if (state.hasInitialized) return;
      let url = 'http://13.50.242.240:8000/shop/user-vouchers';
      axios.get(`${url}/${user_id}`).then(response => {

        commit('setVouchers', response.data)
      }).catch(error => {
        console.log('error', error)
      })
    }
  },
  getters: {
    user(state) {
      return state.user
    },
    basket(state) {
      return state.basket
    },
    productList(state) {
      return state.productList
    },
    orders(state) {
      return state.orders
    },
    vouchers(state) {
      return state.vouchers
    },
    bundleProducts(state) {
      return state.bundleProducts
    },
    notifications(state) {
      return state.notifications
    }
  }
});