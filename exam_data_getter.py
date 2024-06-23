import requests

years = [2022, 2023, 2024]
semester_name = ["spring", "fall"]

# create a list of semesters with all combinations semester_name + year
semesters = []
for year in years:
    for name in semester_name:
        semesters.append(name + str(year))

url = "https://cdn.web.uta.edu/-/media/project/website/administration/registrar/documents/exam-schedules/"

# get all exam schedules if they exist and save as pdf in the exam_data_pdf
for semester in semesters:
    response = requests.get(url + semester + "-master.pdf")
    if response.status_code == 200:
        with open("exam_data_pdf/" + semester + ".pdf", "wb") as f:
            f.write(response.content)
    else:
        print("No exam schedule found for " + semester)
