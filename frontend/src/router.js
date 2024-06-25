import { createWebHashHistory, createRouter } from 'vue-router'

import HeroSection from './components/HeroSection.vue'
import DetailedProduct from './components/DetailedProduct.vue'
import ProductList from './components/ProductList.vue'
import OrderForm from './components/OrderForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import OrderList from './components/admin/OrderList.vue'
import AdminBundleList from './components/admin/AdminBundleList.vue'
import AdminUserList from './components/admin/AdminUserList.vue'
import AdminPaymentList from './components/admin/AdminPaymentList.vue'


const routes = [
  { path: '/', component: HeroSection },
  { path: '/product/:id', name: 'detailedProduct', component: DetailedProduct, props: true},
  { path: '/promotion/:ids', name: 'detailedProductBundle', component: DetailedProduct, props: true },
  { path: '/products/:category/:type', name:'productList', component: ProductList, props: true},
  { path: '/order', name: 'orderForm', component: OrderForm, props: true},
  { path: '/register', name: 'registerForm', component: RegisterForm, props: true},
  { path: '/products/new', name: 'newProductList', component: ProductList},

  //Admin routes
  { path: '/admin', name: 'adminPanel' },
  { path: '/admin/orders', component: OrderList, name: 'orderList', props: (route) => ({ username: route.query.username }) },
  { path: '/admin/bundles', component: AdminBundleList, name: 'adminBundleList' },
  { path: '/admin/users', component: AdminUserList, name: 'adminUserList' },
  { path: '/admin/payments', component: AdminPaymentList, name: 'adminPaymentList' },
]


const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router