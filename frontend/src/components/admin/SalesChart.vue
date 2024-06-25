<template>
  <div class="canvas-wrapper">
    <h3>Sales in last 6 months:</h3>
    <canvas id="myChart"></canvas>
  </div>
</template>
  
  <script>
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import axios from "axios";
Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);
export default {
  name: "SalesChart",
  data() {
    return {
      payments: [],
      date: "",
      baseUrl: this.$baseUrl,
    };
  },
  methods: {
    renderChart() {
      const chartData = this.prepareChartData();
      const ctx = document.getElementById("myChart").getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: chartData.labels,
          datasets: [
            {
              label: "Total sales",
              data: chartData.data,
              backgroundColor: this.generateColors(chartData.labels.length),
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
    getPayments() {
      axios
        .get(`${this.baseUrl}/payments`)
        .then((response) => {
          this.payments = response.data;
          this.filterPaymentsByDate();
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
    getDates() {
      const currentDate = new Date();
      const sixMonthsAgo = new Date();
      sixMonthsAgo.setMonth(currentDate.getMonth() - 6);
      if (currentDate.getMonth() < 6) {
        sixMonthsAgo.setFullYear(currentDate.getFullYear() - 1);
      }
      return {
        today: currentDate,
        sixMonthsAgo: sixMonthsAgo,
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
    filterPaymentsByDate() {
      const { today, sixMonthsAgo } = this.getDates();
      const todayTime = today.getTime();
      const sixMonthsAgoTime = sixMonthsAgo.getTime();
      this.payments = this.payments.filter((payment) => {
        const paymentDate = new Date(payment.payment_date);
        const paymentTime = paymentDate.getTime();
        return paymentTime >= sixMonthsAgoTime && paymentTime <= todayTime;
      });
    },
    groupPaymentsByMonth() {
      const groupedPayments = {};
      this.payments.forEach((payment) => {
        const paymentDate = new Date(payment.payment_date);
        const monthKey = `${paymentDate.getFullYear()}-${
          paymentDate.getMonth() + 1
        }`;
        const amount = parseFloat(payment.amount);
        if (!groupedPayments[monthKey]) {
          groupedPayments[monthKey] = amount;
        } else {
          groupedPayments[monthKey] += amount;
        }
      });
      return groupedPayments;
    },
    prepareChartData() {
      const groupedPayments = this.groupPaymentsByMonth();
      const labels = [];
      const data = [];
      Object.keys(groupedPayments)
        .sort()
        .forEach((monthKey) => {
          labels.push(monthKey);
          data.push(groupedPayments[monthKey]);
        });
      return {
        labels,
        data,
      };
    },
  },
  mounted() {
    this.getPayments();
  },
  watch: {
    payments() {
      this.renderChart();
    },
  },
};
</script>
  
  <style scoped>
.canvas-wrapper {
max-height: 50%;
 display: flex;
 flex-direction: column;
 text-align: left;
}
</style>