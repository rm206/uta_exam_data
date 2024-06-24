import pandas as pd
import os

buildings = set()
instructors = set()
courses = set()

csv_directory_path = "exam_data_csv"

for filename in os.listdir(csv_directory_path):
    csv_file_path = os.path.join(csv_directory_path, filename)

    df = pd.read_csv(csv_file_path)
    # iterate over all rows in the dataframe
    for index, row in df.iterrows():
        courses.add((row["Subject"], row["Course"]))
        instructors.add(row["Instructor"])
        # if Building column exists, use it, otherwise use BuildingName
        if "Building" in df.columns:
            buildings.add(row["Building"])
        else:
            buildings.add(row["BuildingName"])


with open("lists/course_list.txt", "w") as f:
    for course in courses:
        f.write(f"{course[0]} {course[1]}\n")

with open("lists/instructor_list.txt", "w") as f:
    for instructor in instructors:
        f.write(f"{instructor}\n")

with open("lists/building_list.txt", "w") as f:
    for building in buildings:
        f.write(f"{building}\n")
