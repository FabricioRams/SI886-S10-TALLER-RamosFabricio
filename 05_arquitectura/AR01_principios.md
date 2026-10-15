# Principios de Arquitectura Empresarial (AR01)
## Código: AR01 · Principios de Arquitectura del PETI
### Organización: CrediTech Perú S.A.C. | RUC: 20608945123
**Plan Estratégico de Tecnologías de la Información (PETI) 2026-2028**  
**Autor:** Fabricio Farid Edmilson Ramos Atahuachi (2023076798) · Escuela de Ingeniería de Sistemas, UPT

---

### Introducción y Propósito

Los principios de arquitectura empresarial son declaraciones fundamentales de dirección y orientación que definen el marco de referencia y los límites para la toma de decisiones tecnológicas, de información, de aplicaciones y de procesos en CrediTech Perú S.A.C. De acuerdo con el estándar **TOGAF 10th Edition** y los lineamientos del marco **COBIT 2019 (objetivo APO03 Managed Enterprise Architecture)**, estos principios garantizan la coherencia del diseño frente a la visión estratégica institucional y evitan la proliferación desordenada de soluciones fragmentadas o islas de datos.

A continuación, se declaran los seis principios de arquitectura que gobernarán todas las iniciativas, adquisiciones, desarrollos y proyectos del PETI institucional:

---

### 1. Principio PR-01: Dato único con fuente autoritativa y dueño designado

| Campo | Contenido de Arquitectura |
|---|---|
| **Nombre** | **Dato único con fuente autoritativa y dueño designado** |
| **Declaración** | Cada entidad de negocio fundamental (cliente, crédito, pagaré, mora, colaborador) reside en una única fuente autoritativa oficial y cuenta con un único dueño de dato (*Data Owner*) designado formalmente por cargo gerencial. |
| **Razón** | Las decisiones comerciales y de evaluación de riesgo crediticio se toman hoy sobre cifras discrepantes entre el Core de Créditos, el Portal Web, el ERP contable y múltiples hojas de cálculo operativas (detectándose más de 68,000 registros divergentes de clientes y saldos desfasados). Esta dispersión imposibilita el cálculo certero de mora y genera fricciones en auditoría. |
| **Implicancias** | 1. Queda terminantemente prohibida la creación de bases de datos locales, réplicas no controladas o silos departamentales de entidades ya existentes.<br/>2. Todo aplicativo o servicio que consuma una entidad debe hacerlo conectándose a su fuente autoritativa mediante la capa de integración de servicios (APIs).<br/>3. Antes de financiar proyectos analíticos avanzados (Machine Learning v2), es condición obligatoria ejecutar el proyecto de Gobierno del Dato y Maestro de Clientes (MDM). |
| **Trazabilidad** | Deriva del diagnóstico de la Sección 3.1.3 (ventaja competitiva no capturada por inconsistencia de datos maestros), del hallazgo del taller de normatividad (Sección 4.1) y de la dinámica de modelado de la Semana 10. |

---

### 2. Principio PR-02: Integración desacoplada mediante APIs y servicios seguros

