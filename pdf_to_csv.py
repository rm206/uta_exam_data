import tabula
import pandas as pd
import os

pdf_directory_path = "exam_data_pdf"
csv_directory_path = "exam_data_csv"

for filename in os.listdir(pdf_directory_path):
    pdf_file_path = os.path.join(pdf_directory_path, filename)

    df = tabula.read_pdf(pdf_file_path, pages="all")
    df = pd.concat(df, ignore_index=True)
    df.fillna("-", inplace=True)
    df.columns = df.columns.str.replace(" ", "")
    df.columns = df.columns.str.replace("\n", "")

    csv_file_path = os.path.join(csv_directory_path, filename.replace(".pdf", ".csv"))
    df.to_csv(csv_file_path, index=False)
