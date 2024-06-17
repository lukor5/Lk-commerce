<template>
  <div class="common-dropdown-wrapper">
    <div class="button-wrapper">
      <button
        @click="toggleDropdown"
        class="filter-button"
        :class="{ active: isActive }"
      >
        {{ this.name }} <font-awesome-icon :icon="['fas', 'angle-down']" />
      </button>
      <button
        v-if="isActive"
        @click="removeFilter"
        class="remove-filter-button"
      >
        <font-awesome-icon class="fa-xs" :icon="['fas', 'x']" />
      </button>
    </div>
    <div
      v-if="name === 'Price range'"
      class="range-dropdown-list"
      :class="{ 'show-dropdown': showDropdown }"
    >
      <div class="range-slider-container">
        <input
          class="min-value"
          type="range"
          min="0"
          max="300"
          v-model="firstValue"
          @input="addFilter('Price range', this.priceBracket)"
        />
        <input
          class="max-value"
          type="range"
          min="0"
          max="300"
          v-model="secondValue"
          @input="addFilter('Price range', this.priceBracket)"
        />
      </div>
      <div class="price-bracket-container">
        <p>{{ this.priceBracket.min }}$</p>
        <font-awesome-icon :icon="['fas', 'angle-right']" class="fa-sm" />
        <p>{{ this.priceBracket.max }}$</p>
      </div>
    </div>
    <div
      v-if="name === 'Discount'"
      class="common-dropdown-list"
      :class="{ 'show-dropdown': showDropdown }"
    >
      <ul>
        <li
          v-for="(discount, index) in groupedDiscounts"
          :key="index"
          @click="addFilter('Discount', discount)"
          :class="{ active: isInActiveFilters(discount) }"
        >
          {{ discount.discountBracket
          }}{{ discount.count > 1 ? ` (${discount.count})` : "" }}
        </li>
      </ul>
    </div>
    <div
      v-if="name === 'Size'"
      class="common-dropdown-list"
      :class="{ 'show-dropdown': showDropdown }"
    >
      <ul>
        <li
          v-for="size in sizes"
          @click="addFilter('Size', size)"
          :key="size"
          :class="{ active: isInActiveFilters(size) }"
        >
          {{ size }}
        </li>
      </ul>
    </div>
    <div
      v-if="name === 'Brand'"
      class="common-dropdown-list"
      :class="{ 'show-dropdown': showDropdown }"
    >
      <ul>
        <li
          v-for="brand in brands"
          @click="addFilter('Brand', brand)"
          :key="brand"
          :class="{ active: isInActiveFilters(brand) }"
        >
          {{ brand }}
        </li>
      </ul>
    </div>
    <div
      v-if="name === 'Color'"
      class="common-dropdown-list"
      :class="{ 'show-dropdown': showDropdown }"
    >
      <ul>
        <li
          v-for="color in colors"
          @click="addFilter('Color', color)"
          :key="color"
          :class="{ active: isInActiveFilters(color) }"
        >
          {{ color }}
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "SingleFilter",
  props: {
    name: String,
  },
  computed: {
    ...mapState(["productList", "originalProductList", "activeFilters"]),
    priceBracket() {
      return {
        min: Math.min(this.firstValue, this.secondValue),
        max: Math.max(this.firstValue, this.secondValue),
      };
    },
    groupedDiscounts() {
      const discounts = {};
      const groupedDiscounts = [];

      if (this.productList) {
        const products = this.productList;
        products.forEach((product) => {
          let discountBracket;
          const discountValue = product.discount;

          if (discountValue <= 1 && discountValue >= 0.75) {
            discountBracket = "0 - 25%";
          } else if (discountValue < 0.75 && discountValue >= 0.5) {
            discountBracket = "26 - 50%";
          } else if (discountValue < 0.5 && discountValue >= 0.25) {
            discountBracket = "51 - 75%";
          } else if (discountValue < 0.25 && discountValue > 0) {
            discountBracket = "76 - 99%";
          }

          if (discounts[discountBracket]) {
            discounts[discountBracket].count++;
            discounts[discountBracket].discounts.push(discountValue);
          } else {
            discounts[discountBracket] = {
              count: 1,
              discounts: [discountValue],
            };
          }
        });

        for (const discountBracket in discounts) {
          groupedDiscounts.push({
            discountBracket: discountBracket,
            count: discounts[discountBracket].count,
            discounts: discounts[discountBracket].discounts,
          });
        }
        groupedDiscounts.sort((a, b) => {
          const firstNumber = Number(a.discountBracket.charAt(0));
          const secondNumber = Number(b.discountBracket.charAt(0));
          return firstNumber - secondNumber;
        });
      }

      return groupedDiscounts;
    },
    sizes() {
      if (this.productList) {
        const allSizes = this.productList.reduce((sizes, product) => {
          const productSizes = product.product_variants.map(
            (variant) => variant.size
          );
          productSizes.forEach((size) => {
            if (!sizes.includes(size)) {
              sizes.push(size);
            }
          });
          return sizes;
        }, []);

        allSizes.sort((a, b) => {
          if (!isNaN(a) && !isNaN(b)) {
            return a - b;
          } else if (!isNaN(a)) {
            return -1;
          } else if (!isNaN(b)) {
            return 1;
          } else {
            return a.localeCompare(b);
          }
        });

        return allSizes;
      } else {
        return [];
      }
    },
    brands() {
      const brands = [];
      if (this.productList) {
        const productBrands = this.productList;
        productBrands.forEach((product) => {
          if (!brands.includes(product.brand)) {
            brands.push(product.brand);
          }
        });
      }
      return brands;
    },
    colors() {
      const colors = [];
      if (this.productList) {
        const productColors = this.productList;

        productColors.forEach((product) => {
          let variants = product.product_variants;
          variants.forEach((variant) => {
            if (!colors.includes(variant.color)) {
              colors.push(variant.color);
            }
          });
        });
      }
      return colors;
    },
    isActive() {
      // Check if the computed property is in activeFilters
      return this.activeFilters.some((filter) => filter.filter === this.name);
    },
  },
  data() {
    return {
      showDropdown: false,
      rangeInput: [],
      firstValue: 0,
      secondValue: 300,
      selectedDiscount: null,
    };
  },
  methods: {
    ...mapActions([
      "updateProductList",
      "updateActiveFilters",
      "removeActiveFilter",
    ]),
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    addFilter(filter, option) {
      if (filter !== "Price range") {
        this.showDropdown = !this.showDropdown;
        this.isActive = true;
      }
      this.updateActiveFilters({ filter: filter, option: option });
    },
    removeFilter() {
      const index = this.activeFilters.findIndex(
        (element) => element.filter === this.name
      );
      this.removeActiveFilter(index);
      this.isActive = false;
    },
    isInActiveFilters(option) {
      return this.activeFilters.some(
        (activeFilter) => activeFilter.option === option
      );
    },
    sortByPriceBracket(priceBracket) {
      const filteredProducts = this.productList.filter((product) => {
        const price = product.price * product.discount;
        return price >= priceBracket.min && price <= priceBracket.max;
      });
      this.updateProductList(filteredProducts);
    },
    filterProductList() {
      this.updateProductList(this.$store.state.originalProductList);
      this.activeFilters.forEach((activeFilter) => {
        switch (activeFilter.filter) {
          case "Discount":
            this.sortByDiscount(activeFilter.option);
            break;
          case "Size":
            this.sortBySize(activeFilter.option);
            break;
          case "Price range":
            this.sortByPriceBracket(activeFilter.option);
            break;
          case "Brand":
            this.sortByBrand(activeFilter.option);
            break;
          case "Color":
            this.sortByColor(activeFilter.option);
            break;
        }
      });
    },
    sortByDiscount(discount) {
      this.selectedDiscount = discount;

      const selectedDiscountValues = new Set(this.selectedDiscount.discounts);

      const filteredProducts = this.$store.state.productList.filter((product) =>
        selectedDiscountValues.has(product.discount)
      );
      this.updateProductList(filteredProducts);
    },

    sortBySize(size) {
      const filteredProducts = this.productList.filter((product) => {
        return product.product_variants.some(
          (variant) => variant.size === size
        );
      });
      this.updateProductList(filteredProducts);
    },
    sortByBrand(brand) {
      const filteredProducts = this.productList.filter((product) => {
        return brand === product.brand;
      });
      this.updateProductList(filteredProducts);
    },
    sortByColor(color) {
      const filteredProducts = this.productList.filter((product) => {
        return product.product_variants.some(
          (variant) => variant.color === color
        );
      });

      this.updateProductList(filteredProducts);
    },
    handleClickOutside(event) {
      if (this.$el && !this.$el.contains(event.target)) {
        this.showDropdown = false;
      }
    },
  },
  mounted() {
    this.rangeInput = document.querySelectorAll(".range-input input");
    document.addEventListener("click", this.handleClickOutside);
  },
  watch: {
    activeFilters: {
      handler() {
        if (
          !this.activeFilters.some(
            (activeFilter) => activeFilter.filter === "Price range"
          )
        ) {
          this.firstValue = 0;
          this.secondValue = 300;
        }
        this.filterProductList();
      },
      deep: true,
    },
  },
};
</script>
<style scoped lang="scss">
@import "../assets/styles/main.scss";