| Campo | Contenido de Arquitectura |
|---|---|
| **Nombre** | **Integración desacoplada mediante APIs y servicios seguros** |
| **Declaración** | Toda comunicación e intercambio de información entre componentes de software, tanto internos como con proveedores externos (burós crediticios, pasarelas de pago, SUNAT, RENIEC), debe realizarse exclusivamente a través de interfaces de programación (APIs RESTful seguras, estandarizadas y documentadas bajo OpenAPI), erradicando las transferencias mediante archivos planos o accesos directos a bases de datos. |
| **Razón** | La sincronización actual entre el Core de Créditos y el sistema contable/financiero se ejecuta mediante scripts nocturnos por lotes (*batch*) y transferencias manuales de archivos CSV. Este mecanismo genera desfasajes temporales de hasta 24 horas, bloqueos por fallos de formato, reprocesos manuales recurrentes e incapacidad de consultar el saldo en tiempo real. |
| **Implicancias** | 1. Se debe desplegar una capa corporativa de gestión de APIs (*API Gateway*) con políticas homogéneas de autenticación (OAuth 2.0 / mTLS), cuotas de consumo (*rate limiting*) y telemetría.<br/>2. Ningún proyecto de software podrá consultar o modificar directamente las tablas de base de datos de otro componente.<br/>3. Los contratos de integración con proveedores de servicios externos deberán exigir interfaces síncronas o webhooks con cifrado TLS 1.3. |
| **Trazabilidad** | Deriva de la Resolución SBS N.° 504-2021 (Art. 20, seguridad en desarrollo e integraciones), de la capacidad requerida de interoperabilidad (Sección 3.1.5) y de la Estrategia E-01 del FODA cruzado (Sección 3.5). |

---

### 3. Principio PR-03: Automatización end-to-end y erradicación del Shadow IT

| Campo | Contenido de Arquitectura |
|---|---|
| **Nombre** | **Automatización end-to-end y erradicación del Shadow IT** |
| **Declaración** | Los procesos misionales de la cadena de valor crediticia deben operar sobre sistemas corporativos auditables y homologados, prohibiéndose terminantemente el uso de hojas de cálculo o herramientas ofimáticas personales para tareas operativas de ruteo, scoring manual o asignación de cobranzas. |
| **Razón** | Procesos de alto impacto financiero como la asignación de cartera en mora y la reevaluación de créditos observados operan hoy sobre libros compartidos de Microsoft Excel. Esta práctica expone a la organización a corrupción de datos, fórmulas alteradas sin control de versiones, fuga de información confidencial de deudores y carencia absoluta de pistas de auditoría. |
| **Implicancias** | 1. La funcionalidad de ruteo y gestión de cobranzas debe integrarse nativamente en una plataforma CRM/BPM corporativa auditada.<br/>2. Las reglas de negocio de evaluación crediticia deben residir en motores de reglas o servicios analíticos versionados en Git, no en celdas de cálculo.<br/>3. La Dirección de TI auditará trimestralmente las estaciones de trabajo para asegurar el desmantelamiento de repositorios informales de datos. |
| **Trazabilidad** | Deriva del diagnóstico de debilidad operacional (Sección 3.1.2), de la Resolución SBS N.° 11356-2008 (control del riesgo operacional en procesos críticos) y del mandato de retiro de Shadow IT de la Sección 3.5 (Estrategia E-02). |

---

### 4. Principio PR-04: Privacidad, seguridad y cumplimiento normativo por diseño y por defecto

| Campo | Contenido de Arquitectura |
|---|---|
| **Nombre** | **Privacidad, seguridad y cumplimiento normativo por diseño y por defecto (Security & Privacy by Design)** |
| **Declaración** | Toda solución tecnológica, arquitectura de software, infraestructura y base de datos debe incorporar controles de seguridad de la información, cifrado de datos en reposo y en tránsito, y respeto estricto a los derechos ARCO de los titulares desde su concepción inicial y no como una capa añadida a posteriori. |
| **Razón** | CrediTech procesa datos biométricos faciales, historial crediticio y transacciones económicas sensibles de más de 210,000 ciudadanos. La auditoría previa de la Sección 4.1 reveló una tasa de incumplimiento del 50% en exigencias de la SBS y ANPD, exponiendo a la empresa a sanciones de hasta 100 UIT y revocación de habilitación operativa. |
| **Implicancias** | 1. Es obligatorio el modelado de amenazas y la ejecución automatizada de análisis estático/dinámico de código (SAST/DAST) en el pipeline de despliegue antes de cualquier liberación a producción.<br/>2. Todos los repositorios de datos que contengan datos personales sensibles deben cifrarse con AES-256 en reposo y TLS 1.3 en tránsito.<br/>3. Todo flujo de usuario debe capturar consentimiento explícito e inequívoco y registrarlo en una pista de auditoría inmutable (SIEM/SOC). |
| **Trazabilidad** | Deriva de la Ley N.° 29733 y D.S. 016-2024-JUS (Protección de Datos Personales), de la Resolución SBS N.° 504-2021 (Reglamento de Seguridad y Ciberseguridad) y de los Proyectos No Negociables de la Sección 4.1.5. |

