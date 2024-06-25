<template>
  <div class="canvas-wrapper">
    <h3>Top 10 Products:</h3>
    <canvas id="productChart"></canvas>
  </div>
</template>
  
  <script>
import {
  Chart,
  DoughnutController,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
Chart.register(DoughnutController, Title, Tooltip, Legend, ArcElement);
import axios from "axios";
export default {
  name: "ProductChart",
  data() {
    return {
      baseUrl: this.$baseUrl,
      products: [],
    };
  },
  methods: {
    renderChart() {
      const ctx = document.getElementById("productChart").getContext("2d");
      const chartData = this.prepareChartData();

      new Chart(ctx, {
        type: "doughnut",
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
            tooltip: {
              callbacks: {
                label: (context) => {
                  const index = context.dataIndex;
                  const value = context.raw;
                  const category = chartData.categories[index];
                  return [`Count: ${value}`, `Category: ${category}`];
                },
              },
            },
          },
        },
      });
    },
    prepareChartData() {
      const labels = [];
      const data = [];
      const categories = [];
      this.products.forEach((product) => {
        labels.push(product.product_name);
        data.push(product.count);
        categories.push(product.product_category);
      });
      return {
        labels,
        data,
        categories,
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
    getPopularProducts() {
      axios
        .get(`${this.baseUrl}/popular-products`)
        .then((response) => {
          this.products = response.data.product_counts;
          this.renderChart();
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
  mounted() {
    this.getPopularProducts();
  },
};
</script>
  
  <style lang="scss">
.canvas-wrapper {
  max-height: 50%;
  display: flex;
  flex-direction: column;
  text-align: left;
  #productChart {
    align-self: center;
  }
}
</style>