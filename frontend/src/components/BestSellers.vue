<template>
  <div class="bestsellers">
    <h1>Featured products</h1>
    <h3>Chosen by our satisfied customers</h3>
    <div class="carousel-wrapper">
      <button @click="handleCarouselClicked('left')">
        <font-awesome-icon :icon="['fas', 'angles-left']" />
      </button>
      <div class="bestsellers-wrapper">
        <div
          :style="{ 'animation-duration': animationDuration }"
          class="main-carousel"
          :class="{
            'move-carousel-right': moveCarousel === 'right',
            'move-carousel-left': moveCarousel === 'left',
            'main-carousel': moveCarousel === 'none',
          }"
          @animationend="animationEnded()"
        >
          <PreviewProduct
            :class="{
              'show-carousel-product': showCarouselProduct === 'left',
              'hide-carousel-product':
                showCarouselProduct === 'right' ||
                showCarouselProduct === 'none',
            }"
            style="left: -200px"
            v-if="carouselHiddenBestsellers.length > 0"
            :product="carouselHiddenBestsellers[0]"
          />
          <PreviewProduct
            v-for="(bestseller, index) in carouselBestsellers"
            :key="bestseller.id"
            :direction="this.moveCarousel"
            :index="index"
            :product="bestseller"
            @product-clicked="handleProductClicked"
          ></PreviewProduct>
          <PreviewProduct
            :class="{
              'show-carousel-product': showCarouselProduct === 'right',
              'hide-carousel-product':
                showCarouselProduct === 'left' ||
                showCarouselProduct === 'none',
            }"
            style="right: -200px"
            v-if="carouselHiddenBestsellers.length > 0"
            :product="carouselHiddenBestsellers[1]"
          />
        </div>
      </div>
      <button @click="handleCarouselClicked('right'), toggleLoopCarousel()">
        <font-awesome-icon :icon="['fas', 'angles-right']" />
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import PreviewProduct from "./PreviewProduct.vue";

export default {
  name: "BestSellers",
  components: {
    PreviewProduct,
  },
  computed: {
    animationDuration() {
      return `${this.duration}s`;
    },
  },
  data() {
    return {
      bestsellers: [],
      carouselBestsellers: [],
      carouselHiddenBestsellers: [],
      leftIndex: 0,
      rightIndex: 3,
      showCarouselProduct: "none",
      moveCarousel: "none",
      moving: false,
      isMovingByItself: true,
      autoCarouselTimer: null,
      duration: 2,
      windowWidth: window.innerWidth,
      smallBestsellersMode: false,
      baseUrl: this.$baseUrl,
    };
  },
  methods: {
    getBestSellers() {
      axios
        .get(this.$baseUrl + "/bestsellers")
        .then((response) => {
          this.bestsellers = response.data;

          this.carouselBestsellers = this.bestsellers.slice(0, 3);
          this.carouselHiddenBestsellers[0] = this.bestsellers[0];
          this.carouselHiddenBestsellers[1] = this.bestsellers[2];
        })
        .catch((error) => {
          console.error("Error fetching bestsellers:", error);
        });
    },
    handleProductClicked(product) {
      this.$emit("product-clicked", product);
        window.scrollTo({
      top: 0,          
      behavior: 'smooth' 
    });
    },
    handleCarouselClicked(direction) {
      if (!this.moving) {
        this.moving = true;

        const length = this.bestsellers.length;
        switch (direction) {
          case "left":
            this.leftIndex = (this.leftIndex - 1 + length) % length;
            this.rightIndex = (this.rightIndex - 1 + length) % length;
            this.carouselHiddenBestsellers[0] =
              this.bestsellers[this.leftIndex];
            this.carouselHiddenBestsellers[1] =
              this.bestsellers[(this.rightIndex + 1) % length];

            this.showCarouselProduct = "left";
            this.moveCarousel = "left";

            break;

          case "right":
            this.leftIndex = (this.leftIndex + 1) % length;
            this.rightIndex = (this.rightIndex + 1) % length;
            this.carouselHiddenBestsellers[0] =
              this.bestsellers[(this.leftIndex - 1 + length) % length];
            this.carouselHiddenBestsellers[1] =
              this.bestsellers[(this.rightIndex - 1 + length) % length];

            this.showCarouselProduct = "right";
            this.moveCarousel = "right";

            break;
        }
      }
    },
    animationEnded() {
      this.updateCarousel();
      this.moveCarousel = "none";
      this.showCarouselProduct = "none";
      setTimeout(() => {
        this.moving = false;
      }, 100);
    },
    updateCarousel() {
      const length = this.bestsellers.length;
      const start = this.leftIndex;
      const end =
        this.rightIndex >= start ? this.rightIndex : this.rightIndex + length;
      this.carouselBestsellers = [];
      for (let i = start; i < end; i++) {
        this.carouselBestsellers.push(this.bestsellers[i % length]);
      }
      if (this.smallBestsellersMode) {
        this.carouselBestsellers = this.carouselBestsellers.slice(2, 3);
      }
    },
    toggleLoopCarousel() {
      this.isMovingByItself = false;
      this.duration = 1;
    },
    loopCarousel() {
      if (this.autoCarouselTimer) {
        clearInterval(this.autoCarouselTimer);
      }
      this.autoCarouselTimer = setInterval(() => {
        if (this.isMovingByItself) {
          this.handleCarouselClicked("right");
        }
      }, 5000);
    },
    updateVisibleProducts() {
      const width = window.innerWidth;
      const visibleCount = width < 900 ? 1 : 3;
      this.carouselBestsellers = this.bestsellers.slice(0, visibleCount);
    },
    handleResize() {
      this.windowWidth = window.innerWidth;
      if (this.windowWidth < 760) {
        this.smallBestsellersMode = true;
      } else {
        this.smallBestsellersMode = false;
      }
    },
  },
  emits: ["product-clicked"],

  mounted() {
    this.getBestSellers();
    this.loopCarousel();
    window.addEventListener("resize", this.handleResize);
  },
  watch: {},
};
</script>

<style lang="scss" scoped>
:root {
}

.bestsellers {
  z-index: 2;
  background-color: var(--background-color);
  margin-inline: 5%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
h3 {
  letter-spacing: 5px;
  padding-bottom: 5px;
  border-bottom: 1px solid var(--secondary-color);
}
.carousel-wrapper {
  display: flex;
  flex-direction: row;
  gap: 20px;

  button {
    position: static;
    z-index: 9999;
  }

  .bestsellers-wrapper {
    display: flex;
    position: relative;
    flex: 0;
    flex-direction: row;
    height: auto;
    justify-content: center;
    gap: 10px;

    .main-carousel {
      display: flex;
      position: static;
    }

    .move-carousel-right {
      animation-name: moveCarouselRight;
      animation-duration: 0.5s;
    }

    .move-carousel-left {
      animation-name: moveCarouselLeft;
      animation-duration: 0.5s;
    }

    .hide-carousel-product {
      transform: scale(0);
      opacity: 0;
      visibility: hidden;
      position: absolute;
    }

    .show-carousel-product {
      visibility: visible;

      position: absolute;
    }
  }
}

@keyframes moveCarouselRight {
  0% {
    transform: translateX(0);
  }

  75% {
    transform: translateX(-200px);
  }

  100% {
    transform: translateX(-200px);
  }
}

@keyframes moveCarouselLeft {
  0% {
    transform: translateX(0);
  }

  75% {
    transform: translateX(200px);
  }

  100% {
    transform: translateX(200px);
  }
}

@media (max-width: 800px) {
  .single-product {
    width: 200px;
  }
}
</style>