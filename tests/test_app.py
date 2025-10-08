import pytest
from app import dir_to_list

# Create a temporary folder and file
@pytest.fixture
def temporary_dir(tmp_path):
    folder = tmp_path / "data2"
    folder.mkdir()
    (folder / "test_file_1.txt").write_text("test1")
    return folder

# Test if directory is missing
def test_dir_to_list_missing(tmp_path):
    missing = tmp_path / "dir_does_not_exist"
    result = dir_to_list(str(missing))
    assert result == []

# Test if directory exists
def test_dir_to_list_exists(temporary_dir):
    result = dir_to_list(str(temporary_dir))
    assert result == ["test_file_1.txt"]