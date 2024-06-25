<template>
<div v-if="length" class="pagination">
    <button class="icon-button" @click="handleIconClicked('left')" :class="{'disabled': isFirstPage}"><font-awesome-icon class="icon" :icon="['fas', 'angles-left']" /></button>
    <div class="pages">
        <button @click="handlePageClick(index)" class="pagination-button" v-for="(page, index) in numberOfPages" :key="index" :class="{'active': currentlyClicked == index}">{{ index + 1 }}</button>
    </div>
    <button class="icon-button" @click="handleIconClicked('right')" :class="{'disabled': isLastPage}"><font-awesome-icon class="icon" :icon="['fas', 'angles-right']" /></button>
</div>
</template>

<script>
export default {
    name: 'AdminPagination',
    props: {
        length: {
            type: Number,
            required: true
        },
        perPage: {
            type: Number,
            required: true
        }
    },
    computed: {
        numberOfPages() {
            return Math.ceil(this.length / this.perPage);
        },
        isFirstPage() {
            return this.currentlyClicked === 0;
        },
        isLastPage() {
            return this.currentlyClicked === this.numberOfPages - 1;
        }
    },
    data() {
        return {
            currentlyClicked: 0 
        };
    },
    methods: {
        handlePageClick(index) {
            this.currentlyClicked = index;
            this.$emit('page-clicked', index);
        },
        handleIconClicked(direction) {
            if (direction === 'right' && !this.isLastPage) {
                this.handlePageClick(this.currentlyClicked + 1);
            } else if (direction === 'left' && !this.isFirstPage) {
                this.handlePageClick(this.currentlyClicked - 1);
            }
        }
    }
};
</script>

<style lang="scss">
@import '../../assets/styles/main.scss';
.pagination {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    * {
        box-shadow: none !important;
    }
    .icon-button:hover {
        background-color: var(--primary-color);
    }
    .disabled {
        * {
            color: var(--subtle-border-color) ;
        }
        &:hover {
            background-color: var(--background-color);
            cursor: default;
        }
    }
    .pages {
        .active {
            color: white;
            background-color: var(--primary-color);
            border-radius: 15px;
        }
        .pagination-button {
            &:hover {
                transform: scale(1.1);
            }
        }
      
        
    }
}
</style>