.button-dropdown-wrapper {
}

.button-wrapper {
  position: relative;

  .filter-button {
    display: flex;
    flex-direction: row;
    position: relative;
    justify-content: space-between;
    align-items: center;
    padding: 5px;
    border-radius: 10px;
    border: 1px solid var(--secondary-color);
    color: gray;
    background-color: var(--background-color);
  }

  .active {
    @include secondary-button;
  }

  .remove-filter-button {
    position: absolute;
    right: -10px;
    background-color: var(--secondary-color);
    color: white;
    border-radius: 25px;
    width: 22px;
    height: 22px;
    bottom: -10px;
    border: 1px solid var(--border-color);
  }

  .remove-filter-button:hover {
    color: var(--secondary-color);
    background-color: white;
  }
}

.dropdown {
  display: none;
}

.range-dropdown-list {
  position: absolute;

  background-color: white;
  border: 1px solid var(--subtle-border-color);
  z-index: 1;
  padding: 10px;
  display: none;

  .range-slider-container {
    position: relative;
    height: auto;
    margin-bottom: 10px;
    min-width: 80px;
  }

  .price-bracket-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 5px 0;
    border-top: 1px solid var(--subtle-border-color);
  }
}

.show-dropdown {
  display: flex;
  flex-direction: column;
  width: min-content;
}

input[type="range"] {
  position: absolute;
  left: 0px;
  height: 5px;
  margin: 0;
  padding: 0;
  -webkit-appearance: none;
  width: 100%;

  appearance: none;
  background-color: var(--secondary-color);
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background-color: var(--secondary-color);
  border: 2px solid #ffffff;
  border-radius: 50%;
  cursor: pointer;
  position: relative;
  z-index: 2;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  /* Adjust the width of the slider thumb */
  height: 20px;
  /* Adjust the height of the slider thumb */
  background-color: #007bff;
  /* Adjust the color of the slider thumb */
  border: 2px solid #ffffff;
  /* Adjust the border of the slider thumb */
  border-radius: 50%;
  /* Adjust the border-radius of the slider thumb to make it circular */
  cursor: pointer;
  position: relative;
  z-index: 2;
}
</style>