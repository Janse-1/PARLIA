<script setup>
import { ref } from 'vue'

const activeTab = ref('estructura')
</script>

<template>
  <section class="capsule-view">
    <div class="callout callout-gold">
      <strong>Cápsula Informativa de Consulta Libre:</strong>
      Esta vista es un recurso de referencia rápida y <strong>no computa dentro del porcentaje de progreso formal</strong> del laboratorio.
    </div>

    <header class="view-header">
      <span class="badge badge-secondary">Cápsula Visual</span>
      <h1>Modelos de Difusión y Generación de Imágenes</h1>
      <p class="subtitle">
        Comprende cómo operan las arquitecturas generativas visuales y cómo estructurar instrucciones técnicas precisas para diagramas, prototipos y visualización conceptual.
      </p>
    </header>

    <div class="tabs-bar">
      <button
        type="button"
        class="btn"
        :class="activeTab === 'estructura' ? 'btn-primary' : 'btn-outline'"
        @click="activeTab = 'estructura'"
      >
        1. Anatomía de un Prompt Visual
      </button>
      <button
        type="button"
        class="btn"
        :class="activeTab === 'difusion' ? 'btn-primary' : 'btn-outline'"
        @click="activeTab = 'difusion'"
      >
        2. ¿Cómo funciona la Difusión?
      </button>
      <button
        type="button"
        class="btn"
        :class="activeTab === 'etica' ? 'btn-primary' : 'btn-outline'"
        @click="activeTab = 'etica'"
      >
        3. Límites Técnicos y Propiedad Intelectual
      </button>
    </div>

    <div v-if="activeTab === 'estructura'" class="card">
      <h2>Estructura Sistemática para Prompts de Imagen</h2>
      <p>
        A diferencia de una conversación libre, los generadores visuales (DALL-E, Midjourney, Stable Diffusion) responden mejor a descriptores estructurados por capas:
      </p>

      <div class="formula-grid">
        <div class="formula-step">
          <span class="badge badge-primary">Capa 1: Sujeto Principal</span>
          <p>Define con precisión el objeto, sistema o escena central sin ambigüedades.</p>
        </div>
        <div class="formula-step">
          <span class="badge badge-secondary">Capa 2: Estilo y Medio Técnico</span>
          <p>Isométrico 3D, corte transversal CAD, infografía vectorial limpia o fotografía industrial.</p>
        </div>
        <div class="formula-step">
          <span class="badge badge-accent">Capa 3: Iluminación y Composición</span>
          <p>Vista ortogonal, fondo neutro de alto contraste, iluminación de estudio.</p>
        </div>
      </div>

      <pre>[Sujeto: Turbina eólica de eje horizontal en corte técnico] + [Estilo: Diagrama isométrico limpio estilo manual de ingeniería] + [Composición: Fondo blanco puro, etiquetas minimalistas, alta nitidez]</pre>
    </div>

    <div v-else-if="activeTab === 'difusion'" class="card">
      <h2>Del Ruido Gaussiano a la Imagen Coherente</h2>
      <p>
        Los modelos de difusión aprenden el proceso inverso a la destrucción de información: parten de una matriz de ruido aleatorio y, guiados por los vectores semánticos de tu texto (CLIP/Embeddings), eliminan el ruido paso a paso hasta formar la imagen.
      </p>
      <div class="callout">
        <strong>Advertencia para Ingeniería:</strong>
        Un modelo de difusión optimiza la coherencia visual, <strong>no las leyes de la física ni las cotas dimensionales</strong>. Nunca utilices una imagen generada por IA como plano constructivo ni esquema eléctrico real.
      </div>
    </div>

    <div v-else class="card">
      <h2>Consideraciones Éticas y Académicas</h2>
      <p>
        Al incluir ilustraciones conceptuales generadas por IA en presentaciones o pósteres académicos, declara siempre la herramienta utilizada en el pie de figura y evita imitar logotipos protegidos o rostros de personas reales.
      </p>
    </div>
  </section>
</template>

<style scoped>
.view-header {
  margin: var(--space-5) 0;
}

.subtitle {
  color: var(--text-secondary);
  margin-top: var(--space-2);
}

.tabs-bar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.formula-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-4);
  margin: var(--space-4) 0;
}

.formula-step {
  padding: var(--space-4);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background-color: var(--bg-app);
}

.formula-step p {
  margin-top: var(--space-2);
  margin-bottom: 0;
  font-size: 0.9rem;
}
</style>

