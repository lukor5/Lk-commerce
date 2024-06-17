<template>
  <div class="filter-list-wrapper">
    <div class="common-dropdown-wrapper">
      <div class="filter-button-wrapper">
        <button @click="toggleFiltersDropdown" class="filters-button">
          <b>Filters</b
          ><b :style="{ visibility: activeFiltersVisibility }">
            ({{ activeFilters.length }})</b
          >
        </button>
      </div>
      <div
        v-if="showDropdown"
        class="filter-dropdown-list"
        :class="{ 'show-dropdown': showDropdown }"
      >
        <ul>
          <li v-for="(activeFilter, index) in activeFilters" :key="index">
            {{ activeFilter.filter }}
            <template v-if="activeFilter.filter === 'Price range'">
              {{ activeFilter.option.min }} - {{ activeFilter.option.max }}
            </template>
            <template v-else-if="activeFilter.filter === 'Discount'">
              {{ activeFilter.option.discountBracket }}
            </template>
            <template v-else>
              {{ activeFilter.option }}
            </template>
            <button @click="removeFilter(index)" class="icon-button">
              <font-awesome-icon :icon="['fas', 'x']" />
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div class="filters-wrapper">
      <SingleFilter
        :name="'Price range'"
        @priceBracketChanged="emitPriceBracket"
      />
      <SingleFilter :name="'Discount'" />
      <SingleFilter :name="'Size'" />
      <SingleFilter :name="'Brand'" />
      <SingleFilter :name="'Color'" />
    </div>
  </div>
</template>
<script>
import SingleFilter from "./SingleFilter.vue";
import { mapActions, mapState } from "vuex";
export default {
  name: "FilterList",
  components: {
    SingleFilter,
  },
  computed: {
    ...mapState(["activeFilters"]),
    activeFiltersVisibility() {
      return this.hasActiveFilters() ? "visible" : "hidden";
    },
  },
  data() {
    return {
      showDropdown: false,
    };
  },
  methods: {
    ...mapActions(["removeActiveFilter"]),
    emitPriceBracket(priceBracket) {
      this.$emit("priceBracketChanged", priceBracket);
    },
    toggleFiltersDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    removeFilter(index) {
      this.removeActiveFilter(index);
    },
    hasActiveFilters() {
      return this.activeFilters.length > 0;
    },
    handleClickOutside(event) {
      if (this.$el && !this.$el.contains(event.target)) {
        this.showDropdown = false;
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  watch: {
    activeFiltersVisibility(newValue) {
      if (newValue === "hidden") {
        this.showDropdown = false;
      }
    },
  },
};
</script>
<style scoped lang="scss">
@import "../assets/styles/main.scss";

.filter-list-wrapper {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 10px;

  .filter-button-wrapper {
    display: flex;
    flex-direction: row;
    flex: 1;
    gap: 10px;
  }

  .common-dropdown-wrapper {
  }

  .filter-dropdown-list {
    display: none;
    position: absolute;
    text-align: left;
    width: 100%;
    min-width: max-content;
    background-color: var(--background-color);
    z-index: 3;
    box-shadow: 8px 8px 20px 1px
      rgba(var(--shadow-color-rgb), var(--shadow-opacity));

    li {
      list-style: none;
      border: 1px solid lightgray;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
    }
  }

  .show-dropdown {
    display: flex;
    flex-direction: column;
  }

  .filters-wrapper {
    display: flex;
    flex: 1;
    justify-content: center;
    flex-direction: row;
    gap: 1%;
    flex-wrap: wrap;
  }
}
</style>