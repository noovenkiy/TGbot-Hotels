import os
import json


def write_response(resp: dict, name: str) -> None:
    while "materials" not in os.listdir():
        os.chdir("..")
    file_name = os.path.join("materials", "api_request")
    file_name = os.path.join(file_name, "city_" + name)

    file_name += ".json"
    print(file_name)
    print(os.path.abspath(file_name))
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(resp, file, indent=4, ensure_ascii=False)
