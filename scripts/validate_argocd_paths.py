from pathlib import Path
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/tksabins/shop-platform.git"

errors = []
validated = 0

argocd_dir = REPO_ROOT / "argocd"

manifest_files = sorted(
    file
    for file in argocd_dir.rglob("*")
    if file.is_file() and file.suffix in {".yaml", ".yml"}
)

for file in manifest_files:
    with file.open() as stream:
        documents = list(yaml.safe_load_all(stream))

    for manifest in documents:
        if not manifest or manifest.get("kind") != "Application":
            continue

        name = manifest["metadata"]["name"]
        spec = manifest.get("spec", {})
        source = spec.get("source", {})

        if spec.get("sources") or source.get("repoURL") != REPO_URL:
            errors.append(f"{name}: Unsupported source configuration")
            continue

        if source.get("targetRevision") != "main":
            errors.append(f"{name}: Unsupported target revision")
            continue

        path = source.get("path")

        if not isinstance(path, str) or not path.strip():
            errors.append(f"{name}: Source path is missing")
            continue

        source_path = (REPO_ROOT / path).resolve()

        if Path(path).is_absolute() or not source_path.is_relative_to(REPO_ROOT):
            errors.append(f"{name}: Path is outside repository")
            continue

        if not source_path.is_dir():
            errors.append(f"{name}: Directory not found: {path}")
            continue

        print(f"PASS: {name} -> {path}")
        validated += 1

print(f"\nValidated Applications: {validated}")
print(f"Validation errors: {len(errors)}")

for error in errors:
    print(f"FAIL: {error}")

if errors or validated == 0:
    sys.exit(1)

sys.exit(0)
