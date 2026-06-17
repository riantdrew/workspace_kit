# Cursor Starter Kit

Протокол внедрения **agent workspace** в существующий проект для [Cursor](https://cursor.com).

**Версия kit:** 1.4 · **Дата:** 18.06.2026

## Что это

[`starter_kit.md`](starter_kit.md) — единый документ-инструкция для агента Cursor. Он проводит аудит репозитория, определяет стадию `workspace/`, задаёт вопросы и по вашему согласию создаёт файлы контекста агента — без дублирования README и без лишней автономности.

Каталог агента: `workspace/`. Skills Cursor: `.cursor/skills/`.

## Быстрый старт

**Без локального файла (рекомендуется):**

1. Откройте чат в Cursor и вставьте:

   ```
   https://github.com/riantdrew/cursor_starter_kit — помоги внедрить agent workspace
   ```

2. Агент загрузит актуальный kit с GitHub. Если локальная копия уже есть — сверит версию.
3. Ответьте на вопросы агента и подтвердите создание файлов.
4. Для рабочей сессии в новом чате: `@workspace/BOOTSTRAP.md`.

**С локальной копией:**

1. Скопируйте [`starter_kit.md`](starter_kit.md) в **корень** своего проекта.
2. Чат: `@starter_kit.md помоги внедрить agent workspace`.
3. Дальше — как выше, шаги 2–4.

### Raw URL (для агента)

```
https://raw.githubusercontent.com/riantdrew/cursor_starter_kit/main/starter_kit.md
```

## Что внутри kit

- **10 правил (CRITICAL)** — протокол без пропуска шагов
- **Загрузка с GitHub** — без копирования файла в проект; проверка версии remote vs local
- **Стадии 0–5** — от аудита до полноценного workspace
- **Шаблоны** — SOUL, MEMORY, CONSTITUTION, BOOTSTRAP, AGENTS и др.
- **Интеграции Cursor** — rules, hooks, skills
- **Профили** — solo и team
- **Changelog и миграции** — обновление kit без потери данных

## Осознанные ограничения

Kit **не** включает HEARTBEAT, CRON, `/loop` и Cursor Automations — только явные сессии и контролируемый контекст.

## Лицензия

MIT — используйте свободно в своих проектах.
