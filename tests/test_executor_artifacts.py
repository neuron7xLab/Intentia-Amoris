from pathlib import Path


def test_executor_file_exists():
    assert Path('scripts/verify_all.sh').exists()