---

### 5. Principio PR-05: Resiliencia, alta disponibilidad e inmutabilidad de la infraestructura

| Campo | Contenido de Arquitectura |
|---|---|
| **Nombre** | **Resiliencia, alta disponibilidad e inmutabilidad de la infraestructura (Cloud Resilience)** |
| **Declaración** | La infraestructura tecnológica de soporte a los servicios misionales debe diseñarse para tolerar contingencias mayores sin interrupción del negocio (RTO ≤ 1 hora, RPO ≤ 15 minutos), con arquitecturas distribuidas multizona en la nube y mecanismos de respaldo inmutables protegidos contra ransomware. |
| **Razón** | La organización mantiene servidores físicos locales sin redundancia para contabilidad y un despliegue en la nube en una única zona de disponibilidad (Single-AZ) sin conmutación automática de contingencia probada. Un incidente de ransomware o caída de infraestructura provocaría la paralización de la colocación de créditos y la cobranza por tiempo indeterminado. |
| **Implicancias** | 1. Desmantelamiento de servidores físicos locales y migración de cargas transaccionales a arquitecturas contenerizadas en la nube con balanceo de carga multizona (Multi-AZ).<br/>2. Implementación de políticas de inmutabilidad documental (*WORM - Write Once, Read Many*) mediante AWS S3 Object Lock para pagarés electrónicos y facturas tributarias.<br/>3. Realización obligatoria de dos simulacros anuales de recuperación ante desastres (DRP) con verificación formal de tiempos de recuperación. |
| **Trazabilidad** | Deriva de la Resolución SBS N.° 504-2021 (Art. 27, Plan de Continuidad Tecnológica), del marco COBIT 2019 (objetivo DSS04 Managed Continuity) y de los compromisos de disponibilidad de la Sección 4.3. |

---

### 6. Principio PR-06: Autoservicio omnicanal con explicabilidad algorítmica

| Campo | Contenido de Arquitectura |
|---|---|
| **Nombre** | **Autoservicio omnicanal con explicabilidad algorítmica** |
| **Declaración** | Los canales digitales (portal web, aplicativo móvil, bots de mensajería) deben brindar una experiencia de autoservicio continuo 24/7 al solicitante de crédito, garantizando transparencia en las decisiones crediticias mediante modelos de scoring explicables y opción de atención asistida por un asesor humano. |
| **Razón** | El 68% de las solicitudes rechazadas por el motor analítico provocan abandono y reclamos formales debido a mensajes genéricos opacos («Su crédito no califica»), lo cual incumple el marco de conducta de mercado SBS y erosiona la lealtad de la cartera de clientes. |
| **Implicancias** | 1. La arquitectura de canales debe exponer interfaces de usuario claras que desglosen de manera entendible los factores objetivos determinantes de la calificación de riesgo.<br/>2. El sistema debe incorporar un botón directo para que el usuario pueda apelar el dictamen algorítmico y solicitar revisión humana asistida en un plazo máximo de 24 horas.<br/>3. El motor de scoring debe proporcionar coeficientes de explicabilidad (SHAP values / LIME) en cada inferencia registrada. |
| **Trazabilidad** | Deriva de la Visión institucional de la Sección 2.2 («80% de créditos autogestionados por canal digital»), de la Resolución SBS N.° 3198-2023 (Art. 15 y 18, conducta de mercado y no discriminación) y de la Estrategia E-03. |
