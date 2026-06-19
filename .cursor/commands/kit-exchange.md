# kit-exchange

Двусторонний обмен с [workspace_kit](https://github.com/riantdrew/workspace_kit).

**A. Kit → проект:** только **kit-managed** артефакты (merge, не blind replace). Полный протокол — `workspace_kit.md` → «Merge при kit → проект».

**B. Ручной:** + `workspace/<login>/memory/` (7 дней). **Automation:** только MEMORY.md + reports/.

**C. Отчёт:** `workspace/reports/kit-exchange/YYYY-MM-DD.md`.

При расхождении версий INDEX vs kit — сначала [миграция через агента](https://github.com/riantdrew/workspace_kit/blob/main/workspace_kit.md). Репозиторий kit **не коммитить** из этого проекта.
