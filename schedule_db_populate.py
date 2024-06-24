from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

with open("schedule.csv", "r") as f:
    for line in f:
        (
            course_id,
            section,
            days_met,
            date,
            start_time,
            end_time,
            building_id,
            room_no,
            instructor_id,
        ) = line.strip().split(",")
        if course_id == "course_id":
            continue
        supabase.table("schedule").insert(
            {
                "course_id": course_id,
                "section": section,
                "days_met": days_met,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "building_id": building_id,
                "room_no": room_no,
                "instructor_id": instructor_id,
            }
        ).execute()
