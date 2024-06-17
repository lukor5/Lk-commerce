<template>
  <div class="review-popup">
    <div class="review-details">
      <div class="form-wrapper" v-if="addReview === true">
        <button @click="this.addReview = false" class="go-back-button">
          <font-awesome-icon :icon="['fas', 'arrow-left']" class="fa-lg" />
        </button>
        <form @submit.prevent>
          <h1>Add review</h1>
          <div class="input-wrapper">
            <label>Name</label>
            <input class="primary-input" type="text" v-model="name" placeholder="Your name..." />
          </div>
          <div class="textarea-wrapper">
            <label>Review</label>
            <textarea v-model="reviewBody" placeholder="Type something..."></textarea>
          </div>
          <button @click="submitForm" class="primary-button">Add review</button>
        </form>
      </div>
      <div v-else>
        <h1>Thank you for your rating!</h1>
        <h2>Would you like to add a review?</h2>
        <div class="row">
          <button @click="addReview = true" class="primary-button">
            Add review
          </button>
          <button @click="handleNoClicked" class="primary-button">No</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AddReviewPopup",
  props: {
    data: Object,
  },
  data() {
    return {
      addReview: false,
      name: null,
      reviewBody: null,
      baseUrl: this.$baseUrl,
    };
  },
  methods: {
    handleNoClicked() {
      this.$emit("close-popup");
    },
    submitForm() {
      const data = {
        ...this.data,
        name: this.name,
        review_body: this.reviewBody,
      };

      axios
        .post(this.baseUrl + "/rate-product", data)
        .then((response) => {
          if (response.status === 200) {
            this.$emit("close-popup");
          }
        })
        .catch((error) => {
          this.$emit("close-popup");
          this.$emit(
            "result",
            "Sorry, you already added review for this product"
          );
          console.log("error", error);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/styles/main.scss";

.review-popup {
  display: flex;
  position: absolute;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  z-index: 9999;

  .review-details {
    display: flex;
    padding: 20px;
    background-color: var(--background-color);
    min-height: 30%;

    .row {
      margin-top: 10%;
      display: flex;
      flex-direction: row;
      justify-content: center;
      gap: 20px;

      * {
        min-width: 30%;
      }
    }
  }

  .form-wrapper {
    display: flex;
    flex: 1;
    text-align: left;
    position: relative;

    .go-back-button {
      position: absolute;
    }

    form {
      padding: 20px;
      display: flex;
      gap: 10px;
      flex-direction: column;
      flex: 1;

      .input-wrapper {
        .primary-input {}
      }

      .textarea-wrapper {
        display: flex;
        flex-direction: column;
        flex: 1;

        textarea {
          min-height: 200px;
          height: 100%;
          width: 100%;
        }
      }
    }
  }
}
</style>