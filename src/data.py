
import s3fs
import os
import pandas as pd
from pathlib import Path


def connect_s3() -> s3fs.S3FileSystem:
    """Retourne un filesystem S3 authentifié."""

    return s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"},
        key=os.environ["AWS_ACCESS_KEY_ID"],
        secret=os.environ["AWS_SECRET_ACCESS_KEY"],
        token=os.environ["AWS_SESSION_TOKEN"],
    )


def detect_file_type(path: str) -> str:
    """Détermine le type de fichier depuis le chemin."""
    ext = Path(path).suffix
    ext = path.rsplit(".", 1)[-1].lower()
    if ext == "ods":
        return "odf"
    elif ext == "xlsx":
        return "openpyxl"
    elif ext == "csv":
        return "csv"

    raise ValueError(f"Extension non supportée : '{ext}'")


def read_file(filepath: str):
    extension = detect_file_type(filepath)

    # Ouverture selon la source
    ctx = connect_s3().open(filepath) if filepath.startswith("s3") else open(filepath, "rb")

    with ctx as f:
        if extension == "csv":
            # nom du fichier : le contenu
            return {Path(filepath).stem: pd.read_csv(f)}
        else:
            return pd.read_excel(f, sheet_name=None, engine=extension)


def upload_output(
    df: pd.DataFrame,
    input_path: str,
    output_folder: str
):
    filename = Path(input_path).stem + ".csv"
    output_path = output_folder+filename

    ctx = connect_s3().open(output_path) if output_path.startswith("s3") else open(output_path, "wb")

    with ctx as f:
        df.to_csv(f, index=False)
