<template>
  <div class="readme-wrapper">
    <div class="readme">
      <h1>Important Notice</h1>
      <h2>About This Project</h2>
      <div class="details">
        <p>
          This web-commerce project has been developed to demonstrate my
          technical skills and expertise in web development to potential
          employers.
        </p>
        <p>
          All products showcased are generated via scripts, and all images used
          are stock photos.
        </p>
        <p>
          For demonstration purposes, please use the following dummy payment
          card number: <b>4444 3333 2222 1111</b> with any CVV and expiry date.
        </p>
        <p>
          You can access the admin panel by adding <b>"/admin"</b> to Url and
          logging in with following credentials:
        </p>
        <p><b>Login:</b> Admin <b>Password:</b> lkcommerceadmin</p>
        <p>The website is hosted on Amazon Web Services (AWS).</p>
      </div>
      <button @click="emitNoticeRead">Ok</button>
    </div>
  </div>
</template>
<script>
export default {
  name: "ShopReadme",
  data() {},
  methods: {
    emitNoticeRead() {
      this.$emit("notice-read");
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../assets/styles/main.scss";
.readme-wrapper {
  position: absolute;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;

  min-height: 100vh;
  width: 100vw;
}

.readme {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  padding: 20px;
  text-align: center;

  button {
    border-radius: 15px;
    padding: 10px;
    border: 1px solid var(--secondary-color);
    width: 40%;
  }
  button:hover {
    @include secondary-button;
  }

  h1 {
    font-size: 2em;
    margin-bottom: 10px;
    color: #ff5722;
  }

  h2 {
    font-size: 1.5em;
    margin-bottom: 20px;
    color: #333333;
  }

  .details {
    font-size: 1em;
    line-height: 1.6;
    color: #666666;
    text-align: left;

    p {
      margin-bottom: 15px;
    }
  }
}
</style>