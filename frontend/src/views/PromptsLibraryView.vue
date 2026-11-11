<script setup>
import { ref, computed } from 'vue'

const selectedCategory = ref('all')
const copiedId = ref(null)

const categories = [
  { id: 'all', label: 'Todos los Patrones' },
  { id: 'role', label: 'Asignación de Rol y Contexto' },
  { id: 'cot', label: 'Desglose Paso a Paso (Chain-of-Thought)' },
  { id: 'audit', label: 'Auditoría y Detección de Fallos' },
]

const promptPatterns = [
  {
    id: 'pat-1',
    category: 'role',
    title: 'Patrón: Especificación Técnica con Restricciones',
    summary: 'Delimita el rol profesional, las condiciones de borde y el formato verificable de salida.',
    template: `Actúa como [Rol de Ingeniería específico].
Contexto del sistema: [Describe entorno, versión de herramientas, variables conocidas].
Restricciones: [Qué no debe usar o qué límites físicos/técnicos existen].
Tarea: [Acción concreta solicitada].
Formato de salida: Entrega primero los supuestos asumidos, luego el desarrollo técnico y finalmente una lista de verificación para validar la respuesta.`,
  },
  {
    id: 'pat-2',
    category: 'cot',
    title: 'Patrón: Razonamiento Paso a Paso y Verificación Dimensional',
    summary: 'Obliga al modelo a desglosar cada etapa lógica y explicitar las unidades físicas antes de calcular.',
    template: `Analiza el siguiente problema de ingeniería paso a paso sin saltar etapas intermedias:
1. Lista todas las variables de entrada con sus unidades en el Sistema Internacional.
2. Enuncia los principios físicos o algorítmicos aplicables y sus ecuaciones base.
3. Realiza el análisis dimensional antes de reemplazar valores numéricos.
4. Señala qué resultado intermedio debo verificar manualmente.`,
  },
  {
    id: 'pat-3',
    category: 'audit',
    title: 'Patrón: Abogado del Diablo / Auditoría de Código y Lógica',
    summary: 'Utiliza la IA para encontrar casos borde, vulnerabilidades o supuestos débiles en tu propia solución.',
    template: `He diseñado la siguiente solución / algoritmo para [describe el problema]:
[Pega aquí tu código o planteamiento]

No reescribas la solución todavía. Actúa como un revisor técnico crítico y enumera:
1. Tres casos borde (edge cases) donde esta lógica podría fallar.
2. Posibles riesgos de seguridad o cuellos de botella de rendimiento.
3. Qué pruebas unitarias concretas debería escribir para comprobar su robustez.`,
  },
]

const filteredPrompts = computed(() => {
  if (selectedCategory.value === 'all') return promptPatterns
  return promptPatterns.filter((p) => p.category === selectedCategory.value)
})

async function handleCopy(id, text) {
  try {
    await navigator.clipboard.writeText(text)
    copiedId.value = id
    setTimeout(() => {
      if (copiedId.value === id) copiedId.value = null
    }, 2000)
  } catch {
    copiedId.value = null
  }
}
</script>

<template>
  <section class="prompts-view">
    <div class="callout callout-gold">
      <strong>Biblioteca de Patrones de Prompts (Consulta Libre):</strong>
      Copia y adapta estas plantillas estructuradas en tus actividades diarias. Su uso es libre y no modifica tu porcentaje de avance.
    </div>

    <header class="view-header">
      <span class="badge badge-primary">Repositorio Interactivo</span>
      <h1>Biblioteca de Patrones de Ingeniería de Prompts</h1>
      <p class="subtitle">
        Plantillas probadas bajo técnicas de Rol, Pocos Ejemplos (Few-Shot) y Razonamiento Paso a Paso (Chain-of-Thought).
      </p>
    </header>

    <div class="filter-bar">
      <button
        v-for="cat in categories"
        :key="cat.id"
        type="button"
        class="btn"
        :class="selectedCategory === cat.id ? 'btn-secondary' : 'btn-outline'"
        @click="selectedCategory = cat.id"
      >
        {{ cat.label }}
      </button>
    </div>

    <div class="patterns-list">
      <article v-for="pat in filteredPrompts" :key="pat.id" class="card pattern-card">
        <div class="pattern-header">
          <div>
            <h2>{{ pat.title }}</h2>
            <p class="pattern-summary">{{ pat.summary }}</p>
          </div>
          <button
            type="button"
            class="btn btn-primary"
            @click="handleCopy(pat.id, pat.template)"
          >
            {{ copiedId === pat.id ? 'Copiado al portapapeles' : 'Copiar plantilla' }}
          </button>
        </div>
        <pre>{{ pat.template }}</pre>
      </article>
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

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
}

.patterns-list {
  display: grid;
  gap: var(--space-5);
}

.pattern-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.pattern-summary {
  color: var(--text-secondary);
  margin-top: var(--space-1);
  margin-bottom: 0;
}
</style>

