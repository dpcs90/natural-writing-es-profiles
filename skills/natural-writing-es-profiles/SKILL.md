---
name: natural-writing-es-profiles
description: Redactar, editar, reescribir y auditar textos naturales mediante perfiles académico, profesional/comercial o personal, cada uno en variante neutral o personalizada. Usar cuando se necesite cambiar de perfil, inferir el ámbito por el encargo, preservar una voz autoral a partir de 3 a 10 muestras auténticas, revisar muletillas y marcas discursivas sin reproducir errores, o restablecer la escritura al estado neutral.
---

# Natural Writing ES · Profiles

Escribe como una versión más clara del autor, no como una voz genérica ni como una imitación de sus errores. Conserva el idioma del texto de origen salvo petición expresa.

## 1. Resolver el encargo

Determina tres ejes independientes:

1. **Modo**: `Draft`, `Edit`, `Rewrite`, `Detect`, `Profile`, `Select` o `Reset`.
2. **Ámbito**: `academic`, `professional-commercial`, `personal` o `auto`.
3. **Variante**: `neutral` o `custom`.

Usa la selección explícita del usuario. Si no existe, consulta `profiles/selection.json`; si tampoco existe, usa `auto + neutral`. En `auto`, infiere el ámbito por propósito, destinatario y medio. Ante ambigüedad material, pregunta; si no cambia sustancialmente el resultado, elige el ámbito más conservador.

Los modos de redacción son:

- **Draft**: redacta desde hechos, notas o instrucciones proporcionadas.
- **Edit**: realiza la mínima edición efectiva. El texto fuente y su voz prevalecen sobre el perfil seleccionado.
- **Rewrite**: permite reorganización profunda solo si se solicita.
- **Detect**: audita sin reescribir el texto completo ni atribuir autoría humana o artificial.
- **Profile**: analiza muestras y propone un perfil candidato; no lo activa automáticamente.
- **Select**: cambia el ámbito o la variante activa.
- **Reset**: restablece una capa, la selección o todo el estado personalizado.

## 2. Aplicar perfiles por capas

Carga siempre el perfil neutral del ámbito:

- académico: `profiles/neutral/academic.md`
- profesional/comercial: `profiles/neutral/professional-commercial.md`
- personal: `profiles/neutral/personal.md`

Para la variante `custom`, añade `profiles/custom/base.md` y, si existe, el ajuste `profiles/custom/<ámbito>.md`. Si falta el perfil base, usa la variante neutral e indícalo brevemente. Si existe la base pero no el ajuste del ámbito, combina la base con el perfil neutral correspondiente.

Orden de prioridad:

1. significado, hechos y restricciones explícitas;
2. corrección gramatical, precisión y seguridad;
3. voz observable en el texto fuente;
4. perfil personalizado aplicable;
5. convenciones neutrales del ámbito.

No impongas la voz personalizada del usuario sobre citas, textos de terceros o documentos que deban conservar otra autoría.

## 3. Personalizar sin imitar errores

Para crear o actualizar un perfil, sigue `references/personalization.md` y usa de 3 a 10 muestras auténticas, variadas y suficientemente extensas. Distingue:

- rasgos estables del autor;
- rasgos dependientes del ámbito o género;
- hábitos corregibles;
- errores ortográficos, gramaticales o sintácticos.

Puedes conservar **marcas autorales válidas**: muletillas discursivas, aperturas, conectores preferidos, incisos, repeticiones deliberadas, ritmo y patrones recurrentes de puntuación o encuadre temático.

Nunca conviertas en estilo una puntuación que rompa dependencias sintácticas, una concordancia incorrecta ni otro error. Evalúa cada marca por recurrencia, función, adecuación al medio y corrección. No maximices su frecuencia: conserva una presencia natural y proporcional.

Registra los rasgos con evidencia y límites de uso mediante `profiles/profile-template.md`. Mantén en privado las muestras y los perfiles derivados.

## 4. Reglas esenciales

- Preserva significado, criterio, opinión, incertidumbre, tecnicidad y nivel de formalidad.
- No inventes hechos, cifras, fechas, fuentes, ejemplos ni conclusiones.
- No simplifiques una idea hasta volverla menos correcta.
- Prefiere formulaciones claras, sin imponer voz activa o frases cortas artificialmente.
- Permite oraciones largas, sujetos impersonales y terminología técnica cuando funcionen.
- Usa listas, encabezados y énfasis solo cuando mejoren la comprensión.
- Evita relleno, simetría mecánica, abstracciones vacías, atribuciones vagas, cierres repetitivos y grandilocuencia.
- Trata expresiones sospechosas como indicios contextuales, no como prohibiciones. Consulta `references/patterns.md` cuando el texto muestre repetición, burocratización o pulido genérico.
- Antes de entregar, aplica la revisión interna de `references/eval.md`.

## 5. Comportamiento de salida

En `Draft`, `Edit` y `Rewrite`, entrega por defecto solo el texto final listo para usar. No añadas “Qué cambié” salvo petición.

En `Detect`, señala patrones concretos, efecto y tipo de corrección; no reescribas el texto entero.

En `Profile`, presenta hallazgos, incertidumbres y perfil candidato. Solicita confirmación antes de activarlo. Si faltan muestras o diversidad, limita el alcance en vez de inventar rasgos.

En `Reset`, explica de forma breve qué capas se eliminarán. El reseteo de `base` elimina también los ajustes personalizados dependientes y la selección, por lo que vuelve a `auto + neutral`; el reseteo `selection` conserva perfiles pero vuelve a `auto + neutral`; el reseteo `all` elimina selección y perfiles personalizados. Exige confirmación explícita para borrar perfiles.

Usa `scripts/profile_manager.py` para validar, activar, seleccionar, consultar o restablecer perfiles cuando se opere sobre archivos locales.
