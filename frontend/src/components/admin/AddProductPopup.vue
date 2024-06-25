<template>
  <div class="popup-wrapper">
    <div class="popup">
      <button
        @click="closePopup"
        class="exit-button"
        style="position: absolute; right: 5%"
      >
        <font-awesome-icon :icon="['fas', 'x']" />
      </button>
      <form class="add-product-form">
        <div class="row">
          <div class="input-wrapper">
            <label for="nameInput">Product name</label>
            <input v-model="productName" type="text" id="nameInput" />
          </div>
        </div>
        <div class="row">
          <div class="input-wrapper">
            <label for="priceInput">Price</label>
            <input
              v-model="price"
              type="number"
              id="priceInput"
              placeholder="Price ..."
            />
          </div>
          <div class="input-wrapper">
            <label for="discount">Discount</label>
            <input
              v-model="discount"
              type="number"
              id="discount"
              step="0.01"
              min="0.01"
              max="1"
            />
          </div>
        </div>
        <div class="row">
          <div class="textarea-wrapper">
            <label for="bodyInput">Body</label>
            <textarea
              v-model="body"
              id="bodyInput"
              type="text"
              placeholder="Product body ..."
            />
          </div>
        </div>
        <div class="row">
          <div class="input-wrapper">
            <label for="type">Type</label>
            <div class="common-dropdown-wrapper">
              <div
                v-if="this.selectedType.type"
                class="primary-button"
                @click="toggleTypeDropdown"
              >
                {{ this.selectedType.type }}
                <font-awesome-icon :icon="['fas', 'caret-down']" />
              </div>
              <div v-else class="primary-button" @click="toggleTypeDropdown">
                Select type <font-awesome-icon :icon="['fas', 'caret-down']" />
              </div>
              <div
                class="common-dropdown-list"
                :class="{ 'show-dropdown': showDropdown }"
              >
                <ul>
                  <li
                    @click="setSelectedType(type)"
                    v-for="(type, index) in types"
                    :key="index"
                  >
                    {{ type.type }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="input-wrapper">
            <label for="isBestseller">Bestseller</label>
            <input v-model="isBestseller" type="checkbox" id="isBestseller" />
          </div>
          <ul class="category-radio-list">
            <li v-for="(category, index) in this.categoryList" :key="index">
              <span>{{ category }}</span
              ><label class="radio-container"
                ><input
                  v-model="selectedCategory"
                  :value="category"
                  type="radio"
                  name="categoryRadio"
                  id="categoryRadio" /><span class="radio"></span
              ></label>
            </li>
          </ul>
        </div>

        <button class="primary-button" @click.prevent="submitForm">
          Add product
        </button>
      </form>
      <div class="variants">
        <div>
          <h3>Please add variants</h3>
          <div class="row">
            <input type="text" v-model="variantSize" placeholder="size" />
            <input type="text" v-model="variantColor" placeholder="color" />
            <input type="number" v-model="variantStock" placeholder="stock" />
            <button
              class="primary-button"
              id="addVariantButton"
              @click="addVariant"
            >
              <span>Add</span><font-awesome-icon :icon="['fas', 'plus']" />
            </button>
          </div>
          <ul>
            <li v-for="(variant, index) in this.variants" :key="index">
              <span>{{ variant.size }}</span
              ><span>{{ variant.color }}</span
              ><span>{{ variant.stock }}</span
              ><button class="icon-button" @click="deleteVariant(index)">
                <font-awesome-icon :icon="['fas', 'minus']" />
              </button>
            </li>
          </ul>
        </div>
        <div class="image-container">
          <h2>Image</h2>
          <img v-if="selectedImage" :src="selectedImage" />
          <img v-else :src="productUrl" />
          <label class="file-upload">
            <input
              type="file"
              @change="handleImageUpload"
              accept="image/png, image/jpeg"
            />
            Upload
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";
export default {
  name: "AddProductPopup",
  computed: {
    ...mapState(["categoryList"]),
    isPriceValid() {
      if (typeof this.price === "number") {
        return this.price > 0;
      }
      if (typeof this.price === "string") {
        let convertedPrice = parseFloat(this.price.replace(",", "."));
        if (!isNaN(convertedPrice) && convertedPrice > 0) {
          return true;
        }
      }
      return false;
    },
    isDiscountValid() {
      return this.discount > 0 && this.discount <= 1;
    },
    isTypeSelected() {
      return this.selectedType.id;
    },
    hasVariants() {
      return this.variants.length > 0;
    },
    isColorValid() {
      return this.acceptableColors.find((color) => color === this.variantColor);
    },
  },
  props: {
    productId: null,
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      baseMediaUrl: this.$baseMediaUrl,
      types: [],
      showDropdown: false,
      variantSize: "",
      variantColor: "",
      variantStock: null,
      variants: [],
      selectedType: [],
      productName: "",
      price: null,
      discount: null,
      isBestseller: false,
      body: "",
      selectedCategory: null,
      messages: [],
      product: null,
      productUrl: "",
      selectedImage: null,
      uploadedImage: null,
      acceptableColors: [
        "Red",
        "Orange",
        "Yellow",
        "Green",
        "Blue",
        "Purple",
        "Pink",
        "Black",
        "White",
        "Gray",
        "Brown",
        "Beige",
      ],
    };
  },
  methods: {
    getProductTypes() {
      axios
        .get(this.baseUrl + "/types")
        .then((response) => {
          this.types = response.data;
        })
        .catch((error) => {
          console.log("error: ", error);
        });
    },
    getProduct() {
      axios
        .get(this.baseUrl + "/products/" + this.productId)
        .then((response) => {
          this.product = response.data;
          this.price = this.product.price;
          this.discount = this.product.discount;
          this.isBestseller = this.product.is_bestseller;
          this.productName = this.product.name;
          let typeId = this.product.product_type;
          let filteredType = this.types.filter((type) => type.id === typeId);
          this.selectedType = filteredType[0];
          this.product.product_variants.forEach((variant) => {
            this.variants.push({
              size: variant.size,
              color: variant.color,
              stock: variant.stock,
            });
          });
          this.body = this.product.body;
          this.selectedCategory = this.product.category;
          this.productUrl = this.baseMediaUrl + this.product.product_image;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    toggleTypeDropdown() {
      this.showDropdown = !this.showDropdown;
    },

    setSelectedType(selectedType) {
      this.selectedType = selectedType;
      this.showDropdown = false;
    },
    closePopup() {
      this.$emit("close-popup");
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      this.uploadedImage = file;
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.selectedImage = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    addVariant() {
      if (this.variantSize && this.variantColor && this.variantStock) {
        let firstLetter = this.variantColor.charAt(0).toUpperCase();
        this.variantColor = firstLetter + this.variantColor.slice(1);
        if (this.isColorValid) {
          let variant = {
            size: this.variantSize,
            color: this.variantColor,
            stock: this.variantStock,
          };
          this.variants.push(variant);
          (this.variantSize = ""),
            (this.variantColor = ""),
            (this.variantStock = null);
        } else {
          this.messages = [];
          this.messages.push(
            "Error: Color not recognized. Please type in a basic color"
          );
          this.$emit("result", this.messages);
        }
      } else {
        this.messages.push("Error: Empty Variant!");
      }
    },
    deleteVariant(index) {
      this.variants.splice(index, 1);
    },
    submitForm() {
      if (!this.checkFormValidity()) {
        this.$emit("result", this.messages);
        return;
      }
      let formData = new FormData();
      formData.append("name", this.productName);
      formData.append("type", this.selectedType.id);
      formData.append("category", this.selectedCategory);
      formData.append("price", this.price);
      formData.append("discount", this.discount);
      formData.append("is_bestseller", this.isBestseller);
      formData.append("body", this.body);
      formData.append("product_image", this.uploadedImage);
      formData.append("category", this.selectedCategory);
      formData.append("variants", JSON.stringify(this.variants));

      if (formData) {
        axios
          .post(this.baseUrl + "/create-product", formData)
          .then((response) => {
            if (response.status == 200) {
              this.messages.push("Product added successfully");
              this.$emit("result", this.messages);
              this.$emit("close-popup");
            }
          })
          .catch((error) => {
            console.log("error:", error);
          });
      }
    },

    checkFormValidity() {
      this.messages = [];
      if (!this.isPriceValid) {
        this.messages.push("Error: Price Invalid");
      }
      if (!this.isDiscountValid) {
        this.messages.push("Error: Discount Invalid");
      }
      if (!this.isTypeSelected) {
        this.messages.push("Error: No type selected");
      }
      if (!this.hasVariants) {
        this.messages.push("Error: No variants added");
      }
      return this.messages.length == 0;
    },
  },
  mounted() {
    this.getProductTypes();
    if (this.productId) {
      this.getProduct();
    }
  },
};
</script>

<style lang="scss">
@import "../../assets/styles/main.scss";

.popup-wrapper {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;

  .popup {
    position: relative;
    display: flex;
    background-color: var(--background-color);
    gap: 30px;
    padding: 15px;
    border-radius: 5px;
    flex-wrap: wrap;
    margin: auto;
    .exit-button {
      position: absolute;
      &:hover {
        * {
          color: red;
        }
      }
    }

    .variants {
      border-left: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      width: auto;
      gap: 20px;
      padding: 15px;

      ul {
        display: grid;
        grid-template-columns: 1fr;
        max-height: 30vh;
        list-style: none;
        overflow-y: scroll;

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

        li {
          padding: 0;
          display: grid;
          grid-template-columns: 1fr 1fr 1fr min-content;
          text-align: left;
        }
      }

      .row {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        text-align: center;

        input {
          max-width: 80px;
        }
        #addVariantButton {
          display: flex;
          gap: 5px;
          align-items: center;
        }
      }
    }

    .image-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 15px;
      border-top: 1px solid var(--border-color);
      padding-top: 20px;

      img {
        max-width: 200px;
        object-fit: contain;
      }

      .file-upload {
        cursor: pointer;
        background-color: var(--primary-color);
        color: white;
        padding: 10px;

        &:hover {
          background-color: #222325;
        }

        input {
          display: none;
        }
      }
    }

    .add-product-form {
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding: 15px;
      justify-content: space-around;

      .row {
        display: flex;
        flex-direction: row;
        gap: 20px;
        align-items: center;
        width: 100%;
      }

      .input-wrapper {
        display: flex;
        flex-direction: column;
        text-align: left;

        input {
          border-bottom: 1px solid var(--border-color);
          padding: 5px;
        }
      }

      .textarea-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
        text-align: left;

        textarea {
          height: 200px;
        }
      }

      .row {
        display: flex;
        flex-direction: row;
      }

      .category-radio-list {
        display: flex;
        flex-direction: row;
        list-style: none;
        gap: 10px;

        li {
          display: flex;
          flex-direction: column;
          padding: 0px;
        }
      }
    }

    .show-dropdown {
      display: block;
    }
  }
}

@media (max-width: 1000px) {
  .popup-wrapper {
    .popup {
      justify-content: center;

      .variants {
        width: 45%;
      }

      .add-product-form {
        width: 45%;
      }
    }
  }
}

@media (max-width: 750px) {
  .popup-wrapper {
    height: auto;

    .popup {
      .variants {
        width: auto;
        border-left: none;
        max-height: auto;
      }

      .add-product-form {
        width: auto;
      }
    }
  }
}
</style>