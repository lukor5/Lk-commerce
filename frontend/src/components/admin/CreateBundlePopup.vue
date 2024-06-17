<template>
  <div class="popup-wrapper">
    <div class="popup">
        <button
        class="exit-button"
        @click="$emit('close-popup')"
      >X</button>
      <h1>Create promotion bundle</h1>
      <div v-if="!primaryProduct || !discountedProduct" class="search-row">
        <h2>Add {{ productCount }} product:</h2>
        <div class="search-dropdown-wrapper">
          <div class="search-bar">
            <SearchBar
              @product-selected="handleProductSelected"
              @dropdown-toggled="handleDropdownToggled"
              :addBundleMode="true"
              :admin="true"
              :closeDropdown="this.showSearchResults"
            />
          </div>
        </div>
      </div>
      <div v-else class="search-row">
        <h2>Set discount:</h2>
        <div class="input-wrapper">
        <input
          type="number"
          class="primary-input"
          placeholder="Discount ..."
          v-model="discount"
          :max="maxDiscount"
        />
        <span>$</span>
        </div>
      </div>
      <div class="product-row">
        <div class="product-wrapper" v-if="primaryProduct">
        <PreviewProduct  :product="primaryProduct" />
        <button class="icon-button" @click="this.primaryProduct = null, this.productCount = 'primary'">Delete <font-awesome-icon :icon="['fas', 'trash']" /></button>
        </div>
        <div class="product-wrapper" v-if="discountedProduct">
        <PreviewProduct  :product="discountedProduct" />
        <button @click="this.discountedProduct = null, this.productCount = 'discounted'" class="icon-button">Delete <font-awesome-icon :icon="['fas', 'trash']" /></button>
        </div>
      </div>
      <div class="button-row">
        <div></div>
      <button @click="createBundle" v-if="primaryProduct && discountedProduct && discount" class="primary-button">Create bundle</button>
      </div>
    </div>
  </div>
</template>
<script>
import SearchBar from "../SearchBar.vue";
import PreviewProduct from "../PreviewProduct.vue";
import axios from "axios";
export default {
  name: "CreateBundlePopup",
  components: {
    SearchBar,
    PreviewProduct,
  },
  props: {
    promotion: Object
  },
  computed: {
    maxDiscount() {
        if (this.discountedProduct) {
        return Math.round(this.discountedProduct.price * this.discountedProduct.discount * 100) / 100;
      }
      return null;
    }
  },
  data() {
    return {
      searchInput: "",
      showSearchResults: true,
      primaryProduct: null,
      discountedProduct: null,
      productCount: "primary",
      discount: null,
      baseUrl: this.$baseUrl,
      id: null
    };
  },
  methods: {
    closeDropdowns(event) {
      const isSearchResults =
        event.target.closest(".dropdown-products") !== null;
      if (!isSearchResults) {
        this.showSearchResults = false;
      }
    },
    handleDropdownToggled(dropdown) {
      this.showSearchResults = dropdown;
    },
    handleProductSelected(product) {
      if (!this.primaryProduct) {
        this.primaryProduct = product;
        this.productCount = "discounted";
      } else {
        this.discountedProduct = product;
        this.productCount = "primary"
      }
    },
    setBundleData() {
      console.log(this.promotion)
      this.primaryProduct = this.promotion.primary_product
      this.discountedProduct = this.promotion.discounted_product
      this.discount = this.promotion.discount
      this.id = this.promotion.id
    },
    createBundle() {
        let data = {
            primary_product: this.primaryProduct.id,
            discounted_product: this.discountedProduct.id,
            discount: this.discount
        }
        if(this.id) {
          data.id = this.id
        }
        console.log(data)
        axios.post(`${this.baseUrl}/create-bundle`, data).then(response => {
            if(response.status == 200) {
                this.$emit('result', 'Bundle added succesfully')
                this.$emit('close-popup')
            }
        }).catch(error => {
            console.log('error:', error)
            this.$emit('result', 'Error while creating bundle')
        })
        
    }
},
   
  watch: {
    discount(newVal) {
      if (newVal > this.maxDiscount) {
        this.discount = this.maxDiscount;
      }
    }
  },
  mounted() {
    document.addEventListener("click", this.closeDropdowns);
    if(this.promotion) {
      this.setBundleData()
    }
  },
};
</script>
<style lang="scss" scoped>
@import "../../assets/styles/main.scss";
.popup-wrapper {
    min-height: 100vh;
    
.popup {
  display: flex;
  flex-direction: column;
  min-height: 65vh;
  min-width: 35vw;
  padding: 25px;

  .exit-button {
      position: absolute;
      top: 10px;
      right: 10px;
      background: transparent;
      border: none;
      font-size: 1.5em;
      cursor: pointer;
      color: var(--text-color);
    }
  .search-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 20px;
    .input-wrapper {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-direction: row;
    .primary-input {
      width: 100px;
      text-align: center;
    }
}
    /* Chrome, Safari, Edge, Opera */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }

    /* Firefox */
    input[type="number"] {
      -moz-appearance: textfield;
    }
  }
  .button-row {
    display: flex;
    flex-direction: row;
    .primary-button {
        margin-left: auto;
    }
  }
  .product-row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 20px;
    .product-wrapper {
        display: flex;
        flex-direction: column;
        
        .icon-button {
            margin-left: auto;
        }
    }
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
</style>