<template>
  <div class="popup-wrapper">
    <div class="popup">
      <button @click="this.$emit('close-popup')" class="exit-button">X</button>
      <div class="popup-top">
        <h2>Send email</h2>
        <p>
          Recipient: <b>{{ this.userToEmail.email }}</b>
        </p>
        <p>
          <b>{{ this.userToEmail.first_name }}</b>
          <b>{{ this.userToEmail.last_name }}</b>
        </p>
      </div>
      <div class="input-label">
        <label>Subject</label>
        <input class="primary-input" type="text" v-model="subject" />
      </div>
      <div class="input-label">
        <label>Message</label>
        <textarea class="primary-input" type="text" v-model="body" />
      </div>
      <div class="input-label">
        <label>Attach files</label>
        <div class="buttons">
          <div class="file-attach-wrapper">
            <label for="file-attach" class="custom-file-attach">
              <b>Attach file</b>
              <font-awesome-icon :icon="['fas', 'paperclip']" class="fa-xl" />
            </label>
            <div class="files-count" v-if="filesLength > 0">
              {{ filesLength }}
            </div>

            <input
              id="file-attach"
              type="file"
              class="file-attach"
              multiple
              @change="handleFileChange"
            />
          </div>
          <button @click="sendEmail" class="primary-button">Send</button>
        </div>
      </div>
      <div v-if="filesLength > 0" class="attachment-list">
        <div
          v-for="(file, index) in files"
          :key="index"
          class="single-attachment"
        >
          <span>{{ file.name }}</span>
          <button @click="deleteAttachment(index)" class="icon-button">
            <font-awesome-icon :icon="['fas', 'trash']" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SendEmailPopup",
  props: {
    userToEmail: Object,
  },
  computed: {
    filesLength() {
      return this.files.length;
    },
  },
  data() {
    return {
      baseUrl: this.$baseUrl,
      files: [],
      subject: '',
      body: ''
    };
  },
  methods: {
    sendEmail() {
        const formData = new FormData()
        formData.append('user', JSON.stringify(this.userToEmail))
        formData.append('subject', this.subject)
        formData.append('body', this.body)
        this.files.forEach((file, index) => {
        formData.append(`files[${index}]`, file);
      });
      console.log(formData)
      axios
        .post(`${this.baseUrl}/email-customer`, formData, {
            headers: {
          'Content-Type': 'multipart/form-data'
        }
        })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    handleFileChange(event) {
      this.files = Array.from(event.target.files);
    },
    deleteAttachment(index) {
      this.files.splice(index, 1);
    },
  },
  mounted() {
    console.log(this.userToEmail);
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/styles/main.scss";
.popup-wrapper {
    position: absolute;
  display: flex;
  width: 100%;
  height: 100vh;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  .popup {
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: var(--background-color);
    gap: 20px;
    padding: 15px;
    min-width: 40vw;
    border-radius: 5px;
    max-height: 100vh;
    flex-wrap: wrap;
    margin: auto;
    .exit-button {
      position: absolute;
      top: 10px;
      right: 10px;
      background: transparent;
      border: none;
      font-size: 1.5em;
      cursor: pointer;
      color: var(--text-color);
    }
    .exit-button:hover {
      color: red;
    }
    .popup-top {
      display: flex;
      flex-direction: column;
      text-align: left;
    }
    .input-label {
      text-align: left;
      display: flex;
      flex-wrap: wrap;
      flex-direction: column;
      padding: 10px;
      gap: 10px;

      label {
        @include small-text;
      }
      textarea {
        resize: none;
        min-height: 20vh;
      }
      .buttons {
        display: flex;
        flex-direction: row;
        gap: 20px;
        flex-wrap: wrap;
        .primary-button {
          flex: 1;
        }
        .file-attach-wrapper {
          position: relative;
          input[type="file"] {
            display: none;
          }
          .custom-file-attach {
            display: flex;
            flex-direction: row;
            cursor: pointer;
            padding: 10px;
            font-size: 1em;
            width: auto;
            flex-wrap: wrap;
            gap: 10px;
            border: 1px solid var(--border-color);
            border-radius: 5px;
          }
          .custom-file-attach:hover {
            color: var(--text-color);
          }
          .files-count {
            position: absolute;
            bottom: -10px;
            right: -10px;
            width: 25px;
            height: 25px;
            border-radius: 100%;
            text-align: center;
            background-color: var(--secondary-color);
            border: 1px solid var(--secondary-color);
            color: white;
          }
        }
      }
    }
    .attachment-list {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      max-width: 50vw;
      .single-attachment {
        @include small-text;
      }
    }
  }
}
@media (max-width: 800px) {
  .popup-wrapper {
    .popup {
      width: 95%;
      .input-label {
        .buttons {
            flex-direction: column;
        }
      }
    }
  }
}
</style>