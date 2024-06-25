<template>
    <div class="bundle-list">
        <div class="search-bar">
            <AdminSearchBar @search-input="handleSearchInput" :placeholder="'Search bundles ...'"/>
        </div>
    <div class="grid-container">
        <div class="bundles">
    <div v-for="(promotion, index) in paginatedPromotionList" :key="index" class="admin-grid-item">
        <div class="row"><PreviewProduct :product="promotion.primary_product"/> <PreviewProduct :product="promotion.discounted_product"/></div>
        <div class="bottom-row">
            <div >
            <b>Discount: </b>
            {{ promotion.discount }} $
            </div>
            <button @click="this.$emit('bundle-clicked', promotion)" class="primary-button">Edit</button>
        </div>
    </div>
    </div>
    </div>
    <AdminPagination @page-clicked="handlePageClicked" :length="filteredPromotionList.length" :perPage="9"/>
    </div>
</template>
<script>
import axios from 'axios';
import PreviewProduct from '../PreviewProduct.vue';
import AdminSearchBar from './AdminSearchBar.vue';
import AdminPagination from './AdminPagination.vue';
export default {
    name: 'AdminBundleList',
    components: {
        PreviewProduct,
        AdminSearchBar,
        AdminPagination
    },
    data() {
        return {
            baseUrl: this.$baseUrl,
            promotions: [],
            searchPhrase: '',
            currentPage: 0,
        }
    },
    computed: {
        filteredPromotionList() {
            let searchPhrase = this.searchPhrase || '';
            return this.promotions.filter((promotion) =>
            promotion.primary_product.name.toLowerCase().includes(searchPhrase.toLowerCase()) ||
            promotion.discounted_product.name.toLowerCase().includes(searchPhrase.toLowerCase()))
        },
        paginatedPromotionList() {
      const start = this.currentPage * 9;
      const end = start + 9;
      return this.filteredPromotionList.slice(start, end);
    },
    },
    methods: {
        getPromotionBundles() {
            axios.get(`${this.baseUrl}/product-promotions`).then(response => {
                this.promotions = response.data.sort((a, b) => a.id - b.id);
            }).catch(error => {
                console.log('error', error)
            })
        },
        handlePageClicked(pageIndex) {
            this.currentPage = pageIndex; 
        },
        handleSearchInput(string){
            this.searchPhrase = string
        }
    },
    mounted(){
        this.getPromotionBundles()
    }
}
</script>
<style lang="scss">
@import '../../assets/styles/main.scss';
.bundle-list {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-inline: 5vw;
    gap: 20px;
    margin-top: 20px;
    .search-bar {
        display: flex;
        flex-direction: row;
        
    }
.grid-container {
    .bundles {
        display: grid;
        grid-template-columns: auto auto auto;
        grid-template-rows: auto auto auto;
        gap: 15px;
        height: 100%;
    }
}
}
@media (max-width: 1400px) {
    .bundle-list {
        .grid-container {
            .bundles {
                grid-template-columns: 1fr 1fr;
                justify-items: center;
                .admin-grid-item {
                    padding: 10px;
                    width: min-content;
                }
            }
        }
    }
}
@media (max-width: 950px) {
    .bundle-list {
        .grid-container {
            .bundles {
                grid-template-columns: 1fr;
                grid-template-rows: 1fr;
                justify-items: center;
                
                .admin-grid-item {
                    width: min-content;
                    padding: 11px;
                }
            }
        }
    }
}


</style>