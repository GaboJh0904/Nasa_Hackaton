<template>
    <div class="bibliography-page">
      <!-- Hero Section -->
      <section class="hero" data-aos="fade-in">
        <div class="hero-content">
          <h1 data-aos="zoom-in">Historia de los Orreries</h1>
          <p data-aos="fade-up">
            Explorando la evolución desde los modelos mecánicos hasta las simulaciones virtuales del sistema solar.
          </p>
        </div>
      </section>
  
      <!-- Main Content Section -->
      <section class="content" id="content">
        <div class="content-block" data-aos="fade-up">
          <h2>Origen del Orrery</h2>
          <div class="block-content">
            <div class="text">
              <p>
                Un orrery es un modelo mecánico del sistema solar que muestra el movimiento de los planetas alrededor del Sol. Este tipo de modelo fue presentado por primera vez a Charles Boyle, 4.º conde de Orrery, en 1713, de donde proviene su nombre. Desde entonces, se ha utilizado para enseñar astronomía durante siglos.
              </p>
            </div>
            <div class="image" data-aos="zoom-in">
              <img src="/src/assets/imagenes/john.jpg" alt="Orrery Mecánico" />
            </div>
          </div>
        </div>
  
        <div class="content-block reverse" data-aos="fade-up">
          <h2>La Evolución Hacia lo Virtual</h2>
          <div class="block-content">
            <div class="text">
              <p>
                Con el avance de la tecnología, los orreries se han transformado en simulaciones digitales. Herramientas como Three.js y APIs como la NEOWS de la NASA permiten representar el sistema solar en tiempo real, añadiendo un nivel de precisión sin precedentes.
              </p>
            </div>
            <div class="image" data-aos="zoom-in">
              <img src="/src/assets/imagenes/evol.jpg" alt="Orrery Virtual" />
            </div>
          </div>
        </div>
  
        <!-- APIs para la Ciencia en Tiempo Real -->
        <div class="content-block" data-aos="fade-up">
          <h2>APIs para la Ciencia en Tiempo Real</h2> <!-- Título sobre el texto -->
          <div class="block-content">
            <div class="text">
              <p>
                Los orreries virtuales se han enriquecido con datos en tiempo real gracias a APIs como el NEO (Near-Earth Object) de la NASA. Estas herramientas permiten visualizar asteroides y otros cuerpos celestes que podrían representar una amenaza para la Tierra, integrando datos científicos de forma visual.
              </p>
            </div>
            <div class="image" data-aos="zoom-in">
              <img src="/src/assets/imagenes/apis.jpg" alt="API de la NASA" />
            </div>
          </div>
        </div>
  
      </section>
    </div>
  </template>
  
  <script>
    import AOS from 'aos';
    import 'aos/dist/aos.css';
  
    export default {
      name: "Bibliography",
      mounted() {
        AOS.init({
          duration: 1500, // Duración más suave de las animaciones
          once: true,     // Ejecuta las animaciones una sola vez
          easing: 'ease-in-out', // Añade suavidad en la animación
        });
      }
    };
  </script>
  
  <style scoped>
    /* Hero Section */
    .hero {
      position: relative;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: url('/src/assets/imagenes/Fondo-mundo-e1486373480361.jpg') no-repeat center center/cover;
      text-align: center;
      color: #333; /* Texto oscuro sobre fondo claro */
    }
  
    .hero-content {
      position: relative;
      width: 100%;
      max-width: 1000px;
      padding: 0 20px;
    }
  
    .hero-content h1 {
      font-size: 4rem;
      margin-bottom: 15px;
      font-weight: 600; /* Peso de fuente más ligero para una apariencia moderna */
      text-transform: uppercase;
      letter-spacing: 2px;
      color: #eceff3; /* Color oscuro pero no negro, para suavizar el diseño */
    }
  
    .hero-content p {
      font-size: 1.5rem;
      margin-bottom: 20px;
      color: #dee6f3; /* Texto ligeramente más claro */
    }
  
    /* Content Section */
    .content {
      max-width: 1200px;
      margin: 60px auto;
      padding: 0 30px;
    }
  
    .content-block {
      margin-bottom: 60px;
      padding: 30px 0;
    }
  
    .block-content {
      display: flex;
      flex-wrap: wrap;
      align-items: flex-start; /* Alinea los elementos desde el inicio */
      gap: 40px;
    }
  
    .block-content.reverse {
      flex-direction: row-reverse;
    }
  
    .text {
      flex: 1;
      font-size: 1.4rem;
      line-height: 1.8;
      color: #768193; /* Color de texto gris oscuro */
    }
  
    .image {
      flex: 1;
      transition: transform 0.4s ease-in-out;
    }
  
    .image img {
      width: 100%;
      border-radius: 10px;
      object-fit: cover;
    }
  
    .image:hover {
      transform: scale(1.05);
    }
  
    /* Media Queries */
    @media (max-width: 768px) {
      .block-content {
        flex-direction: column;
      }
  
      .block-content.reverse {
        flex-direction: column;
      }
  
      .hero-content h1 {
        font-size: 3rem;
      }
  
      .hero-content p {
        font-size: 1.2rem;
      }
    }
  </style>
  