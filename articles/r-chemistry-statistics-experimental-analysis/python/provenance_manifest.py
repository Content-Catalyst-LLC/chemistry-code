"""
Create a provenance manifest for R chemistry workflows.

Run from article directory:
    python python/provenance_manifest.py
"""

from pathlib import Path
import hashlib
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ARTICLE_DIR / "data" / "workflow_manifest.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_sha256(path: Path) -> str:
    if path.exists() and path.is_file():
        return sha256_file(path)
    return "not_available"


def hash_artifacts(value: str) -> str:
    hashes = []
    for artifact in str(value).split(";"):
        data_path = ARTICLE_DIR / "data" / artifact
        output_path = ARTICLE_DIR / artifact
        script_path = ARTICLE_DIR / artifact
        if data_path.exists():
            path = data_path
        elif output_path.exists():
            path = output_path
        elif script_path.exists():
            path = script_path
        else:
            path = ARTICLE_DIR / artifact
        hashes.append(f"{artifact}:{safe_sha256(path)}")
    return "|".join(hashes)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    workflow = pd.read_csv(WORKFLOW_PATH)
    workflow["input_sha256"] = workflow["input_artifact"].apply(hash_artifacts)
    workflow["output_sha256"] = workflow["output_artifact"].apply(
        lambda artifact: safe_sha256(ARTICLE_DIR / artifact)
    )

    workflow.to_csv(OUTPUT_PATH, index=False)
    print(workflow.to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
