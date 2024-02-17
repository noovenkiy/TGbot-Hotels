from . import history


def save_request_to_db(
    hotels: list, user_id, sort, city, city_id, check_in, check_out, **kwarg
) -> None:
    with history:
        row = history.execute(
            """
        INSERT INTO request (user, city, checkin, checkout, sort)
        VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, city_id, check_in, check_out, sort),
        )

        req_id = row.lastrowid

        for hotel in hotels:
            history.execute(
                """
            INSERT INTO history
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (req_id, *hotel.values()),
            )

        history.execute(
            """
        REPLACE INTO city
        VALUES (?, ?)
        """,
            (city_id, city),
        )


def get_history_from_db(user_id: int) -> list:
    with history:
        cur = history.execute(
            "SELECT req_id, date, (SELECT name FROM city WHERE id=request.city) AS city, "
            "checkin, checkout, sort FROM request WHERE user=:user",
            {"user": user_id},
        )
    return cur.fetchall()


def get_last(user_id: int) -> list:
    with history:
        return history.execute(
            "SELECT date, city AS city_id, (SELECT name FROM city WHERE id=request.city) AS city, "
            "checkin, checkout, sort FROM request WHERE user=(?) ORDER BY date DESC LIMIT 1",
            (user_id,),
        ).fetchall()


def get_req_from_db(req_id: str) -> tuple:
    with history:
        cur = history.execute(
            "SELECT date, city AS city_id, (SELECT name FROM city WHERE id=request.city) AS city, "
            "checkin, checkout, sort FROM request WHERE req_id=:req",
            {"req": req_id},
        )
    return cur.fetchall()[0]


def get_hotel_by_req(req_id: str) -> list:
    with history:
        records = history.execute(
            "SELECT * FROM history WHERE req_id=(?)", (req_id,)
        ).fetchall()
    hotels = []
    for record in records:
        hotels.append(
            {
                "id": record[1],
                "url": record[2],
                "name": record[3],
                "address": record[4],
                "price": record[5],
                "latitude": record[6],
                "longitude": record[7],
            }
        )
    return hotels
