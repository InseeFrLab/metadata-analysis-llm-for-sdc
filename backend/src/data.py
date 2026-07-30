
import os
from pathlib import Path

import pandas as pd
import s3fs


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
    ext = path.rsplit(".", 1)[-1].lower()
    engines = {"ods": "odf", "xlsx": "openpyxl", "csv": "csv"}
    if ext not in engines:
        raise ValueError(f"Extension non supportée : '{ext}'")
    return engines[ext]


def read_file(filepath: str) -> dict[str, pd.DataFrame]:
    extension = detect_file_type(filepath)

    # Ouverture selon la source ; fermé juste en dessous via `with ctx as f`,
    # donc pas un vrai leak malgré ce que dit SIM115 (qui n'a pas de vue sur le ternaire).
    ctx = connect_s3().open(filepath) if filepath.startswith("s3") else open(filepath, "rb")  # noqa: SIM115

    with ctx as f:
        if extension == "csv":
            # nom du fichier : le contenu ou modifier si besoin pour csv
            return {Path(filepath).stem: pd.read_csv(f)}
        else:
            return pd.read_excel(f, sheet_name=None, engine=extension)


def upload_output(
    df: pd.DataFrame,
    input_path: str,
    output_folder: str
) -> None:
    filename = Path(input_path).stem + ".csv"
    output_path = output_folder+filename

    # Fermé juste en dessous via `with ctx as f` ; voir commentaire de read_file.
    ctx = connect_s3().open(output_path) if output_path.startswith("s3") else open(output_path, "wb")  # noqa: SIM115

    with ctx as f:
        df.to_csv(f, index=False)
