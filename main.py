from datetime import datetime
from pathlib import Path

from loguru import logger as log

from qr_creator import QRcreator

BASE_DIR = Path().parent


class ExampleQRcreator(QRcreator):
    csv_file = Path("./example.csv")

    # префикс и постфикс нужны для формирования имени файла .svg типа: OUT_DIR/231015_FIO_ru.svg
    prefix = datetime.now().strftime("%y%m%d")
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

    # Для полей email, phone, fax, videophone, url, title, photo_uri, cellphone, homephone, workphone
    # допускается несколько значений через "," или ";"


def main() -> None:
    log.info("Файл с данными: {}", ExampleQRcreator.csv_file.absolute())
    log.info("Папка для .svg файлов: {}", ExampleQRcreator.out_dir.absolute())

    ExampleQRcreator.create_qr_files(error_correction_level="L", log_vcard=False)


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
