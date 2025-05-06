import random
from datetime import datetime, timedelta
from string import ascii_lowercase, digits


# Пока хардкод, т.к. неизвестны msisdn "Ромашки", при реальной генерации внутри функции будет запрос к БД
def get_romashka_msisdn() -> list[str]:
    return ["79876543221", "79123219841", "76123456789", "71123219841", "72113214841", "79138129801", "77771234567"]

# msisdn "Ромашки" с тарифом "Классика" (при реальной генерации внутри функции будет запрос к БД)
def get_romashka_classika_msisdn() -> list[str]:
    return ["79876543221", "79123219841", "76123456789"]

# msisdn "Ромашки" с тарифом "Помесячный" остатком минут > 1 (при реальной генерации внутри функции будет запрос к БД)
def get_romashka_pomesyachny_with_rest_msisdn() -> list[str]:
    return ["71123219841", "72113214841"]

# msisdn "Ромашки" с тарифом "Помесячный" пустым остатком минут (при реальной генерации внутри функции будет запрос к БД)
def get_romashka_pomesyachny_with_no_rest_msisdn() -> list[str]:
    return ["79138129801", "77771234567"]

# Словарь с ключом msisdn и значением - датой начала расчётного периода
def get_pomesyachny_subscribers_info() -> dict:
    return {"71123219841": datetime(2023, 6, 10, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)),
            "72113214841": datetime(2023, 6, 15, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)),
            "79138129801": datetime(2023, 6, 21, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)),
            "77771234567": datetime(2023, 6, 5, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))}

# Словарь с ключом msisdn и значением - датой регистрации абонента
def get_classica_subscribers_info() -> dict:
    return {"79876543221": datetime(2023, 5, 3, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)),
            "79123219841": datetime(2023, 1, 11, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)),
            "76123456789": datetime(2022, 12, 4, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))}

# Тоже харкод, при реальной генерации внутри функции будет запрос к БД
def get_call_types() -> list[str]:
    return ["01", "02"]


# Генерация случайного года из уже полностью прошедших
def get_random_year_from_past(from_year: int = 1990) -> int:
    return random.randint(from_year, datetime.now().year - 1)

# Генерация случайного года из будущего
def get_random_year_from_future(to_year: int = 2035) -> int:
    return random.randint(datetime.now().year + 1, to_year)

# Генерация случайного msisdn
def get_random_msisdn() -> str:
    # В данном случае генерируется случайный msisdn из 11 цифр, начинающийся с 7
    return str(random.randint(71111111111, 79999999999))

# Выбор двух случайных msisdn
def choose_two_random_msisdn(msisdn_pack1: list[str] | None, msisdn_pack2: list[str] | None, msisdn_romashka: list[str]) -> tuple[str, str]:
    if msisdn_pack1:
        selected_served_msisdn = random.choice(msisdn_pack1)
    else:
        selected_served_msisdn = get_random_msisdn()
    if msisdn_pack2:
        selected_second_msisdn = random.choice(msisdn_pack2)
        while selected_served_msisdn == selected_second_msisdn:
            selected_second_msisdn = random.choice(msisdn_pack2)
    else:
        selected_second_msisdn = get_random_msisdn()
        while selected_served_msisdn == selected_second_msisdn or selected_second_msisdn in msisdn_romashka:
            selected_second_msisdn = get_random_msisdn()
    return (selected_served_msisdn, selected_second_msisdn)

# Выбор одного случайного msisdn абонента "Ромашки"
def choose_one_random_romashka(msisdn_romashka: list[str]) -> str:
    return random.choice(msisdn_romashka)

# Случайный выбор последовательности из двух типов звонка (Исх->Вх или Вх->Исх)
def choose_two_call_types_randomly(call_types: list[str]) -> tuple[str, str]:
    selected_call_type1 = random.choice(call_types)
    index = abs(
        call_types.index(selected_call_type1) - 1
    )  # Если выбран первый элемент, то выбираем нулевой и наоборот
    selected_call_type2 = call_types[index]
    return (selected_call_type1, selected_call_type2)

# Случайный выбор одного из типов звонка (Исх/Вх)
def choose_call_type_randomly(call_types: list[str]) -> str:
    return random.choice(call_types)

# Запись в файл .csv тестовых данных, test_id - идентификатор тест-кейса, будет передан в название файла
def write_to_csv(test_id: str, call_records: list):
    with open("test_data/" + test_id +"_testdata.csv", "w", newline="") as csvfile:
        csvfile.write("\n".join(",".join(cdr) for cdr in call_records))

