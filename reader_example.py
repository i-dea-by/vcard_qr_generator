import csv

from schema import DCvCard


def import_from_csv(filename: str) -> list[DCvCard]:
    """
    Загружает из .csv данные разнося по нужным атрибутам класса DCvCard

    Args:
        filename (str): файл с данными визиток

    Returns:
        list[DCvCard]: список с объектами класса DCvCard
    """
    result = []
    with open(filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            result.append(
                DCvCard(
                    displayname=row["ФИО"].strip(),
                    title=row["Должность"].strip(),
                    cellphone=row["Моб"].strip().replace(" ", "").split("\n"),
                    email=row["Почта"].strip(),
                    workphone=row["Городской"].strip().replace(" ", "").split("\n"),
                    org="ООО Рога и копыта",
                    country="Вейшнория",
                    zipcode="123456",
                    city="г. Задрыпинск",
                    street="ул. Трамповая, д. 12, оф. 6",
                )
            )
    return result
