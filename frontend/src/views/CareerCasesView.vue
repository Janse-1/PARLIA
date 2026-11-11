<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const copiedId = ref(null)

const careerCatalog = {
  Sistemas: {
    title: 'Ingeniería de Sistemas',
    focus: 'Arquitectura de software, diseño de bases de datos relacionales, seguridad y auditoría de algoritmos.',
    cases: [
      {
        id: 'sis-1',
        title: 'Auditoría de Índices y Consultas SQL',
        scenario: 'Optimización de consultas lentas en MySQL 8.0 evitando escaneos completos de tabla (Full Table Scan).',
        prompt: 'Actúa como Arquitecto de Bases de Datos en MySQL 8.0. Analiza la siguiente consulta SELECT y la estructura DDL de las tablas involucradas. Identifica posibles problemas de rendimiento N+1 o falta de índices compuestos, y explica qué mostraría el comando EXPLAIN antes y después de tu propuesta.',
        verification: 'Ejecuta EXPLAIN ANALYZE en tu entorno local con datos de prueba antes de aplicar cualquier índice en producción.',
      },
      {
        id: 'sis-2',
        title: 'Revisión de Seguridad OWASP en Endpoints REST',
        scenario: 'Prevención de vulnerabilidades IDOR e inyección en controladores de API.',
        prompt: 'Revisa este endpoint de Django REST Framework buscando vulnerabilidades de control de acceso (IDOR) o exposición excesiva de campos en el Serializer. Señala las líneas de riesgo y propón la corrección restringiendo la consulta a request.user.',
        verification: 'Escribe un test automatizado intentando acceder a un registro ajeno cambiando el ID del parámetro.',
      },
    ],
  },
  Industrial: {
    title: 'Ingeniería Industrial',
    focus: 'Optimización de procesos, investigación de operaciones, logística y control estadístico de calidad.',
    cases: [
      {
        id: 'ind-1',
        title: 'Formulación de Modelos de Programación Lineal',
        scenario: 'Definición de variables de decisión, función objetivo y restricciones operativas.',
        prompt: 'Actúa como especialista en Investigación de Operaciones. A partir del siguiente problema de asignación de planta con 3 líneas de ensamble y restricciones de horas-hombre, plantea formalmente: 1) Variables de decisión con sus unidades, 2) Función objetivo de minimización de costos y 3) Restricciones matemáticas explícitas.',
        verification: 'Comprueba dimensionalmente cada restricción y verifica los casos borde en un solver (PuLP / Excel Solver).',
      },
      {
        id: 'ind-2',
        title: 'Estandarización de Procedimientos Operativos (SOP)',
        scenario: 'Estructuración clara de manuales técnicos de seguridad y calidad en planta.',
        prompt: 'Estructura una plantilla de Procedimiento Operativo Estándar (SOP) bajo enfoque ISO 9001 para la inspección de recepción de materias primas, incluyendo indicadores de aceptación, responsables y registro de no conformidades.',
        verification: 'Valida que los umbrales de muestreo correspondan a las tablas técnicas reales de la planta.',
      },
    ],
  },
  Mecanica: {
    title: 'Ingeniería Mecánica',
    focus: 'Diseño mecánico, termodinámica, planes de mantenimiento preventivo y modelado físico-matemático.',
    cases: [
      {
        id: 'mec-1',
        title: 'Análisis de Modos y Efectos de Falla (AMEF)',
        scenario: 'Estructuración de planes de mantenimiento centrados en confiabilidad para sistemas de bombeo.',
        prompt: 'Actúa como Ingeniero de Confiabilidad Mecánica. Construye una matriz preliminar AMEF para una bomba centrífuga industrial que presenta cavitación recurrente. Detalla modo de falla, causa raíz física, efecto en el sistema y acciones de control recomendadas.',
        verification: 'Contrasta las curvas NPSH requerido vs. NPSH disponible en el catálogo técnico del fabricante.',
      },
    ],
  },
  Civil: {
    title: 'Ingeniería Civil',
    focus: 'Especificaciones estructurales, geotecnia, presupuestos de obra y redacción de memorias de cálculo.',
    cases: [
      {
        id: 'civ-1',
        title: 'Estructuración de Memorias de Cálculo y Normativa',
        scenario: 'Organización metodológica de informes técnicos estructurales.',
        prompt: 'Propón el índice técnico detallado para una memoria de cálculo de diseño de cimentaciones superficiales, indicando qué parámetros geotécnicos de entrada, hipótesis de carga y verificaciones de capacidad portante y asentamientos deben documentarse paso a paso.',
        verification: 'Nunca aceptes coeficientes sísmicos o numerales de la norma NSR-10 generados por IA sin contrastarlos directamente con el documento oficial vigente.',
      },
    ],
  },
  Ambiental: {
    title: 'Ingeniería Ambiental',
    focus: 'Evaluación de impacto ambiental, gestión integral de recursos hídricos y monitoreo de emisiones.',
    cases: [
      {
        id: 'amb-1',
        title: 'Matrices de Evaluación de Impacto Ambiental',
        scenario: 'Identificación de factores ambientales y medidas de manejo en proyectos de infraestructura.',
        prompt: 'Actúa como especialista en Evaluación de Impacto Ambiental. Para un proyecto de planta de tratamiento de aguas residuales, estructura los componentes abióticos, bióticos y socioeconómicos a evaluar, y sugiere indicadores medibles de seguimiento.',
        verification: 'Verifica que los límites máximos permisibles citados correspondan a la resolución ambiental colombiana vigente.',
      },
    ],
  },
  Energias: {
    title: 'Ingeniería en Energías',
    focus: 'Sistemas fotovoltaicos, eólicos, eficiencia energética y transición energética en La Guajira.',
    cases: [
      {
        id: 'ene-1',
        title: 'Dimensionamiento Preliminar Fotovoltaico',
        scenario: 'Verificación de variables de irradiancia solar, pérdidas térmicas y autonomía.',
        prompt: 'Enumera y explica las ecuaciones paso a paso para el dimensionamiento preliminar de un sistema solar fotovoltaico conectado a red (On-Grid), detallando cómo influye el coeficiente térmico de potencia de los módulos en climas cálidos como La Guajira.',
        verification: 'Recalcula manualmente las expresiones matemáticas y utiliza datos reales de irradiación del atlas solar IDEAM.',
      },
    ],
  },
}

