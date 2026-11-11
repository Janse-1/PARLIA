<script setup>
const newsFeed = [
  {
    id: 1,
    date: 'Octubre 2026',
    tag: 'Verificación de Código',
    title: 'Modelos de Razonamiento y Verificación Formal en Ingeniería de Software',
    summary: 'Nuevos estudios destacan que combinar pruebas unitarias automatizadas con prompts de especificación reduce drásticamente defectos lógicos en código asistido por IA.',
    source: 'IEEE Software / ArXiv',
    url: 'https://arxiv.org/list/cs.SE/recent',
  },
  {
    id: 2,
    date: 'Octubre 2026',
    tag: 'Ética y Educación Superior',
    title: 'Lineamientos UNESCO para el Uso Ético de IA Generativa en Universidades',
    summary: 'La guía enfatiza el enfoque formativo centrado en la autonomía cognitiva del estudiante, la transparencia metodológica y la protección de datos locales.',
    source: 'UNESCO Digital Library',
    url: 'https://www.unesco.org/es/digital-education/artificial-intelligence',
  },
  {
    id: 3,
    date: 'Septiembre 2026',
    tag: 'Seguridad Informática',
    title: 'Prevención de Slopsquatting: Por qué auditar cada librería sugerida por un LLM',
    summary: 'Investigadores de seguridad alertan sobre paquetes inexistentes alucinados por modelos de lenguaje y recomiendan verificar siempre los repositorios oficiales.',
    source: 'OWASP Top 10 for LLM Applications',
    url: 'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
  },
]
</script>

<template>
  <section class="news-view">
    <header class="view-header">
      <span class="badge badge-accent">Actualidad Científica y Técnica</span>
      <h1>Noticias y Avances en Inteligencia Artificial</h1>
      <p class="subtitle">
        Síntesis curada de publicaciones, estándares de seguridad y lanzamientos relevantes para estudiantes de ingeniería.
      </p>
    </header>

    <div class="news-list">
      <article v-for="item in newsFeed" :key="item.id" class="card news-card">
        <div class="news-top">
          <span class="badge badge-secondary">{{ item.tag }}</span>
          <span class="news-date">{{ item.date }} · {{ item.source }}</span>
        </div>
        <h2>{{ item.title }}</h2>
        <p>{{ item.summary }}</p>
        <a
          :href="item.url"
          target="_blank"
          rel="noopener noreferrer"
          class="news-link"
        >
          Consultar fuente original
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

.news-list {
  display: grid;
  gap: var(--space-5);
}

.news-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.news-date {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.news-card h2 {
  margin-bottom: var(--space-2);
}

.news-card p {
  color: var(--text-secondary);
}

.news-link {
  font-size: 0.88rem;
  font-weight: 600;
}
</style>

