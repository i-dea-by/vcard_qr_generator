from datetime import date
from typing import Any, Iterable

from pydantic import BaseModel, field_serializer


class DCvCard(BaseModel):
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
    lat: str | float | None = None
    lng: str | float | None = None
    source: str | None = None
    rev: str | date | None = None
    title: str | Iterable[str] | None = None
    photo_uri: str | Iterable[str] | None = None
    cellphone: str | Iterable[str] | None = None
    homephone: str | Iterable[str] | None = None
    workphone: str | Iterable[str] | None = None

    def model_post_init(self, __context: Any) -> None:
        if self.name is None:
            self.name = self.displayname.replace(" ", ";")

    @field_serializer(
        "email",
        "phone",
        "fax",
        "videophone",
        "url",
        "title",
        "photo_uri",
        "cellphone",
        "homephone",
        "workphone",
        mode="plain",
    )
    def str_or_list_serialazer(self, value: str | Iterable[str] | None) -> list | None:
        if isinstance(value, str):
            if "," in value:
                return value.split(",")
            if ";" in value:
                return value.split(";")
            return [value]
        elif isinstance(value, Iterable):
            return list(value)

    @field_serializer("lat", "lng", when_used="json", mode="plain")
    def float_serialazer(self, value: Any) -> float | None:
        if value is not None:
            return float(value)
