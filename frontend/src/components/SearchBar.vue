<template>
  <input
    v-model="input"
    class="primary-input"
    style="width: 100%"
    type="text"
    placeholder="Search products..."
    :class="{'admin-input': admin == true}"
  />

  <div
    class="search-dropdown"
    :class="{ 'show-search-results': this.closeDropdown && this.showSearchResults && filterList  }"
  >
    <div
      class="dropdown-products"
      v-for="product in filterList()"
      :key="product"
    >
      <a @click="handleProductClick(product)">{{ product.name }}</a>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "SearchBar",
  props: {
    closeDropdown: null,
    admin: Boolean,
    addBundleMode: Boolean
  },
  computed: {
    ...mapState(["allProductList"]),
  },

  data() {
    return {
      productList: [],
      input: "",
      showSearchResults: false,
    };
  },

  methods: {
    filterList() {
      if (this.input.trim() === "") {
        this.showSearchResults = false;
        return [];
      }
      return this.allProductList.filter((product) =>
        product.name.toLowerCase().includes(this.input.toLowerCase())
      );
    },
    handleProductClick(product) {
      if (this.$route.path.includes( "/admin")) {
        if(this.addBundleMode == true) {
          this.$emit('product-selected', product)
        } else {
        this.$emit("product-clicked", product.id);
        }
        this.showSearchResults = false;
        this.input = "";
      } else {
        this.$emit("product-clicked", product.id);
        this.input = "";
        this.$router.push({
          name: "detailedProduct",  
          params: { id: product.id },
        });
      }
    },
  },
  mounted() {
  },
  watch: {
    input(newValue) {
      if (newValue !== "") {
        this.showSearchResults = true;

        this.$emit("dropdown-toggled", this.showSearchResults, "search");
      }
    },
    closeDropdown() {
      this.showDropdown = this.closeDropdown;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.search-bar {
  .search-dropdown {
    display: none;
    position: absolute;
    top: 40px;
    background-color: var(--background-color);
    z-index: 2;
    &::-webkit-scrollbar {
      width: 12px;
    }

    &::-webkit-scrollbar-thumb {
      background-color: var(--secondary-color);
      border-radius: 4px;
      border: 2px solid var(--background-color);
    }
    &::-webkit-scrollbar-thumb:hover {
      background-color: var(--background-color);
      border-radius: 4px;
      border: 2px solid var(--secondary-color);
    }
    &::-webkit-scrollbar-track {
      background: var(--background-color);
    }

    .dropdown-products {
      display: flex;
      width: 100%;
      flex-direction: column;
      text-align: left;
      text-indent: 10px;
      border-bottom: 1px solid var(--subtle-border-color);
      border-left: 1px solid var(--subtle-border-color);
      border-right: 1px solid var(--subtle-border-color);
    }
  }
  .primary-input {
    border-top-left-radius: 25px;
    border-bottom-left-radius: 25px;
  }
  .admin-input {
    border-top-right-radius: 25px;
    border-bottom-right-radius: 25px;
  }
  .show-search-results {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 40vh;
    overflow-y: scroll;
    color: black;
   
  }

  a {
    padding: 10px;
  }

  a:hover {
    @include secondary-button;
    font-weight: bold;
    cursor: pointer;
  }
}
</style>