# workspace_kit — внедрение Workspace Kit в существующий проект

**Версия kit:** 1.13  
**Дата:** 19.06.2026  
**Схема workspace:** 1.5 (совместима с ≥ 1.0)  
**Профиль по умолчанию:** team — см. [Профили: team](#профили-team) (solo: [сноска](#solo-сноска))  
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
10. **MUST NOT** включать HEARTBEAT, CRON, `/loop` и произвольные Automations — вне scope kit; **исключение:** [еженедельный kit-exchange](#еженедельный-kit-exchange-cursor-automation) (стадия 3+).

**Триггеры запуска:** `@workspace_kit.md`, `@starter_kit.md` (legacy), ссылка на GitHub-репозиторий kit, raw URL `workspace_kit.md`, «помоги с workspace / Workspace Kit», «внедри Workspace Kit», «обнови kit», «накати новую версию kit», «мигрируй workspace» (legacy: «внедри agent workspace»).

---

## Быстрый старт

### Для человека

**Вариант A — без локального файла (рекомендуется):**

1. Чат: вставьте ссылку на репозиторий — https://github.com/riantdrew/workspace_kit — и напишите «помоги внедрить Workspace Kit».
2. Агент подтянет актуальный `workspace_kit.md` с GitHub и сверит версию, если локальная копия уже есть.
3. Ответьте на вопросы перехода **0 → 1**.
4. Подтвердите создание файлов стадии 1 (и 2, если готовы).
5. Новый чат: `@workspace/BOOTSTRAP.md` — рабочая сессия; в конце — «завершаем сессию».

**Вариант B — локальная копия:**

1. Положите `workspace_kit.md` в **корень** проекта (или обновите из [канонического репозитория](#источники-загрузки-kit)). Legacy-имя `starter_kit.md` тоже принимается.
2. Чат: `@workspace_kit.md помоги внедрить Workspace Kit`.
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
| Ссылка на репозиторий | `https://github.com/riantdrew/workspace_kit — внедри Workspace Kit` |
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
| **1.13** | 19.06.2026 | **Миграция через агента:** вопросы, diff-план, безопасный merge; без жёстких скриптов; ветки по версиям INDEX |
| **1.12** | 19.06.2026 | **Team-first:** `workspace/<login>/`, local/cloud; **workspace-sync**; kit-exchange B fix; skill `gh-workspace` |
| **1.11** | 19.06.2026 | Еженедельный **kit-exchange** (Cursor Automation + GitHub MCP): kit↔проект автоматически |
| **1.10** | 19.06.2026 | Обратная связь только через **GitHub Issues + MCP**; убраны kit-sync, manifest, Python-скрипты, модель «пилот» |
| **1.9** | 19.06.2026 | ~~Kit-sync~~ — отменено в 1.10 | Единое имя **kit-sync** (каталог релиза и протокол); legacy `pilot-sync/`; таблица имён |
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
| `/loop`, произвольные Automations | Непредсказуемая автономность | Только [kit-exchange](#еженедельный-kit-exchange-cursor-automation) по расписанию |
| `agent/` как каталог | Путаница с npm-пакетами, CLI | `workspace/` |
| `workspace/skills/` как runtime | Cursor не подхватывает этот путь | `.cursor/skills/<name>/SKILL.md` + каталог `workspace/SKILLS.md` |
| Skills в корне `./skills/` | Не стандарт Cursor | `.cursor/skills/` |
| Полный `AGENTS.md` в корне | Дублирование; раздувание контекста | Корень = указатель 5–15 строк; мануал в `workspace/AGENTS.md` |
| Redirect-файлы в корне (`SOUL.md` → workspace) | Путают агента и людей | Миграция с удалением после подтверждения |
| Автоудаление при миграции | Риск потери данных | Перенос → проверка → удаление **только** после «да» |
| `workspace.yaml` / `workspace.md` как карта | Дублирование kit | Единый `workspace_kit.md` |
| Копия `workspace_kit.md` в `workspace/` | Две версии расходятся | Канон — GitHub; версия и источник в `workspace/INDEX.md` |
| Произвольный cron / push в kit | Риск без контроля | Только **kit-exchange** Automation (≥1 раз/нед) + GitHub MCP |
| Push/commit в workspace_kit из другого prod-проекта | Нарушение границ | Issues через MCP; правки kit — только в репозитории kit по просьбе |
| Python `kit_sync.py`, manifest, `kit-sync/` | Дублирует GitHub; лишний код | `get_file_contents` + issues через **GitHub MCP** |
| Роль «пилот», pilot-sync, SKL-журнал | Неверная модель; все проекты боевые | MEMORY/reports локально; в kit — issues по просьбе |
| USER/memory в корне `workspace/` (team) | Конфликты PR между коллегами | `workspace/<login>/USER.md`, `<login>/memory/` |
| workspace-sync в repo workspace_kit | Путаница протоколов | Issues **своего** repo; kit — только kit-exchange |
| Login в shared INDEX.md | Перезапись между коллегами | `data/workspace_user` (gitignore) |

### Sync-протоколы: local/cloud и kit-exchange

**Константа team:** команда 2+, **приватный** общий репозиторий.

| Слой | Где | Что |
|------|-----|-----|
| **Local (git)** | `workspace/` shared + `.cursor/` | GOALS, MEMORY, knowledge, законы; настройки агента **общие** |
| **Local personal** | `workspace/<github-login>/` | USER.md (git); memory/ (gitignore) |
| **Cloud** | GitHub Issues **своего** repo | Задачи, планы, обсуждение — [workspace-sync](#workspace-sync-issues-своего-repo) |
| **Kit (внешний)** | `riantdrew/workspace_kit` | [kit-exchange](#kit-exchange-cursor-automation) |

**Login (локально, не в INDEX.md):** `gh auth status` → `data/workspace_user` → спросить один раз.

#### GOALS vs Issues

- **GOALS.md** — индекс периода (5–15 строк): приоритеты, out_of_scope, ссылки `#N` на Issues
- **Issues** — исполняемое; текст **для людей** (инфостиль); техника — ссылкой на файлы `workspace/`

#### memory vs MEMORY

- `workspace/<login>/memory/` — сырьё сессий (gitignore); hooks пишут сюда
- **MEMORY.md** — проверенные **командные** факты; перенос явно (закрытие issue, «зафиксируй в MEMORY»)

### Обратная связь и эволюция kit (GitHub Issues + MCP)

Любой проект с `workspace/` — **автономный боевой** репозиторий. Отдельной роли «пилот» нет.

**Канон kit:** https://github.com/riantdrew/workspace_kit — открытый репозиторий.  
Issues публичны: читать и создавать может любой участник GitHub.

#### Два направления

| Направление | Кто | Как |
|-------------|-----|-----|
| **Kit → проект** | Агент (еженедельно или по `/kit-exchange`) | GitHub MCP: `get_file_contents` → `workspace_kit.md`; сверить версию; обновить `.cursor/` и `INDEX.md` |
| **Проект → kit** | Агент (еженедельно или по `/kit-exchange`) | GitHub MCP: `search_issues` → comment; иначе `issue_write` (create). **Без Python-скриптов** |

#### Что накапливается локально

Уроки и идеи — в `MEMORY.md`, `workspace/<login>/memory/`, `workspace/reports/`, `knowledge/`.  
При **kit-exchange** агент собирает универсальное для feedback в kit (см. [B-шаг](#протокол-одного-прогона-kit-exchange) — режимы Automation vs ручной).

**В issues kit:** переносимые паттерны workspace/Cursor (hooks, rules, стадии, пробелы kit).  
**Не в issues:** домен продукта, секреты, внутренние URL, клиенты, бизнес-метрики.

#### Алгоритм агента (проект → kit)

1. **Поиск:** `search_issues` в `riantdrew/workspace_kit` — тема, ключевые слова.
2. **Issue уже есть** и ваш пункт дополняет обсуждение → `add_issue_comment` (**не** создавать дубликат).
3. **Решено не делать** (closed `not_planned`, явный отказ в комментариях) → **не** предлагать снова; при необходимости сослаться на issue.
4. **Новый пробел или прошлая реализация неверна** → `issue_write` (create) с конкретным предложением для `workspace_kit.md`.
5. **Анонимизация:** убрать `/Users/...`, prod URL, токены, email, имя репозитория проекта; описать паттерн обобщённо.
6. **Коммиты в kit** — только когда вы явно работаете **в репозитории workspace_kit** или просите PR в kit.

#### Алгоритм агента (kit → проект)

1. `get_file_contents` / raw URL → `workspace_kit.md`.
2. Сравнить версию kit с `workspace/INDEX.md` → `starter_kit_version`.
3. Diff-план: новые rules, hooks, разделы workspace. Если разрыв версий **≥ 1 minor** или есть legacy (kit-sync, flat USER/memory) — [миграция через агента](#миграция-проекта-при-обновлении-kit-агент): вопросы → план → apply, не blind replace.
4. **Ручной запуск:** применить после «да». **kit-exchange Automation:** применить без запроса только **kit-managed** артефакты (см. [merge при kit → проект](#merge-при-kit--проект)) и `starter_kit_version` в `INDEX.md`; **не** трогать SOUL, BOOTSTRAP, AUTONOMY, AGENTS, PROJECT, domain, CONSTITUTION, `workspace/<login>/`, `.env`, project-specific rules/skills/commands.

#### GitHub MCP (инструменты)

| Задача | MCP tool | Repo |
|--------|----------|------|
| Issues **kit** | `list_issues`, `search_issues`, `issue_read`, `issue_write`, `add_issue_comment` | `riantdrew/workspace_kit` |
| Issues **проекта** | те же | **свой** owner/repo — [workspace-sync](#workspace-sync-issues-своего-repo) |
| Прочитать kit | `get_file_contents` | `riantdrew/workspace_kit` |

MCP server: **user-github**. Перед вызовом — прочитать schema дескриптора tool.

#### workspace-sync (Issues своего repo)

Задачи команды — в Issues **приватного** репозитория проекта. Без скриптов, labels, Projects.

| Артефакт | Назначение |
|----------|------------|
| `workspace/workspace-sync.md` | Протокол (шаблон ниже) |
| `.cursor/skills/gh-workspace/SKILL.md` | MCP workflow; доставка через kit-exchange A |

**Repo guard:** workspace-sync = `owner/repo` из git remote проекта; **never** `riantdrew/workspace_kit` (это kit-exchange).

Create/update/close Issues — **только по явной просьбе**. Skill: триггеры «задачи», «issue», «что в работе».

**Не создавать:** `workspace_sync.py`, state json, command `/workspace-sync`, rule `workspace-sync.mdc`.

#### Границы (обязательно)

| Проект **может** | Проект **не может** |
|------------------|---------------------|
| Issues и комментарии через MCP | Push/commit в `workspace_kit` без явной просьбы |
| Предложить diff kit в чате | Закрывать чужие issues, менять labels без просьбы |
| Еженедельный kit-exchange Automation | Python-скрипты, manifest, произвольный cron |

Зафиксировать в `workspace/AUTONOMY.md` → `never`: commit/push в репозиторий workspace_kit из другого prod-проекта.


#### Еженедельный kit-exchange (Cursor Automation)

**Обязательно со стадии 3:** один раз в неделю агент **сам** выполняет оба направления — без Python-скриптов, через **GitHub MCP** и Cursor **Automation** (cron).

| Параметр | Значение |
|----------|----------|
| Расписание | ≥1 раз/нед, рекомендуем **понедельник 09:00** (`0 9 * * 1`) |
| Инструменты Automation | MCP **github** (GitHub MCP) |
| Репозиторий Automation | **этот** prod-проект (не workspace_kit) |
| Ручной дубль | `/kit-exchange` — тот же протокол вне расписания |

**Настройка (один раз, стадия 3+):**

1. Cursor → **Automations** → Create → **On a schedule** → weekly (понедельник 09:00).
2. Tools: включить **Use MCP server** → **github**.
3. Git: checkout **этого** репозитория, ветка `main` (или ваша default).
4. Instructions — скопировать из [шаблона Automation](#шаблон-cursor-automation-kit-exchange) ниже.
5. Зафиксировать в `workspace/AUTONOMY.md` → `always_allowed`: «kit-exchange Automation: отчёт, issues, обновление `.cursor/` и `starter_kit_version`».
6. Записать в `workspace/INDEX.md`: `kit_exchange_schedule: weekly`, `kit_exchange_last_run: —`.

**Протокол одного прогона (kit-exchange):**

```
A. Kit → проект
   1. get_file_contents → workspace_kit.md (riantdrew/workspace_kit)
   2. Сверить версию с workspace/INDEX.md → starter_kit_version
   3. Если remote новее — diff-план; применить **только kit-managed** (см. [merge](#merge-при-kit--проект)):
      новые kit commands/rules/skills; **не** перезаписывать project-specific
   4. Обновить starter_kit_version, starter_kit_source: remote в INDEX.md
   5. НЕ перезаписывать: workspace/<login>/, SOUL, GOALS, MEMORY, PROJECT,
      knowledge/domain/, constitution rules, .env

B. Проект → kit
   Режим Automation (cron):
     - Источники: MEMORY.md, workspace/reports/, workspace/reports/kit-exchange/
     - НЕ читать workspace/*/memory/ (gitignore — нет в checkout)
     - НЕ резолвить login
   Режим ручной (/kit-exchange):
     - + workspace/<login>/memory/ (7 дней; login: gh → data/workspace_user)
   1. Выделить универсальные паттерны workspace/Cursor (без домена и секретов)
   2. Если нечего — пропустить с пометкой в отчёте
   3. search_issues (repo:riantdrew/workspace_kit) → comment или issue_write (create)
   4. Не дублировать closed not_planned

C. Отчёт
   workspace/reports/kit-exchange/YYYY-MM-DD.md + kit_exchange_last_run в INDEX.md
```

**MUST NOT в Automation:** commit/push в workspace_kit; закрывать чужие issues; force-push; читать gitignored memory.

#### Протокол мейнтейнера kit (в репозитории workspace_kit)

1. Читать issues и комментарии (GitHub MCP или UI).
2. Вносить изменения в `workspace_kit.md`; bump версии, Changelog, [Осознанные отказы](#осознанные-отказы).
3. Отвечать в issue: принято / отложено / `not_planned` с причиной.
4. Проекты подтягивают kit через агента ([kit → проект](#алгоритм-агента-kit--проект)) — без manifest и скриптов.

### Протокол эволюции kit

По запросу «обнови workspace_kit» / «эволюционируй kit до X» / «накати новую версию kit»:

1. Прочитать kit: локальный `./workspace_kit.md` (или legacy `./starter_kit.md`) **или** [канонический raw URL](#канонические-url); сверить версии по [алгоритму](#алгоритм-загрузки-и-проверки-агент). `workspace/INDEX.md` → `starter_kit_version`.
2. Сравнить с целевой версией по Changelog и [Осознанные отказы](#осознанные-отказы).
3. Показать **diff-план**: что добавить в kit, что мигрировать в проекте, что удалить.
4. Обновить `workspace_kit.md`: bump версии, запись в Changelog, новые отказы — если есть.
5. Для **проекта-потребителя** — запустить [Миграция проекта при обновлении kit](#миграция-проекта-при-обновлении-kit-агент); **не** применять без подтверждения.
6. **Не** применять миграцию проекта без подтверждения.

---

### Миграция проекта при обновлении kit (агент)

**Принцип:** миграция — **сессия с агентом**, не скрипт. Каждый проект уникален (solo/team, git/no-git, legacy kit-sync, кастомный BOOTSTRAP, свой `session_memory.py`). Агент **сначала** аудит и вопросы, **потом** diff-план, **потом** правки — итерациями ≤8 файлов.

**Триггеры:** `starter_kit_version` в INDEX **старше** канона; `/kit-exchange` при расхождении версий; «обнови workspace», «накати kit 1.13», «мигрируй workspace».

#### Алгоритм агента (обязательный порядок)

1. **Снимок** — прочитать `workspace/INDEX.md` → `starter_kit_version`; канон kit → целевая версия; **не менять файлы**.
2. **Аудит delta** — что уже есть vs что требует целевая версия (см. Changelog между версиями). Зафиксировать legacy: `kit_sync.py`, `starter-kit-learnings.md`, `cursor_starter_kit`, корневой `USER.md` / `memory/`, кастом `.cursor/`.
3. **Вопросы** — блок [Обязательные вопросы миграции](#обязательные-вопросы-миграции). Не применять, пока нет ответов на блокирующие.
4. **Diff-план** — таблица: файл | действие (создать / merge / перенести / удалить после «да» / пропустить) | риск. Показать пользователю.
5. **Согласование** — одно «да» на итерацию или на весь план. Без «да» — только отчёт.
6. **Apply** — ≤8 файлов за итерацию; [безопасный merge](#безопасный-merge-данных); бэкап копий в `workspace/reports/kit-migrate/YYYY-MM-DD/` перед перезаписью kit-managed файлов.
7. **Верификация** — чеклист [После миграции](#после-миграции); при ошибке — откат из бэкапа, не продолжать молча.
8. **INDEX** — обновить `starter_kit_version`, `starter_kit_source`; отчёт `workspace/reports/kit-migrate/YYYY-MM-DD.md`.

**MUST NOT:** запускать фиксированный bash/python «migration script»; удалять legacy без «да»; перезаписывать кастомный BOOTSTRAP/GOALS/AUTONOMY; blind replace всего `.cursor/`.

#### Обязательные вопросы миграции

Задай **одним сообщением** (пропускай, если ответ уже в репо):

1. **Профиль:** team или solo на практике? Сколько человек в `workspace/`?
2. **Git:** есть remote? private? Если нет — нужен ли сейчас (для Issues / Automation)?
3. **Login:** `gh auth status` → кто `<github-login>` для `workspace/<login>/`?
4. **USER / memory:** где сейчас (`workspace/USER.md`, `memory/`)? Есть ли `session_memory.py` или hooks — куда пишут?
5. **Кастом:** что **нельзя** трогать (BOOTSTRAP backlog, domain knowledge, product rules/skills/commands)?
6. **Legacy kit:** есть `kit_sync.py`, `starter-kit-learnings.md`, `kit-sync` commands — удалить после переноса?
7. **kit-exchange Automation:** включать сейчас или отложить?
8. **workspace-sync (Issues):** нужен GitHub repo проекта сейчас или позже?

#### Ориентиры по версиям (не скрипт)

Агент **собирает** нужные шаги из Changelog между `starter_kit_version` и целевой. Ниже — типичные вехи; **не все** применимы к каждому проекту.

| С версии | Часто нужно | Пропустить если |
|----------|-------------|-----------------|
| **< 1.10** | Убрать kit-sync stack; feedback → MCP/issues | уже нет `kit_sync.py` |
| **< 1.11** | kit-exchange; AUTONOMY: exception для Automation | уже настроено |
| **< 1.12** | `workspace/<login>/`; workspace-sync; gh-workspace; gitignore memory | уже `<login>/` |
| **→ 1.13** | протокол миграции через агента; merge policy | — |

**Пример solo без git (legacy 1.4):** перенос USER/memory в `<login>/`, патч `session_memory.py`, merge rules (не replace), удалить kit_sync, AUTONOMY → workspace_kit, workspace-sync — **после** git init. BOOTSTRAP с локальными backlog — **не** переносить в Issues.

#### Безопасный merge данных

| Действие | Как |
|----------|-----|
| **Перенос** USER, memory | Копировать → показать diff → удалить старый путь **только после «да»** |
| **Правка hooks / session_memory** | Показать diff одного файла; проверить запись в новый path (тестовый чекпоинт) |
| **`.gitignore`** | Добавить patterns; **не** удалять существующие project-specific строки |
| **Legacy удаление** | Список файлов → «удалить?» → только после «да» |
| **GOALS / BOOTSTRAP** | Не сжимать насильно до «индекса»; локальные backlog **остаются** valid |

#### Merge при kit → проект

При kit-exchange A или ручной миграции — **не** затирать project-specific:

| Класс | Примеры | Правило |
|-------|---------|---------|
| **Kit-managed** | `gh-workspace/SKILL.md`, `kit-exchange.md`, шаблоны security-git / workspace-isolation (если нет кастома) | Можно обновить; бэкап перед overwrite |
| **Project-specific** | `conventions-*.mdc`, `sync.md`, domain skills, кастом `workspace-read`, `agent-knowledge` | **merge** или **skip_if_exists** — показать diff, спросить |
| **Protected workspace** | SOUL, BOOTSTRAP, AUTONOMY, AGENTS, GOALS, MEMORY, PROJECT, `knowledge/domain/`, `<login>/` | **Never** auto-overwrite |

**Локальные backlog** (BOOTSTRAP § задачи, чеклисты C00–S99) — **не** обязаны переезжать в GitHub Issues.

#### После миграции

- [ ] `starter_kit_version` = канон
- [ ] Hooks пишут в `workspace/<login>/memory/` (если team/solo с `<login>/`)
- [ ] Rules/commands проекта на месте (product-constitution, sync, conventions)
- [ ] Legacy kit-sync отсутствует или помечен deprecated
- [ ] Отчёт в `workspace/reports/kit-migrate/`
- [ ] Один smoke: session_start по BOOTSTRAP — пути читаются

#### Миграция 1.11 → 1.12 (ориентир)

См. [ориентиры по версиям](#ориентиры-по-версиям-не-скрипт). Типичные шаги: `<login>/`, workspace-sync, gh-workspace, gitignore memory, патч session memory. **Только** после [алгоритма](#алгоритм-агента-обязательный-порядок) и вопросов.

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
- **Обновление kit:** если `starter_kit_version` в INDEX **старше** канона — предложить [миграцию](#миграция-проекта-при-обновлении-kit-агент) (сначала вопросы и diff-план, без apply)

### 3. Задай обязательные вопросы

Только блок [Обязательные вопросы](#обязательные-вопросы-по-стадиям) для перехода **текущая → следующая** стадия.  
Не задавай вопросы следующих переходов, пока не закрыт текущий — кроме «сразу всё».

Если ответ уже в репо или чате — не спрашивай, процитируй.

Уточни **профиль:** по умолчанию team; solo — [сноска](#solo-сноска), если один автор и нет CODEOWNERS.

### 4. Дай рекомендации

- Что создать на **следующей** стадии (имена, без дублирования [Каталог файлов](#каталог-файлов))
- Что повесить на `.cursor/` (rules, hooks, skills) — [Интеграции Cursor](#интеграции-cursor)
- Что **не** коммитить; что не дублировать из README / docs
- Лимит: **≤8 файлов** за итерацию; порядок создания

### 5. Обнови проект (только после согласия)

- Создавай файлы с **заголовками обязательных разделов** и содержимым из ответов пользователя
- Шаблоны — [Шаблоны](#шаблоны-разделов)
- **Создание по шаблону на стадии N** = разрешено; **правка содержимого после** — по правилам «кто редактирует» в каталоге
- Защищённые файлы (правка содержимого только по явной команде): `workspace/SOUL.md`, `workspace/CONSTITUTION.md`, `workspace/AUTONOMY.md`, `workspace/BOOTSTRAP.md`, `workspace/<login>/USER.md`, `workspace/examples/`
- `workspace/AGENTS.md`: **создать** по шаблону на стадии 2 = да; менять процедуры потом — только по запросу
- **Автономная эволюция** (в `session_end`): `workspace/<login>/memory/`, `workspace/MEMORY.md`, `workspace/GOALS.md`, `workspace/knowledge/` (черновики)
- Новые workspace-файлы — только в `workspace/`, кроме [исключений](#исключения-вне-workspace)
- При создании `workspace/INDEX.md` — записать `starter_kit_version: "1.13"` и `starter_kit_source: "local"` или `"remote"`

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
| Push/commit в workspace_kit из другого prod-проекта | Нарушение границ | Issues через GitHub MCP; правки kit — только в repo kit |
| Отправить feedback в kit без поиска дубликатов | Шум в issues | `search_issues` → comment или create |
| Feedback без анонимизации | Утечка домена/секретов | Обобщить паттерн; убрать URL, токены, пути |
| Python sync-скрипты, manifest | Отменено в 1.10 | Агент + GitHub MCP |
| USER/memory в корне workspace/ (team) | Конфликты PR | `workspace/<login>/` |
| workspace-sync в repo workspace_kit | Путаница | Issues своего repo |
| kit-exchange Automation читает gitignored memory | Пустой checkout | Automation: MEMORY + reports only |
| Auto-create/close Issues без просьбы | Риск для команды | Только по явной команде |
| Login в shared INDEX.md | Перезапись | `data/workspace_user` (gitignore) |
| GOALS дублирует Issues без `#N` | Расхождение | GOALS = индекс; Issues = работа |
| Агентский жаргон в Issue body | Нечитаемо для людей | Инфостиль; техника — ссылкой на файл |
| Blind replace `.cursor/` при миграции | Потеря project rules/skills | [Merge при kit → проект](#merge-при-kit--проект) |
| Жёсткий migration script | Не учитывает кейс | [Миграция через агента](#миграция-проекта-при-обновлении-kit-агент) |
| Удалить legacy / старые paths без «да» | Потеря данных | Diff → подтверждение → бэкап в kit-migrate/ |
| Накатить kit без вопросов | Неверный профиль/paths | [Обязательные вопросы миграции](#обязательные-вопросы-миграции) |
| Переписать BOOTSTRAP/GOALS под шаблон kit | Потеря backlog | Merge; локальные задачи — valid |

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
**Профиль (предположение):** team (solo — [сноска](#solo-сноска))
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

**Workspace Kit** (папка **`workspace/`**) — слой markdown-контекста, отдельно от исходников:

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
├── INDEX.md                # starter_kit_version, kit_exchange_* (стадия 4+)
├── BOOTSTRAP.md
├── SOUL.md
├── USER.example.md         # → workspace/<login>/USER.md
├── GOALS.md
├── PROJECT.md
├── workspace-sync.md       # Issues своего repo (стадия 3+)
├── AGENTS.md
├── AUTONOMY.md
├── CONSTITUTION.md
├── CONVENTIONS.md
├── MEMORY.md
├── knowledge/
│   ├── INDEX.md
│   ├── domain/
│   ├── runbooks/
│   ├── faq/
│   └── references/
├── <github-login>/         # per user (team)
│   ├── USER.md             # в git (по умолчанию)
│   └── memory/             # gitignore → YYYY-MM-DD.md
├── SKILLS.md
├── TOOLS.md
├── ENV.md
├── PLAYBOOK.md
├── reports/
│   └── kit-exchange/
├── examples/               # опционально
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

## Профили: team

**По умолчанию:** team — команда 2+, приватный репо, shared workspace + personal `workspace/<github-login>/`.

| Аспект | team (default) |
|--------|----------------|
| Shared | GOALS, MEMORY, knowledge, SOUL, CONSTITUTION, PROJECT, … — корень `workspace/` |
| Personal USER | `workspace/<login>/USER.md` — **в git** (приватный репо) |
| Personal memory | `workspace/<login>/memory/` — **`.gitignore`** |
| Шаблон USER | `workspace/USER.example.md` в git |
| Login | `gh auth status` → `data/workspace_user` (gitignore); **не** в INDEX.md |
| `.cursor/` | Общие rules, hooks, skills, commands |
| Cloud tasks | GitHub Issues **своего** repo — [workspace-sync](#workspace-sync-issues-своего-repo) |

**Escape hatch:** если профиль чувствителен — добавить `workspace/*/USER.md` в `.gitignore`.

#### Solo (сноска)

Один разработчик: та же схема `<login>/`, репо может быть private solo. Shared/personal split сохраняется — меньше смысла в Issues, но workspace-sync опционален.

---

## Принципы

### 1. Один факт — одно место

| Тип информации | Где хранить |
|----------------|-------------|
| Жёсткий запрет | `.cursor/rules/` + `workspace/AUTONOMY.md` |
| Архитектура и безопасность | `workspace/CONSTITUTION.md` |
| Текущие приоритеты (индекс) | `workspace/GOALS.md` + ссылки `#N` на Issues |
| Исполняемые задачи | GitHub Issues **своего** repo |
| Долгосрочные выводы (команда) | `workspace/MEMORY.md` |
| Сырьё за день | `workspace/<login>/memory/YYYY-MM-DD.md` |
| Регламенты, FAQ | `workspace/knowledge/` |
| Onboarding продукта | `workspace/PROJECT.md` |
| Профиль человека | `workspace/<login>/USER.md` |
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
- Cursor **не** шлёт «сессия закончилась» — без команды `workspace/<login>/memory/` не обновится

### 5. Автономность документов

**Без отдельного «да»** в `session_end`: `workspace/<login>/memory/`, `workspace/MEMORY.md`, `workspace/GOALS.md` (мелкие правки), `workspace/knowledge/` (draft).

**Только по явной команде** (после первичного создания): `SOUL`, `CONSTITUTION`, `AUTONOMY`, `BOOTSTRAP`, `workspace/<login>/USER`, `examples/`. `AGENTS.md` — процедуры по запросу; создание по шаблону на стадии 2 — разрешено.

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

#### `workspace/<login>/USER.md`
**Разделы:** `profile`, `communication`, `expertise`, `preferences`, `availability`  
**Team:** путь `workspace/<github-login>/USER.md`; шаблон — `USER.example.md`; **в git** (escape hatch: gitignore)

#### `workspace/workspace-sync.md` *(стадия 3+)*
**Назначение:** протокол Issues **своего** repo; см. [workspace-sync](#workspace-sync-issues-своего-repo)  
**Разделы:** `repo`, `when`, `rules`, `mcp`, `goals`, `boundaries`

#### `workspace/PROJECT.md`
**Разделы:** `overview`, `audience`, `stack`, `repositories`, `key_entities`  
**Ограничения:** без секретов; ссылки на README; `repositories` — owner/repo для workspace-sync

#### `workspace/GOALS.md`
**Разделы:** `period`, `priorities`, `out_of_scope`, `success_criteria`, `guardrails`  
**Team:** индекс периода + ссылки `#N` на Issues; не дублировать исполняемое

### Операции

#### `workspace/BOOTSTRAP.md`
**Разделы:** `session_start`, `session_end`, `before_destructive_action`

#### `workspace/AGENTS.md`
**Разделы:** `roles`, `responsibilities`, `limitations`, `workflows`, `escalation`  
**Создание** по шаблону стадии 2 — агент; **правки** процедур — человек или по запросу

#### `workspace/AUTONOMY.md`
**Разделы:** `always_allowed`, `ask_first`, `never`, `environments`  
**Kit feedback:** в `never` — push/commit в репозиторий workspace_kit из другого prod-проекта

#### `workspace/reports/` *(опционально, стадия 3+)*
**Назначение:** отчёты сессий, аудитов; источник для feedback в kit через GitHub MCP по просьбе.

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

#### `workspace/<login>/memory/`
**Имена:** `YYYY-MM-DD.md` — разделы: `done`, `in_progress`, `blockers`, `notes`  
**Gitignore** (team); hooks и session_memory пишут сюда

### Навыки и инфраструктура

#### `workspace/SKILLS.md` *(стадия 3+)*
**Разделы:** `skills` (таблица: имя, триггер, путь к `.cursor/skills/`), `conflict_resolution`

#### `.cursor/skills/<name>/SKILL.md` *(стадия 3+)*
**Назначение:** runtime skill для Cursor.  
**Индекс** в `workspace/SKILLS.md`. Приоритет над глобальными — проектный выше.

#### `workspace/TOOLS.md` *(стадия 3+)*
**Разделы:** `apis`, `databases`, `servers`, `cli`, `mcp`  
**Prerequisites:** GitHub MCP (**user-github**), `gh auth login`; kit-exchange Automation (стадия 3+)

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
| **3** | + Конвенции языка | + check secrets/shell | ≥1 skill (+ gh-workspace) | kit-exchange |
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
- Personal (team): USER и memory только в `workspace/<github-login>/`, не в корне workspace/
- Не пиши в чужой каталог `workspace/<другой-login>/`
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

Resolve login (team): `gh auth status` → `data/workspace_user` → спросить один раз.

При любой нетривиальной задаче прочитай:
1. `workspace/GOALS.md` — приоритеты (индекс + `#N` на Issues)
2. `workspace/MEMORY.md` — командные выводы
3. `workspace/<login>/USER.md` — профиль текущего пользователя

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

Resolve login перед чтением personal paths (см. workspace-read).

Перед ответом на вопрос о проекте агент самостоятельно находит факты:

1. `workspace/MEMORY.md` — решения, уроки, контекст
2. `workspace/<login>/memory/` — последние 7 дней
3. `workspace/knowledge/` — по INDEX.md
4. `workspace/GOALS.md` — приоритеты (goal lens)
5. `workspace/reports/` — актуальные отчёты
6. GitHub Issues своего repo — по запросу или skill `gh-workspace`
7. Код продукта — только если задача требует

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

### Хуки — жизненный цикл сессии (стадия 2+)

События Cursor hooks:

| Событие | Триггер | Действие |
|---------|---------|----------|
| `sessionStart` | Новый чат | Снимок GOALS + MEMORY + git (+ orphan detection) |
| `sessionEnd` | Закрытие чата | Консолидация в `workspace/<login>/memory/YYYY-MM-DD.md` |
| `afterFileEdit` | Правка `workspace/` | Журнал изменений |
| `stop` / `afterResponse` | После ответа агента | Чекпоинт → `workspace/<login>/memory/YYYY-MM-DD.md` |

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

В практике выработан трёхслойный механизм без HEARTBEAT/CRON:

1. **Журнал** (`afterFileEdit`) — каждая правка `workspace/` пишется в JSONL-журнал
2. **Чекпоинт** (`stop`) — после ответа агента: `auto_checkpoint` → `workspace/<login>/memory/YYYY-MM-DD.md`
3. **Консолидация** (`sessionEnd` или `sessionStart`) — orphan detection

Явный `session_end` не обязателен — orphan detection закрывает пробелы.  
Ручной догон: `.cursor/commands/session-end.md` → `python3 session_consolidate.py --orphans`.

**Login для путей:** env `WORKSPACE_USER` или `data/workspace_user` или `gh auth status`.

Реализация: `session_memory.py` + shell-обёртки в hooks/ — **локальная** инфраструктура проекта, не часть kit repo. Пишет в `workspace/<login>/memory/`, не в корень.

### Skills

| Уровень | Где лежит | Кто подхватывает |
|---------|-----------|------------------|
| Встроенные Cursor | `~/.cursor/skills-cursor/` | Cursor (не трогать) |
| Глобальные | `~/.cursor/skills/` | Cursor |
| **Проектные** | `.cursor/skills/<name>/SKILL.md` | Cursor |
| Каталог | `workspace/SKILLS.md` | Агент читает по необходимости |

**Стадия 3:** `workspace/SKILLS.md` + skill `gh-workspace` (минимум) + опционально deploy и др.

### Commands

| Команда | Назначение | Путь |
|---------|------------|------|
| `workspace/BOOTSTRAP.md` | Ритуал сессии | workspace |
| `workspace/GOALS.md`, `workspace/MEMORY.md` | Контекст | workspace |
| `workspace_kit.md` / GitHub URL | Внедрение / эволюция kit | корень / remote |
| session-end | Принудительная консолидация памяти | `.cursor/commands/` |
| kit-exchange | Обмен kit↔проект (GitHub MCP) | `.cursor/commands/` |

**Skill workspace-sync:** `.cursor/skills/gh-workspace/SKILL.md` — без отдельной command.

**Вне scope:** `/loop`, произвольные Automations и cron — кроме [kit-exchange](#еженедельный-kit-exchange-cursor-automation).

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
2. **Чекпоинт** — после ответа агента `auto_checkpoint` → `workspace/<login>/memory/YYYY-MM-DD.md` (хук `stop`)
3. **Консолидация** — при `sessionEnd` или новом чате (orphan detection)

Явный `session_end` не обязателен. Автоматика пишет **только** в `workspace/<login>/memory/YYYY-MM-DD.md`, не перезаписывает `MEMORY.md`. Сжатие в `MEMORY.md` — осознанный шаг агента.

Правки вне `workspace/` (код, `.cursor/`) в автожурнал не попадают — фиксировать руками в `done`.

### В конце сессии

1. `workspace/<login>/memory/YYYY-MM-DD.md` — если не было авто-записи
2. `workspace/MEMORY.md` — сжатие важного (не автоматически)
3. `workspace/GOALS.md` — при сдвиге приоритетов (ссылки `#N` на Issues)
4. `workspace/knowledge/` — черновики (`status: draft`, `source` обязателен)

### Запись в MEMORY.md

```
- ДД.ММ.ГГГГ: <факт>. Причина: <одна строка>.
```

Не писать: предположения, непроверенные гипотезы, секреты.  
Гипотезы — в отдельный раздел `hypotheses_and_ideas`, не в `decisions`.

### knowledge/

Факт только из кода, docs пользователя или его слов. Иначе — TODO в `workspace/<login>/memory/`.

### Предлагать, не менять самому

`SOUL`, `CONSTITUTION`, `AUTONOMY`, `BOOTSTRAP`, `workspace/<login>/USER` — diff в чате + «применить?».

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

- [ ] `BOOTSTRAP.md`, `SOUL.md`, `GOALS.md`, `AGENTS.md`, `MEMORY.md`, `PROJECT.md`
- [ ] `workspace/<login>/USER.md` из `USER.example.md`
- [ ] `workspace/<login>/memory/.gitkeep` или первый лог

**В корне:**

- [ ] `AGENTS.md` — указатель
- [ ] `.gitignore`: `workspace/*/memory/`, `data/workspace_user`

**Cursor:**

- [ ] `workspace-read.mdc`, `constitution-enforce.mdc`
- [ ] hook `sessionStart` (опционально)

**Team:** `USER.example.md`

---

### Стадия 3 — Инфраструктура и навыки

- [ ] `CONVENTIONS.md`, `TOOLS.md`, `ENV.md`, `SKILLS.md`
- [ ] `knowledge/INDEX.md`
- [ ] `workspace-sync.md` + skill `gh-workspace`
- [ ] command `kit-exchange` + [Cursor Automation kit-exchange](#еженедельный-kit-exchange-cursor-automation) (weekly)
- [ ] hooks: секреты + shell (audit-first)
- [ ] Правила конвенций языка
- [ ] GitHub MCP (**user-github**) + `gh auth login`

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
- [ ] `memory/` — записи за последние 7 дней в `workspace/<login>/memory/`
- [ ] hooks session memory → `<login>/memory/`
- [ ] kit-exchange Automation ≥1 раз/нед; `kit_exchange_last_run` актуален
- [ ] GOALS ↔ open Issues — сверка по запросу (skill gh-workspace)

---

## Чек-лист стадий

**Текущая стадия** = максимальная, где **все** обязательные пункты выполнены и файлы содержат обязательные разделы. Иначе: «N (частично)» — работаем с N, не объявляем N+1.

| Стадия | Условие |
|--------|---------|
| **0** | Аудит выполнен; `workspace/` нет или пуст (кроме `.gitkeep`) |
| **1** | `CONSTITUTION.md` + `AUTONOMY.md` + `security-git.mdc` + `workspace-isolation.mdc` |
| **2** | Стадия 1 + файлы стадии 2 + корневой `AGENTS.md` + `workspace-read.mdc` |
| **3** | Стадия 2 + CONVENTIONS, TOOLS, ENV, SKILLS + `knowledge/INDEX.md` + `workspace-sync.md` + `gh-workspace` + kit-exchange |
| **4** | Стадия 3 + `INDEX.md` + `PLAYBOOK.md` |
| **5** | Стадия 4 + operational: актуальный `GOALS.period` + memory за 7 дней |

---

## Обязательные вопросы по стадиям

Один блок за сообщение — только для перехода **текущая → следующая**.

### 0 → 1

1. Стек и где prod (если есть)?
2. Топ-3 действия, которые агент **никогда** не делает без спроса?
3. Коммиты в git — только по вашей команде?
4. Приватный repo, gh auth у всех, CODEOWNERS (team)?

### 1 → 2

5. Как общаться (кратко/подробно, язык, «вы/ты»)?
6. Три приоритета на 2 недели и что **не** в scope?
7. Одной фразой: роль агента (SOUL)?

### 2 → 3

8. Основные API, БД, CLI (`composer test`, docker…)?
9. Имена переменных `.env` (без значений)?
10. Повторяющиеся workflow для skills (deploy, release, review)?
11. Настроить kit-exchange Automation (понедельник 09:00, MCP github)?
12. GitHub MCP для workspace-sync (Issues своего repo)?

### 3 → 4

11. Типовой инцидент и первые 3 шага?
12. Нужны `examples/` для тона ответов?

### 4 → 5

13. Как часто напоминать про review GOALS, MEMORY и open Issues?

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
| kit-exchange Automation настроена (стадия 3+) | ☐ |
| GitHub MCP (user-github) доступен | ☐ |
| `workspace/<login>/` и `.gitignore` для memory (team) | ☐ |
| `workspace-sync.md` + skill `gh-workspace` (стадия 3+) | ☐ |
| При обновлении kit: миграция через агента, отчёт kit-migrate | ☐ |

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
- Push/commit в репозиторий workspace_kit из другого prod-проекта
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

### `workspace/<login>/USER.md`

```markdown
# USER

Путь: `workspace/<ваш-github-login>/USER.md` (шаблон — USER.example.md)

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
# USER (пример — скопируйте в workspace/<ваш-github-login>/USER.md)

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
1. Resolve login: `gh auth status` → `data/workspace_user`
2. `workspace/GOALS.md` — приоритеты (**goal lens**; индекс + `#N` на Issues)
3. `workspace/MEMORY.md` + `workspace/<login>/memory/` (последние 7 дней)
4. `workspace/<login>/USER.md` — профиль
5. При необходимости — `workspace/knowledge/` по INDEX.md
6. `git status`
7. Опционально: «покажи задачи» → skill `gh-workspace`

## session_end
1. `workspace/<login>/memory/YYYY-MM-DD.md` (авто-журнал мог записать — проверить)
2. Сжать важное в `workspace/MEMORY.md` (командные факты; без секретов)
3. `workspace/GOALS.md` — при сдвиге фокуса
4. Универсальный паттерн для kit → `/kit-exchange` или Automation

## before_destructive_action
- force-push, DROP prod, массовое удаление — только по явной просьбе
- Разрушительные действия вне `workspace/` — спросить, если не было явной команды
```

### `workspace/workspace-sync.md` (стадия 3+)

```markdown
# workspace-sync

Issues **этого** репозитория — задачи команды. Skill: `.cursor/skills/gh-workspace/SKILL.md`.

## repo
<!-- owner/repo из git remote или PROJECT.md -->

## when
По запросу («задачи», «issue»). Опционально — session_start/end.

## rules
- Create/update/close Issues — **только по явной просьбе**
- Body — для людей (инфостиль); техника — ссылкой на файлы workspace/
- **Repo guard:** never `riantdrew/workspace_kit` (это kit-exchange)

## mcp
user-github: `list_issues`, `issue_read`, `issue_write`, `add_issue_comment` на **своём** repo.

## goals
GOALS.md = индекс периода + `#N`. Issues = исполняемое.

## boundaries
| Тема | Куда |
|------|------|
| Задачи команды | Issues этого repo |
| Feedback kit | `/kit-exchange` |
| Факты | MEMORY.md |
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

### `.cursor/commands/kit-exchange.md` (стадия 3+)

```markdown
# kit-exchange

Двусторонний обмен с [workspace_kit](https://github.com/riantdrew/workspace_kit) — тот же протокол, что [еженедельная Automation](#еженедельный-kit-exchange-cursor-automation).

**A. Kit → проект:** загрузить `workspace_kit.md`, сверить версию; обновить `.cursor/commands`, `.cursor/rules`, `.cursor/skills/gh-workspace/`; `starter_kit_version` в INDEX.md.

**B. Проект → kit (ручной):** `MEMORY.md`, `reports/`, + `workspace/<login>/memory/` (7 дней) → GitHub MCP kit repo. Анонимизировать.

**B. Automation:** только `MEMORY.md` + `reports/` (не gitignored memory).

**C. Отчёт:** `workspace/reports/kit-exchange/YYYY-MM-DD.md`.

Репозиторий kit **не коммитить** из этого проекта.
```

### Шаблон Cursor Automation (kit-exchange)

Instructions для Automation (cron weekly, MCP **github**):

```
Еженедельный kit-exchange для этого репозитория. Выполни полностью, без вопросов пользователю.

A. Kit → проект
- GitHub MCP: workspace_kit.md из riantdrew/workspace_kit (main)
- Сверить версию с workspace/INDEX.md → starter_kit_version
- Если новее — обновить **только kit-managed** (.cursor/skills/gh-workspace/, kit-exchange.md); rules/commands — skip_if_exists / merge, не затирать project-specific
- Обновить starter_kit_version, starter_kit_source: remote
- НЕ перезаписывать: workspace/<login>/, SOUL, BOOTSTRAP, AUTONOMY, AGENTS, GOALS, MEMORY, PROJECT, knowledge/domain/, project rules/skills, .env

B. Проект → kit (Automation — без gitignored memory)
- Прочитать MEMORY.md, workspace/reports/ (НЕ workspace/*/memory/)
- Универсальные паттерны → search_issues repo:riantdrew/workspace_kit; comment или create
- Анонимизировать; пропустить если нечего; не дублировать closed not_planned

C. Отчёт
- workspace/reports/kit-exchange/YYYY-MM-DD.md
- kit_exchange_last_run в workspace/INDEX.md

НЕ commit/push в workspace_kit. НЕ закрывать issues. НЕ читать workspace/*/memory/.
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
1. … (#42 — ссылка на Issue при наличии)

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

### `workspace/<login>/memory/YYYY-MM-DD.md`

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
| gh-workspace | «задачи», issue, доска | .cursor/skills/gh-workspace/SKILL.md |

## conflict_resolution
Проектный skill в `.cursor/skills/` приоритетнее глобального.
```

### `workspace/INDEX.md`

```markdown
# INDEX

## starter_kit_version
1.13

## starter_kit_source
remote

## workspace_stage
4

## files
| Файл | Назначение |
|------|------------|
| GOALS.md | Приоритеты |

## editable_by_agent
- `<login>/memory/`, MEMORY.md, GOALS.md (мелкие), knowledge/ (draft)

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

### Team (default)

| Путь | Коммитить |
|------|-----------|
| Shared workspace (GOALS, MEMORY, knowledge, SOUL, …) | Да |
| `workspace/<login>/USER.md` | Да (escape hatch: gitignore) |
| `workspace/<login>/memory/` | **Нет** → `.gitignore` |
| `data/workspace_user` | **Нет** → `.gitignore` |
| `USER.example.md`, `workspace-sync.md` | Да |
| `.cursor/rules/`, `.cursor/skills/` | Да |

**`.gitignore` (team):**

```
workspace/*/memory/
data/workspace_user
# опционально: workspace/*/USER.md
```

### Solo (сноска)

Та же схема `<login>/`; memory по желанию в git или gitignore.

---

## Не-git проекты

Если репозитория нет:

- Kit всё равно загружается с [GitHub](#канонические-url) — git в **вашем** проекте не нужен для `workspace/`
- Аудит = структура папок на диске
- Пропустить шаги про git в BOOTSTRAP и security-git (оставить запрос на коммит «на будущее»)
- **workspace-sync** и **kit-exchange Automation** — отложить до `git init` + remote; repo указать в `PROJECT.md` / `workspace-sync.md` вручную
- Стадии и `workspace/` — те же; `<login>/` и session memory — применимы без git
- Миграция — [через агента](#миграция-проекта-при-обновлении-kit-агент); вопрос «есть ли git?» обязателен

---

*Конец workspace_kit v1.13*
