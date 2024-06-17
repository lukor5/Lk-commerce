<template>
    <input class="primary-input" type="text" v-model="searchPhrase" @input="emitInput" :placeholder="placeholder">
</template>
<script>
export default {
    name: 'AdminSearchBar',
    props: {
        placeholder: String
    },
    data() {
        return {
            searchPhrase: '',
        }
    },
    methods: {
        emitInput() {
            this.$emit('search-input', this.searchPhrase)
        }
    }
}
</script>
<style lang="scss" scoped>
@import '../../assets/styles/main.scss';
.primary-input {
    width: min-content;
}
</style>
