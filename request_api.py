import os
from dotenv import load_dotenv
import re
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

def clean_dish_name(dish: str) -> str:
    dish: str = re.sub(r"[\(\[].*?[\)\]]", "", dish)
    return dish.strip("*! ")

def clean_menu(raw: str) -> str:
    dishes: str = raw.split("<br/>")
    return [clean_dish_name(d) for d in dishes]

def find_school(office_code: str, school_name: str) -> str :
    url: str = "https://open.neis.go.kr/hub/schoolInfo"
    params: dict = {
        "KEY": API_KEY, "Type": "json",
        "pIndex": 1, "pSize": 5,
        "ATPT_OFCDC_SC_CODE": office_code,
        "SCHUL_NM": school_name
    }
    data: str = requests.get(url, params=params).json()
    school: str = data["schoolInfo"][1]["row"][0]
    return school["SD_SCHUL_CODE"]

def get_meal(office_code: str, school_code: str, date: str) -> str :
    url: str = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params: dict = {
        "KEY": API_KEY, "Type": "json",
        "pIndex": 1, "pSize": 5,
        "ATPT_OFCDC_SC_CODE": office_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": date
    }
    data: str = requests.get(url, params=params).json()
    return data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]

def get_info(date: str, school_name: str) -> list[str] :
    office_code: str = "J10"
    school_code: str = find_school(office_code, school_name)
    return [clean_menu(get_meal(office_code=office_code, school_code=school_code, date=date.strftime("%Y%m%d"))), office_code, school_code]

# def main():
#     school_name: str = "광문고등학교"
#     date: str = "20261106"

#     menu: str = clean_menu(get_meal(office_code, school_code, date))

#     print(f"{school_name}의 {date} 급식:")
    # print(menu)