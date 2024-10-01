from pathlib import Path

import pandas as pd
from docxtpl import DocxTemplate
from tqdm import tqdm
from utils.box_client_ccg import AppConfig


def execute_mail_merge():
    conf = AppConfig()

    df = pd.read_csv(conf.local_file_csv, sep=",", quotechar='"')
    doc = DocxTemplate(conf.local_file_template)
    print("\nGenerating sample files:")

    for row in tqdm(df.to_dict(orient="records")):
        context = {
            "Tenant": row.get("Tenant"),
            "Email": row.get("Email"),
            "LeaseDate": row.get("LeaseDate"),
            "StartDate": row.get("StartDate"),
            "EndDate": row.get("EndDate"),
            "Property": row.get("Property"),
            "PropertyType": row.get("PropertyType"),
            "Description": row.get("Description"),
            "BedRooms": row.get("BedRooms"),
            "Rent": f"${row.get("Rent"):,.2f}",
        }
        doc.render(context)

        # make sure folder samples exists and create if not
        Path(f"{conf.local_folder_files}").mkdir(parents=True, exist_ok=True)

        doc_file_path = f"{conf.local_folder_files}/{row.get('Property')}.docx"
        doc.save(doc_file_path)
        # print(f"Generated: {doc_file_path}")

    print(f"\nGenerated {len(df)} sample files in {conf.local_folder_files}")
