import csv
from pathlib import Path
from typing import Literal

import segno
from loguru import logger as log
from segno import helpers

from schema import vCard


class QRcreator:
    """
    Соотносит колонки в файле с полями vCard.

    """

    csv_file: Path
    out_dir: Path

    prefix: str | None = None
    postfix: str | None = None
    ext: Literal["eps", "pdf", "svg", "png"] = "svg"  # другие форматы - см. документацию к segno
    sep: str = "_"

    # колонки в csv файле
    displayname_col: str | None
    name_col = None
    email_col = None
    phone_col = None
    fax_col = None
    videophone_col = None
    memo_col = None
    nickname_col = None
    birthday_col = None
    url_col = None
    pobox_col = None
    street_col = None
    city_col = None
    region_col = None
    zipcode_col = None
    country_col = None
    org_col = None
    lat_col = None
    lng_col = None
    source_col = None
    rev_col = None
    title_col = None
    photo_uri_col = None
    cellphone_col = None
    homephone_col = None
    workphone_col = None

    def __init__(self, file_path):
        self.file_path = file_path

    @classmethod
    def from_csv_file(cls, filename: Path) -> list[vCard]:
        """
        Считывает данные из CSV файла и создает список объектов DCvCard.
        """
        result = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                vcard_data = {
                    field: row.get(getattr(cls, f"{field}_col"))
                    for field in vCard.model_fields.keys()
                    if getattr(cls, f"{field}_col") is not None
                }
                result.append(vCard(**vcard_data))  # type: ignore
        return result

    @classmethod
    def create_qr_files(
        cls,
        error_correction_level: Literal["L", "M", "Q", "H"] = "L",
        log_vcard: bool = False,
    ) -> None:
        """
        Создает QR-коды и сохраняет их

        Args:
            error_correction_level ("L", "M", "Q", "H") : Уровень коррекции ошибок. По умолчанию "L". Подробнее см. https://segno.readthedocs.io/en/latest/api.html#segno.make.params.error

            log_vcard (bool): Выводить ли в лог текст vCard. По умолчанию False.
        """
        if cls.csv_file is None:
            raise ValueError(
                "Файл с данными CSV не указан. Используйте метод from_csv_file "
                "или установите csv_file в классе."
            )
        contact_data = cls.from_csv_file(cls.csv_file)
        for index, card in enumerate(contact_data, 1):
            vcard_str = helpers.make_vcard_data(**card.model_dump(exclude_unset=True))
            # перед запятыми ставит слэш, оно может почеу-то и надо, но
            # на iPhone когда читает такой QR в строке адреса появляются
            # ненужные символы перед запятыми
            vcard_str = vcard_str.replace("\\", "")
            if log_vcard:
                log.debug("vCard: \n{}", vcard_str)

            qr = segno.make(vcard_str, error=error_correction_level, encoding="utf-8")

            # если каталога нет то создаем его
            cls.out_dir.mkdir(parents=True, exist_ok=True)

            filename = (
                cls.out_dir
                / f"{cls.prefix}{cls.sep}{card.displayname}{cls.sep}{cls.postfix}.{cls.ext}"
            )
            qr.save(str(filename), scale=10)
            log.info("[{}/{}] {} - {}", index, len(contact_data), card.displayname, filename.name)
