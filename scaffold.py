"""Create the RemoteAI starter directories when bootstrapping a checkout."""
from pathlib import Path

DIRECTORIES = ["app/api", "app/providers", "app/tools", "static", "data", "docs", "tests"]

def main() -> None:
    root = Path(__file__).resolve().parent
    for directory in DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)
    print("RemoteAI directories are ready.")

if __name__ == "__main__":
    main()
