# Генератор QR-кодов для визитных карточек (vCard)

Этот проект представляет собой простой скрипт на Python для генерации изображений QR-кодов, содержащих информацию контактных данных в формате vCard. QR-коды сохраняются в различных графических форматах (например, SVG, PNG, PDF, EPS).

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/i-dea-by/vcard_qr_generator.git
   cd vcard_qr_generator
   ```

2. Установите необходимые зависимости:

    - если используете pip
        ```bash
        pip install -r requirements.txt
        ```
    - тут используется uv, тогда:
        ```bash
        uv sync
        ```


## Использование

1. Подготовьте CSV-файл с данными для визитных карточек. Пример формата CSV можно найти в data/example.csv.

2. Настройка производится через аргументы класса. Думаю в примере всё понятно расписано:

    ```python
    class ExampleQRcreator(QRcreator):
        csv_file = Path("./example.csv")

        # префикс и постфикс нужны для формирования имени файла .svg типа: OUT_DIR/231015_FIO_ru.svg
        prefix = datetime.now().strftime("%y%m%d")  # дата вида 250316
        postfix = "ru"

        # папка для файлов изображений, если нужна другая, то указать напрямую
        out_dir = BASE_DIR / "out"  # или Path("d:/work/vizitki/svg/")
        # формат изображения, другие возможные варианты - png/svg/pdf/eps
        ext = "svg"  # svg - по умолчанию

        # соотносим колонки в файле с полями vCard
        displayname_col = "ФИО"
        title_col = "Должность"
        cellphone_col = "Моб"
        workphone_col = "Городской"
        email_col = "Почта"

        # соотношение (маппинг) поля vCard с колонками в csv файле строится по такому принципу:
        # смотрим подходящее поле в vCard, например, title ("Должность" в csv файле),
        # дописываем ему _col, получаем title_col и через = пишем то, название колонки из csv файла:
        # title_col = "Должность"

        # Для полей email, phone, fax, videophone, url, title, photo_uri, cellphone, homephone,
        # workphone допускается несколько значений через "," или ";"
    ```

    Весь набор полей vCard:
    ```python
    # FN - Полное имя в виде единой строки без разделителей
    displayname: str
    # N - фамилия; имя; отчество (дополнительные имена); префиксы; суффиксы
    name: str | None = None
    email: str | Iterable[str] | None = None
    phone: str | Iterable[str] | None = None
    fax: str | Iterable[str] | None = None
    videophone: str | Iterable[str] | None = None
    memo: str | None = None
    nickname: str | None = None
    birthday: str | date | None = None
    url: str | Iterable[str] | None = None
    # ADR (pobox, street, city, region, zipcode, country)
    pobox: str | None = None  # P.O. box (address information).
    street: str | None = None  # Street address.
    city: str | None = None  # City (address information).
    region: str | None = None  # Region (address information).
    zipcode: str | None = None  # Zip code (address information).
    country: str | None = None  # Country (address information).
    org: str | None = None
    lat: str | float | None = None
    lng: str | float | None = None
    source: str | None = None
    rev: str | date | None = None
    title: str | Iterable[str] | None = None
    photo_uri: str | Iterable[str] | None = None
    cellphone: str | Iterable[str] | None = None
    homephone: str | Iterable[str] | None = None
    workphone: str | Iterable[str] | None = None
    ```
> [!WARNING]
> ACHTUNG!Алярма!!11 Если не используете uv, то не забудьте создать и активировать виртуальное окружение. Если конечно не ставите всё это в рутовый питон (:
3. Запустите скрипт:

    ```bash
    python main.py
    ```

    или с использованием uv:

    ```bash
    uv run main.py
    ```

Скрипт создаст QR-коды для каждой визитной карточки и сохранит их в папку out/.


## Зависимости

- segno: Для генерации QR-кодов.

- loguru: Для логирования.


## Особенности текста коммитов

```
+ <текст> - добавил
- <текст> - убрал, удалил
* <текст> - изменил
upd - изменение не достойное упоминания - ошибки в тексте, опечатки и тд
fix <текст> - бакгфикс, испрвление ошибки
refactor - разнос по отдельным модулям
reformat - переформатирование по black, например
```

## Лицензия

Этот проект распространяется под лицензией MIT.