# Генерация случайного msisdn, не являющегося абонентом "Ромашки"
def gen_msisdn_non_romashka(msisdn_romashka: list[str]) -> str:
    random_msisdn = get_random_msisdn()
    while random_msisdn in msisdn_romashka:
        random_msisdn = get_random_msisdn()
    return random_msisdn


# Тест TUCBRT01: CDR-файл с корректными звонками абонентов "Ромашки"
def gen_TUCBRT01(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    # Пусть первый звонок начинается 31 декабря в 0:00
    test_year = get_random_year_from_past()
    call_start_dt = datetime(test_year, 12, 31, 0, 0, 0)
    # Сгенерируем 3 звонка от абонента "Ромашки" абоненту "Ромашки", на каждый исходящий звонок сгенерируем парный входящий
    for i in range(3):
        # Выберем двух разных абонентов "Ромашки"
        chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
        chosen_call_types = choose_two_call_types_randomly(call_types)
        # Генерируем время окончания звонка
        if i == 0:
            # Самый первый звонок длится не больше минуты
            call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 59))
        else:
            # Последующие звонки длятся от 1 секунды до 2 часов
            call_end_dt = call_start_dt + timedelta(
                seconds=random.randint(1, 2 * 60 * 60)
            )
        # Две парные записи о звонке
        call_records.append(
            [
                chosen_call_types[0],
                chosen_romashka[0],
                chosen_romashka[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )
        call_records.append(
            [
                chosen_call_types[1],
                chosen_romashka[1],
                chosen_romashka[0],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )

        # Смещаем время начала звонка относительно предыдущего на произвольное значение от 1 секунды до 3 часов
        call_start_dt += timedelta(seconds=random.randint(1, 3 * 60 * 60))

    # Последние 4 записи в CDR-файле проверяют переход через полночь
    call_start_dt = datetime(test_year, 12, 31, 23, 0, 0) + timedelta(
        seconds=random.randint(30 * 60, 59 * 60)
    )
    call_end_dt = call_start_dt + timedelta(seconds=random.randint(30 * 60, 60 * 60))
    # Пусть звонок совершат те же абоненты, что и в предыдущей строке CDR-файла
    call_records.append(
        [
            chosen_call_types[0],
            chosen_romashka[0],
            chosen_romashka[1],
            call_start_dt.isoformat(),
            datetime(test_year, 12, 31, 23, 59, 59).isoformat(),
        ]
    )
    call_records.append(
        [
            chosen_call_types[1],
            chosen_romashka[1],
            chosen_romashka[0],
            call_start_dt.isoformat(),
            datetime(test_year, 12, 31, 23, 59, 59).isoformat(),
        ]
    )
    call_records.append(
        [
            chosen_call_types[0],
            chosen_romashka[0],
            chosen_romashka[1],
            datetime(test_year + 1, 1, 1, 0, 0, 0).isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    call_records.append(
        [
            chosen_call_types[1],
            chosen_romashka[1],
            chosen_romashka[0],
            datetime(test_year + 1, 1, 1, 0, 0, 0).isoformat(),
            call_end_dt.isoformat(),
        ]
    )

    # Сформируем CDR-файл
    write_to_csv("TUCBRT01", call_records)

# Тест TUCBRT02: CDR-файл с корректными звонками абонентов другого оператора
def gen_TUCBRT02(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    # Пусть первый звонок начинается в 0:00:00
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 11)
    test_day = random.randint(1, 27)
    call_start_dt = datetime(test_year, test_month, test_day, 0, 0, 0)
    # Сгенерируем 8 звонков между абонентами другого оператора
    for _ in range(8):
        # Выбираем двух разных абонентов другого оператора
        random_msisdn = choose_two_random_msisdn(None, None, msisdn_romashka)
        chosen_call_type = choose_call_type_randomly(call_types)
        # Генерируем время окончания звонка
        call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 2 * 60 * 60))

        call_records.append(
            [
                chosen_call_type,
                random_msisdn[0],
                random_msisdn[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )
        # Смещаем время начала звонка относительно предыдущего на произвольное значение от 1 секунды до 3 часов
        call_start_dt += timedelta(seconds=random.randint(1, 3 * 60 * 60))

    call_start_dt = datetime(test_year, test_month, test_day, 23, 0, 0) + timedelta(
        seconds=random.randint(30 * 60, 59 * 60)
    )
    call_end_dt = call_start_dt + timedelta(seconds=random.randint(30 * 60, 60 * 60))

    call_records.append(
        [
            chosen_call_type,
            random_msisdn[0],
            random_msisdn[1],
            call_start_dt.isoformat(),
            datetime(test_year, test_month, test_day, 23, 59, 59).isoformat(),
        ]
    )
    call_records.append(
        [
            chosen_call_type,
            random_msisdn[0],
            random_msisdn[1],
            datetime(test_year, test_month, test_day + 1, 0, 0, 0).isoformat(),
            call_end_dt.isoformat(),
        ]
    )

    # Сформируем CDR-файл
    write_to_csv("TUCBRT02", call_records)

# Тест TUCBRT03: CDR-файл с пустыми значениями некоторых полей
def gen_TUCBRT03(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 11)
    test_day = random.randint(1, 27)
    call_start_dt = datetime(
        test_year,
        test_month,
        test_day,
        random.randint(0, 18),
        random.randint(0, 59),
        random.randint(0, 59),
    )
    for _ in range(5):
        # Выберем двух разных абонентов "Ромашки"
        chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
        chosen_call_types = choose_two_call_types_randomly(call_types)
        # Генерируем время окончания звонка
        call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 2 * 60 * 60))
        # Две парные записи о звонке
        call_records.append(
            [
                chosen_call_types[0],
                chosen_romashka[0],
                chosen_romashka[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )
        call_records.append(
            [
                chosen_call_types[1],
                chosen_romashka[1],
                chosen_romashka[0],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )

        # Смещаем время начала звонка относительно предыдущего на произвольное значение от 1 секунды до 1 часа
        call_start_dt += timedelta(seconds=random.randint(1, 60 * 60))

    # Формируем индексы для удаления значений полей (в первых 5 строках будет удалено какое-то 1 значение,
    # далее в двух строках 2 поля, в оставшихся 3/10 строках будет удалено 3, 4 и все 5 значений)
    indexes_to_delete = [
        *([i] for i in range(5)),
        [0, 1],
        [1, 2],
        [1, 2, 3],
        [1, 2, 3, 4],
        [0, 1, 2, 3, 4],
    ]
    # Удаляем значения по индексам
    for indexes, cdr in zip(indexes_to_delete, call_records):
        for index in indexes:
            cdr[index] = ""

    # Сформируем CDR-файл
    write_to_csv("TUCBRT03", call_records)

# Тест TUCBRT04: CDR-файл с некорректными типами звонка
def gen_TUCBRT04(msisdn_romashka: list[str], call_types: list[str]):
    # Сформируем список некорректных типов звонка
    strange_call_types = [
        choose_call_type_randomly(call_types) + random.choice(digits),
        "03",
        str(random.randint(0, 100)),
        random.choice(ascii_lowercase),
        choose_call_type_randomly(call_types) + random.choice(ascii_lowercase),
        random.choice(ascii_lowercase) + choose_call_type_randomly(call_types),
        choose_call_type_randomly(call_types)
        + " "
        + "".join(random.choices(ascii_lowercase, k=2)),
        choose_call_type_randomly(call_types) + "$",
        "?" + choose_call_type_randomly(call_types),
        choose_call_type_randomly(call_types) + ".",
    ]
    call_records = []
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 28)
    # Дата и время начала звонка
    call_start_dt = datetime(
        test_year,
        test_month,
        test_day,
        random.randint(0, 18),
        random.randint(0, 59),
        random.randint(0, 59),
    )
    for i in range(10):
        # Выберем двух разных абонентов "Ромашки"
        chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
        # Генерируем время окончания звонка
        call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 2 * 60 * 60))

        call_records.append(
            [
                strange_call_types[i],
                chosen_romashka[0],
                chosen_romashka[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )

        call_start_dt += timedelta(seconds=random.randint(1, 60 * 60))

    write_to_csv("TUCBRT04", call_records)

# Тест TUCBRT05: CDR-файл со звонками отрицательной продолжительности
def gen_TUCBRT05(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 28)
    # Пусть первый звонок закончится в 0:00
    call_end_dt = datetime(test_year, test_month, test_day, 0, 0, 0)
    call_start_dt = call_end_dt + timedelta(seconds=random.randint(1, 30 * 60))
    for i in range(10):
        # Выбрать двух разных абонентов "Ромашки"
        chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
        chosen_call_types = choose_two_call_types_randomly(call_types)
        # Генерируем время окончания звонка
        if i:
            call_end_dt = call_start_dt - timedelta(seconds=random.randint(1, 30 * 60))

        call_records.append(
            [
                chosen_call_types[0],
                chosen_romashka[0],
                chosen_romashka[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )
        # Перед последней итерацией установим время конца звонка 23:59:59
        if i < 8:
            call_start_dt += timedelta(seconds=random.randint(30 * 60, 2 * 60 * 60))
        else:
            call_start_dt = datetime(test_year, test_month, test_day, 23, 59, 59)

    write_to_csv("TUCBRT05", call_records)

# Тест TUCBRT06: CDR-файл со звонками абонента самому себе
def gen_TUCBRT06(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 27)

    call_start_dt = datetime(test_year, test_month, test_day, 0, 0, 0)

    for _ in range(8):
        # Выбрать абонента "Ромашки"
        chosen_romashka = choose_one_random_romashka(msisdn_romashka)
        chosen_call_types = choose_call_type_randomly(call_types)
        # Генерируем время окончания звонка
        call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 60 * 60))
        call_records.append(
            [
                chosen_call_types,
                chosen_romashka,
                chosen_romashka,
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )

        call_start_dt += timedelta(seconds=random.randint(1, 2 * 60 * 60))

    # Последние две записи относятся к одному звонку, перешедшему за полночь
    chosen_call_types = choose_two_call_types_randomly(call_types)

    call_start_dt = datetime(test_year, test_month, test_day, 23, 0, 0) + timedelta(
        seconds=random.randint(30 * 60, 59 * 60)
    )
    call_end_dt = call_start_dt + timedelta(seconds=random.randint(31 * 60, 60 * 60))
    call_records.append(
        [
            chosen_call_types[0],
            chosen_romashka,
            chosen_romashka,
            call_start_dt.isoformat(),
            datetime(test_year, test_month, test_day, 23, 59, 59).isoformat(),
        ]
    )
    call_records.append(
        [
            chosen_call_types[1],
            chosen_romashka,
            chosen_romashka,
            datetime(test_year, test_month, test_day + 1, 0, 0, 0).isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TUCBRT06", call_records)

# Тест TUCBRT07: CDR-файл со звонками из будущего
def gen_TUCBRT07(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    test_year = get_random_year_from_future()
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 27)
    call_start_dt = datetime(test_year, test_month, test_day, 0, 0, 0)
    for _ in range(8):
        # Выбрать двух разных абонентов "Ромашки"
        chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
        chosen_call_types = choose_call_type_randomly(call_types)
        # Генерируем время окончания звонка
        call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 2 * 60 * 60))
        call_records.append(
            [
                chosen_call_types,
                chosen_romashka[0],
                chosen_romashka[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )
        call_start_dt += timedelta(seconds=random.randint(1, 2 * 60 * 60))

    # Последние две записи относятся к одному звонку, перешедшему за полночь
    call_start_dt = datetime(test_year, test_month, test_day, 23, 0, 0) + timedelta(
        seconds=random.randint(30 * 60, 59 * 60)
    )
    call_end_dt = call_start_dt + timedelta(seconds=random.randint(30 * 60, 60 * 60))

    call_records.append(
        [
            chosen_call_types[0],
            chosen_romashka[0],
            chosen_romashka[1],
            call_start_dt.isoformat(),
            datetime(test_year, test_month, test_day, 23, 59, 59).isoformat(),
        ]
    )
    call_records.append(
        [
            chosen_call_types[0],
            chosen_romashka[0],
            chosen_romashka[1],
            datetime(test_year, test_month, test_day + 1, 0, 0, 0).isoformat(),
            call_end_dt.isoformat(),
        ]
    )

    write_to_csv("TUCBRT07", call_records)

# Тест TUCBRT08: пустой файл
def gen_TUCBRT08():
    write_to_csv("TUCBRT08", list())

# Тест TUCBRT09: файл с одной записью о звонке
def gen_TUCBRT09(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 28)
    call_start_dt = datetime(
        test_year,
        test_month,
        test_day,
        random.randint(0, 22),
        random.randint(0, 59),
        random.randint(0, 59),
    )
    # Выбрать двух разных абонентов "Ромашки"
    chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
    chosen_call_type = choose_call_type_randomly(call_types)
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 60 * 60))
    call_records.append(
        [
            chosen_call_type,
            chosen_romashka[0],
            chosen_romashka[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TUCBRT09", call_records)

# Тест TUCBRT10: файл с 11 записями о звонках
def gen_TUCBRT10(msisdn_romashka: list[str], call_types: list[str]):
    call_records = []
    test_year = get_random_year_from_past()
    test_month = random.randint(1, 12)
    test_day = random.randint(1, 28)
    call_start_dt = datetime(test_year, test_month, test_day, 0, 0, 0)
    for _ in range(11):
        # Выбрать двух разных абонентов "Ромашки"
        chosen_romashka = choose_two_random_msisdn(msisdn_romashka, msisdn_romashka, msisdn_romashka)
        chosen_call_types = choose_two_call_types_randomly(call_types)
        # Генерируем время окончания звонка
        call_end_dt = call_start_dt + timedelta(seconds=random.randint(1, 2 * 60 * 60))
        call_records.append(
            [
                chosen_call_types[0],
                chosen_romashka[0],
                chosen_romashka[1],
                call_start_dt.isoformat(),
                call_end_dt.isoformat(),
            ]
        )
        call_start_dt += timedelta(seconds=random.randint(1, 2 * 60 * 60))

    write_to_csv("TUCBRT10", call_records)

# Тест TINTEGR01: файл с одной записью об исходящем звонке абонента "Ромашки"
# с тарифом "Классика" другому абоненту "Ромашки" длительностью 1 минуту
def gen_TINTEGR01(msisdn_romashka: list[str], msisdn_classica: list[str], classica_info: dict[str, datetime]):
    call_records = []
    # Выбрать двух разных абонентов: "Ромашки" с тарифом "Классика" и "Ромашки"
    chosen_msisdn = choose_two_random_msisdn(msisdn_classica, msisdn_romashka, msisdn_romashka)
    call_start_dt = classica_info[chosen_msisdn[0]] + timedelta(
        days=random.randint(0, 365), 
        hours = random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59))
    
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=60)
    call_records.append(
        [
            "01",
            chosen_msisdn[0],
            chosen_msisdn[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TINTEGR01", call_records)

# Тест TINTEGR02: файл с одной записью об исходящем звонке абонента "Ромашки"
# с тарифом "Классика" абоненту другого оператора длительностью 1 минуту
def gen_TINTEGR02(msisdn_romashka: list[str], msisdn_classica: list[str], classica_info: dict[str, datetime]):
    call_records = []
    # Выбрать двух разных абонентов: "Ромашки" с тарифом "Классика" и НЕ "Ромашки"
    chosen_msisdn = choose_two_random_msisdn(msisdn_classica, None, msisdn_romashka)
    call_start_dt = classica_info[chosen_msisdn[0]] + timedelta(
        days=random.randint(0, 365), 
        hours = random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59))
    
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=60)
    call_records.append(
        [
            "01",
            chosen_msisdn[0],
            chosen_msisdn[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TINTEGR02", call_records)

# Тест TINTEGR03: файл с одной записью о входящем звонке абонента "Ромашки"
# с тарифом "Классика" от другого абонента "Ромашки" длительностью 1 минуту
def gen_TINTEGR03(msisdn_romashka: list[str], msisdn_classica: list[str], classica_info: dict[str, datetime]):
    call_records = []
    # Выбрать двух разных абонентов: "Ромашки" с тарифом "Классика" и "Ромашки"
    chosen_msisdn = choose_two_random_msisdn(msisdn_classica, msisdn_romashka, msisdn_romashka)
    call_start_dt = classica_info[chosen_msisdn[0]] + timedelta(
        days=random.randint(0, 365), 
        hours = random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59))
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=60)
    call_records.append(
        [
            "02",
            chosen_msisdn[0],
            chosen_msisdn[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TINTEGR03", call_records)

# Тест TINTEGR04: файл с одной записью об исходящем звонке абонента "Ромашки"
# с тарифом "Помесячный" другому абоненту "Ромашки" длительностью 1 минуту
def gen_TINTEGR04(msisdn_romashka: list[str], msisdn_pomesyachny: list[str], pomesyachny_info: dict[str, datetime]):
    call_records = []
    # Выбрать двух разных абонентов: "Ромашки" с тарифом "Помесячный" и "Ромашки"
    chosen_msisdn = choose_two_random_msisdn(msisdn_pomesyachny, msisdn_romashka, msisdn_romashka)
    call_start_dt = pomesyachny_info[chosen_msisdn[0]] + timedelta(
        days=random.randint(0, 28), 
        hours = random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59))
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=60)
    call_records.append(
        [
            "01",
            chosen_msisdn[0],
            chosen_msisdn[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TINTEGR04", call_records)

# Тест TINTEGR05: файл с одной записью об исходящем звонке абонента "Ромашки"
# с тарифом "Помесячный" и отсутствием минут по тарифу другому абоненту "Ромашки" длительностью 1 минуту
def gen_TINTEGR05(msisdn_romashka: list[str], msisdn_pomesyachny: list[str], pomesyachny_info: dict[str, datetime]):
    call_records = []
    # Выбрать двух разных абонентов: "Ромашки" с тарифом "Помесячный" и "Ромашки"
    chosen_msisdn = choose_two_random_msisdn(msisdn_pomesyachny, msisdn_romashka, msisdn_romashka)
    call_start_dt = pomesyachny_info[chosen_msisdn[0]] + timedelta(
        days=random.randint(0, 28), 
        hours = random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59))
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=60)
    call_records.append(
        [
            "01",
            chosen_msisdn[0],
            chosen_msisdn[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TINTEGR05", call_records)

# Тест TINTEGR06: файл с одной записью об исходящем звонке абонента "Ромашки"
# с тарифом "Помесячный" и отсутствием минут по тарифу другому абоненту "Ромашки" длительностью 1 минуту
def gen_TINTEGR06(msisdn_romashka: list[str], msisdn_pomesyachny: list[str], pomesyachny_info: dict[str, datetime]):
    call_records = []
    # Выбрать двух разных абонентов: "Ромашки" с тарифом "Помесячный" и другого абонента
    chosen_msisdn = choose_two_random_msisdn(msisdn_pomesyachny, None, msisdn_romashka)
    call_start_dt = pomesyachny_info[chosen_msisdn[0]] + timedelta(
        days=random.randint(0, 28), 
        hours = random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59))
    
    # Генерируем время окончания звонка
    call_end_dt = call_start_dt + timedelta(seconds=60)
    call_records.append(
        [
            "01",
            chosen_msisdn[0],
            chosen_msisdn[1],
            call_start_dt.isoformat(),
            call_end_dt.isoformat(),
        ]
    )
    write_to_csv("TINTEGR06", call_records)


def main():
    msisdn_romashka = get_romashka_msisdn()
    msisdn_classica = get_romashka_classika_msisdn()
    msisdn_pomesyachny_with_rest = get_romashka_pomesyachny_with_rest_msisdn()
    msisdn_pomesyachny_with_no_rest = get_romashka_pomesyachny_with_no_rest_msisdn()
    pomesyachny_info = get_pomesyachny_subscribers_info()
    classica_info = get_classica_subscribers_info()
    call_types = get_call_types()
    
    gen_TUCBRT01(msisdn_romashka, call_types)
    gen_TUCBRT02(msisdn_romashka, call_types)
    gen_TUCBRT03(msisdn_romashka, call_types)
    gen_TUCBRT04(msisdn_romashka, call_types)
    gen_TUCBRT05(msisdn_romashka, call_types)
    gen_TUCBRT06(msisdn_romashka, call_types)
    gen_TUCBRT07(msisdn_romashka, call_types)
    gen_TUCBRT08()
    gen_TUCBRT09(msisdn_romashka, call_types)
    gen_TUCBRT10(msisdn_romashka, call_types)

    gen_TINTEGR01(msisdn_romashka, msisdn_classica, classica_info)
    gen_TINTEGR02(msisdn_romashka, msisdn_classica, classica_info)
    gen_TINTEGR03(msisdn_romashka, msisdn_classica, classica_info)
    gen_TINTEGR04(msisdn_romashka, msisdn_pomesyachny_with_rest, pomesyachny_info)
    gen_TINTEGR05(msisdn_romashka, msisdn_pomesyachny_with_no_rest, pomesyachny_info)
    gen_TINTEGR06(msisdn_romashka, msisdn_pomesyachny_with_no_rest, pomesyachny_info)

if __name__ == "__main__":
    main()
