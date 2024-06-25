  <template>
    <div class="hello" :style="{ height: helloHeight }">
      <div class="catch-phrase">
        <h1>Fashion, your way</h1>
      </div>
      <div
        id="left"
        class="sub-section"
        :style="{
          backgroundImage: 'url(' + currentLeftImage + ')',
          opacity: this.leftOpacity,
        }"
      ></div>
      <div
        id="right"
        class="sub-section"
        :style="{
          backgroundImage: 'url(' + currentRightImage + ')',
          opacity: this.rightOpacity,
        }"
        @animationend="handleImageChange"
      ></div>
    </div>
  </template>

  <script>
  import { setInterval } from "core-js";

  export default {
    name: "HeroSection",
    props: {
      quickAccessHeight: Number,
      navBarHeight: Number,
    },
    computed: {
      currentLeftImage() {
        return this.leftImages[this.currentLeftIndex];
      },
      currentRightImage() {
        return this.rightImages[this.currentRightIndex];
      },
      helloHeight() {
      const remainingHeight = `calc(100vh - ${this.quickAccessHeight}px - ${this.navBarHeight}px)`;
      return remainingHeight;
    },
    },
    data() {
      return {
        leftImages: [
          require("../assets/pexels-left-1.jpg"),
          require("../assets/pexels-left-2.jpg"),
          require("../assets/pexels-left-3.jpg"),
        ],
        rightImages: [
          require("../assets/pexels-right-1.jpg"),
          require("../assets/pexels-right-2.jpg"),
          require("../assets/pexels-right-3.jpg"),
        ],
        currentLeftIndex: 0,
        currentRightIndex: 0,
        leftInterval: 8000, // Duration in milliseconds for left
        rightInterval: 8000, // Duration in milliseconds for right
        leftOpacity: 0, // Start fully visible for left
        rightOpacity: 0, // Start fully visible for right
      };
    },
    methods: {
      setLeftImageLoop() {
        setInterval(() => {
          this.leftOpacity = 0; // Set opacity to 0 for left
          setTimeout(() => {
            this.currentLeftIndex =
              (this.currentLeftIndex + 1) % this.leftImages.length;
            this.leftOpacity = 1; // Reset opacity to 1 for left
          }, 1350); // Short delay before changing images and resetting opacity
        }, this.leftInterval);
      },
      setRightImageLoop() {
        setInterval(() => {
          this.rightOpacity = 0; // Set opacity to 0 for right
          setTimeout(() => {
            this.currentRightIndex =
              (this.currentRightIndex + 1) % this.rightImages.length;
            this.rightOpacity = 1; // Reset opacity to 1 for right
          }, 2000); // Short delay before changing images and resetting opacity
        }, this.rightInterval);
      },
      setImageLoop() {
        this.setLeftImageLoop();
        this.setRightImageLoop();
      },
    },
    mounted() {
      this.setImageLoop();
      setTimeout(() => {
        this.leftOpacity = 1;
        this.rightOpacity = 2;
      }, 300);
    },
  };
  </script>

  <style lang="scss" scoped>
  @import "../assets/styles/main.scss";

  .hello {
    display: flex;
    flex-direction: row;
    position: relative;
    font-family: $main-font-stack;
    justify-content: center;
    .catch-phrase {
      position: absolute;
      top: 60%;
      left: 0;
      z-index: 9;
      h1 {
        background-color: rgba(255, 255, 255, 0.3);
        color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-bottom-left-radius: 20px;
        border-top-right-radius: 40px;
      }
    }

    #left {
      transition: opacity 1.3s ease;
      background-size: cover;
      width: 60%;
    }

    #right {
      transition: opacity 2s ease;
      background-size: cover;
      width: 40%;
    }

    .sub-section {
      display: flex;
      flex-direction: column;
      height: auto;
      justify-content: flex-end;
      text-align: left;
    }
  }
  </style>

  <!-- Add "scoped" attribute to limit CSS to this component only -->