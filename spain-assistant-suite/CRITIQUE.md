# Product critique and implemented improvements — 0.2.0

## Shared diagnosis

The first release was installable, but looked more like seven API wrappers than seven clear first-use products. Long safety/runtime intros and JSON-only output obscured the payoff. The correction is not seven SaaS backends: it is useful source-grounded outputs, a demonstrable first result, focused workflows and reliability checks.

The redesign improves presentation and implementation; no measured adoption uplift is asserted. The public examples are labelled snapshots, not fabricated live results.

## Licita España

**Weakness found:** Un aviso actualizado no es necesariamente una oportunidad abierta. El cursor anterior podía saltarse coincidencias y la primera experiencia era JSON sin contexto.

**Implemented:** Continuación dentro de la página, lectura explícita de plazos, filtro opcional por fecha e informe legible con fuentes.

**Remaining boundary:** Ventana acotada del feed de PLACSP, no todas las licitaciones españolas. No lee automáticamente los PDF ni presenta ofertas. La decisión requiere pliegos, correcciones y perfil oficial.

[Live product page](https://samihalawa.github.io/licita-espana/) · [Change log](https://github.com/samihalawa/licita-espana/blob/v0.2.0/CHANGELOG.md)

## Ayudas España

**Weakness found:** Las funciones separadas obligaban a reconstruir cada convocatoria. La promesa de elegibilidad era más fuerte que la verificación disponible.

**Implemented:** Shortlist con detalle de llamadas, fechas, beneficiarios y bases; señales de concesión directa sin una falsa garantía de elegibilidad.

**Remaining boundary:** Hasta cinco detalles por llamada. Fechas, abierto y palabras como nominativa no sustituyen bases, modificaciones y sede. No presenta solicitudes ni garantiza financiación.

[Live product page](https://samihalawa.github.io/ayudas-espana/) · [Change log](https://github.com/samihalawa/ayudas-espana/blob/v0.2.0/CHANGELOG.md)

## BOE Impact

**Weakness found:** El diff técnico no mostraba cómodamente el antes y el después. Las respuestas de error del sumario podían parecer búsquedas sin resultados.

**Implemented:** Textos y fechas explícitas, informe de cambios legible y validación del estado del proveedor.

**Remaining boundary:** La consolidación es informativa. No decide automáticamente aplicabilidad, régimen transitorio o conformidad legal. Verifica la publicación original para decisiones jurídicas.

[Live product page](https://samihalawa.github.io/boe-impact/) · [Change log](https://github.com/samihalawa/boe-impact/blob/v0.2.0/CHANGELOG.md)

## BORME Intelligence

**Weakness found:** Una consulta de un único día era demasiado estrecha para la promesa de inteligencia empresarial. No había una vista cómoda de varios días.

**Implemented:** Consulta por intervalo, informe por anuncio y cobertura que conserva los días no comprobados.

**Remaining boundary:** No es un historial completo, monitor continuo, certificado registral ni evaluación crediticia. Una coincidencia de nombre no prueba identidad. No crea perfiles de personas.

[Live product page](https://samihalawa.github.io/borme-intelligence/) · [Change log](https://github.com/samihalawa/borme-intelligence/blob/v0.2.0/CHANGELOG.md)

## Catastro Pro

**Weakness found:** Algunos errores del Catastro se devolvían como éxito. Las coordenadas eran campos técnicos sin ejes normalizados.

**Implemented:** Ficha clara, errores explícitos, puntos validados y ejes etiquetados; varias propiedades nunca se reducen a una por defecto.

**Remaining boundary:** Solo datos no protegidos. No acredita propiedad, habitabilidad, valor o licencia urbanística. El punto no delimita una parcela. Navarra y País Vasco usan sistemas separados.

[Live product page](https://samihalawa.github.io/catastro-pro/) · [Change log](https://github.com/samihalawa/catastro-pro/blob/v0.2.0/CHANGELOG.md)

## INE Evidence

**Weakness found:** El JSON exigía interpretar códigos y el límite local ocultaba series. Un ejemplo histórico podía confundirse con un dato vigente.

**Implemented:** Tablas legibles, offsets explícitos, periodos visibles y demostración etiquetada como histórica.

**Remaining boundary:** No ofrece previsiones ni asesoramiento de inversión. Una serie disponible puede estar discontinuada o usar una base antigua. No une series incompatibles ni infiere actualidad por disponibilidad.

[Live product page](https://samihalawa.github.io/ine-evidence/) · [Change log](https://github.com/samihalawa/ine-evidence/blob/v0.2.0/CHANGELOG.md)

## Spain Open Data

**Weakness found:** Una lista de enlaces se parecía demasiado a una búsqueda genérica. Faltaba una ficha útil y el identificador explícito para continuar.

**Implemented:** Fichas comparables, identificadores de dataset y errores de esquema explícitos, con checklist de reutilización.

**Remaining boundary:** No descarga automáticamente distribuciones externas ni ejecuta archivos. No garantiza licencias o descargas vigentes. La fecha del catálogo no equivale al periodo del dato.

[Live product page](https://samihalawa.github.io/spain-open-data/) · [Change log](https://github.com/samihalawa/spain-open-data/blob/v0.2.0/CHANGELOG.md)

## Portfolio judgement

Ayudas and Licita have the clearest decision-oriented promise, but also the highest cost of mistaken eligibility or coverage claims. BOE and Catastro offer especially concrete demonstrations; usefulness still depends on respecting legal/property limits. INE offers repeatable evidence work with less sales drama. BORME and Open Data need a sufficiently specific recurring user task to avoid being occasional lookup tools. These are product judgments, not measured demand or revenue rankings.

The next proof needed is users completing their own real tasks and returning—not another directory listing. No analytics or unsolicited tracking was added.
