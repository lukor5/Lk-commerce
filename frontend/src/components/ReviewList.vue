<template>
  <div class="reviews-wrapper">
    <div class="review" v-for="(review, index) in reviewsPerPage" :key="index">
      <div class="review-top">
        <div class="name-date-wrapper">
          <b v-if="review.review">{{ review.review.name }}</b
          ><b v-else>User</b>
          <p>{{ formattedDate(review.created_at) }}</p>
        </div>
        <StarRating :rating="review.rating" :mode="'Review'" />
      </div>

      <div v-if="review.review" class="review-body">
        {{ review.review.body }}
      </div>
    </div>
  </div>
  <div v-if="reviews.length > 0" class="pagination">
    <font-awesome-icon :icon="['fas', 'chevron-left']" />
    <button
      @click="changePage(index)"
      v-for="(page, index) in numberOfPages"
      :key="index"
    >
      {{ index + 1 }}
    </button>
    <font-awesome-icon :icon="['fas', 'chevron-right']" />
  </div>
  <div v-else>
    <h3>No reviews yet :(</h3>
  </div>
</template>

<script>
import axios from "axios";
import StarRating from "./StarRating.vue";
import { Date } from "core-js";
export default {
  name: "ReviewList",
  components: {
    StarRating,
  },
  props: {
    product: Object,
  },
  computed: {
    reviewsPerPage() {
      return this.reviews.slice(this.firstIndex, this.secondIndex);
    },
    numberOfPages() {
      return Math.ceil(this.reviews.length / 6);
    },
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      reviews: [],
      date: null,
      firstIndex: 0,
      secondIndex: 6,
    };
  },
  methods: {
    getReviews() {
      axios
        .get(`${this.baseUrl}/reviews/${this.product.id}`)
        .then((response) => {
          this.reviews = response.data;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    formattedDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-us", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    changePage(index) {
      if (index === 0) {
        this.firstIndex = 0;
        this.secondIndex = 6;
      } else {
        this.firstIndex = index * 6;
        this.secondIndex = this.firstIndex + 6;
      }
    },
  },
  mounted() {
    if (this.product) {
      this.getReviews();
    }
  },
  watch: {
    product() {
      this.getReviews();
    },
  },
};
</script>

<style lang="scss">
@import "../assets/styles/main.scss";

.reviews-wrapper {
  display: flex;
  position: relative;
  flex-direction: row;
  flex-wrap: wrap;
  height: 100%;
  justify-content: center;
  gap: 20px;
  width: 100%;
  animation: slidein 0.5s linear;

  z-index: 1;

  .review {
    display: flex;
    max-width: 35%;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
    min-height: 15%;
    border-bottom: 1px solid var(--secondary-color);

    .review-top {
      display: flex;
      flex-direction: row;
      justify-content: space-between;

      gap: 20px;

      .name-date-wrapper {
        display: flex;
        flex: 1;
        flex-direction: row;
        align-items: center;
        gap: 10px;

        p {
          @include small-text;
        }
      }
    }
    .review-body {
      text-align: left;
    }
  }
}
.pagination {
  display: flex;
  flex-direction: row;
  justify-content: center;
  padding: 40px;
  align-items: center;
  gap: 10px;
  button {
    min-width: 30px;
    min-height: 30px;
    box-shadow: 4px 4px 24px -5px rgba(var(--shadow-color-rgb), var(--shadow-opacity));
    border: 1px solid var(--subtle-border-color) "";
  }
}

@media (max-width: 1250px) {
  .reviews-wrapper {
    .review {
      max-width: 40%;
      min-height: 10%;
      .review-top {
        flex-direction: column;
        .name-date-wrapper {
          flex-direction: column;
        }
      }
    }
  }
}
</style>