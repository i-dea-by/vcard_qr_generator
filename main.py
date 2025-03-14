from datetime import datetime
from pathlib import Path

from decouple import config
from loguru import logger as log

from services import create_qr_files, csvReaderColumns

BASE_DIR = Path().parent
OUT_DIR = BASE_DIR / "out"  # если нужен свой тогда, например, Path("d:/work/vizitki/svg/")
# префикс и постфикс нужны для формирования имени файла .svg типа: OUT_DIR/231015_FIO_ru.svg
# они берутся из переменных окружения (или файла .env), если не указаны, то берутся
# значения по умолчанию: для префикса дата в виде YYMMDD, а для постфикса - ru
FILE_PREFIX = str(config("PREFIX", default=datetime.now().strftime("%y%m%d")))
FILE_POSTFIX = str(config("POSTFIX", default="ru"))


class ExampleReader(csvReaderColumns):
    # если в .env файле указан свой файл то используется он, если нет,
    # то используется "./example.csv". можно и прямо указать и свой путь "d:/work/vizitki/data.csv"
    csv_file = str(config("PATH_TO_CSV", default="./example.csv"))

    # соотносим колонки в файле с полями vCard
    displayname_col = "ФИО"
    title_col = "Должность"
    cellphone_col = "Моб"
    workphone_col = "Городской"
    email_col = "Почта"


def main() -> None:
    log.info("Файл с данными: {}", ExampleReader.csv_file)
    log.info("Папка для .svg файлов: {}", OUT_DIR.absolute())

    # .read_csv() - читает файл указанный при инициализации класса
    # можно указать прямо используя метод .from_csv_file("путь/к/файлу.csv")
    cards = ExampleReader.read_csv()

    create_qr_files(
        qr_data=cards,
        prefix=FILE_PREFIX,
        postfix=FILE_POSTFIX,
        out_dir=OUT_DIR,
        ext="svg",
        sep="_",
        log_vcard=False,
    )


if __name__ == "__main__":
    main()

    """
        L recovers 7% of data
        M recovers 15% of data
        Q recovers 25% of data
        H recovers 30% of data

    Возможно с русским поможет
        BEGIN:VCARD
        VERSION:3.0
        N;CHARSET=UTF-8:ФИРМА.РФ
        FN;CHARSET=UTF-8:ФИРМА.РФ
        TEL:+7123456789
        EMAIL:info@info.ru
        ORG;CHARSET=UTF-8:Название фирмы
        URL;CHARSET=UTF-8:http://фирма.рф
        NOTE:https://instagram.com/name
        END:VCARD
    """
