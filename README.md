# Agent Workspace Kit

Протокол внедрения **agent workspace** в существующий проект для [Cursor](https://cursor.com).

**Версия kit:** 1.11 · **Дата:** 19.06.2026

## Что это

[`workspace_kit.md`](workspace_kit.md) — единый документ-инструкция для агента. Он проводит аудит репозитория, определяет стадию `workspace/`, задаёт вопросы и по вашему согласию создаёт файлы контекста агента — без дублирования README и без лишней автономности.

Каталог агента: `workspace/`. Конфиг Cursor: `.cursor/` (rules, hooks, skills, commands).

## Быстрый старт

**Без локального файла (рекомендуется):**

1. Откройте чат в Cursor и вставьте:

   ```
   https://github.com/riantdrew/workspace_kit — помоги внедрить agent workspace
   ```

2. Агент загрузит актуальный kit с GitHub и создаст конфиг `.cursor/`.
3. Ответьте на вопросы агента и подтвердите создание файлов.
4. Для рабочей сессии: `workspace/BOOTSTRAP.md`.

**С локальной копией:**

1. Скопируйте [`workspace_kit.md`](workspace_kit.md) в **корень** своего проекта.
2. Текст: `workspace_kit.md — помоги внедрить agent workspace`.
3. Дальше — как выше, шаги 2–4.

> Старые проекты могут хранить локальную копию как `starter_kit.md` — kit поддерживает оба имени.

### Raw URL (для агента)

```
https://raw.githubusercontent.com/riantdrew/workspace_kit/main/workspace_kit.md
```

## Что внутри kit

- **10 правил (CRITICAL)** — протокол без пропуска шагов
- **Загрузка с GitHub** — без копирования файла в проект; проверка версии remote vs local
- **Стадии 0–5** — от аудита до полноценного workspace
- **Шаблоны** — SOUL (+ communication), MEMORY (+ hypotheses), GOALS (+ guardrails), CONSTITUTION, BOOTSTRAP, PLAYBOOK, AGENTS и др.
- **Интеграции Cursor** — rules, hooks, skills, commands (staged по стадиям)
- **Сессионная память** — 3 слоя (журнал → чекпоинт → консолидация + orphan detection)
- **Goal lens** — принцип сверки любой задачи с целями
- **Профили** — solo и team
- **Changelog и миграции** — обновление kit без потери данных
- **Обратная связь** — GitHub Issues + MCP; **kit-exchange** — автоматически ≥1 раз/нед (Cursor Automation)

## Осознанные ограничения

Kit **не** включает HEARTBEAT, CRON, `/loop` и Automations — только явные сессии и контролируемый контекст.

## Лицензия

MIT — используйте свободно в своих проектах.
