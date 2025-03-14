import csv
from pathlib import Path
from typing import Any, Literal

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

    @staticmethod
    def cell_or_none(row: dict, column_name: str | None) -> Any | None:
        """
        Возвращает содержимое ячейки для столбца column_name из строки row.
        Если имя столбца не задано или столбец не существует  возвращает None.
        """
        return None if column_name is None else row.get(column_name)

    @staticmethod
    def fmt(string: str | None, del_spaces: bool = False) -> str | None:
        """
        Возвращает строку string без пробелов в начале и конце.
        Если del_spaces=True, то также удаляет все пробелы внутри строки.
        """
        if string is not None:
            if del_spaces:
                return string.strip().replace(" ", "")
            return string.strip()

    @classmethod
    def from_csv_file(cls, filename) -> list[DCvCard]:
        result = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                result.append(
                    DCvCard(
                        displayname=row[cls.displayname_col].strip(),
                        name=cls.fmt(cls.cell_or_none(row, cls.name_col)),
                        email=cls.fmt(cls.cell_or_none(row, cls.email_col)),
                        phone=cls.fmt(cls.cell_or_none(row, cls.phone_col)),
                        fax=cls.fmt(cls.cell_or_none(row, cls.fax_col)),
                        videophone=cls.fmt(cls.cell_or_none(row, cls.videophone_col)),
                        memo=cls.fmt(cls.cell_or_none(row, cls.memo_col)),
                        nickname=cls.fmt(cls.cell_or_none(row, cls.nickname_col)),
                        birthday=cls.fmt(cls.cell_or_none(row, cls.birthday_col)),
                        url=cls.fmt(cls.cell_or_none(row, cls.url_col)),
                        pobox=cls.fmt(cls.cell_or_none(row, cls.pobox_col)),
                        street=cls.fmt(cls.cell_or_none(row, cls.street_col)),
                        city=cls.fmt(cls.cell_or_none(row, cls.city_col)),
                        region=cls.fmt(cls.cell_or_none(row, cls.region_col)),
                        zipcode=cls.fmt(cls.cell_or_none(row, cls.zipcode_col)),
                        country=cls.fmt(cls.cell_or_none(row, cls.country_col)),
                        org=cls.fmt(cls.cell_or_none(row, cls.org_col)),
                        lat=cls.cell_or_none(row, cls.lat_col),
                        lng=cls.cell_or_none(row, cls.lng_col),
                        source=cls.fmt(cls.cell_or_none(row, cls.source_col)),
                        rev=cls.fmt(cls.cell_or_none(row, cls.rev_col)),
                        title=cls.fmt(cls.cell_or_none(row, cls.title_col)),
                        photo_uri=cls.fmt(cls.cell_or_none(row, cls.photo_uri_col)),
                        cellphone=cls.fmt(cls.cell_or_none(row, cls.cellphone_col)),
                        homephone=cls.fmt(cls.cell_or_none(row, cls.homephone_col)),
                        workphone=cls.fmt(cls.cell_or_none(row, cls.workphone_col)),
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
