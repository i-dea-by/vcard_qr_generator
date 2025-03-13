from importlib import import_module
from pathlib import Path
from typing import Literal

import segno
from decouple import config
from loguru import logger as log
from segno import helpers

from schema import DCvCard


def create_qr_files(
    qr_data: list[DCvCard],
    prefix: str,
    postfix: str,
    out_dir: Path,
    ext: Literal["eps", "pdf", "svg", "png"] = "svg",  # другие форматы - см. документацию к segno
    sep: str = "_",
    print_vcard: bool = False,
) -> None:
    """
    Создает QR-коды для каждой карты в списке `qr_data` и сохраняет их в директории `out_dir`.

    Args:
        qr_data (list[DCvCard]): Список для создания QR-кодов.
        prefix (str): Префикс для имени файла.
        postfix (str): Постфикс для имени файла.
        out_dir (Path): Директория для сохранения QR-кодов.
        ext (Literal["eps", "pdf", "svg", "png"], optional): Расширение файла для сохранения QR-кода. По умолчанию "svg".
        sep (str, optional): Разделитель для имени файла. По умолчанию "_".
        print_vcard (bool, optional): Флаг для вывода vCard в лог. По умолчанию False.

    Returns:
        None
    """

    for index, card in enumerate(qr_data, 1):
        vcard_str = helpers.make_vcard_data(**card.to_dict())
        # перед запятыми ставит слэш, оно может почеу-то и надо, но
        # на iPhone когда читает такой QR в строке адреса появляются
        # ненужные символы перед запятыми
        vcard_str = vcard_str.replace("\\", "")
        if print_vcard:
            log.debug("vCard: \n{}", vcard_str)

        qr = segno.make(vcard_str, error="L", encoding="utf-8")

        # если каталога нет то создаем его
        out_dir.mkdir(parents=True, exist_ok=True)

        filename = out_dir / f"{prefix}{sep}{card.displayname}{sep}{postfix}.{ext}"
        qr.save(str(filename), scale=10)
        log.info("[{}/{}] {} - {}", index, len(qr_data), card.displayname, filename)


def main() -> None:
    # Импортируем модуль, имя которого указано в переменной окружения "READER". Если переменная
    # не установлена, то используется значение по умолчанию "reader_example"
    reader_module = str(config("READER", default="reader_example"))
    log.debug("Используем модуль: {!r}", reader_module)
    reader = import_module(reader_module, ".")

    BASE_DIR = Path().parent
    OUT_DIR = BASE_DIR / "out"  # если нужен свой тогда, например, Path("d:/work/vizitki/svg/")
    log.info("Папка для файлов: {}", OUT_DIR.absolute())

    # Берем из .env файла. Пример заполнения в .env.example
    # Если не охота заполнять переменные окружения то можно задать значения прямо в скрипте напрямую
    # например: FILE_PREFIX = "231015" и FILE_POSTFIX = "ru"
    PATH_TO_CSV = Path(str(config("PATH_TO_CSV")))
    log.info("Файл с данными: {}", PATH_TO_CSV)
    FILE_PREFIX = str(config("PREFIX"))
    FILE_POSTFIX = str(config("POSTFIX"))
    # префикс и постфикс нужны для формирования имени файла .svg типа: OUT_DIR/231015_FIO_ru.svg

    cards: list[DCvCard] = reader.import_from_csv(PATH_TO_CSV)

    create_qr_files(
        qr_data=cards,
        prefix=FILE_PREFIX,
        postfix=FILE_POSTFIX,
        out_dir=OUT_DIR,
        ext="svg",
        sep="_",
        print_vcard=False,
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
