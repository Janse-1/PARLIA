<script setup>
const videoCatalog = [
  {
    id: 1,
    title: '¿Qué es un Transformer y cómo funcionan los LLMs? (3Blue1Brown)',
    category: 'Módulo 1: Fundamentos',
    duration: '27 min',
    summary: 'Explicación visual y matemática sobre vectores de palabras, capas de atención y predicción de tokens.',
    url: 'https://www.youtube.com/watch?v=aircAruvnKk',
  },
  {
    id: 2,
    title: 'Introducción a Large Language Models (Andrej Karpathy)',
    category: 'Módulo 1 y 3: Arquitectura y Seguridad',
    duration: '60 min',
    summary: 'Cómo se pre-entrenan los modelos base, el ajuste por instrucciones (RLHF) y los retos de seguridad.',
    url: 'https://www.youtube.com/watch?v=zjkBMFhNj_g',
  },
  {
    id: 3,
    title: 'Prompt Engineering para Desarrolladores e Ingenieros',
    category: 'Módulo 2: Ingeniería de Prompts',
    duration: '18 min',
    summary: 'Principios prácticos de claridad, delimitadores estructurados y descomposición de problemas técnicos.',
    url: 'https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/',
  },
]
</script>

<template>
  <section class="videos-view">
    <header class="view-header">
      <span class="badge badge-secondary">Videoteca Curada</span>
      <h1>Recursos Audiovisuales de Profundización</h1>
      <p class="subtitle">
        Selección de conferencias y explicaciones visuales externas de alta calidad para reforzar conceptos sin sobrecarga de texto.
      </p>
    </header>

    <div class="videos-grid">
      <article v-for="video in videoCatalog" :key="video.id" class="card video-card">
        <div>
          <div class="video-meta">
            <span class="badge badge-primary">{{ video.category }}</span>
            <span class="duration">{{ video.duration }}</span>
          </div>
          <h2>{{ video.title }}</h2>
          <p>{{ video.summary }}</p>
        </div>

        <a
          :href="video.url"
          target="_blank"
          rel="noopener noreferrer"
          class="btn btn-outline"
        >
          Ver Recurso Externo
        </a>
      </article>
    </div>
  </section>
</template>

<style scoped>
.view-header {
  margin-bottom: var(--space-6);
}

.view-header h1 {
  margin-top: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
  margin-top: var(--space-2);
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: var(--space-5);
}

.video-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-4);
}

.video-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.duration {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.video-card h2 {
  margin-bottom: var(--space-2);
}

.video-card p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 0;
}
</style>

