import _bootstrap  # noqa: F401

from kriyax_workbench.workspace import ensure_workspace


if __name__ == "__main__":
    for key, value in ensure_workspace().items():
        print(f"{key}: {value}")
