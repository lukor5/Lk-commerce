<template>
    <div class="canvas-wrapper">
        <h3>Popular categories:</h3>
      <canvas id="categoryChart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, PieController, Title, Tooltip, Legend, ArcElement } from "chart.js";
  Chart.register(PieController, Title, Tooltip, Legend, ArcElement);
  import axios from "axios";
  export default {
    name: "CategoryChart",
    data() {
        return {
            baseUrl: this.$baseUrl,
            categories: []
        }
    },
    methods: {
      renderChart() {
        const ctx = document.getElementById("categoryChart").getContext("2d");
        const chartData = this.prepareChartData();
  
        new Chart(ctx, {
          type: "pie",
          data: {
            labels: chartData.labels,
            datasets: [
              {
                label: "Count",
                data: chartData.data,
                backgroundColor: this.generateColors(chartData.labels.length),
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: "top",
              },
            
            },
          },
        });
      },
      prepareChartData() {
      const labels = [];
      const data = [];
        this.categories.forEach((category) => {
          labels.push(category.type);
          data.push(category.count);
        });
      return {
        labels,
        data,
      };
    },
    generateColors(count) {
      const colors = [
        "#6c757d", 
        "#17a2b8", 
        "#28a745", 
        "#007bff", 
        "#fd7e14", 
        "#dc3545", 
        "#ffc107", 
        "#6610f2", 
        "#6f42c1", 
        "#e83e8c", 
      ];

      return colors.slice(0, count);
    },
      getPopularCategories() {
        axios.get(`${this.baseUrl}/popular-types`).then(response => {
            this.categories = response.data.type_counts
            this.renderChart()
        }).catch(error => {
            console.log('error', error)
        })
      }
    },
    mounted() {
      this.getPopularCategories()
    },
  };
  </script>
  
  <style lang="scss">
.canvas-wrapper {
    max-height: 50%;
    display: flex;
    flex-direction: column;
    text-align: left;
    #categoryChart {
        align-self: center;
    }
}
  </style>