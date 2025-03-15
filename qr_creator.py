import csv
from pathlib import Path
from typing import Any, Literal

import segno
from loguru import logger as log
from segno import helpers

from schema import DCvCard


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
    def from_csv_file(cls, filename: Path) -> list[DCvCard]:
        result = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                vcard_data = {
                    field: row.get(getattr(cls, f"{field}_col"))
                    for field in DCvCard.model_fields.keys()
                    if getattr(cls, f"{field}_col") is not None
                }
                result.append(DCvCard(**vcard_data))  # type: ignore
        return result

    @classmethod
    def create_qr_files(
        cls,
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

            qr = segno.make(vcard_str, error="L", encoding="utf-8")

            # если каталога нет то создаем его
            cls.out_dir.mkdir(parents=True, exist_ok=True)

            filename = (
                cls.out_dir
                / f"{cls.prefix}{cls.sep}{card.displayname}{cls.sep}{cls.postfix}.{cls.ext}"
            )
            qr.save(str(filename), scale=10)
            log.info("[{}/{}] {} - {}", index, len(contact_data), card.displayname, filename.name)
