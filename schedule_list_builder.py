import pandas as pd
import os
from supabase import create_client
from pprint import pprint


def date_converter(date):
    month, day, year = date.split("/")
    if len(month) == 1:
        month = f"0{month}"
    if len(day) == 1:
        day = f"0{day}"
    return f"{year}-{month}-{day}"


def time_converter(time):
    time, am_pm = time.split(" ")
    hour, minute = time.split(":")
    # convert to 24 hour time
    if am_pm == "PM":
        hour = int(hour) + 12
    if len(str(hour)) == 1:
        hour = f"0{hour}"
    if len(minute) == 1:
        minute = f"0{minute}"
    return f"{hour}:{minute}:00"


def get_semester(filename):
    filename = filename.split(".")[0]
    name, year = filename[:-4], filename[-4:]
    return (name.title(), int(year))


df = pd.DataFrame(
    columns=[
        "semester_id",
        "course_id",
        "section",
        "days_met",
        "date",
        "start_time",
        "end_time",
        "building_id",
        "room_no",
        "instructor_id",
    ]
)

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

buildings_res, _ = supabase.table("buildings").select("id", "building_name").execute()
buildings_res = buildings_res[1]
buildings = {}
for building in buildings_res:
    buildings[building["building_name"]] = building["id"]

courses_res, _ = (
    supabase.table("courses").select("id", "course_subject", "course_number").execute()
)
courses_res = courses_res[1]
courses = {}
for course in courses_res:
    courses[(course["course_subject"], course["course_number"])] = course["id"]

instructors_res, _ = (
    supabase.table("instructors").select("id", "instructor_name").execute()
)
instructors_res = instructors_res[1]
instructors = {}
for instructor in instructors_res:
    instructors[instructor["instructor_name"]] = instructor["id"]

semester_res, _ = (
    supabase.table("semesters").select("id", "semester_name", "semester_year").execute()
)
semester_res = semester_res[1]
semesters = {}
for semester in semester_res:
    semesters[(semester["semester_name"], semester["semester_year"])] = semester["id"]

for filename in os.listdir("exam_data_csv"):
    temp = pd.read_csv(f"exam_data_csv/{filename}")
    for index, row in temp.iterrows():
        course_id = courses[(row["Subject"], row["Course"])]
        instructor_id = instructors[row["Instructor"]]
        if "Building" in temp.columns:
            building_id = buildings[row["Building"]]
        else:
            building_id = buildings[row["BuildingName"]]
        semester_id = semesters[get_semester(filename)]
        new_row = pd.DataFrame(
            [
                {
                    "semester_id": semester_id,
                    "course_id": course_id,
                    "section": (
                        row["Section"] if "Section" in temp.columns else row["Section#"]
                    ),
                    "days_met": row["DaysMet"],
                    "date": date_converter(row["StartDate"]),
                    "start_time": time_converter(row["StartTime"]),
                    "end_time": time_converter(row["EndTime"]),
                    "building_id": building_id,
                    "room_no": row["Room"] if "Room" in temp.columns else row["Room#"],
                    "instructor_id": instructor_id,
                }
            ]
        )
        df = pd.concat([df, new_row], ignore_index=True)


df.to_csv("schedule.csv", index=False)
