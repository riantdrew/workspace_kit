# workspace_kit — внедрение agent workspace в существующий проект

**Версия kit:** 1.9  
**Дата:** 19.06.2026  
**Схема workspace:** 1.5 (совместима с ≥ 1.0)  
**Профиль по умолчанию:** solo — см. [Профили: solo и team](#профили-solo-и-team)  
**Канонический репозиторий:** https://github.com/riantdrew/workspace_kit  
**Канонический raw URL:** https://raw.githubusercontent.com/riantdrew/workspace_kit/main/workspace_kit.md  
**Ветка по умолчанию:** `main`  
**Локальный путь (опционально):** `workspace_kit.md` в **корне** проекта — для `@workspace_kit.md` (legacy: `starter_kit.md` / `@starter_kit.md`)  
**Каталог агента:** `workspace/` — markdown-контекст агента **только здесь**, не в корне и не рядом с кодом приложения

> Загрузите в чат: ссылку на [канонический репозиторий](#источники-загрузки-kit), raw URL или `@workspace_kit.md` (legacy: `@starter_kit.md`). Агент **обязан** начать с [CRITICAL](#critical--10-правил-для-агента), [Источник и версия kit](#0-источник-и-версия-kit) и [Протокол для агента](#протокол-для-агента).

---

## CRITICAL — 10 правил для агента

1. **MUST** выполнить [Протокол](#протокол-для-агента) **строго по порядку**: сначала [Источник и версия kit](#0-источник-и-версия-kit), затем [аудит репозитория](#стадия-0--аудит-репозитория), затем оценка `workspace/`.
2. **MUST** при локальной копии сверить её с [каноническим raw URL](#источники-загрузки-kit) и работать по **более свежей** версии kit.
3. **MUST NOT** рекурсивно обходить весь репозиторий — только [алгоритм выборочного аудита](#алгоритм-аудита-без-перегрузки-контекста).
4. **MUST NOT** создавать файлы без согласия пользователя — сначала отчёт и рекомендации.
5. **MUST NOT** выдумывать бизнес-факты — `TODO: уточнить у USER`.
6. **MUST NOT** дублировать README, `docs/` продукта, существующие ADR в `workspace/`.
7. **MUST** класть markdown агента **только** в `workspace/`. Правила, хуки, skills и commands — **только** в `.cursor/`. Ничего из `.cursor/` не класть в `workspace/`.
8. **MUST NOT** создавать более **8 файлов за одну итерацию** (кроме явной просьбы «сразу всё»).
9. **MUST** верифицировать созданные файлы по [чек-листу разделов](#верификация-после-создания).
10. **MUST NOT** включать HEARTBEAT, CRON, `/loop`, Automations — вне scope kit; см. [Осознанные отказы](#осознанные-отказы).

**Триггеры запуска:** `@workspace_kit.md`, `@starter_kit.md` (legacy), ссылка на GitHub-репозиторий kit, raw URL `workspace_kit.md`, «помоги с workspace / workspace kit», «внедри agent workspace».

---

## Быстрый старт

### Для человека

**Вариант A — без локального файла (рекомендуется):**

1. Чат: вставьте ссылку на репозиторий — https://github.com/riantdrew/workspace_kit — и напишите «помоги внедрить agent workspace».
2. Агент подтянет актуальный `workspace_kit.md` с GitHub и сверит версию, если локальная копия уже есть.
3. Ответьте на вопросы перехода **0 → 1**.
4. Подтвердите создание файлов стадии 1 (и 2, если готовы).
5. Новый чат: `@workspace/BOOTSTRAP.md` — рабочая сессия; в конце — «завершаем сессию».

**Вариант B — локальная копия:**

1. Положите `workspace_kit.md` в **корень** проекта (или обновите из [канонического репозитория](#источники-загрузки-kit)). Legacy-имя `starter_kit.md` тоже принимается.
2. Чат: `@workspace_kit.md помоги внедрить agent workspace`.
3. Дальше — как в варианте A, шаги 3–5.

### Для агента (одна строка)

источник kit + версия → CRITICAL → аудит репо → стадия `workspace/` → вопросы текущего перехода → рекомендации → создание (≤8 файлов) → верификация → итог.

---

## Источники загрузки kit

Kit **не обязан** лежать в проекте. Канон — публичный GitHub-репозиторий; локальный `workspace_kit.md` — опциональная копия для `@workspace_kit.md` (legacy: `starter_kit.md`).

### Канонические URL

| Назначение | URL |
|------------|-----|
| Репозиторий | https://github.com/riantdrew/workspace_kit |
| Raw (для агента) | https://raw.githubusercontent.com/riantdrew/workspace_kit/main/workspace_kit.md |
| Ветка по умолчанию | `main` |
| Путь в репо | `workspace_kit.md` (корень репозитория kit) |

> Если вы форкаете kit — обновите URL в форке; проекты могут ссылаться на ваш fork тем же способом.

### Как запустить в чате

| Способ | Пример |
|--------|--------|
| Ссылка на репозиторий | `https://github.com/riantdrew/workspace_kit — внедри agent workspace` |
| Raw URL | `https://raw.githubusercontent.com/riantdrew/workspace_kit/main/workspace_kit.md` |
| Локальный файл | `@workspace_kit.md` в корне **вашего** проекта (legacy: `@starter_kit.md`) |

### Нормализация GitHub-ссылок (для агента)

Любую ссылку пользователя приведи к raw URL `workspace_kit.md`:

| Вход | Raw URL |
|------|---------|
| `https://github.com/OWNER/REPO` | `https://raw.githubusercontent.com/OWNER/REPO/main/workspace_kit.md` |
| `https://github.com/OWNER/REPO/tree/BRANCH` | `https://raw.githubusercontent.com/OWNER/REPO/BRANCH/workspace_kit.md` |
| `https://github.com/OWNER/REPO/blob/BRANCH/workspace_kit.md` | `https://raw.githubusercontent.com/OWNER/REPO/BRANCH/workspace_kit.md` |
| Legacy blob `…/starter_kit.md` | `https://raw.githubusercontent.com/OWNER/REPO/BRANCH/starter_kit.md` |
| Уже raw | использовать как есть |

Если ветка не указана — `main`, затем `master`. Если `workspace_kit.md` недоступен (404) — пробуй legacy `starter_kit.md` на той же ветке.

### Сравнение версий (semver-lite)

Версия kit — строка **`X.Y`** в шапке файла (`**Версия kit:**`). Сравнение:

1. Старше та, у которой больше **major** (`2.0` > `1.4`).
2. При равном major — больше **minor** (`1.4` > `1.3`).
3. Патч и суффиксы kit **не использует** — только `X.Y`.

При равных версиях, но разном содержимом — предпочитай **remote**, если локальная копия не из канонического репозитория (hash/commit не проверяем — достаточно версии и явного расхождения текста шапки).

### Алгоритм загрузки и проверки (агент)

1. **Определи источник сессии:**
   - `@workspace_kit.md`, `@starter_kit.md` (legacy) или локальный путь → `local`
   - GitHub / raw URL в чате → `remote` (нормализуй URL)
   - Только текстовый триггер без URL и без локального файла → загрузи **канонический raw URL**
2. **Прочитай remote:** первые ~50 строк канонического raw URL (`WebFetch` / `curl` / аналог). Извлеки `**Версия kit:**`.
3. **Если есть `./workspace_kit.md` или `./starter_kit.md` (legacy) в корне проекта:**
   - Прочитай локальный файл, извлеки версию.
   - Сравни по [semver-lite](#сравнение-версий-semver-lite).
   - **Remote новее** → сообщи пользователю (локальная X.Y, каноническая Z.W), работай по **remote**; предложи обновить локальный файл **после согласия** (≤1 файл).
   - **Локальная новее или равна** → работай по локальной; если remote недоступен — локальная + предупреждение.
4. **Если локального файла нет** → загрузи полный remote и работай по нему.
5. **Если remote недоступен** и локального нет → остановись: «Не удалось загрузить workspace_kit. Проверьте сеть или положите workspace_kit.md в корень проекта».
6. **Зафиксируй в отчёте сессии:** источник (`local` / `remote`), версия kit, результат сверки.

### Что не делать

- **MUST NOT** копировать `workspace_kit.md` в `workspace/` — версия только в `workspace/INDEX.md`.
- **MUST NOT** молча игнорировать более свежий remote.
- **MUST NOT** перезаписывать локальный файл без согласия пользователя.

---

## Версия и эволюция kit

Этот файл **эволюционирует** вместе с практиками ИИ-разработки. Каждый проект фиксирует в `workspace/INDEX.md`: `starter_kit_version`, `starter_kit_source` (`local` / `remote`).

### Changelog

| Версия | Дата | Изменения |
|--------|------|-----------|
| **1.9** | 19.06.2026 | Единое имя **kit-sync** (каталог релиза и протокол); legacy `pilot-sync/`; таблица имён |
| **1.8** | 19.06.2026 | Kit только для Cursor; убраны OpenCode и MCP как отдельные среды |
| **1.7** | 19.06.2026 | Kit-sync: протокол pull/push, learnings + issues, manifest, граница пилот vs kit repo |
| **1.6** | 19.06.2026 | Переименование в workspace_kit; обновление всех ссылок и упоминаний |
| **1.5** | 19.06.2026 | Платформонезависимая архитектура; session memory (3 слоя + orphan); SOUL.communication; MEMORY.hypotheses; GOALS.guardrails; PLAYBOOK.md; goal lens; agent-knowledge rule |
| **1.4** | 18.06.2026 | Загрузка kit по GitHub/raw URL без локальной копии; проверка версии remote vs local; канонический репозиторий; шаг протокола «Источник и версия kit» |
| **1.3** | 18.06.2026 | CRITICAL-блок; аудит больших репо; staged rules; `.cursor/skills/`; шаблоны rules/hooks; эволюция kit; team-профиль; верификация; anti-patterns |
| **1.2** | — | Каталог `workspace/`; изоляция от кода; миграция из корня |
| **1.1** | — | Интеграции Cursor (rules, hooks, commands); стадии 0–5 |
| **1.0** | — | Первая схема файлов SOUL, MEMORY, CONSTITUTION, BOOTSTRAP |

### Осознанные отказы

| Было | Почему отказались | Альтернатива в 1.4 |
|------|-------------------|---------------------|
| Локальная копия kit обязательна | Устаревает; лишний шаг | GitHub raw URL или опциональный `@workspace_kit.md` |
| `starter_kit.md` / `workspace_kit.md` в корне проекта | Дублирование канона | Канон в GitHub; корень проекта — опциональная копия |
| `HEARTBEAT.md`, `CRON.md` | Cursor не даёт фон без Automations; риск автозапуска | Явный `session_end` + hooks audit-only |
| `/loop`, Cursor Automations | Вне scope; непредсказуемая автономность | Ручной старт чата + BOOTSTRAP |
| `agent/` как каталог | Путаница с npm-пакетами, CLI | `workspace/` |
| `workspace/skills/` как runtime | Cursor не подхватывает этот путь | `.cursor/skills/<name>/SKILL.md` + каталог `workspace/SKILLS.md` |
| Skills в корне `./skills/` | Не стандарт Cursor | `.cursor/skills/` |
| Полный `AGENTS.md` в корне | Дублирование; раздувание контекста | Корень = указатель 5–15 строк; мануал в `workspace/AGENTS.md` |
| Redirect-файлы в корне (`SOUL.md` → workspace) | Путают агента и людей | Миграция с удалением после подтверждения |
| Автоудаление при миграции | Риск потери данных | Перенос → проверка → удаление **только** после «да» |
| `workspace.yaml` / `workspace.md` как карта | Дублирование kit | Единый `workspace_kit.md` |
| Копия `workspace_kit.md` в `workspace/` | Две версии расходятся | Канон — GitHub; версия и источник в `workspace/INDEX.md` |
| Авто-cron / Automations для kit-sync | Непредсказуемость; риск push без согласия | Ручной ритуал: `sync --dry-run` → согласование → pull / push |
| Push в репозиторий kit из пилота | Нарушение владения; инцидент SKL-012 | Пилот → learnings + issues; релиз manifest — только из **проекта kit** |
| Имя `pilot-sync/` (legacy) | Дублирует kit-sync | Канон с 1.9: **`kit-sync/`**; pull пробует оба пути при 404 |

### Kit-sync — обмен пилот ↔ kit

**Kit-sync** — одно имя протокола: pull (обновления kit) и push (learnings → issues).  
Не путать с CRM-sync, indexing-sync и session memory.

#### Имена (один протокол)

| Форма | Где | Зачем |
|-------|-----|-------|
| **kit-sync** | Документация | Имя протокола |
| **`kit-sync/`** | Репозиторий kit | Релиз: manifest + artifacts |
| **`kit_sync.py`** | Пилот | CLI (snake_case — Python) |
| **`/kit-sync`** | `.cursor/commands/` | Pull, status, dry-run |
| **`/kit-submit`** | `.cursor/commands/` | Push learnings — направление push того же kit-sync |
| **`kit_sync_state.json`** | Пилот | State inbound/outbound |

Legacy: каталог **`pilot-sync/`** — старое имя; при pull сначала `kit-sync/manifest.json`, при 404 — `pilot-sync/manifest.json`.

#### Роли

| Роль | Что это | Владение |
|------|---------|----------|
| **Server (канон)** | `https://github.com/riantdrew/workspace_kit` | `workspace_kit.md`, `kit-sync/`, релизы manifest |
| **Client (пилот)** | Любой проект с `workspace/` | `workspace/starter-kit-learnings.md`, локальные скрипты sync, issues outbound |

```
Пилот (client)                         Сервер kit
     │                                      │
     │  push: аноним. issues (gh)           │
     ├─────────────────────────────────────►│  мейнтейнер обрабатывает
     │                                      │  публикует kit-sync/manifest.json
     │  pull: manifest + artifacts          │
     │◄─────────────────────────────────────┤
     │  kit_sync.py pull                    │
```

#### Server-side (только репозиторий kit)

| Путь | Назначение |
|------|------------|
| `kit-sync/manifest.json` | Версия kit, список артефактов, sha256, `stage_min` |
| `kit-sync/artifacts/` | Файлы для pull в пилоты (скрипты, rules, commands) |
| `scripts/kit_sync_manifest.py` | Сборка manifest после релиза — **только у мейнтейнера kit** |

**MUST NOT** создавать или пушить `kit-sync/` из пилотного проекта — только релиз из kit repo после обработки issues.

#### Client-side (пилот, стадия 3+)

| Путь | Назначение |
|------|------------|
| `workspace/starter-kit-learnings.md` | Единственный журнал выводов для kit (backlog + SKL-журнал) |
| `scripts/kit_common.py` | Константы, protected paths, анонимизация, state |
| `scripts/kit_sync.py` | `status`, `pull`, `push`, `sync` |
| `scripts/kit_learning_issue.py` | Создание issues из learnings |
| `data/kit_sync_state.json` | `pilot_fingerprint`, `inbound.applied`, `outbound.submitted` |
| `.cursor/commands/kit-sync.md` | `/kit-sync` — pull, status |
| `.cursor/commands/kit-submit.md` | `/kit-submit` — push (kit-sync) |
| `.cursor/rules/starter-kit-learnings.mdc` | Rule на globs (не `alwaysApply`) |

Артефакты client-side **приходят pull'ом** с сервера kit — не копировать вручную из чужого репо.

#### Pull (server → пилот)

Обновления kit в пилот без auth (публичный raw GitHub).

```bash
python3 scripts/kit_sync.py status
python3 scripts/kit_sync.py pull [--dry-run] [--force]
```

| Шаг | Действие |
|-----|----------|
| 1 | Загрузить `kit-sync/manifest.json` (fallback: legacy `pilot-sync/manifest.json`) |
| 2 | Сверить `kit_version` с `workspace/INDEX.md` → `starter_kit_version` |
| 3 | Для каждого артефакта: проверить `sha256`, `stage_min`, `mode` |
| 4 | Пропустить [protected paths](#protected-paths-при-pull) |
| 5 | Бэкап перед перезаписью → `workspace/reports/kit-backups/{version}/` |
| 6 | Отчёт → `workspace/reports/kit-pull-*.md` |
| 7 | Обновить `starter_kit_version` и `data/kit_sync_state.json` → `inbound` |

**Режимы артефакта (`mode`):**

| mode | Поведение |
|------|-----------|
| `kit_managed` | Kit перезаписывает файл (с бэкапом) |
| `skip_if_exists` | Не трогать, если файл уже есть в пилоте |

**Fallback без manifest:** сверка только `workspace_kit.md` на GitHub; снимок в `workspace/reports/kit-remote-workspace_kit.md`.

##### Protected paths при pull

**MUST NOT** перезаписывать при pull — только проектный контент:

- `workspace/SOUL.md`, `USER.md`, `GOALS.md`, `MEMORY.md`, `CONSTITUTION.md`, `AUTONOMY.md`, `BOOTSTRAP.md`, `PROJECT.md`
- `workspace/knowledge/domain/`
- `.cursor/rules/constitution-enforce.mdc`, `agent-knowledge.mdc`, `security-git.mdc`, `workspace-isolation.mdc`, `workspace-read.mdc`
- `.env`

#### Push (пилот → server)

Опыт пилота → issues в kit repo. **Только по явной просьбе пользователя.**

```bash
python3 scripts/kit_sync.py push --list      # что готово
python3 scripts/kit_sync.py push --ready     # создать issues
```

| Требование | Детали |
|------------|--------|
| Auth | `gh auth login` |
| Labels | `kit-learning`, `from-pilot`, `anonymized` |
| Дедуп | `data/kit_sync_state.json` → `outbound.submitted` |
| Одна issue | На каждый `SKL-NNN` со статусом `ready_for_kit` |
| Анонимизация | `pilot_fingerprint` — анонимный ID пилота, не имя протокола |

**MUST NOT:** коммиты, push, PR или API-правки репозитория kit из пилота.

#### Полный цикл (ручной ритуал)

Без cron и Automations — осознанный cadence:

```bash
python3 scripts/kit_sync.py sync --dry-run   # еженедельно или перед релизом
# → согласование с владельцем → pull (apply) → push --ready (если есть ready_for_kit)
```

| Команда | Auth | Когда |
|---------|------|-------|
| `status` | — | Проверить версии local / manifest / remote |
| `pull --dry-run` | — | План изменений без apply |
| `pull` | — | Apply после согласия |
| `push --ready` | `gh` | Только по просьбе |
| `sync` | pull + опционально push | Полный цикл |

#### Learnings + issues

**Единственный файл** выводов по kit в пилоте: `workspace/starter-kit-learnings.md`.  
Не дублировать в BOOTSTRAP, TOOLS, MEMORY.

**Сюда:** универсальные паттерны workspace, hooks, rules, пробелы kit.  
**Не сюда:** продукт, домены, метрики, клиент, секреты.

Структура файла:

1. **Мета** — `kit_version (проект)`, `last_entry`
2. **Протокол sync** — таблица команд pull/push (кратко; детали — в этом kit)
3. **Backlog** — таблица `SKL-NNN | статус | суть` — единственная сводка «что переносить в kit»
4. **Журнал** — детали по ID; не дублировать backlog текстом

Формат записи:

```markdown
### SKL-NNN | ГГГГ-ММ-ДД — заголовок

- **Категория:** pattern | behavior | gap | anti-pattern | integration
- **Суть:** 1–2 предложения
- **Для kit:** одно конкретное изменение в workspace_kit.md
- **Статус:** draft | ready_for_kit
```

**Статусы:**

| Статус | Действие |
|--------|----------|
| `draft` | Только в пилоте |
| `ready_for_kit` | Кандидат на issue (`push --ready`) |

**Rule `starter-kit-learnings.mdc`:** `alwaysApply: false`, globs на `memory/`, `knowledge/`, hooks, learnings — порог «новый универсальный паттерн», не каждый ход.

#### Manifest (server)

Пример `kit-sync/manifest.json`:

```json
{
  "kit_version": "1.9",
  "released_at": "2026-06-19T12:00:00",
  "changelog": "Kit-sync: единое имя протокола и каталога релиза",
  "artifacts": [
    {
      "id": "kit-sync-cli",
      "src": "kit-sync/artifacts/kit_sync.py",
      "dest": "scripts/kit_sync.py",
      "sha256": "<hex>",
      "stage_min": 3,
      "mode": "kit_managed"
    }
  ]
}
```

Поля артефакта: `id`, `src`, `dest`, `sha256`, `stage_min`, `mode`.

#### Протокол мейнтейнера kit

1. Обработать issues с labels `kit-learning`, `from-pilot`
2. Внести изменения в `workspace_kit.md` и артефакты
3. Bump версии, запись в Changelog
4. `kit_sync_manifest.py` → commit `kit-sync/manifest.json` + artifacts
5. Пилоты делают `pull` — получают обновлённые скрипты и rules

При инциденте (несанкционированный push в kit main): откат main, manifest пересобрать из канона.

#### Граница пилот vs kit (обязательно)

| Пилот **может** | Пилот **не может** |
|-----------------|-------------------|
| Писать learnings | Коммитить в kit repo |
| `push --ready` → issues | Публиковать `kit-sync/` |
| `pull` артефакты | Менять labels/issues kit без просьбы |
| Предлагать diff для kit в чате | Force-push kit main |

Зафиксировать в `workspace/AUTONOMY.md` → `never`: «Push/commit в репозиторий workspace_kit из пилота».

### Протокол эволюции kit

По запросу «обнови workspace_kit» / «эволюционируй kit до X»:

1. Прочитать kit: локальный `./workspace_kit.md` (или legacy `./starter_kit.md`) **или** [канонический raw URL](#канонические-url); сверить версии по [алгоритму](#алгоритм-загрузки-и-проверки-агент). `workspace/INDEX.md` → `starter_kit_version`.
2. Сравнить с целевой версией по Changelog и [Осознанные отказы](#осознанные-отказы).
3. Показать **diff-план**: что добавить в kit, что мигрировать в проекте, что удалить.
4. Обновить `workspace_kit.md`: bump версии, запись в Changelog, новые отказы — если есть.
5. Предложить миграцию `workspace/` и kit-sync: переименования, новые rules, `kit_sync.py pull`, обновление `starter_kit_version` и `starter_kit_source`.
6. **Не** применять миграцию проекта без подтверждения.

---

## Протокол для агента

Если сработал триггер — выполни **строго по порядку**:

### 0. Источник и версия kit

Выполни [Алгоритм загрузки и проверки](#алгоритм-загрузки-и-проверки-агент).  
Выход: какой kit используется (`local` / `remote`), версия `X.Y`, результат сверки с каноном. **Файлы проекта не создавать.**

### 1. Аудит репозитория (стадия 0)

Выполни [Стадия 0 — Аудит репозитория](#стадия-0--аудит-репозитория).  
Выход: [формат отчёта аудита](#формат-отчёта-аудита). **Файлы не создавать.**

### 2. Определи стадию workspace

Пройди [Чек-лист стадий](#чек-лист-стадий) по `workspace/` и [исключениям](#исключения-вне-workspace). Запиши:

- **Стадия:** 0–5 — **максимальная**, для которой выполнены **все** обязательные пункты; иначе «N (частично)»
- **starter_kit_version** и **starter_kit_source** в `workspace/INDEX.md` — если есть; иначе «не зафиксированы»
- **Что уже есть** в `workspace/`
- **Чего не хватает** для текущей и следующей стадии
- **Расхождения:** файл есть, но пустой / без обязательных разделов
- **Миграция:** SOUL, MEMORY и т.п. в **корне** → предложить перенос в `workspace/` (см. [Миграция из корня](#миграция-из-корня))
- **Конфликты:** полный `AGENTS.md` в корне, дубли rules, legacy `agent/`

### 3. Задай обязательные вопросы

Только блок [Обязательные вопросы](#обязательные-вопросы-по-стадиям) для перехода **текущая → следующая** стадия.  
Не задавай вопросы следующих переходов, пока не закрыт текущий — кроме «сразу всё».

Если ответ уже в репо или чате — не спрашивай, процитируй.

Уточни **профиль:** solo или team — если неочевидно из репо.

### 4. Дай рекомендации

- Что создать на **следующей** стадии (имена, без дублирования [Каталог файлов](#каталог-файлов))
- Что повесить на `.cursor/` (rules, hooks, skills) — [Интеграции Cursor](#интеграции-cursor)
- Что **не** коммитить; что не дублировать из README / docs
- Лимит: **≤8 файлов** за итерацию; порядок создания

### 5. Обнови проект (только после согласия)

- Создавай файлы с **заголовками обязательных разделов** и содержимым из ответов пользователя
- Шаблоны — [Шаблоны](#шаблоны-разделов)
- **Создание по шаблону на стадии N** = разрешено; **правка содержимого после** — по правилам «кто редактирует» в каталоге
- Защищённые файлы (правка содержимого только по явной команде): `workspace/SOUL.md`, `workspace/CONSTITUTION.md`, `workspace/AUTONOMY.md`, `workspace/BOOTSTRAP.md`, `workspace/USER.md`, `workspace/examples/`
- `workspace/AGENTS.md`: **создать** по шаблону на стадии 2 = да; менять процедуры потом — только по запросу
- **Автономная эволюция** (в `session_end`): `workspace/memory/`, `workspace/MEMORY.md`, `workspace/GOALS.md`, `workspace/knowledge/` (черновики)
- Новые workspace-файлы — только в `workspace/`, кроме [исключений](#исключения-вне-workspace)
- При создании `workspace/INDEX.md` — записать `starter_kit_version: "1.9"` и `starter_kit_source: "local"` или `"remote"`

### 6. Верификация

Пройди [Верификация после создания](#верификация-после-создания). Сообщи расхождения.

### 7. Закрой итерацию

Формат:

1. **Kit:** источник (`local`/`remote`), версия, результат сверки с каноном
2. **Стадия** (текущая / частично)
3. **Сделано** в этой итерации
4. **Осталось** до следующей стадии
5. **Одно** следующее действие для пользователя

---

## Anti-patterns для агента

| Нельзя | Почему | Вместо |
|--------|--------|--------|
| Сканировать `node_modules`, `vendor`, `.git`, `dist`, `build` | Перегрузка контекста | Алгоритм выборочного аудита |
| Копировать README в `workspace/PROJECT.md` | Дублирование | Ссылки + 5–10 строк резюме |
| Создать все стадии 1–4 за один проход | Нет валидации | ≤8 файлов, по стадиям |
| Положить SKILL.md в `workspace/skills/` как runtime | Cursor не подхватит | `.cursor/skills/<name>/SKILL.md` |
| Rule на 200 строк | Раздувает каждый чат | ≤50 строк; детали в workspace |
| Rule со ссылками на GOALS/MEMORY до стадии 2 | Битые ссылки | Staged rules: см. ниже |
| Удалить legacy-файлы из корня без спроса | Потеря данных | Перенос → подтверждение → удаление |
| Выдумать API, env, контакты | Ложная память | `TODO` или вопрос пользователю |
| Игнорировать более свежий kit на GitHub | Устаревшие инструкции | [Алгоритм загрузки и проверки](#алгоритм-загрузки-и-проверки-агент) |
| Коммит без запроса | Риск для пользователя | Только по явной команде |
| Push/commit в репозиторий workspace_kit из пилота | Нарушение владения kit | Learnings + `push --ready` → issues; `kit-sync/` — только из kit repo |
| Дублировать выводы по kit в BOOTSTRAP/TOOLS/MEMORY | Шум; рассинхрон | Только `workspace/starter-kit-learnings.md` |
| Push learnings без анонимизации | Утечка домена/секретов | `pilot_fingerprint`, redact, labels `anonymized` |

---

## Стадия 0 — Аудит репозитория

**Цель:** понять, что уже есть. **Не создавать и не менять файлы.**

### Алгоритм аудита (без перегрузки контекста)

1. **Корень:** список файлов и папок **верхнего уровня** (один уровень, без рекурсии).
2. **Манифесты:** прочитать только найденные — `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `composer.json`, `Gemfile`, `pom.xml`, `build.gradle`, `Makefile`, `docker-compose.yml`.
3. **Документация:** `README.md`, `CONTRIBUTING.md`, `docs/` — **только** индекс (список файлов) + README целиком.
4. **Cursor:** `.cursor/rules/`, `.cursor/hooks.json`, `.cursor/skills/`, `.cursorignore` — список и краткое содержимое.
5. **CI/CD:** `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` — имена файлов + первая строка/название job.
6. **Безопасность:** проверить, нет ли в git `.env`, `*.pem`, `id_rsa`, `credentials.json` (по `.gitignore` и top-level именам).
7. **Legacy agent:** искать в **корне** (не рекурсия): `SOUL.md`, `MEMORY.md`, `GOALS.md`, `AGENTS.md`, `agent/`, `workspace/` — фиксировать содержимое/размер.
8. **Monorepo:** если есть `apps/`, `packages/`, `services/` — отметить; не обходить рекурсивно.

**Не читать** каталоги из `.gitignore` и типичные артефакты: `node_modules`, `vendor`, `.git`, `dist`, `build`, `target`, `__pycache__`, `.next`, `coverage`.

**Пустой репозиторий:** стадия 0 всё равно выполняется; в отчёте — «greenfield, стек не определён».

### Формат отчёта аудита

```markdown
## Отчёт аудита (стадия 0)

**Репозиторий:** <имя / greenfield>
**Профиль (предположение):** solo | team
**Размер (оценка):** малый | средний | крупный | монорепо

### Найдено
| Область | Есть | Действие |
|---------|------|----------|
| README / docs | … | не дублировать / … |
| .cursor/rules | … | дополнить / не трогать |
| Legacy agent-файлы в корне | … | мигрировать в workspace/ |
| Секреты в git | да/нет | … |

### Риски
- …

### Рекомендация
Следующая стадия workspace: **N**; переход **N → N+1**.
```

---

## Зачем этот набор файлов

ИИ в Cursor **не помнит** прошлые чаты. Каждый новый чат — «чистый лист», кроме:

- rules, skills, hooks — подставляет IDE;
- файлов в репозитории, прочитанных по BOOTSTRAP.

**Agent workspace** — слой markdown в **`workspace/`**, отдельно от исходников:

1. **Фиксирует** личность, законы, цели и память между сессиями.
2. **Разделяет** «кто агент», «что делать», «что помнить», «чем пользоваться».
3. **Ограничивает** риски (prod, секреты, автономность).
4. **Даёт агенту** опору для развития документации — в разрешённых файлах.
5. **Не смешивается** с `src/`, `docs/` продукта — только ссылками.

README — для людей; `.cursor/rules/` — жёсткие ограничения IDE; `workspace/` — живой контекст агента.

---

## Директория `workspace/`

Все markdown workspace — в **`workspace/`**. Корень — код продукта и [минимальные исключения](#исключения-вне-workspace).

### Дерево

```
workspace_kit.md              # опционально в корне вашего проекта (@workspace_kit.md)
                            # legacy: starter_kit.md (@starter_kit.md)
                            # канон: GitHub raw URL — см. «Источники загрузки kit»

workspace/
├── INDEX.md                # карта + starter_kit_version, starter_kit_source (стадия 4+)
├── BOOTSTRAP.md
├── SOUL.md
├── USER.md                 # solo: опционально в git; team: см. USER.example.md
├── GOALS.md
├── PROJECT.md
├── AGENTS.md               # полный операционный мануал
├── AUTONOMY.md
├── CONSTITUTION.md
├── CONVENTIONS.md
├── MEMORY.md
├── memory/                 # YYYY-MM-DD.md
├── knowledge/
│   ├── INDEX.md
│   ├── domain/
│   ├── runbooks/
│   ├── faq/
│   └── references/
├── SKILLS.md               # каталог → .cursor/skills/
├── TOOLS.md
├── ENV.md
├── PLAYBOOK.md
├── starter-kit-learnings.md  # стадия 3+: learnings для kit-sync push
├── examples/               # good.md, bad.md (опционально)
├── STYLE.md                # опционально
├── IDENTITY.md             # опционально
└── CONTACTS.md             # опционально

.cursor/                    # конфиг Cursor — НЕ в workspace/
├── rules/
├── hooks/
├── skills/                 # проектные SKILL.md (Cursor подхватывает отсюда)
└── commands/

AGENTS.md                   # КОРЕНЬ: указатель 5–15 строк → workspace/
```

### Исключения вне `workspace/`

| Путь | Зачем не в `workspace/` |
|------|-------------------------|
| `.cursor/rules/*.mdc` | Cursor читает только этот путь |
| `.cursor/hooks.json` | API hooks фиксирован |
| `.cursor/skills/<name>/SKILL.md` | Cursor подхватывает skills отсюда |
| `.cursor/commands/*.md` | Cursor slash-commands |
| `AGENTS.md` (корень) | Cursor ищет в корне — **короткий указатель** |
| `workspace_kit.md` (корень проекта) | Опционально: `@workspace_kit.md`; legacy: `starter_kit.md`; канон — GitHub raw |

### Корневой `AGENTS.md` — только указатель

Если в корне уже есть **полный** `AGENTS.md` (>20 строк, процедуры, роли):

1. Предложить перенести содержимое в `workspace/AGENTS.md`
2. Заменить корневой на указатель (шаблон ниже)
3. Только после подтверждения

### Правила путей для агента

- Markdown workspace — **только** `workspace/`
- Skills runtime — **только** `.cursor/skills/`
- Каталог skills для людей — `workspace/SKILLS.md` (пути на `.cursor/skills/`)
- Не класть workspace в `docs/`, `src/`, `.cursor/rules/`

### Миграция из корня

Если `SOUL.md`, `MEMORY.md` и т.п. в корне:

1. Скопировать содержимое в `workspace/<имя>.md`
2. Показать diff пользователю
3. Удалить из корня **только после «да»**
4. Обновить rules/hooks на префикс `workspace/`

### `.cursorignore` (рекомендуется для крупных репо)

При аудите крупного репо предложить дополнения в `.cursorignore`:

```
node_modules/
vendor/
dist/
build/
.git/
*.min.js
coverage/
```

Цель: агент не тратит контекст на артефакты. **Не** скрывать `workspace/`, `.cursor/`, исходники продукта.

---

## Профили: solo и team

| Аспект | solo | team |
|--------|------|------|
| `workspace/USER.md` | Коммитить или локально | Часто в `.gitignore` |
| Шаблон | — | `workspace/USER.example.md` в git |
| `workspace/memory/` | По желанию в git | Обычно в `.gitignore` |
| `workspace/GOALS.md` | Коммитить | Коммитить (shared) |
| `workspace/MEMORY.md` | По желанию | Коммитить (shared выводы) |
| `workspace/CONSTITUTION.md` | Коммитить | Коммитить |

Агент определяет профиль: один автор в git → solo; `CODEOWNERS`, несколько контрибьюторов → team.

---

## Принципы

### 1. Один факт — одно место

| Тип информации | Где хранить |
|----------------|-------------|
| Жёсткий запрет | `.cursor/rules/` + `workspace/AUTONOMY.md` |
| Архитектура и безопасность | `workspace/CONSTITUTION.md` |
| Текущие приоритеты | `workspace/GOALS.md` |
| Долгосрочные выводы | `workspace/MEMORY.md` |
| Сырьё за день | `workspace/memory/YYYY-MM-DD.md` |
| Регламенты, FAQ | `workspace/knowledge/` |
| Onboarding продукта | `workspace/PROJECT.md` |
| Профиль человека | `workspace/USER.md` |
| Процедуры skills | `.cursor/skills/` + индекс `workspace/SKILLS.md` |
| Код продукта | `src/`, `docs/` — не дублировать |

### 2. Короткое в rules, длинное в markdown

Rules — ≤50 строк. CONSTITUTION, CONVENTIONS — контекст.

### 3. Приоритет при конфликте

1. `.cursor/rules/`
2. `workspace/CONSTITUTION.md`
3. `workspace/AUTONOMY.md`
4. `workspace/GOALS.md`
5. `workspace/AGENTS.md`
6. `workspace/MEMORY.md`
7. `workspace/SOUL.md`

### 4. Сессия в Cursor

- **Новый чат** → `session_start` из `workspace/BOOTSTRAP.md`
- **Конец** → явная фраза «завершаем сессию» → `session_end`
- Cursor **не** шлёт «сессия закончилась» — без команды `workspace/memory/` не обновится

### 5. Автономность документов

**Без отдельного «да»** в `session_end`: `workspace/memory/`, `workspace/MEMORY.md`, `workspace/GOALS.md` (мелкие правки), `workspace/knowledge/` (draft).

**Только по явной команде** (после первичного создания): `SOUL`, `CONSTITUTION`, `AUTONOMY`, `BOOTSTRAP`, `USER`, `examples/`. `AGENTS.md` — процедуры по запросу; создание по шаблону на стадии 2 — разрешено.

### 6. Стадия 5 = режим поддержки

Стадия 5 — не цель первого запуска. Это ongoing: актуальные GOALS, свежая memory, review knowledge.

---

## Каталог файлов

Пути относительно `workspace/`, если не указано иное.

### Ядро

#### `workspace/SOUL.md`
**Назначение:** ценности, этика, принципы, жёсткие «нет».  
**Разделы:** `identity`, `values`, `boundaries`, `decision_principles`  
**Редактирует:** человек (агент — по явной команде)

#### `workspace/STYLE.md` *(опционально, стадия 4+)*
**Разделы:** `language`, `tone`, `response_format`, `anti_patterns`

#### `workspace/IDENTITY.md` *(опционально, стадия 4+)*
**Разделы:** `name`, `role`, `avatar`, `tagline`

### Человек и контекст

#### `workspace/USER.md`
**Разделы:** `profile`, `communication`, `expertise`, `preferences`, `availability`  
**Team:** коммитить `USER.example.md`; личный `USER.md` — в `.gitignore`

#### `workspace/PROJECT.md`
**Разделы:** `overview`, `audience`, `stack`, `repositories`, `key_entities`  
**Ограничения:** без секретов; ссылки на README

#### `workspace/GOALS.md`
**Разделы:** `period`, `priorities`, `out_of_scope`, `success_criteria`

### Операции

#### `workspace/BOOTSTRAP.md`
**Разделы:** `session_start`, `session_end`, `before_destructive_action`

#### `workspace/AGENTS.md`
**Разделы:** `roles`, `responsibilities`, `limitations`, `workflows`, `escalation`  
**Создание** по шаблону стадии 2 — агент; **правки** процедур — человек или по запросу

#### `workspace/AUTONOMY.md`
**Разделы:** `always_allowed`, `ask_first`, `never`, `environments`  
**Kit-sync:** в `never` — push/commit в репозиторий workspace_kit из пилота

#### `workspace/starter-kit-learnings.md` *(стадия 3+, kit-sync)*
**Назначение:** единственный журнал универсальных выводов для kit; backlog SKL + журнал.  
**Разделы:** мета, протокол sync (кратко), backlog, журнал  
**Редактирует:** агент (новые паттерны); outbound — только `push --ready` по просьбе  
**Ограничения:** без домена, секретов, продуктовых метрик; см. [Kit-sync](#kit-sync--обмен-пилот--kit)

#### `workspace/PLAYBOOK.md` *(стадия 4+)*
**Разделы:** `scenarios`

### Законы

#### `workspace/CONSTITUTION.md`
**Разделы:** `architecture`, `security`, `global_bans`, `data_handling`

#### `workspace/CONVENTIONS.md` *(стадия 3+)*
**Разделы:** `naming`, `structure`, `commits`, `testing`

### Память

#### `workspace/MEMORY.md`
**Разделы:** `decisions`, `client_context`, `lessons_learned`, `do_not_repeat`  
**Ограничения:** `[устарело ДД.ММ.ГГГГ]`; <150 строк; без секретов

#### `workspace/memory/`
**Имена:** `YYYY-MM-DD.md` — разделы: `done`, `in_progress`, `blockers`, `notes`

### Навыки и инфраструктура

#### `workspace/SKILLS.md` *(стадия 3+)*
**Разделы:** `skills` (таблица: имя, триггер, путь к `.cursor/skills/`), `conflict_resolution`

#### `.cursor/skills/<name>/SKILL.md` *(стадия 3+)*
**Назначение:** runtime skill для Cursor.  
**Индекс** в `workspace/SKILLS.md`. Приоритет над глобальными — проектный выше.

#### `workspace/TOOLS.md` *(стадия 3+)*
**Разделы:** `apis`, `databases`, `servers`, `cli`, `mcp`

#### `workspace/ENV.md` *(стадия 3+)*
**Разделы:** `modes`, `variables`, `secrets_policy`

### Знания

#### `workspace/knowledge/`
**Обязательно:** `INDEX.md`. Подкаталоги: `domain/`, `runbooks/`, `faq/`, `references/`  
**На странице:** `title`, `updated`, `source`, `status`, `content`

#### `workspace/examples/` *(опционально)*
**Файлы:** `good.md`, `bad.md`

### Мета

#### `workspace/INDEX.md` *(стадия 4+)*
**Разделы:** `starter_kit_version`, `starter_kit_source`, `workspace_stage`, `files`, `editable_by_agent`, `integrations`

#### `workspace/CONTACTS.md` *(опционально)*
**Разделы:** `contacts`

---

## Интеграции Cursor

Rules, hooks, skills и commands — механизмы **Cursor IDE**. Kit описывает концепцию и даёт шаблоны для `.cursor/`.

### Staged integrations

| Стадия | Rules | Hooks | Skills | Commands |
|--------|-------|-------|--------|----------|
| **1** | Безопасность + изоляция | — | — | — |
| **2** | + Чтение GOALS/MEMORY + конституция | sessionStart | — | session-end |
| **3** | + Конвенции языка | + check secrets/shell | ≥1 skill | kit-sync, kit-submit |
| **4** | — | + afterFileEdit, stop | полный | полный набор |

**Стадия 1:** правила **без** ссылок на GOALS/MEMORY (их ещё нет).  
**Стадия 2:** добавить правило с GOALS/MEMORY.

### `.cursor/` — структура

| Компонент | Путь | Формат |
|-----------|------|--------|
| Rules | `.cursor/rules/` | `.mdc` (YAML frontmatter + Markdown) |
| Hooks | `.cursor/hooks.json` + `.cursor/hooks/` | JSON + shell/python |
| Skills | `.cursor/skills/<name>/SKILL.md` | Markdown + frontmatter |
| Commands | `.cursor/commands/*.md` | Markdown |

#### `.cursor/rules/` — шаблоны

#### `security-git.mdc` (стадия 1)

```markdown
---
description: Безопасность git и секретов
alwaysApply: true
---

# Security & Git

- Не коммить `.env`, ключи, токены, пароли, `*.pem`, `credentials.json`
- Не выполнять `git push`, `commit`, `tag` без явной просьбы пользователя
- Не `git push --force` на main/master без явной просьбы
- Не выводить секреты в чат, логи, workspace-файлы
```

#### `workspace-isolation.mdc` (стадия 1)

```markdown
---
description: Изоляция markdown агента в workspace/
alwaysApply: true
---

# Workspace isolation

- Markdown контекста агента — только в `workspace/`
- Не создавай SOUL.md, MEMORY.md, GOALS.md в корне репозитория
- Не дублируй README в workspace — используй ссылки в PROJECT.md
- Проектные skills — в `.cursor/skills/`, не в workspace/
```

#### `workspace-read.mdc` (стадия 2+)

```markdown
---
description: Читать цели и память при задачах
alwaysApply: true
---

# Workspace context

При любой нетривиальной задаче прочитай:
1. `workspace/GOALS.md` — приоритеты
2. `workspace/MEMORY.md` — долгосрочные выводы

Старт сессии: `workspace/BOOTSTRAP.md`
```

#### `constitution-enforce.mdc` (стадия 2+)

```markdown
---
description: Жёсткие запреты из CONSTITUTION
alwaysApply: true
---

# Constitution enforce

<!-- Заменить на 3–5 пунктов из workspace/CONSTITUTION.md → global_bans -->

- Не деплоить в prod без явной просьбы
- Не выполнять destructive SQL (DROP, TRUNCATE) без подтверждения
- TODO: заполнить из workspace/CONSTITUTION.md
```

#### `agent-knowledge.mdc` (стадия 3+)

```markdown
---
description: Агент отвечает сам — не просит пользователя открывать файлы
alwaysApply: true
---

# Agent knowledge first

Перед ответом на вопрос о проекте агент самостоятельно находит факты:

1. `workspace/MEMORY.md` — решения, уроки, контекст
2. `workspace/memory/` — последние 7 дней
3. `workspace/knowledge/` — по INDEX.md
4. `workspace/GOALS.md` — приоритеты (goal lens: если запрос уводит от целей — сказать)
5. `workspace/reports/` — актуальные отчёты
6. Код продукта — только если задача требует

Не просить пользователя открыть файл — процитировать суть в чате.
```

#### `goal-lens.mdc` (стадия 2+)

```markdown
---
description: Любую задачу сверять с GOALS.md
alwaysApply: true
---

# Goal lens

При любой нетривиальной задаче:
1. Прочитай `workspace/GOALS.md`.
2. Если запрос уводит от приоритетов — прямо скажи и предложи альтернативу.
3. Не выполняй молча то, что противоречит целям сессии.
```

#### `starter-kit-learnings.mdc` (стадия 3+)

См. [шаблон](#cursorrulesstarter-kit-learningsmdc-стадия-3) в разделе Шаблоны. `alwaysApply: false`, globs — не каждый ход.

### Хуки — жизненный цикл сессии (стадия 2+)

События Cursor hooks:

| Событие | Триггер | Действие |
|---------|---------|----------|
| `sessionStart` | Новый чат | Снимок GOALS + MEMORY + git (+ orphan detection) |
| `sessionEnd` | Закрытие чата | Консолидация в `memory/YYYY-MM-DD.md` |
| `afterFileEdit` | Правка `workspace/` | Журнал изменений |
| `stop` / `afterResponse` | После ответа агента | Чекпоинт (auto_checkpoint) |

**Стадия 3+:** добавить проверку секретов, опасных команд. Начинать **audit-only** (fail open); deny — только для явно опасного.

#### `.cursor/hooks.json`

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [{ "command": ".cursor/hooks/session-start.sh" }],
    "sessionEnd":   [{ "command": ".cursor/hooks/session-end.sh" }],
    "afterFileEdit":[{ "command": ".cursor/hooks/after-workspace-edit.sh" }],
    "stop":         [{ "command": ".cursor/hooks/stop-checkpoint.sh" }]
  }
}
```

#### Память сессии (3 слоя, стадия 4+)

В пилотных проектах выработан трёхслойный механизм без HEARTBEAT/CRON:

1. **Журнал** (`afterFileEdit`) — каждая правка `workspace/` пишется в JSONL-журнал
2. **Чекпоинт** (`stop`) — после ответа агента: `auto_checkpoint` → `memory/YYYY-MM-DD.md`
3. **Консолидация** (`sessionEnd` или `sessionStart`) — при закрытии чата или новом чате догон orphan

Явный `session_end` не обязателен — orphan detection закрывает пробелы.  
Ручной догон: `.cursor/commands/session-end.md` → `python3 session_consolidate.py --orphans`.

Реализация: `session_memory.py` (single Python module) + shell-обёртки в hooks/.  
Этот модуль **не в workspace/** — он часть агентской инфраструктуры, распространяется как artifact kit через `kit-sync/`.

### Skills

| Уровень | Где лежит | Кто подхватывает |
|---------|-----------|------------------|
| Встроенные Cursor | `~/.cursor/skills-cursor/` | Cursor (не трогать) |
| Глобальные | `~/.cursor/skills/` | Cursor |
| **Проектные** | `.cursor/skills/<name>/SKILL.md` | Cursor |
| Каталог | `workspace/SKILLS.md` | Агент читает по необходимости |

**Стадия 3:** `workspace/SKILLS.md` + 1 проектный skill.

### Commands

| Команда | Назначение | Путь |
|---------|------------|------|
| `workspace/BOOTSTRAP.md` | Ритуал сессии | workspace |
| `workspace/GOALS.md`, `workspace/MEMORY.md` | Контекст | workspace |
| `workspace_kit.md` / GitHub URL | Внедрение / эволюция kit | корень / remote |
| session-end | Принудительная консолидация памяти | `.cursor/commands/` |
| kit-sync | Pull обновлений kit + статус; см. [Kit-sync](#kit-sync--обмен-пилот--kit) | `.cursor/commands/` |
| kit-submit | Push learnings (kit-sync); только по просьбе | `.cursor/commands/` |

**Вне scope:** `/loop`, Automations, cron.

### Прочее

| Механизм | Рекомендация |
|----------|--------------|
| Глобальные user rules | Общие привычки; проектное — USER.md + rules |
| MCP-серверы | Описать в `workspace/TOOLS.md`; конфиг — в настройках Cursor; секреты не в markdown |
| `.env.example` | `workspace/ENV.md` зеркалит **имена** |

---

## Автономное развитие документов

### Сессионная память (стадия 4+)

Трёхслойная автоматическая память без HEARTBEAT/CRON:

1. **Журнал** — каждая правка `workspace/` попадает в JSONL (хук `afterFileEdit`)
2. **Чекпоинт** — после ответа агента `auto_checkpoint` → `memory/YYYY-MM-DD.md` (хук `stop`)
3. **Консолидация** — при `sessionEnd` или новом чате (orphan detection)

Явный `session_end` не обязателен. Автоматика пишет **только** в `memory/YYYY-MM-DD.md`, не перезаписывает `MEMORY.md`. Сжатие в `MEMORY.md` — осознанный шаг агента.

Правки вне `workspace/` (код, `.cursor/`) в автожурнал не попадают — фиксировать руками в `done`.

### В конце сессии

1. `workspace/memory/YYYY-MM-DD.md` — если не было авто-записи
2. `workspace/MEMORY.md` — сжатие важного (не автоматически)
3. `workspace/GOALS.md` — при сдвиге приоритетов
4. `workspace/knowledge/` — черновики (`status: draft`, `source` обязателен)

### Запись в MEMORY.md

```
- ДД.ММ.ГГГГ: <факт>. Причина: <одна строка>.
```

Не писать: предположения, непроверенные гипотезы, секреты.  
Гипотезы — в отдельный раздел `hypotheses_and_ideas`, не в `decisions`.

### knowledge/

Факт только из кода, docs пользователя или его слов. Иначе — TODO в `workspace/memory/`.

### Предлагать, не менять самому

`SOUL`, `CONSTITUTION`, `AUTONOMY`, `BOOTSTRAP`, `USER` — diff в чате + «применить?».

---

## Внедрение по фазам

### Стадия 1 — Безопасность и каркас

**Создать:**

- [ ] `workspace/CONSTITUTION.md` (черновик)
- [ ] `workspace/AUTONOMY.md`
- [ ] `.cursor/rules/security-git.mdc` + `workspace-isolation.mdc`
- [ ] Правила изоляции workspace

**Не создавать:** SOUL, MEMORY, GOALS, knowledge, правила чтения GOALS.

---

### Стадия 2 — Минимальный workspace

**В `workspace/`:**

- [ ] `BOOTSTRAP.md`, `SOUL.md`, `USER.md`, `GOALS.md`, `AGENTS.md`, `MEMORY.md`, `PROJECT.md`
- [ ] `memory/.gitkeep` или первый лог

**В корне:**

- [ ] `AGENTS.md` — указатель

**Cursor:**

- [ ] `workspace-read.mdc`, `constitution-enforce.mdc`
- [ ] hook `sessionStart` (опционально)

**Team:** `USER.example.md`

---

### Стадия 3 — Инфраструктура и навыки

- [ ] `CONVENTIONS.md`, `TOOLS.md`, `ENV.md`, `SKILLS.md`
- [ ] `knowledge/INDEX.md`
- [ ] `starter-kit-learnings.md` + rule `starter-kit-learnings.mdc`
- [ ] `kit_sync.py`, `kit_common.py`, `kit_learning_issue.py` (pull с сервера kit или bootstrap)
- [ ] `data/kit_sync_state.json`
- [ ] commands: `kit-sync`, `kit-submit`
- [ ] ≥1 skill в `.cursor/skills/`
- [ ] hooks: секреты + shell (audit-first)
- [ ] Правила конвенций языка
- [ ] `gh auth login` — для push learnings (по просьбе)

---

### Стадия 4 — Зрелость

- [ ] `INDEX.md` (с `starter_kit_version`, `starter_kit_source`)
- [ ] `PLAYBOOK.md`
- [ ] опционально: `examples/`, `STYLE.md`, `IDENTITY.md`, `CONTACTS.md`
- [ ] hooks: afterFileEdit + stop (session memory, опционально)

---

### Стадия 5 — Поддержка (ongoing)

- [ ] `GOALS.md` → актуальный `period`
- [ ] `MEMORY.md` → чистка `[устарело]`
- [ ] `knowledge/` → review `updated`
- [ ] rules ↔ `CONSTITUTION.md` — без противоречий
- [ ] `memory/` — записи за последние 7 дней
- [ ] hooks session memory работают (journal, checkpoint, consolidate)
- [ ] `kit_sync.py sync --dry-run` → при новой версии manifest — pull после согласия
- [ ] learnings: backlog актуален; `ready_for_kit` → push по просьбе

---

## Чек-лист стадий

**Текущая стадия** = максимальная, где **все** обязательные пункты выполнены и файлы содержат обязательные разделы. Иначе: «N (частично)» — работаем с N, не объявляем N+1.

| Стадия | Условие |
|--------|---------|
| **0** | Аудит выполнен; `workspace/` нет или пуст (кроме `.gitkeep`) |
| **1** | `CONSTITUTION.md` + `AUTONOMY.md` + `security-git.mdc` + `workspace-isolation.mdc` |
| **2** | Стадия 1 + файлы стадии 2 + корневой `AGENTS.md` + `workspace-read.mdc` |
| **3** | Стадия 2 + CONVENTIONS, TOOLS, ENV, SKILLS + `knowledge/INDEX.md` + `starter-kit-learnings.md` + kit-sync scripts + ≥1 `.cursor/skills/` |
| **4** | Стадия 3 + `INDEX.md` + `PLAYBOOK.md` |
| **5** | Стадия 4 + operational: актуальный `GOALS.period` + memory за 7 дней |

---

## Обязательные вопросы по стадиям

Один блок за сообщение — только для перехода **текущая → следующая**.

### 0 → 1

1. Стек и где prod (если есть)?
2. Топ-3 действия, которые агент **никогда** не делает без спроса?
3. Коммиты в git — только по вашей команде?
4. Профиль: solo или team?

### 1 → 2

5. Как общаться (кратко/подробно, язык, «вы/ты»)?
6. Три приоритета на 2 недели и что **не** в scope?
7. Одной фразой: роль агента (SOUL)?

### 2 → 3

8. Основные API, БД, CLI (`composer test`, docker…)?
9. Имена переменных `.env` (без значений)?
10. Повторяющиеся workflow для skills (deploy, release, review)?
11. Есть `gh auth login` для отправки learnings в kit (push — только по просьбе)?

### 3 → 4

11. Типовой инцидент и первые 3 шага?
12. Нужны `examples/` для тона ответов?

### 4 → 5

13. Как часто напоминать про review GOALS и MEMORY?

---

## Верификация после создания

Для каждого созданного файла проверь:

| Проверка | OK |
|----------|-----|
| Путь верный (`workspace/` или `.cursor/`) | ☐ |
| Все обязательные разделы-подзаголовки `##` на месте | ☐ |
| Нет выдуманных фактов (только ответы пользователя / аудит) | ☐ |
| Нет секретов | ☐ |
| `CONSTITUTION` ↔ правила конституции согласованы | ☐ |
| Корневой `AGENTS.md` ≤15 строк, ссылки работают | ☐ |
| `workspace/INDEX.md` содержит `starter_kit_version` и `starter_kit_source` | ☐ |
| `starter-kit-learnings.md` есть на стадии 3+; нет дублей выводов по kit в других файлах | ☐ |
| `data/kit_sync_state.json` и kit-sync scripts на месте (стадия 3+) | ☐ |

---

## Шаблоны разделов

### `workspace/CONSTITUTION.md`

```markdown
# CONSTITUTION

## architecture
<!-- 3–7 строк: слои, модули, границы -->

## security
<!-- секреты, auth, PII -->

## global_bans
- Не деплоить в prod без явной просьбы
- …

## data_handling
<!-- бэкапы, retention -->
```

### `workspace/AUTONOMY.md`

```markdown
# AUTONOMY

## always_allowed
- Читать код и docs
- Запускать тесты в dev
- …

## ask_first
- Коммиты, push, deploy
- …

## never
- Force-push main
- Push/commit в репозиторий workspace_kit из пилотного проекта
- …

## environments
| Режим | Можно | Нельзя |
|-------|-------|--------|
| dev | … | … |
| prod | … | … |
```

### `workspace/SOUL.md`

```markdown
# SOUL

## identity
<!-- одна фраза: кто агент в проекте -->

## values
- …

## boundaries
- …

## decision_principles
- При конфликте: `.cursor/rules/` → `workspace/CONSTITUTION.md` → `workspace/knowledge/`.
- **Goal lens:** любую нетривиальную задачу сверять с `GOALS.md`. Если запрос уводит от целей — прямо сказать.
- Данные важнее интуиции: цифры только из проверенных источников.

## communication
- Обращение, тон, уровень детализации.
- Формат ответов: сначала вывод — потом детали.
- Орфография, длина, стиль. Какие anti-patterns избегать.
- Частота апдейтов при долгой работе.
```

### `workspace/USER.md`

```markdown
# USER

## profile
<!-- имя/роль опционально -->

## communication
- Язык: русский
- Тон: …
- Детализация: кратко / подробно

## expertise
- …

## preferences
- …

## availability
<!-- часовой пояс, когда отвечаете -->
```

### `workspace/USER.example.md` (team)

```markdown
# USER (пример — скопируйте в USER.md локально)

## profile
Ваше имя, роль в проекте

## communication
…
```

### `workspace/PROJECT.md`

```markdown
# PROJECT

## overview
<!-- 3–5 строк; ссылка на README -->

## audience
<!-- для кого продукт -->

## stack
<!-- из аудита / ответов -->

## repositories
<!-- monorepo / ссылки -->

## key_entities
<!-- доменные сущности -->
```

### `workspace/AGENTS.md`

```markdown
# AGENTS

## roles
| Роль | Когда |
|------|-------|
| Исполнитель | Код, тесты, docs |
| Ревьюер | По запросу |

## responsibilities
- …

## limitations
- …

## workflows
### Обычная задача
1. session_start
2. …

## escalation
- Блокер → спросить пользователя
- Prod инцидент → PLAYBOOK.md
```

### `workspace/BOOTSTRAP.md`

```markdown
# BOOTSTRAP

## session_start
1. `workspace/GOALS.md` — приоритеты (**goal lens:** сверять с ними любую задачу)
2. `workspace/MEMORY.md` + `workspace/memory/` (последние 7 дней)
3. При необходимости — `workspace/knowledge/` по INDEX.md
4. `git status`

## session_end
1. `workspace/memory/YYYY-MM-DD.md` (авто-журнал уже мог записать чекпоинт — проверить)
2. Сжать важное в `workspace/MEMORY.md` (без секретов, <150 строк)
3. `workspace/GOALS.md` — при сдвиге фокуса
4. Новый универсальный паттерн → `workspace/starter-kit-learnings.md`

## before_destructive_action
- force-push, DROP prod, массовое удаление — только по явной просьбе
- Разрушительные действия вне `workspace/` — спросить, если не было явной команды
```

### `workspace/PLAYBOOK.md` (стадия 4+)

```markdown
# PLAYBOOK

## scenarios

### <Имя сценария>

**Симптомы:**

**Шаги:**
1. …
```

### `workspace/starter-kit-learnings.md` (стадия 3+)

```markdown
# Starter Kit Learnings

Универсальные наблюдения для [workspace_kit](https://github.com/riantdrew/workspace_kit).

**Сюда:** паттерны workspace, hooks/rules/commands, пробелы kit.  
**Не сюда:** продукт, домены, метрики, секреты.

**Репозиторий kit** — правится **только в проекте kit**, по явной просьбе владельца.  
Из пилота: learnings + issues (push) — да; коммиты в kit — **нет**.

## Мета

| Поле | Значение |
|------|----------|
| kit_version (проект) | 1.9 |
| last_entry | ДД.ММ.ГГГГ |

## Протокол sync

| Направление | Команда | Auth |
|-------------|---------|------|
| Статус | `python3 scripts/kit_sync.py status` | — |
| Pull | `python3 scripts/kit_sync.py pull [--dry-run]` | — |
| Push | `python3 scripts/kit_sync.py push --ready` | `gh auth login` |

Подробности — [Kit-sync](workspace_kit.md#kit-sync--обмен-пилот--kit) в workspace_kit.md.

## Backlog для kit

| ID | Статус | Суть |
|----|--------|------|
| SKL-001 | draft | … |

## Журнал

### SKL-001 | ГГГГ-ММ-ДД — заголовок

- **Категория:** pattern
- **Суть:** …
- **Для kit:** …
- **Статус:** draft
```

### `.cursor/commands/kit-sync.md` (стадия 3+)

```markdown
# kit-sync

Kit-sync: status и pull. Протокол — `workspace/starter-kit-learnings.md` и [Kit-sync](#kit-sync--обмен-пилот--kit).

    python3 scripts/kit_sync.py status
    python3 scripts/kit_sync.py sync --dry-run

Push — `/kit-submit`. Репозиторий kit из пилота **не редактировать**.
```

### `.cursor/commands/kit-submit.md` (стадия 3+)

```markdown
# kit-submit

Push learnings (`ready_for_kit`) — **направление push** протокола kit-sync.

    python3 scripts/kit_sync.py push --list
    python3 scripts/kit_sync.py push --ready

Требует `gh auth login`. Только по явной просьбе.
```

### `.cursor/rules/starter-kit-learnings.mdc` (стадия 3+)

```markdown
---
description: Выводы по workspace_kit — только в starter-kit-learnings.md
globs: workspace/memory/**,workspace/MEMORY.md,workspace/starter-kit-learnings.md,workspace/knowledge/**,.cursor/hooks/**,.cursor/rules/**,.cursor/commands/**
alwaysApply: false
---

# Starter kit learnings

Единственный источник выводов по kit: `workspace/starter-kit-learnings.md`.

## Когда писать

Новый **универсальный** паттерн (без знания домена). Не рутинная MEMORY/GOALS.

## Запрещено

- Push/commit в репозиторий workspace_kit из пилота
- Дублировать выводы по kit в BOOTSTRAP/TOOLS/MEMORY
- Outbound с секретами, доменом, именем репо
```

### Корневой `AGENTS.md`

```markdown
# AGENTS

Контекст агента: [workspace/](workspace/).

- [workspace/BOOTSTRAP.md](workspace/BOOTSTRAP.md)
- [workspace/AGENTS.md](workspace/AGENTS.md)
- [workspace/GOALS.md](workspace/GOALS.md)
- [workspace/MEMORY.md](workspace/MEMORY.md)
```

### `workspace/GOALS.md`

```markdown
# GOALS

## period
До ДД.ММ.ГГГГ (МСК)

## priorities
1. …

## out_of_scope
- …

## success_criteria
- …

## guardrails
Что нельзя ломать ради целей:
- …
```

### `workspace/MEMORY.md`

```markdown
# MEMORY

## decisions
- ДД.ММ.ГГГГ: <факт>. Причина: <одна строка>.

## hypotheses_and_ideas
Гипотезы и идеи — **не факты**. Требуют проверки перед использованием.

## client_context

## lessons_learned

## do_not_repeat
```

### `workspace/memory/YYYY-MM-DD.md`

```markdown
# YYYY-MM-DD

## done

## in_progress

## blockers

## notes
```

### `workspace/SKILLS.md`

```markdown
# SKILLS

## skills
| Skill | Триггер | Путь |
|-------|---------|------|
| deploy | «задеплой», deploy | .cursor/skills/deploy/SKILL.md |

## conflict_resolution
Проектный skill в `.cursor/skills/` приоритетнее глобального.
```

### `workspace/INDEX.md`

```markdown
# INDEX

## starter_kit_version
1.9

## starter_kit_source
remote

## workspace_stage
4

## files
| Файл | Назначение |
|------|------------|
| GOALS.md | Приоритеты |

## editable_by_agent
- memory/, MEMORY.md, GOALS.md (мелкие), knowledge/ (draft)

## integrations
- rules: security, isolation, workspace-read, constitution-enforce, agent-knowledge
- hooks: sessionStart, sessionEnd, afterFileEdit, stop
- skills: .cursor/skills/
```

### `.cursor/skills/deploy/SKILL.md` (пример)

```markdown
---
name: deploy
description: Деплой проекта. Use when user asks to deploy or release.
---

# Deploy

1. Проверить workspace/ENV.md → режим
2. …
```

---

## Git

### Solo

| Путь | Коммитить |
|------|-----------|
| `workspace/` (CONSTITUTION, AUTONOMY, AGENTS, BOOTSTRAP, PROJECT, CONVENTIONS…) | Да |
| `workspace/GOALS`, `MEMORY`, `memory/`, `knowledge/` | По желанию |
| `workspace/USER.md` | Да или локально |
| `.cursor/rules/`, `.cursor/skills/` | Да |
| Корневой `AGENTS.md` | Да |
| `workspace_kit.md` (локальная копия) | По желанию — канон на GitHub |
| `data/kit_sync_state.json` | Да (без секретов; только fingerprint и hashes) |

### Team

| Путь | Коммитить |
|------|-----------|
| Shared workspace (без личного USER) | Да |
| `workspace/USER.md` | Нет → `.gitignore` |
| `workspace/memory/*.md` | Обычно нет |
| `USER.example.md` | Да |

**`.gitignore` (опционально):**

```
workspace/USER.md
workspace/memory/*.md
```

---

## Не-git проекты

Если репозитория нет:

- Kit всё равно загружается с [GitHub](#канонические-url) — git в **вашем** проекте не нужен
- Аудит = структура папок на диске
- Пропустить шаги про git в BOOTSTRAP и security-git (оставить запрос на коммит «на будущее»)
- Стадии и `workspace/` — те же

---

*Конец workspace_kit v1.9*
