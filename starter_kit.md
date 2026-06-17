# starter_kit — внедрение agent workspace в существующий проект

**Версия kit:** 1.4  
**Дата:** 18.06.2026  
**Схема workspace:** 1.4 (совместима с ≥ 1.0)  
**Профиль по умолчанию:** solo — см. [Профили: solo и team](#профили-solo-и-team)  
**Канонический репозиторий:** https://github.com/riantdrew/cursor_starter_kit  
**Канонический raw URL:** https://raw.githubusercontent.com/riantdrew/cursor_starter_kit/main/starter_kit.md  
**Ветка по умолчанию:** `main`  
**Локальный путь (опционально):** `starter_kit.md` в **корне** проекта — для `@starter_kit.md`  
**Каталог агента:** `workspace/` — markdown-контекст агента **только здесь**, не в корне и не рядом с кодом приложения

> Загрузите в чат: ссылку на [канонический репозиторий](#источники-загрузки-kit), raw URL или `@starter_kit.md` (если файл лежит локально). Агент **обязан** начать с [CRITICAL](#critical--10-правил-для-агента), [Источник и версия kit](#0-источник-и-версия-kit) и [Протокол для агента](#протокол-для-агента).

---

## CRITICAL — 10 правил для агента

1. **MUST** выполнить [Протокол](#протокол-для-агента) **строго по порядку**: сначала [Источник и версия kit](#0-источник-и-версия-kit), затем [аудит репозитория](#стадия-0--аудит-репозитория), затем оценка `workspace/`.
2. **MUST** при локальной копии сверить её с [каноническим raw URL](#источники-загрузки-kit) и работать по **более свежей** версии kit.
3. **MUST NOT** рекурсивно обходить весь репозиторий — только [алгоритм выборочного аудита](#алгоритм-аудита-без-перегрузки-контекста).
4. **MUST NOT** создавать файлы без согласия пользователя — сначала отчёт и рекомендации.
5. **MUST NOT** выдумывать бизнес-факты — `TODO: уточнить у USER`.
6. **MUST NOT** дублировать README, `docs/` продукта, существующие ADR в `workspace/`.
7. **MUST** класть markdown агента **только** в `workspace/`; skills Cursor — в `.cursor/skills/`.
8. **MUST NOT** создавать более **8 файлов за одну итерацию** (кроме явной просьбы «сразу всё»).
9. **MUST** верифицировать созданные файлы по [чек-листу разделов](#верификация-после-создания).
10. **MUST NOT** включать HEARTBEAT, CRON, `/loop`, Automations — вне scope kit; см. [Осознанные отказы](#осознанные-отказы).

**Триггеры запуска:** `@starter_kit.md`, ссылка на GitHub-репозиторий kit, raw URL `starter_kit.md`, «помоги с workspace / starter kit», «внедри agent workspace».

---

## Быстрый старт

### Для человека

**Вариант A — без локального файла (рекомендуется):**

1. Чат: вставьте ссылку на репозиторий — https://github.com/riantdrew/cursor_starter_kit — и напишите «помоги внедрить agent workspace».
2. Агент подтянет актуальный `starter_kit.md` с GitHub и сверит версию, если локальная копия уже есть.
3. Ответьте на вопросы перехода **0 → 1**.
4. Подтвердите создание файлов стадии 1 (и 2, если готовы).
5. Новый чат: `@workspace/BOOTSTRAP.md` — рабочая сессия; в конце — «завершаем сессию».

**Вариант B — локальная копия:**

1. Положите `starter_kit.md` в **корень** проекта (или обновите из [канонического репозитория](#источники-загрузки-kit)).
2. Чат: `@starter_kit.md помоги внедрить agent workspace`.
3. Дальше — как в варианте A, шаги 3–5.

### Для агента (одна строка)

источник kit + версия → CRITICAL → аудит репо → стадия `workspace/` → вопросы текущего перехода → рекомендации → создание (≤8 файлов) → верификация → итог.

---

## Источники загрузки kit

Kit **не обязан** лежать в проекте. Канон — публичный GitHub-репозиторий; локальный `starter_kit.md` — опциональная копия для `@starter_kit.md`.

### Канонические URL

| Назначение | URL |
|------------|-----|
| Репозиторий | https://github.com/riantdrew/cursor_starter_kit |
| Raw (для агента) | https://raw.githubusercontent.com/riantdrew/cursor_starter_kit/main/starter_kit.md |
| Ветка по умолчанию | `main` |
| Путь в репо | `starter_kit.md` (корень репозитория kit) |

> Если вы форкаете kit — обновите URL в форке; проекты могут ссылаться на ваш fork тем же способом.

### Как запустить в Cursor

| Способ | Пример |
|--------|--------|
| Ссылка на репозиторий | `https://github.com/riantdrew/cursor_starter_kit — внедри agent workspace` |
| Raw URL | `https://raw.githubusercontent.com/riantdrew/cursor_starter_kit/main/starter_kit.md` |
| Локальный файл | `@starter_kit.md` в корне **вашего** проекта |

### Нормализация GitHub-ссылок (для агента)

Любую ссылку пользователя приведи к raw URL `starter_kit.md`:

| Вход | Raw URL |
|------|---------|
| `https://github.com/OWNER/REPO` | `https://raw.githubusercontent.com/OWNER/REPO/main/starter_kit.md` |
| `https://github.com/OWNER/REPO/tree/BRANCH` | `https://raw.githubusercontent.com/OWNER/REPO/BRANCH/starter_kit.md` |
| `https://github.com/OWNER/REPO/blob/BRANCH/starter_kit.md` | `https://raw.githubusercontent.com/OWNER/REPO/BRANCH/starter_kit.md` |
| Уже raw | использовать как есть |

Если ветка не указана — `main`, затем `master`. Если путь другой — только при явном указании пользователя.

### Сравнение версий (semver-lite)

Версия kit — строка **`X.Y`** в шапке файла (`**Версия kit:**`). Сравнение:

1. Старше та, у которой больше **major** (`2.0` > `1.4`).
2. При равном major — больше **minor** (`1.4` > `1.3`).
3. Патч и суффиксы kit **не использует** — только `X.Y`.

При равных версиях, но разном содержимом — предпочитай **remote**, если локальная копия не из канонического репозитория (hash/commit не проверяем — достаточно версии и явного расхождения текста шапки).

### Алгоритм загрузки и проверки (агент)

1. **Определи источник сессии:**
   - `@starter_kit.md` или локальный путь → `local`
   - GitHub / raw URL в чате → `remote` (нормализуй URL)
   - Только текстовый триггер без URL и без локального файла → загрузи **канонический raw URL**
2. **Прочитай remote:** первые ~50 строк канонического raw URL (`WebFetch` / `curl` / аналог). Извлеки `**Версия kit:**`.
3. **Если есть `./starter_kit.md` в корне проекта:**
   - Прочитай локальный файл, извлеки версию.
   - Сравни по [semver-lite](#сравнение-версий-semver-lite).
   - **Remote новее** → сообщи пользователю (локальная X.Y, каноническая Z.W), работай по **remote**; предложи обновить локальный файл **после согласия** (≤1 файл).
   - **Локальная новее или равна** → работай по локальной; если remote недоступен — локальная + предупреждение.
4. **Если локального файла нет** → загрузи полный remote и работай по нему.
5. **Если remote недоступен** и локального нет → остановись: «Не удалось загрузить starter_kit. Проверьте сеть или положите starter_kit.md в корень проекта».
6. **Зафиксируй в отчёте сессии:** источник (`local` / `remote`), версия kit, результат сверки.

### Что не делать

- **MUST NOT** копировать `starter_kit.md` в `workspace/` — версия только в `workspace/INDEX.md`.
- **MUST NOT** молча игнорировать более свежий remote.
- **MUST NOT** перезаписывать локальный файл без согласия пользователя.

---

## Версия и эволюция kit

Этот файл **эволюционирует** вместе с практиками ИИ-разработки. Каждый проект фиксирует в `workspace/INDEX.md`: `starter_kit_version`, `starter_kit_source` (`local` / `remote`).

### Changelog

| Версия | Дата | Изменения |
|--------|------|-----------|
| **1.4** | 18.06.2026 | Загрузка kit по GitHub/raw URL без локальной копии; проверка версии remote vs local; канонический репозиторий; шаг протокола «Источник и версия kit» |
| **1.3** | 18.06.2026 | CRITICAL-блок; аудит больших репо; staged rules; `.cursor/skills/`; шаблоны rules/hooks; эволюция kit; team-профиль; верификация; anti-patterns |
| **1.2** | — | Каталог `workspace/`; изоляция от кода; миграция из корня |
| **1.1** | — | Интеграции Cursor (rules, hooks, commands); стадии 0–5 |
| **1.0** | — | Первая схема файлов SOUL, MEMORY, CONSTITUTION, BOOTSTRAP |

### Осознанные отказы

| Было | Почему отказались | Альтернатива в 1.4 |
|------|-------------------|---------------------|
| Локальная копия kit обязательна | Устаревает; лишний шаг | GitHub raw URL или опциональный `@starter_kit.md` |
| `starter_kit.md` только в корне проекта | Дублирование канона | Канон в GitHub; корень проекта — опциональная копия |
| `HEARTBEAT.md`, `CRON.md` | Cursor не даёт фон без Automations; риск автозапуска | Явный `session_end` + hooks audit-only |
| `/loop`, Cursor Automations | Вне scope; непредсказуемая автономность | Ручной старт чата + BOOTSTRAP |
| `agent/` как каталог | Путаница с npm-пакетами, CLI | `workspace/` |
| `workspace/skills/` как runtime | Cursor не подхватывает этот путь | `.cursor/skills/<name>/SKILL.md` + каталог `workspace/SKILLS.md` |
| Skills в корне `./skills/` | Не стандарт Cursor | `.cursor/skills/` |
| Полный `AGENTS.md` в корне | Дублирование; раздувание контекста | Корень = указатель 5–15 строк; мануал в `workspace/AGENTS.md` |
| Redirect-файлы в корне (`SOUL.md` → workspace) | Путают агента и людей | Миграция с удалением после подтверждения |
| Автоудаление при миграции | Риск потери данных | Перенос → проверка → удаление **только** после «да» |
| `workspace.yaml` / `workspace.md` как карта | Дублирование starter_kit | Единый `starter_kit.md` |
| Копия `starter_kit.md` в `workspace/` | Две версии расходятся | Канон — GitHub; версия и источник в `workspace/INDEX.md` |

### Протокол эволюции kit

По запросу «обнови starter_kit» / «эволюционируй kit до X»:

1. Прочитать kit: локальный `./starter_kit.md` **или** [канонический raw URL](#канонические-url); сверить версии по [алгоритму](#алгоритм-загрузки-и-проверки-агент). `workspace/INDEX.md` → `starter_kit_version`.
2. Сравнить с целевой версией по Changelog и [Осознанные отказы](#осознанные-отказы).
3. Показать **diff-план**: что добавить в kit, что мигрировать в проекте, что удалить.
4. Обновить `starter_kit.md`: bump версии, запись в Changelog, новые отказы — если есть.
5. Предложить миграцию `workspace/`: переименования, новые rules, обновление `starter_kit_version` и `starter_kit_source`.
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
- Что повесить на `.cursor/rules/`, hooks, `.cursor/skills/` — [Интеграции Cursor](#интеграции-cursor)
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
- При создании `workspace/INDEX.md` — записать `starter_kit_version: "1.4"` и `starter_kit_source: "local"` или `"remote"`

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
| `workspace-read.mdc` с GOALS до стадии 2 | Битые ссылки | Staged rules: см. ниже |
| Удалить legacy-файлы из корня без спроса | Потеря данных | Перенос → подтверждение → удаление |
| Выдумать API, env, контакты | Ложная память | `TODO` или вопрос пользователю |
| Игнорировать более свежий kit на GitHub | Устаревшие инструкции | [Алгоритм загрузки и проверки](#алгоритм-загрузки-и-проверки-агент) |
| Коммит без запроса | Риск для пользователя | Только по явной команде |

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
starter_kit.md              # опционально в корне вашего проекта (@starter_kit.md)
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
├── examples/               # good.md, bad.md (опционально)
├── STYLE.md                # опционально
├── IDENTITY.md             # опционально
└── CONTACTS.md             # опционально

.cursor/                    # конфиг Cursor — НЕ в workspace/
├── rules/
├── hooks/
└── skills/                 # проектные SKILL.md (Cursor подхватывает отсюда)

AGENTS.md                   # КОРЕНЬ: указатель 5–15 строк → workspace/
```

### Исключения вне `workspace/`

| Путь | Зачем не в `workspace/` |
|------|-------------------------|
| `.cursor/rules/*.mdc` | Cursor читает только этот путь |
| `.cursor/hooks.json` | API hooks фиксирован |
| `.cursor/skills/<name>/SKILL.md` | Cursor подхватывает skills отсюда |
| `AGENTS.md` (корень) | Cursor ищет в корне — **короткий указатель** |
| `starter_kit.md` (корень проекта) | Опционально: `@starter_kit.md`; канон — GitHub raw |

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
**Индекс** в `workspace/SKILLS.md`. Приоритет над глобальными `~/.cursor/skills/` при конфликте имён — проектный выше.

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
**Разделы:** `starter_kit_version`, `starter_kit_source`, `workspace_stage`, `files`, `editable_by_agent`, `cursor_integrations`

#### `workspace/CONTACTS.md` *(опционально)*
**Разделы:** `contacts`

---

## Интеграции Cursor

### Staged rules (важно)

| Стадия | Файлы rules |
|--------|-------------|
| **1** | `security-git.mdc`, `workspace-isolation.mdc` |
| **2** | + `workspace-read.mdc`, `constitution-enforce.mdc` |
| **3** | + `conventions-{lang}.mdc` по glob |

**Стадия 1:** `workspace-isolation.mdc` — **без** ссылок на GOALS/MEMORY (их ещё нет).  
**Стадия 2:** добавить `workspace-read.mdc` с GOALS/MEMORY.

### `.cursor/rules/` — шаблоны

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

### Hooks — шаблон (стадия 2+)

`.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "command": ".cursor/hooks/session-start.sh"
      }
    ]
  }
}
```

`.cursor/hooks/session-start.sh` (исполняемый):

```bash
#!/bin/bash
# Напоминание: прочитать workspace/GOALS.md и workspace/MEMORY.md
echo '{"followupMessage": "Старт сессии: прочитай workspace/BOOTSTRAP.md, workspace/GOALS.md, workspace/MEMORY.md"}'
```

**Стадия 3+** — добавить `beforeSubmitPrompt` (секреты), `beforeShellExecution` (опасные команды). Начинать **audit-only** (fail open); deny — только для явно опасного.

### Skills

| Уровень | Путь | Кто подхватывает |
|---------|------|------------------|
| Встроенные Cursor | `~/.cursor/skills-cursor/` | Cursor (не трогать) |
| Глобальные | `~/.cursor/skills/` | Cursor |
| **Проектные** | `.cursor/skills/<name>/SKILL.md` | Cursor |
| Каталог | `workspace/SKILLS.md` | Агент читает по триггеру |

**Стадия 3:** `workspace/SKILLS.md` + 1 skill в `.cursor/skills/`.

### Commands

| Команда | Назначение |
|---------|------------|
| `@workspace/BOOTSTRAP.md` | Ритуал сессии |
| `@workspace/GOALS.md` `@workspace/MEMORY.md` | Контекст |
| `@starter_kit.md` / GitHub URL kit | Внедрение / эволюция kit |
| `/compact`, `/clear`, новый чат | Управление контекстом |

**Вне scope:** `/loop`, Automations, cron.

### Прочее

| Механизм | Рекомендация |
|----------|--------------|
| User Rules (глобальные) | Общие привычки; проектное — USER.md + rules |
| MCP | Описать в `workspace/TOOLS.md` → `mcp`; секреты не в markdown |
| `.env.example` | `workspace/ENV.md` зеркалит **имена** |

---

## Автономное развитие документов

### В `session_end`

1. `workspace/memory/YYYY-MM-DD.md`
2. `workspace/MEMORY.md` — сжатие
3. `workspace/GOALS.md` — при сдвиге приоритетов
4. `workspace/knowledge/` — черновики (`status: draft`, `source` обязателен)

### Запись в MEMORY.md

```
- ДД.ММ.ГГГГ: <факт>. Причина: <одна строка>.
```

Не писать: предположения, непроверенные гипотезы, секреты.

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
- [ ] `.cursor/rules/security-git.mdc`
- [ ] `.cursor/rules/workspace-isolation.mdc`

**Не создавать:** SOUL, MEMORY, GOALS, knowledge, workspace-read.mdc.

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
- [ ] `.cursor/skills/` — ≥1 skill
- [ ] hooks: секреты + shell (audit-first)
- [ ] `conventions-{lang}.mdc`

---

### Стадия 4 — Зрелость

- [ ] `INDEX.md` (с `starter_kit_version`, `starter_kit_source`)
- [ ] `PLAYBOOK.md`
- [ ] опционально: `examples/`, `STYLE.md`, `IDENTITY.md`, `CONTACTS.md`
- [ ] hook `afterFileEdit` на workspace/memory/knowledge (опционально)

---

### Стадия 5 — Поддержка (ongoing)

- [ ] `GOALS.md` → актуальный `period`
- [ ] `MEMORY.md` → чистка `[устарело]`
- [ ] `knowledge/` → review `updated`
- [ ] rules ↔ `CONSTITUTION.md` — без противоречий
- [ ] `memory/` — логи за последние 7 дней

---

## Чек-лист стадий

**Текущая стадия** = максимальная, где **все** обязательные пункты выполнены и файлы содержат обязательные разделы. Иначе: «N (частично)» — работаем с N, не объявляем N+1.

| Стадия | Условие |
|--------|---------|
| **0** | Аудит выполнен; `workspace/` нет или пуст (кроме `.gitkeep`) |
| **1** | `CONSTITUTION.md` + `AUTONOMY.md` + `security-git.mdc` + `workspace-isolation.mdc` |
| **2** | Стадия 1 + файлы стадии 2 + корневой `AGENTS.md` + `workspace-read.mdc` |
| **3** | Стадия 2 + CONVENTIONS, TOOLS, ENV, SKILLS + `knowledge/INDEX.md` + ≥1 `.cursor/skills/` |
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
| `CONSTITUTION` ↔ `constitution-enforce.mdc` согласованы | ☐ |
| Корневой `AGENTS.md` ≤15 строк, ссылки работают | ☐ |
| `workspace/INDEX.md` содержит `starter_kit_version: "1.4"` и `starter_kit_source` | ☐ |

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
- …
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
1. workspace/GOALS.md
2. workspace/MEMORY.md + workspace/memory/ (7 дней)
3. git status

## session_end
1. workspace/memory/YYYY-MM-DD.md
2. Сжать в workspace/MEMORY.md
3. workspace/GOALS.md при смене фокуса

## before_destructive_action
- force-push, DROP prod — только по явной просьбе
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
```

### `workspace/MEMORY.md`

```markdown
# MEMORY

## decisions

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
1.4

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

## cursor_integrations
- rules: security-git, workspace-isolation, workspace-read, constitution-enforce
- hooks: sessionStart
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
| `starter_kit.md` (локальная копия) | По желанию — канон на GitHub |

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

*Конец starter_kit v1.4*
