from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

with open("lists/building_list.txt", "r") as f:
    for line in f:
        building = line.strip()
        supabase.table("buildings").insert({"building_name": building}).execute()

with open("lists/course_list.txt", "r") as f:
    for line in f:
        course_subject, course_number = line.strip().split()
        supabase.table("courses").insert(
            {"course_subject": course_subject, "course_number": course_number}
        ).execute()

with open("lists/instructor_list.txt", "r") as f:
    for line in f:
        instructor = line.strip()
        supabase.table("instructors").insert({"instructor_name": instructor}).execute()
