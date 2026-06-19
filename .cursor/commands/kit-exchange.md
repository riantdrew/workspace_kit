# kit-exchange

Двусторонний обмен с [workspace_kit](https://github.com/riantdrew/workspace_kit) — протокол v1.13.

## A. Kit → проект

1. GitHub MCP: `get_file_contents` → `workspace_kit.md` (main)
2. Сверить версию с `workspace/INDEX.md` → `starter_kit_version`
3. Если remote новее — diff-план; обновить **только kit-managed**:
   - `.cursor/skills/gh-workspace/SKILL.md`
   - `.cursor/commands/kit-exchange.md`, `session-end.md` (merge, не blind replace)
4. Обновить `starter_kit_version`, `starter_kit_source: remote` в INDEX.md
5. **Не трогать:** workspace/, SOUL, GOALS, MEMORY, rules, hooks, `.env`

## B. Проект → kit

**Ручной:** MEMORY.md, reports/, + `workspace/riantdrew/memory/` (7 дней).

**Automation:** только MEMORY.md + reports/ (memory в gitignore).

1. Универсальные паттерны workspace/Cursor — без домена и секретов
2. `search_issues` repo:riantdrew/workspace_kit → comment или create
3. Не дублировать closed `not_planned`

## C. Отчёт

`workspace/reports/kit-exchange/YYYY-MM-DD.md` + `kit_exchange_last_run` в INDEX.md.

**Не commit/push в workspace_kit** из этого проекта без явной команды.

При расхождении версий — [миграция через агента](https://github.com/riantdrew/workspace_kit/blob/main/workspace_kit.md).
