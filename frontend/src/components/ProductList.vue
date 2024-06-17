<template>
  <div class="product-options">
    <div class="category-wrapper">
      <div class="common-dropdown-wrapper">
        <div @click="toggleCategoryDropdown" class="category-dropdown-wrapper">
          <b>{{ this.$route.params.category }}</b>
          <font-awesome-icon :icon="['fas', 'arrow-down-wide-short']" />
        </div>
        <div
          class="common-dropdown-list"
          :class="{ 'show-category-dropdown': showCategoryDropdown }"
        >
          <ul>
            <li @click="redirectToType('Men')">Men</li>
            <li @click="redirectToType('Women')">Women</li>
            <li @click="redirectToType('Kids')">Kids</li>
            <li @click="redirectToType('New')">New</li>
          </ul>
        </div>
      </div>
      <font-awesome-icon :icon="['fas', 'angle-right']" class="fa-sm" />
      <b>{{ this.$route.params.type }}</b>
    </div>

    <div class="sort-options-wrapper">
      <span class="sort-title">Sort by</span>
      <button @click="toggleSortingDropdown" class="sorting-button">
        {{ this.currentSortingOption }}
      </button>
      <div
        class="common-dropdown-list"
        style="top: 30px"
        :class="{ 'show-sorting-dropdown': showSortingDropdown }"
      >
        <ul>
          <li @click="onSortingOptionSelected('Alphabetical')">Alphabetical</li>
          <li @click="onSortingOptionSelected('Price descending')">
            Price descending
          </li>
          <li @click="onSortingOptionSelected('Price ascending')">
            Price ascending
          </li>
          <li @click="onSortingOptionSelected('New')">New</li>
        </ul>
      </div>
    </div>
  </div>
  <FilterList @priceBracketChanged="handlePriceBracketChanged" />

  <div class="product-list-wrapper">
    <TypeNavigation ref="typeNavigation" />
    <div v-if="productList.length === 0">No products found</div>
    <div
      class="product-list"
      v-else
      :style="{ marginLeft: this.typeNavigationWidth + 'px' }"
    >
      <PreviewProduct
        v-for="(product, index) in productList"
        :product="product"
        :key="index"
        @product-clicked="handleProductClicked"
      />
    </div>
  </div>
</template>
<script>
import axios from "axios";
import PreviewProduct from "./PreviewProduct.vue";
import TypeNavigation from "./TypeNavigation.vue";
import FilterList from "./FilterList.vue";
import { mapActions, mapState } from "vuex";
export default {
  name: "ProductList",
  components: {
    PreviewProduct,
    TypeNavigation,
    FilterList,
  },
  props: {
    category: String,
    type: String,
  },
  computed: {
    ...mapState(["productList", "originalProductList"]),
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      currentSortingOption: "Alphabetical",
      showSortingDropdown: false,
      showCategoryDropdown: false,
      typeNavigationWidth: null,
    };
  },
  methods: {
    ...mapActions(["updateProductList"]),
    getProductsByParams() {
      let url = "";
      let params = {};
      url = `${this.baseUrl}/products`;
      params = {
        category: this.category,
        type: this.type,
      };

      axios
        .get(url, {
          params,
        })
        .then((response) => {
          this.updateProductList(response.data);
          this.$store.state.originalProductList = response.data;

          this.sortByOption(this.currentSortingOption);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleProductClicked(product) {
      this.$emit("product-clicked", product);
    },
    handlePriceBracketChanged(priceBracket) {
      this.$store.state.productList = [...this.originalProductList];
      const filteredProducts = this.productList.filter((product) => {
        const price = product.price * product.discount;
        return price >= priceBracket.min && price <= priceBracket.max;
      });

      // Sort the filtered products based on price

      // Update productList to contain only the filtered and sorted products
      this.$store.state.productList = filteredProducts;
    },

    toggleSortingDropdown() {
      this.showSortingDropdown = !this.showSortingDropdown;
    },
    toggleCategoryDropdown() {
      this.showCategoryDropdown = !this.showCategoryDropdown;
    },
    closeDropdowns(event) {
      const isDropdown =
        event.target.closest(".sorting-button") !== null ||
        event.target.closest(".category-dropdown-wrapper") !== null;
      if (!isDropdown) {
        (this.showSortingDropdown = false), (this.showCategoryDropdown = false);
      }
    },
    redirectToType(category) {
      this.$router.push({
        name: "productList",
        params: {
          category: category,
        },
      });
      this.showCategoryDropdown = false;
    },
    onSortingOptionSelected(option) {
      this.currentSortingOption = option;
      this.sortByOption(option);
    },

    sortByOption(option) {
      switch (option) {
        case "Alphabetical":
          this.$store.state.productList.sort((a, b) =>
            a.name.localeCompare(b.name)
          );
          break;
        case "Price descending":
          this.$store.state.productList.sort(
            (a, b) => b.price * b.discount - a.price * a.discount
          );

          break;
        case "Price ascending":
          this.$store.state.productList.sort(
            (a, b) => a.price * a.discount - b.price * b.discount
          );

          break;
        case "New":
          // Implement sorting logic for new products
          break;
        default:
          break;
      }
    },
  },
  watch: {
    "$route.params.category": function (newCategory) {
      this.getProductsByParams(newCategory);
    },
    "$route.params.type": function (newType) {
      this.getProductsByParams(newType);
    },
  },
  mounted() {
    this.getProductsByParams();
    document.body.addEventListener("click", this.closeDropdowns);
    this.typeNavigationWidth = this.$refs.typeNavigation.$el.offsetWidth;
  },
};
</script>
<style scoped lang="scss">
@import "../assets/styles/main.scss";

.product-list-wrapper {
  display: flex;
  flex-direction: row;
  height: 100%;
  overflow-y: scroll;
  flex-wrap: wrap;
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
}

.product-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  width: 100%;
}

.product-options {
  display: flex;
  flex-direction: row;
  position: relative;
  justify-content: space-between;
  .category-wrapper {
    display: flex;
    flex-direction: row;
    padding-inline: 50px;
    align-items: center;
    gap: 5px;
  }

  .small-nav {
    position: relative;
    left: 3vw;
    display: flex;
    flex-direction: row;
    gap: 10px;
  }

  .sort-options-wrapper {
    position: relative;
    display: flex;
    right: 10vw;

    .sorting-button {
      min-width: 80px;
      min-height: 30px;
      background-color: var(--background-color);
      border: 1px solid var(--border-color);
      border-radius: 5px;
      color: gray;
    }

    .sorting-button:hover {
      color: var(--text-color);
      border-color: var(--secondary-color);
      cursor: pointer;
    }

    .sort-title {
      position: absolute;
      background-color: var(--background-color);
      font-size: 12px;
      margin-left: 6px;
      bottom: 23px;
    }
  }

  .category-dropdown-wrapper:hover {
    color: var(--secondary-color);
    cursor: pointer;
  }

  .show-category-dropdown {
    display: block;
  }

  .show-sorting-dropdown {
    display: block;
    width: max-content;
  }
}
</style>