<template>
  <div v-if="isVisible" class="modal">
    <div class="modal-content">
      <!-- Botón de cerrar -->
      <button class="close-button" @click="closeModal">✖ Cerrar</button>

      <h2>Dashboard Completo de la Tierra</h2>

      <div class="dashboard-grid">
        <!-- Gráfico de barras: Dimensiones Planetarias -->
        <div class="chart-container">
          <h3>Dimensiones Planetarias</h3>
          <apexchart type="bar" :options="barChartOptions" :series="barChartSeries"></apexchart>
        </div>

        <!-- Gráfico circular: Composición de la atmósfera -->
        <div class="chart-container">
          <h3>Composición de la Atmósfera</h3>
          <apexchart type="pie" :options="pieChartOptions" :series="pieChartSeries"></apexchart>
        </div>

        <!-- Gráfico de área: Cambios en la temperatura promedio -->
        <div class="chart-container">
          <h3>Cambios en la Temperatura Promedio (°C)</h3>
          <apexchart type="area" :options="areaChartOptions" :series="areaChartSeries"></apexchart>
        </div>

        <!-- Gráfico de líneas: Tiempo de Rotación y Traslación -->
        <div class="chart-container">
          <h3>Tiempo de Rotación y Traslación</h3>
          <apexchart type="line" :options="lineChartOptions" :series="lineChartSeries"></apexchart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts,
  },
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      // Opciones para el gráfico de barras (Dimensiones Planetarias)
      barChartOptions: {
        chart: {
          id: "dimensions-chart",
        },
        xaxis: {
          categories: ["Tierra", "Marte", "Venus", "Júpiter", "Saturno"],
        },
        title: {
          text: "Dimensiones Planetarias (km y kg)",
          align: "center",
        },
        yaxis: {
          title: {
            text: "Valores",
          },
        },
      },
      barChartSeries: [
        {
          name: "Radio (km)",
          data: [6371, 3389.5, 6051.8, 69911, 58232], // Radios de los planetas
        },
        {
          name: "Masa (kg)",
          data: [5.972e24, 0.64171e24, 4.8675e24, 1898.19e24, 568.34e24], // Masas de los planetas
        },
        {
          name: "Distancia al Sol (km)",
          data: [149600000, 227939100, 108208000, 778579000, 1433500000], // Distancias al Sol
        },
      ],

      // Opciones para el gráfico circular (pie)
      pieChartOptions: {
        chart: {
          id: "atmosphere-composition",
        },
        labels: ["Nitrógeno", "Oxígeno", "Argón", "Dióxido de Carbono"],
        title: {
          text: "Composición de la Atmósfera",
          align: "center",
        },
      },
      pieChartSeries: [78, 21, 0.93, 0.04], // Datos: Porcentajes de gases

      // Opciones para el gráfico de área (temperatura)
      areaChartOptions: {
        chart: {
          id: "temperature-change",
        },
        xaxis: {
          categories: ["1900", "1950", "2000", "2020", "2023"], // Añadido 2023
        },
        title: {
          text: "Cambios en la Temperatura Promedio (°C)",
          align: "center",
        },
      },
      areaChartSeries: [
        {
          name: "Temperatura Promedio",
          data: [13.7, 14.0, 14.5, 15.0, 15.2], // Datos de temperatura promedio
        },
      ],

      // Opciones para el gráfico de líneas (rotación y traslación)
      lineChartOptions: {
        chart: {
          id: "rotation-translation-time",
        },
        xaxis: {
          categories: ["Tierra", "Marte", "Venus", "Júpiter", "Saturno"],
        },
        title: {
          text: "Tiempos de Rotación y Traslación",
          align: "center",
        },
      },
      lineChartSeries: [
        {
          name: "Tiempo de Rotación (horas)",
          data: [24, 24.6, 243, 9.9, 10.7], // Duraciones de rotación
        },
        {
          name: "Tiempo de Traslación (días)",
          data: [365.25, 687, 225, 4333, 10759], // Duraciones de traslación
        },
      ],
    };
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
/* Modal básico */
.modal {
  display: flex;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
}

/* Contenido del modal con scroll si el contenido es muy grande */
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 85vw; /* Hacer el modal más ancho para que sea más horizontal */
  width: 85vw; /* Hacer el modal más ancho para que sea más horizontal */
  max-height: 90vh;
  height: 90vh;
  overflow-y: auto;
  text-align: center;
  position: relative;
}

/* Botón de cerrar */
.close-button {
  position: absolute;
  top: 10px;
  right: 20px;
  font-size: 18px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: black; /* Texto negro para el botón de cerrar */
}

/* Grid layout para las gráficas */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* Dos columnas */
  grid-template-rows: auto auto; /* Varias filas */
  gap: 20px; /* Espacio entre las gráficas */
}

/* Estilos para contenedores de gráficos individuales */
.chart-container {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-width: 400px;
  min-height: 300px;
}

h2, h3 {
  margin-bottom: 20px;
}

apexchart {
  width: 100%;
  height: 100%;
}
</style>