const currentProgram = computed(() => {
  const key = route.params.program || 'Sistemas'
  return careerCatalog[key] || careerCatalog.Sistemas
})

async function copyPrompt(id, text) {
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
  <section class="career-view">
    <div class="callout callout-gold">
      <strong>Cápsula de Contexto por Carrera (Consulta Libre):</strong>
      Explora estos casos y estructuras de prompts adaptados a tu programa. Consultar esta sección no altera tu porcentaje de progreso formal.
    </div>

    <header class="view-header">
      <span class="badge badge-primary">Facultad de Ingeniería - Uniguajira</span>
      <h1>{{ currentProgram.title }}</h1>
      <p class="subtitle">{{ currentProgram.focus }}</p>
    </header>

    <div class="cases-grid">
      <article v-for="item in currentProgram.cases" :key="item.id" class="card case-card">
        <h2>{{ item.title }}</h2>
        <p class="case-scenario">{{ item.scenario }}</p>

        <div class="prompt-box">
          <div class="prompt-box-header">
            <span>Estructura de Prompt Recomendada</span>
            <button
              type="button"
              class="btn btn-outline btn-sm"
              @click="copyPrompt(item.id, item.prompt)"
            >
              {{ copiedId === item.id ? 'Copiado' : 'Copiar Prompt' }}
            </button>
          </div>
          <pre>{{ item.prompt }}</pre>
        </div>

        <div class="callout">
          <strong>Criterio de Verificación en Ingeniería:</strong>
          {{ item.verification }}
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.view-header {
  margin: var(--space-5) 0 var(--space-6);
}

.view-header h1 {
  margin-top: var(--space-2);
}

.subtitle {
  color: var(--text-secondary);
  margin-top: var(--space-2);
  margin-bottom: 0;
}

.cases-grid {
  display: grid;
  gap: var(--space-6);
}

.case-scenario {
  color: var(--text-secondary);
  margin-top: var(--space-2);
}

.prompt-box {
  margin: var(--space-4) 0;
}

.prompt-box-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}
</style>

