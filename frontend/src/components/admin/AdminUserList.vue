<template>
    <div class="user-list">
    
    <div class="search-bar">
        <AdminSearchBar @search-input="handleSearchInput" :placeholder="'Search users ...'"/>
    </div> 
<div class="grid-container">
    
    <div class="users">
        <div  v-for="(user, index) in paginatedUserList" :key="index" class="admin-grid-item">
            <div class="row">
        <h2>{{ user.username }}</h2>
        <div class="user-status-active" v-if="user.is_active == true">Active</div>
        <div class="user-status-inactive" v-else>Inactive</div>
        </div>
        <div class="row">
            <b>Email: </b>
            <p>{{ user.email }}</p>
        </div>
        <div class="row">
            <div>
            <b>First name: </b>
            <p>{{ user.first_name }}</p>
            </div>
            <div>
            <b>Last name: </b>
            <p>{{ user.last_name }}</p>
            </div>
        </div>
        <div class="row">
            <div>
            <b>Last logged in: </b>
            <p>{{ toReadableDate(user.last_login) }}</p>
            </div>
            <div>
            <b>Signed up on: </b>
            <p>{{toReadableDate(user.date_joined)}}</p>
            </div>
        </div>
        <div class="row">
            <div class="buttons">
            <button @click="handleSendEmail(user)" class="primary-button">Send Email</button>
            <button @click="handleGetUserOrders(user.username)" class="primary-button">Orders</button>
            </div>
        </div>
        </div>
    </div>
</div>
<AdminPagination @page-clicked="handlePageClicked" :length="filteredUserList.length" :perPage="9"/>
</div>
</template>

<script>
import axios from 'axios'
import AdminSearchBar from './AdminSearchBar.vue'
import AdminPagination from './AdminPagination.vue';
export default {
    name: 'AdminUserList',
    components: {
        AdminSearchBar,
        AdminPagination
    },
    data() {
        return {
            users: [],
            baseUrl: this.$baseUrl,
            searchPhrase: '',
            currentPage: 0
        }
    },
    computed: {
        filteredUserList() {
            let searchPhrase = this.searchPhrase || '';
            return this.users.filter((user) =>
        user.username.toLowerCase().includes(searchPhrase.toLowerCase()) ||
        user.first_name.toLowerCase().includes(searchPhrase.toLowerCase())||
        user.last_name.toLowerCase().includes(searchPhrase.toLowerCase()))
    
        },
        paginatedUserList() {
            const start = this.currentPage * 9;
            const end = start + 9;
            return this.filteredUserList.slice(start, end);
        }
    },
    methods: {
        getUsers() {
            axios.get(`${this.baseUrl}/users`).then(response =>
                {
                    this.users = response.data
                }
            ).catch(error => {
                console.log('error', error)
            })
        },
        toReadableDate(string) {
            if(string) {
            const date = new Date(string)
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            const formattedDate = date.toLocaleDateString('en-US', options);
            return formattedDate
            } else {
                return 'Never'
            }
        },
        handleSendEmail(user) {
            this.$emit('send-email-clicked', user)
        },
        handleSearchInput(string) {
            this.searchPhrase = string
        },
        handleGetUserOrders(username) {
            this.$router.push({ path: '/admin/orders', query: { username: username } });
        },
        handlePageClicked(pageIndex) {
            this.currentPage = pageIndex
        }
    },
    mounted() {
        this.getUsers()
    }
}
</script>

<style lang="scss">
.user-list {
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
.users {
    display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
        gap: 15px;
        height: 100%;
        
        .row {
           justify-content: left;
            text-wrap: nowrap;
            text-align: left;
            align-items: center;
            flex-wrap: wrap;
            .buttons {
                margin-left: auto;
                flex: 0;
                gap: 10px;
            }
            div {
                display: flex;
                flex: 1;
                gap: 5px;
                flex-direction: row;
            }
            h2 {
                margin: 0;
            }
            .user-status-active {
                flex: 0;
                background-color: green;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            .user-status-inactive {
                flex: 0;
                background-color: red;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
        }
    }
}
@media (max-width: 800px) {
    .user-list{
    .users {
        grid-template-columns: 1fr 1fr;
     
    }
}
}

@media (max-width: 600px) {
    .user-list {
    .users {
        grid-template-columns: 1fr;
    }
}
}
</style>