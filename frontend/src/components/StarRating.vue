<template>
  <div v-if="mode === 'Review'" class="star-rating-wrapper">
    <font-awesome-icon
      v-for="(icon, index) in maxIcons"
      :key="index"
      :value="index"
      :class="{ 'selected-rating': index < rating }"
      :icon="[index < rating ? 'fas' : 'far', 'star']"
    />
  </div>
  <div v-else class="star-rating-wrapper">
    <font-awesome-icon
      v-for="(icon, index) in maxIcons"
      :key="index"
      :value="index"
      @click="handleRatingClicked(index)"
      :class="{ 'selected-rating': index <= selectedIcon }"
      :icon="[index <= selectedIcon ? 'fas' : 'far', 'star']"
    />
  </div>
</template>

<script>
export default {
  name: "StarRating",
  props: {
    product: Object,
    mode: String,
    rating: String,
  },
  data() {
    return {
      maxIcons: 5,
      selectedIcon: -1,
      baseUrl: this.$baseUrl,
    };
  },
  methods: {
    handleRatingClicked(index) {
      this.selectedIcon = index;
      const data = {
        product_id: this.product.id,
        rating: this.selectedIcon + 1,
        ip: this.$store.state.userIp,
      };
      this.$emit("rating-clicked", data);
    },
  },
};
</script>

<style lang='scss' scoped>
.star-rating-wrapper:hover {
  cursor: pointer;
}
.selected-rating {
  color: gold;
}
</style>