import csv
from pathlib import Path
from typing import Literal

import segno
from loguru import logger as log
from segno import helpers

from schema import DCvCard


class csvReaderColumns:
    """
    Соотносит колонки в файле с полями vCard.

    """
    # колонки в csv файле
    displayname_col: str
    name_col: str | None = None
    email_col: str | None = None
    phone_col: str | None = None
    fax_col: str | None = None
    videophone_col: str | None = None
    memo_col: str | None = None
    nickname_col: str | None = None
    birthday_col: str | None = None
    url_col: str | None = None
    pobox_col: str | None = None
    street_col: str | None = None
    city_col: str | None = None
    region_col: str | None = None
    zipcode_col: str | None = None
    country_col: str | None = None
    org_col: str | None = None
    lat_col: str | None = None
    lng_col: str | None = None
    source_col: str | None = None
    rev_col: str | None = None
    title_col: str | None = None
    photo_uri_col: str | None = None
    cellphone_col: str | None = None
    homephone_col: str | None = None
    workphone_col: str | None = None

    csv_file: str | None = None

    def __init__(self, file_path):
        self.file_path = file_path

    @classmethod
    def from_csv_file(cls, filename) -> list[DCvCard]:
        result = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                result.append(
                    DCvCard(
                        displayname=row[cls.displayname_col],
                        name=None if cls.name_col is None else row[cls.name_col],
                        email=None if cls.email_col is None else row[cls.email_col],
                        phone=None if cls.phone_col is None else row[cls.phone_col],
                        fax=None if cls.fax_col is None else row[cls.fax_col],
                        videophone=None if cls.videophone_col is None else row[cls.videophone_col],
                        memo=None if cls.memo_col is None else row[cls.memo_col],
                        nickname=None if cls.nickname_col is None else row[cls.nickname_col],
                        birthday=None if cls.birthday_col is None else row[cls.birthday_col],
                        url=None if cls.url_col is None else row[cls.url_col],
                        pobox=None if cls.pobox_col is None else row[cls.pobox_col],
                        street=None if cls.street_col is None else row[cls.street_col],
                        city=None if cls.city_col is None else row[cls.city_col],
                        region=None if cls.region_col is None else row[cls.region_col],
                        zipcode=None if cls.zipcode_col is None else row[cls.zipcode_col],
                        country=None if cls.country_col is None else row[cls.country_col],
                        org=None if cls.org_col is None else row[cls.org_col],
                        lat=None if cls.lat_col is None else float(row[cls.lat_col]),
                        lng=None if cls.lng_col is None else float(row[cls.lng_col]),
                        source=None if cls.source_col is None else row[cls.source_col],
                        rev=None if cls.rev_col is None else row[cls.rev_col],
                        title=None if cls.title_col is None else row[cls.title_col],
                        photo_uri=None if cls.photo_uri_col is None else row[cls.photo_uri_col],
                        cellphone=None if cls.cellphone_col is None else row[cls.cellphone_col],
                        homephone=None if cls.homephone_col is None else row[cls.homephone_col],
                        workphone=None if cls.workphone_col is None else row[cls.workphone_col],
                    )
                )
        return result

    @classmethod
    def read_csv(cls) -> list[DCvCard]:
        if cls.csv_file:
            return cls.from_csv_file(cls.csv_file)
        raise ValueError(
            "Файл с данными CSV не указан. Используйте метод from_csv_file "
            "или установите csv_file в классе."
        )


def create_qr_files(
    qr_data: list[DCvCard],
    prefix: str,
    postfix: str,
    out_dir: Path,
    ext: Literal["eps", "pdf", "svg", "png"] = "svg",  # другие форматы - см. документацию к segno
    sep: str = "_",
    log_vcard: bool = False,
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
        log_vcard (bool, optional): Флаг для вывода vCard в лог. По умолчанию False.

    Returns:
        None
    """

    for index, card in enumerate(qr_data, 1):
        vcard_str = helpers.make_vcard_data(**card.to_dict())
        # перед запятыми ставит слэш, оно может почеу-то и надо, но
        # на iPhone когда читает такой QR в строке адреса появляются
        # ненужные символы перед запятыми
        vcard_str = vcard_str.replace("\\", "")
        if log_vcard:
            log.debug("vCard: \n{}", vcard_str)

        qr = segno.make(vcard_str, error="L", encoding="utf-8")

        # если каталога нет то создаем его
        out_dir.mkdir(parents=True, exist_ok=True)

        filename = out_dir / f"{prefix}{sep}{card.displayname}{sep}{postfix}.{ext}"
        qr.save(str(filename), scale=10)
        log.info("[{}/{}] {} - {}", index, len(qr_data), card.displayname, filename.name)
