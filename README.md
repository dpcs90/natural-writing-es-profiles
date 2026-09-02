# natural-writing-es-profiles

Segunda versión de `natural-writing-es`, diseñada para cambiar entre ámbitos de escritura y conservar, cuando exista evidencia suficiente, la voz autoral de una persona sin reproducir sus errores.

La Skill mejora claridad, naturalidad y precisión. No intenta ocultar el uso de IA ni determinar la autoría de un texto.

## Arquitectura

La selección combina tres ejes:

| Eje | Opciones |
| --- | --- |
| Modo | `Draft`, `Edit`, `Rewrite`, `Detect`, `Profile`, `Select`, `Reset` |
| Ámbito | académico, profesional/comercial, personal o automático |
| Variante | neutral o personalizada |

La configuración inicial es `auto + neutral`. En modo automático, la Skill decide el ámbito según el propósito, destinatario y medio.

La variante personalizada usa dos capas:

1. un perfil autoral base con rasgos estables;
2. un ajuste opcional por ámbito cuando existen al menos tres muestras válidas de ese ámbito.

Si existe el perfil base pero no un ajuste específico, se combina la voz autoral con el perfil neutral del ámbito. Esto evita crear seis perfiles independientes y reduce el sobreajuste.

## Uso

Ejemplos de solicitudes:

```text
Usa $natural-writing-es-profiles en modo Edit, ámbito académico y variante neutral. Haz la mínima intervención efectiva.
```

```text
Usa $natural-writing-es-profiles con mi perfil propio para redactar un email profesional. Conserva mis matices y deja clara la acción esperada.
```

```text
Usa $natural-writing-es-profiles en modo Detect. Señala patrones problemáticos, pero no reescribas el texto ni determines si fue escrito por IA.
```

```text
Usa $natural-writing-es-profiles para volver completamente al estado base neutral. Antes de borrar perfiles, indícame qué se eliminará.
```

## Personalización mediante documentos

La personalización deriva una configuración editorial; no entrena ni modifica el modelo de IA.

1. Aporta de 3 a 10 textos auténticos; se recomiendan 5 a 7.
2. Incluye longitudes y géneros distintos: por ejemplo, mensajes, emails, informes, textos académicos o notas personales.
3. Indica para cada documento el propósito, destinatario, ámbito, fecha aproximada y si fue corregido por otra persona o generado parcialmente con IA.
4. Señala cuáles textos representan mejor la voz deseada y cuáles contienen hábitos que prefieres corregir.
5. Solicita el modo `Profile`. La Skill separará rasgos estables, rasgos contextuales y errores.
6. Revisa el perfil candidato y una comparación contra la variante neutral.
7. Confirma expresamente su activación.

Los rasgos detectables incluyen progresión lógica, causalidad, longitud de oración, ritmo, formalidad, vocabulario, conectores, incisos, aperturas, cierres, muletillas y patrones válidos de puntuación. Una marca recurrente puede preservarse, limitarse a ciertos contextos o moderarse. Los errores ortográficos, gramaticales y sintácticos siempre se corrigen.

Las muestras pueden pegarse en el chat, adjuntarse como TXT, Markdown, DOCX o PDF, o suministrarse desde una carpeta acompañada por un manifiesto. La capacidad de leer cada formato depende del agente anfitrión.

## Administración local de perfiles

Consultar el estado:

```bash
python skills/natural-writing-es-profiles/scripts/profile_manager.py status
```

Validar y activar un candidato base:

```bash
python skills/natural-writing-es-profiles/scripts/profile_manager.py validate /ruta/candidate.md --target base
python skills/natural-writing-es-profiles/scripts/profile_manager.py activate /ruta/candidate.md --target base --confirm-activate
```

Seleccionar un ámbito y la variante propia:

```bash
python skills/natural-writing-es-profiles/scripts/profile_manager.py select academic custom
```

Los valores de ámbito son `auto`, `academic`, `professional-commercial` y `personal`.

