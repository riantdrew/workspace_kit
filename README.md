# Agent Workspace Kit

Протокол внедрения **agent workspace** в существующий проект.  
Поддерживаемые среды: Cursor, OpenCode, MCP-клиенты и другие платформы.

**Версия kit:** 1.5 · **Дата:** 19.06.2026

## Что это

[`workspace_kit.md`](workspace_kit.md) — единый документ-инструкция для агента. Он проводит аудит репозитория, определяет стадию `workspace/`, задаёт вопросы и по вашему согласию создаёт файлы контекста агента — без дублирования README и без лишней автономности.

Каталог агента: `workspace/`. Platform-адаптер: `.cursor/` или OpenCode-адаптер (если требуется) или `mcp/` — в зависимости от среды.

## Быстрый старт

**Без локального файла (рекомендуется):**

1. Откройте чат в вашей среде (Cursor, OpenCode и т.д.) и вставьте:

   ```
   https://github.com/riantdrew/cursor_starter_kit — помоги внедрить agent workspace
   ```

2. Агент загрузит актуальный kit с GitHub, определит среду и создаст адаптер под неё.
3. Ответьте на вопросы агента и подтвердите создание файлов.
4. Для рабочей сессии: `workspace/BOOTSTRAP.md`.

**С локальной копией:**

1. Скопируйте [`starter_kit.md`](starter_kit.md) в **корень** своего проекта.
2. Текст: `starter_kit.md — помоги внедрить agent workspace`.
3. Дальше — как выше, шаги 2–4.

### Raw URL (для агента)

```
https://raw.githubusercontent.com/riantdrew/workspace_kit/main/workspace_kit.md
```

## Что внутри kit

- **10 правил (CRITICAL)** — протокол без пропуска шагов
- **Загрузка с GitHub** — без копирования файла в проект; проверка версии remote vs local
- **Стадии 0–5** — от аудита до полноценного workspace
- **Шаблоны** — SOUL (+ communication), MEMORY (+ hypotheses), GOALS (+ guardrails), CONSTITUTION, BOOTSTRAP, PLAYBOOK, AGENTS и др.
- **Интеграции** — универсальная концепция staged integrations с адаптерами под Cursor, OpenCode, MCP
- **Сессионная память** — 3 слоя (журнал → чекпоинт → консолидация + orphan detection)
- **Goal lens** — принцип сверки любой задачи с целями
- **Профили** — solo и team
- **Changelog и миграции** — обновление kit без потери данных

## Осознанные ограничения

Kit **не** включает HEARTBEAT, CRON, `/loop` и Automations — только явные сессии и контролируемый контекст.

## Лицензия

MIT — используйте свободно в своих проектах.
