<template>
  <button class="category-button" @click="toggleCategoryDropdown">
    Categories
  </button>
  <div
    v-if="this.showDropdown"
    class="category-dropdown"
    :class="{ 'show-dropdown': showDropdown }"
  >
    <ul class="dropdown-categories">
      <li v-for="(category, index) in categories" :key="index">
        <h3>{{ category }}</h3>
        <ul class="dropdown-types">
          <li
            v-for="(common_type, index) in common_types"
            :key="index"
            :title="common_type.type"
            @click="redirectToType(category, common_type.type)"
          >
            {{ common_type.type }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  name: "CategoryDropdown",
  props: {
    closeDropdown: null,
  },

  data() {
    return {
      baseUrl: this.$baseUrl,
      categories: [],
      common_types: [],
      winter_types: [],
      showDropdown: false,
    };
  },

  methods: {
    ...mapActions(["setCategoryList"]),
    toggleCategoryDropdown() {
      this.showDropdown = !this.showDropdown;
      this.$emit("dropdown-toggled", this.showDropdown, "category");
    },

    getCategories() {
      axios
        .get(this.baseUrl + "/categories")
        .then((response) => {
          this.categories = response.data.categories;
          this.setCategoryList(this.categories);
        })
        .catch((error) => {
          console.error("Error fetching categories:", error);
        });
    },
    getCommonTypes() {
      axios
        .get(this.baseUrl + "/types")
        .then((response) => {
          this.common_types = response.data;
        })
        .catch((error) => {
          console.error("Error fetching types:", error);
        });
    },
    redirectToType(category, type) {
      this.$emit("category-clicked");
      this.$router.push({
        name: "productList",
        params: {
          category: category,
          type: type,
        },
      });
    },
  },
  mounted() {
    this.getCommonTypes();
    this.getCategories();
  },
  watch: {
    closeDropdown() {
      this.showDropdown = this.closeDropdown;
    },
  },
};
</script>
<style lang="scss">
@import "../assets/styles/main.scss";

.category-button {
  border: 1px solid var(--border-color);
  border-left: none;
  background-color: var(--background-color);
  color: gray;
  border-top-right-radius: 25px;
  border-bottom-right-radius: 25px;
  padding-inline: 10px;
}

.category-dropdown {
  display: none;
  position: absolute;
  top: 40px;
  background-color: var(--background-color);
  z-index: 1;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  border: 1px solid var(--subtle-border-color);
  font-family: $secondary-font-stack;
  box-shadow: 2px 2px 2px 2px
    rgba(var(--shadow-color-rgb), var(--shadow-opacity));

  .dropdown-categories {
    display: flex;
    flex-direction: row;
    margin-top: 0;
    justify-content: space-around;
    list-style: none;
    width: 100%;
    padding-inline: 10px;
    text-align: left;
    gap: 50px;

    .dropdown-types {
      display: flex;
      flex-direction: column;
      list-style: none;
      text-align: left;
      margin: 0;
      padding: 0;
      gap: 10px;

      li {
        border-bottom: 1px solid var(--subtle-border-color);
        position: relative;
      }

      li::before {
        content: attr(title);
        font-weight: bold;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;

        visibility: hidden;
        border-bottom: 1px solid var(--subtle-border-color);
      }

      li:hover::before {
        color: var(--text-color);
        visibility: visible;
        cursor: pointer;
        font-weight: bold;
      }

      li:hover {
        visibility: hidden;
      }
    }
  }
}
.show-dropdown {
  display: flex;
  justify-content: center;
}
.category-button:hover {
  @include secondary-button;
  border: 1px solid var(--secondary-color);
  border-left: none;
  cursor: pointer;
}
</style>