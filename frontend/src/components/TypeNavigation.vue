<template>
  <div class="type-navigation">
    <ul>
      <li
        @click="redirectToType('All')"
        :class="{ 'active-type': activeType === 'All' }"
      >
        <b>All</b>
      </li>
      <li
        v-for="(type, index) in types"
        :key="index"
        :class="{ 'active-type': activeType === type.type }"
      >
        <span @click="redirectToType(type.type, index)">{{ type.type }}</span
        ><span class="count">({{ type.count }})</span>
      </li>
    </ul>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: "TypeNavigation",
  data() {
    return {
      baseUrl: this.$baseUrl,
      types: [],
    };
  },
  computed: {
    category() {
      return this.$route.params.category;
    },
    activeType() {
      return this.$route.params.type;
    },
  },
  methods: {
    getProductTypes() {
      const url = `${this.baseUrl}/types`;
      const data = {
        category: this.category,
      };
      axios
        .get(url, { params: data })
        .then((response) => {
          this.types = response.data;
        })
        .catch((error) => {
          console.log("error fetching types:", error);
        });
    },
    redirectToType(type, index) {
      this.$router.push({
        name: "productList",
        params: {
          category: this.category,
          type: type,
        },
      });
      this.activeType = index;
      this.$store.state.activeFilters = [];
    },
  },
  watch: {
    category(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.getProductTypes();
      }
    },
  },

  mounted() {
    this.getProductTypes();
  },
};
</script>
<style scoped lang="scss">
@import "../assets/styles/main.scss";
.type-navigation {
  display: flex;
  justify-self: left;
  position: fixed;
  width: 10%;
  ul {
    padding-inline: 1vw;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-right: 1px solid var(--subtle-border-color);
    font-family: $secondary-font-stack;
    li {
      display: flex;
      flex-direction: row;
      gap: 10px;

      .count {
        color: gray;
      }
    }
    li:hover {
      cursor: pointer;
      color: rgba(0, 0, 0, 0.7);
    }

    .active-type {
      * {
        color: var(--secondary-color) !important;
      }
    }
  }
}
</style>
