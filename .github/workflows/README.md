# GitHub Actions Workflows

## tests.yml

Этот workflow автоматически запускает тесты и публикует Allure отчеты на GitHub Pages.

### Что делает workflow:

1. **Job `test`**:
   - Устанавливает Python 3.12
   - Устанавливает зависимости через `uv`
   - Устанавливает Playwright и браузеры
   - **Запускает все тесты** с генерацией Allure результатов
   - Загружает артефакты (Allure результаты и coverage отчеты)

2. **Job `publish`** (только для `main`/`master` веток):
   - Скачивает Allure результаты из job `test`
   - Устанавливает Allure commandline tool
   - Генерирует HTML отчет Allure
   - Публикует отчет на GitHub Pages

### Триггеры:

- Push в ветки `main`, `master`, `develop`
- Pull Request в эти ветки
- Ручной запуск через `workflow_dispatch`

### Просмотр отчетов:

После успешного выполнения workflow:
- Отчеты доступны на: `https://<username>.github.io/<repo-name>/`
- Артефакты можно скачать в разделе **Actions** → выберите workflow run → **Artifacts**

### Важно:

- Тесты **обязательно запускаются** в job `test`
- Отчеты публикуются только для веток `main` и `master`
- Если тесты упадут, отчет все равно будет опубликован (с информацией об ошибках)

