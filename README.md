# Telegram Reminder & Screenshot Bot

## Описание

Бот для Telegram, который:
- отправляет напоминания по расписанию,
- принимает скриншоты,
- генерирует отчёты по скринам за разные периоды,
- работает только для разрешённых пользователей (whitelist),
- хранит данные и изображения в Supabase (Postgres + Storage),
- готов к запуску на render.com.

## Быстрый старт

### 1. Клонируйте репозиторий и настройте окружение

```bash
git clone https://github.com/yourusername/reminder-bot.git
cd reminder-bot
cp .env.example .env
# Заполните .env своими данными
```

### 2. Настройте Supabase

- Создайте проект на https://supabase.com
- Создайте таблицы:
    - `users` (user_id: bigint, username: text, is_admin: bool)
    - `reminders` (id: serial, user_id: bigint, type: text, time: time, date: date, days_of_week: text[], interval_min: int, active: bool)
    - `screenshots` (id: serial, user_id: bigint, file_url: text, added_at: timestamp)
    - `reminder_responses` (id: serial, reminder_id: int, user_id: bigint, screenshot_id: int, replied_at: timestamp)
- Создайте bucket `screenshots` в Storage.

### 3. Залейте на GitHub и разверните на render.com

- Создайте новый Web Service на Render.
- Укажите команду запуска:  
  ```bash
  python -m app.main
  ```
- Укажите переменные из `.env` в настройках Render.

### 4. Установите зависимости и запустите локально (по желанию)

```bash
pip install -r requirements.txt
python -m app.main
```

## Основные команды бота

- `/start` — начать работу, показать все команды
- `/info` — справка по командам
- `/reminder_add` — добавить напоминание
- `/reminder_edit` — изменить напоминание
- `/reminder_delete` — удалить напоминание
- `/report_day` — отчёт по скринам за день
- `/report_week` — отчёт за неделю
- `/report_month` — отчёт за месяц
- `/report_user` — отчёт по выбранному диапазону дат
- `/report_use` — отчёт за всё время
- `/debug` — статистика (скринов, напоминаний, ответов)
- `/adduser` — добавить пользователя (только для админа)
- `/removeuser` — удалить пользователя (только для админа)
- `/listusers` — список разрешённых пользователей

## Важно

- Бот работает только для разрешённых пользователей.
- Скриншоты хранятся в Supabase Storage, доступ по ссылке.
- Рекомендуется использовать webhook для Render.

---