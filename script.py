import pandas as pd
from sqlalchemy.orm import Session

from src.eportal.db import sessionLocalFactory
from src.eportal.models import SiteAddress
from src.eportal.models import Service

tables = {
    "SiteAddress" : SiteAddress,
    "Service" : Service
}

def import_site_addresses(file_path: str,table:str):
    df = pd.read_excel(file_path)

    db: Session = sessionLocalFactory()

    try:
        records = []

        model_class = tables.get(table)
        model_columns = set(model_class.__table__.columns.keys())

        for row in df.to_dict(orient="records"):

            clean_row = {}

            for key, value in row.items():

                # Ignore columns that don't exist in the model
                if key not in model_columns:
                    continue

                # Convert NaN to None
                if pd.isna(value):
                    clean_row[key] = None

                # Convert pandas Timestamp to string
                elif isinstance(value, pd.Timestamp):
                    clean_row[key] = value.isoformat()

                else:
                    clean_row[key] = value

            records.append(model_class(**clean_row))

        db.bulk_save_objects(records)
        db.commit()

        print(f"Inserted {len(records)} records.")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


if __name__ == "__main__":
    import_site_addresses("services.xlsx","Service")