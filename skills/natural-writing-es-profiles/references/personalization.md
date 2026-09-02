# Proceso de personalización

## 1. Reunir y clasificar

Sigue `intake.md`. Usa 3–10 muestras. Una muestra puede pegarse en conversación, adjuntarse como archivo o identificarse mediante un manifiesto local. No publiques ni copies los documentos dentro de la Skill.

## 2. Analizar

Observa organización, progresión lógica, causalidad, longitud de oración, ritmo, formalidad, vocabulario, grado de explicitud, conectores, incisos, puntuación y cierres. Separa señales estables de convenciones del género.

Para muletillas y marcas autorales registra:

- forma observada;
- función real en el discurso;
- ámbitos y posiciones donde aparece;
- distribución entre muestras, no solo número bruto;
- frecuencia natural aproximada;
- riesgo de monotonía o ambigüedad;
- condición para preservarla, moderarla o corregirla.

Un patrón de puntuación solo puede registrarse mediante evidencia recurrente, ejemplos estructurales abstractos y revisión sintáctica. Conserva la función autoral demostrada, no una puntuación incorrecta.

## 3. Derivar capas

Crea `base` con rasgos repetidos en varios ámbitos. Crea un ajuste de ámbito únicamente con al menos 3 muestras válidas de ese ámbito y diferencias comprobables respecto de la base.

No rellenes categorías por obligación. Expresa contradicciones y nivel de confianza.

## 4. Proponer y validar

Escribe un candidato conforme a `profiles/profile-template.md`. Valídalo con `scripts/profile_manager.py validate`. Prueba al menos:

- edición mínima de una muestra reservada;
- redacción nueva desde hechos;
- un texto fuera del ámbito esperado;
- presencia natural, no obligatoria, de las marcas autorales;
- corrección de errores recurrentes sin pérdida de voz.

Compara contra la variante neutral y solicita correcciones al usuario. No actives el candidato por el mero hecho de haberlo generado.

## 5. Activar, actualizar o restablecer

Activa solo con confirmación explícita. Una actualización crea primero otro candidato. El reseteo por ámbito elimina ese ajuste; el reseteo de `base` elimina también sus ajustes dependientes; `selection` conserva los archivos y vuelve a `auto + neutral`; `all` vuelve la Skill a su estado base distribuible.
