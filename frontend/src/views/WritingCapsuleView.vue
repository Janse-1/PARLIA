<template>
  <section class="capsule-view">
    <div class="callout callout-gold">
      <strong>Cápsula Informativa de Consulta Libre:</strong>
      Esta guía de redacción técnica está disponible en todo momento y <strong>no afecta tu porcentaje de progreso formal</strong> en PARLIA.
    </div>

    <header class="view-header">
      <span class="badge badge-secondary">Comunicación en Ingeniería</span>
      <h1>Redacción Técnica Asistida sin Perder tu Voz Analítica</h1>
      <p class="subtitle">
        Aprende a utilizar modelos de lenguaje como editores de estilo y estructuradores de ideas, preservando siempre tu autoría intelectual y rigor científico.
      </p>
    </header>

    <div class="writing-grid">
      <article class="card">
        <span class="badge badge-primary">Paso 1: Borrador Humano Primero</span>
        <h2>Escribe tus hallazgos y datos reales antes de abrir el chat</h2>
        <p>
          El error más frecuente es pedirle a la IA que redacte una sección desde cero. Eso produce texto genérico, repetitivo y desconectado de la realidad de tu laboratorio o proyecto en La Guajira.
        </p>
        <div class="callout">
          <strong>Regla práctica:</strong> Redacta tú mismo las ideas centrales, mediciones, limitaciones y conclusiones preliminares en viñetas antes de solicitar apoyo de edición.
        </div>
      </article>

      <article class="card">
        <span class="badge badge-secondary">Paso 2: Paráfrasis Consciente y Claridad</span>
        <h2>Usa la IA para diagnosticar ambigüedades, no para pensar por ti</h2>
        <p>
          En lugar de pedir <em>"Reescribe este texto"</em>, utiliza instrucciones de revisión editorial controlada:
        </p>
        <pre>Actúa como editor de artículos de ingeniería. Revisa el siguiente párrafo que redacté: señala si existen ambigüedades técnicas, oraciones excesivamente largas o saltos lógicos, y sugiere 2 alternativas manteniendo mi vocabulario técnico y mis datos intactos.</pre>
      </article>

      <article class="card">
        <span class="badge badge-accent">Paso 3: Verificación de Citas y Normas</span>
        <h2>Cero delegación de referencias bibliográficas</h2>
        <p>
          Los modelos de lenguaje inventan DOIs, autores y años de publicación al combinar fragmentos estadísticos. Toda cita IEEE o APA debe provenir de artículos que tú hayas consultado y verificado en bases de datos académicas reales (Scopus, IEEE Xplore, Google Scholar).
        </p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.view-header {
  margin: var(--space-5) 0 var(--space-6);
}

.subtitle {
  color: var(--text-secondary);
  margin-top: var(--space-2);
}

.writing-grid {
  display: grid;
  gap: var(--space-5);
}

.writing-grid h2 {
  margin: var(--space-3) 0;
}
</style>

