def classify(changed_files):
    result = {
        "backend": False,
        "training": False,
        "infra": False,
        "docker": False,
        "unknown": False,
    }

    for path in changed_files:
        if path.startswith("backend/"):
            result["backend"] = True
        elif path.startswith("training/"):
            result["training"] = True
        elif path.startswith("shared/") or path == "pyproject.toml":
            result["backend"] = True
            result["training"] = True
        elif path.startswith("infra/"):
            result["infra"] = True
        elif path == "Dockerfile":
            result["docker"] = True
        elif path.startswith("docs/"):
            continue
        else:
            result["unknown"] = True

    return result
