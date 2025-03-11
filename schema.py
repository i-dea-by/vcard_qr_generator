from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass
class DCvCard:
    """
    https://ru.wikipedia.org/wiki/VCard
    """

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
    lat: float | None = None
    lng: float | None = None
    source: str | None = None
    rev: str | date | None = None
    title: str | Iterable[str] | None = None
    photo_uri: str | Iterable[str] | None = None
    cellphone: str | Iterable[str] | None = None
    homephone: str | Iterable[str] | None = None
    workphone: str | Iterable[str] | None = None

    def __post_init__(self):
        if self.name is None:
            self.name = self.displayname.replace(" ", ";")

    def to_dict(self):
        _dict = {key: value for key, value in self.__dict__.items() if value is not None}
        return _dict

    def __str__(self):
        return f"<vCard {self.displayname}>"
