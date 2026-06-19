---
name: gh-workspace
description: GitHub Issues своего проекта — задачи, планы, сверка с GOALS. Use when user asks about tasks, issues, board, what is in progress.
---

# GitHub workspace-sync

Протокол: `workspace/workspace-sync.md` и раздел [workspace-sync](https://github.com/riantdrew/workspace_kit/blob/main/workspace_kit.md) в kit. MCP server: **user-github**.

## Repo guard (обязательно)

1. `owner/repo` = `git remote get-url origin` или `workspace/PROJECT.md` → `repositories`
2. Если repo == `riantdrew/workspace_kit` → **STOP**. Это kit-exchange, не workspace-sync
3. Create/update/close Issues — **только после явной просьбы** пользователя

## Resolve login (team)

Перед чтением personal memory:

1. `gh auth status` → github-login
2. Иначе `data/workspace_user` (gitignore)
3. Иначе спросить один раз

Personal: `workspace/<login>/USER.md`, `workspace/<login>/memory/`

## Read workflow

1. `get_me` (опционально)
2. `list_issues` — state OPEN, owner/repo **проекта**
3. Сверить с `workspace/GOALS.md` (GOALS = индекс + ссылки `#N`; Issues = работа)
4. При расхождении — сказать вслух

## Write workflow (только по просьбе)

1. Подтвердить действие (create / update / comment / close)
2. Body — **для людей** (инфостиль): что произошло, зачем, одно CTA; техника — ссылкой на файл в `workspace/`
3. Не дублировать полные дампы `knowledge/` в issue

## Close

При закрытии issue — предложить строку в shared `workspace/MEMORY.md`, не дублировать в issue.

## Boundaries

| Тема | Куда |
|------|------|
| Задачи команды | Issues **этого** repo |
| Feedback по kit | `/kit-exchange` → `riantdrew/workspace_kit` |
| Обновление kit в проекте | [Миграция через агента](https://github.com/riantdrew/workspace_kit/blob/main/workspace_kit.md) — вопросы, diff-план, merge |
| Командные факты | `workspace/MEMORY.md` |
