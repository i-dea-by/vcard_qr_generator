from datetime import datetime
from pathlib import Path

from decouple import config
from loguru import logger as log

from services import QRcreator

BASE_DIR = Path().parent


class ExampleQRcreator(QRcreator):
    # если в .env файле указан свой файл то используется он, если нет,
    # то используется "./example.csv". можно и прямо указать
    # и свой путь Path("d:/work/vizitki/data.csv")
    csv_file = Path(str(config("PATH_TO_CSV", default="./example.csv")))

    # префикс и постфикс нужны для формирования имени файла .svg типа: OUT_DIR/231015_FIO_ru.svg
    # они берутся из переменных окружения (или файла .env), если не указаны, то берутся
    # значения по умолчанию: для префикса дата в виде YYMMDD, а для постфикса - ru
    prefix = str(config("PREFIX", default=datetime.now().strftime("%y%m%d")))
    postfix = str(config("POSTFIX", default="ru"))
    # или указать напрямую
    # prefix = "250316"
    # postfix = "ru"

    # папка для файлов изображений, если нужна другая, то указать напрямую
    out_dir = BASE_DIR / "out"  # или Path("d:/work/vizitki/svg/")

    # соотносим колонки в файле с полями vCard
    displayname_col = "ФИО"
    title_col = "Должность"
    cellphone_col = "Моб"
    workphone_col = "Городской"
    email_col = "Почта"


def main() -> None:
    log.info("Файл с данными: {}", ExampleQRcreator.csv_file.absolute())
    log.info("Папка для .svg файлов: {}", ExampleQRcreator.out_dir.absolute())

    ExampleQRcreator.create_qr_files(log_vcard=False)


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