Eliminar solo el ajuste académico:

```bash
python skills/natural-writing-es-profiles/scripts/profile_manager.py reset --target academic --confirm-reset
```

Volver a la selección inicial conservando los perfiles derivados:

```bash
python skills/natural-writing-es-profiles/scripts/profile_manager.py reset --target selection --confirm-reset
```

Volver completamente al estado base distribuible:

```bash
python skills/natural-writing-es-profiles/scripts/profile_manager.py reset --target all --confirm-reset
```

El reseteo de `base` elimina también los ajustes personalizados que dependen de él. Ningún reseteo modifica los perfiles neutrales distribuidos con la Skill.

Además, `reset --target base` elimina la selección local y devuelve el comportamiento efectivo a `auto + neutral`.

## Instalación

Este README presupone que el repositorio se publica como `dpcs90/natural-writing-es-profiles`.

### Claude Code

Como marketplace:

```text
/plugin marketplace add dpcs90/natural-writing-es-profiles
/plugin install natural-writing-es-profiles@natural-writing-es-profiles
/reload-plugins
```

Instalación manual para un proyecto:

```bash
cp -R skills/natural-writing-es-profiles .claude/skills/natural-writing-es-profiles
```

Para uso personal, copiar la misma carpeta a `~/.claude/skills/natural-writing-es-profiles`.

### Gemini CLI

```bash
gemini skills install https://github.com/dpcs90/natural-writing-es-profiles.git --path skills/natural-writing-es-profiles
```

Gemini solicitará confirmar la procedencia y los permisos de la Skill. Después de instalarla, ejecutar `/skills reload` dentro de la sesión y comprobarla con `/skills list`.

También puede copiarse la carpeta a `.gemini/skills/natural-writing-es-profiles` o `.agents/skills/natural-writing-es-profiles`, según la versión y el alcance configurado.

### Codex y otros agentes compatibles

En Codex, puede pedirse al instalador de Skills que instale el repositorio y seleccione `skills/natural-writing-es-profiles/`:

```text
Usa $skill-installer para instalar la Skill desde https://github.com/dpcs90/natural-writing-es-profiles y la ruta skills/natural-writing-es-profiles.
```

Para una instalación manual compatible con el estándar compartido, copiar la carpeta a `~/.agents/skills/natural-writing-es-profiles/` en el ámbito personal o a `.agents/skills/natural-writing-es-profiles/` dentro de un proyecto. Algunas instalaciones locales de Codex también reconocen `~/.codex/skills/`; conviene comprobarlo con la versión utilizada. En ChatGPT, puede instalarse el paquete mediante la interfaz disponible para Skills personales.

Si un agente no admite carga progresiva, usar `SKILL.md` como instrucción principal y conservar las rutas relativas de `profiles/`, `references/` y `scripts/`.

### Persistencia de la personalización

El gestor local requiere que la carpeta de la Skill sea escribible. Funciona directamente en instalaciones locales de Claude Code, Gemini CLI y Codex. En entornos alojados, inmutables o que reinstalan la Skill en cada sesión, se debe seleccionar el perfil en cada solicitud o mantener una distribución privada ya configurada; no debe asumirse que `profiles/custom/` persistirá.

## Privacidad

Los documentos fuente no se almacenan en este repositorio. `profiles/custom/`, `profiles/selection.json`, `samples/` y los archivos `*.local.md` están excluidos de Git. Antes de publicar o compartir una copia, ejecutar las validaciones para comprobar que no contenga perfiles activos ni muestras.

## Validación

```bash
python tests/validate_package.py
python tests/test_profile_manager.py
```

## Créditos y licencia

La arquitectura toma como referencia conceptual `no-ai-slop`, de Peter Yang, pero constituye una adaptación independiente en español con selección de ámbitos, capas de personalización, evaluación y reseteo propios. Véase [ATTRIBUTION.md](ATTRIBUTION.md).

Licencia MIT.
