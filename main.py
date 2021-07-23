
from fastapi import FastAPI, File, UploadFile
import io
import pandas as pd
import benford

app = FastAPI()

@app.post("/tests/")
async def create_upload_file(csv_file: UploadFile = File(...)):
    if csv_file.filename[-4:] == ".csv":
        raw_data = csv_file.file.read().decode("utf-8")
        temp_data = io.StringIO(raw_data)
        data = pd.read_csv(temp_data, sep = ",",
                        names=["TransactionNr", "Type", "Date", "Value", "PeriodNr", "Year", "unused"])
        return {"IB": benford.zero_check_ib(data),
                "YB": benford.zero_check_year(data),
                "Benford": benford.benford_test(data)}
    else:
        return "Error, invalid file"

