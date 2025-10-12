import pytest
from modules.utils.imageremover import FlatCleaner,RecursiveCleaner,imageremover


@pytest.fixture
def temp_folder(tmp_path):
    # Create dummy folder and a subfolder
    folder=tmp_path / 'tmp'
    subfolder=folder / 'subfolder'
    folder.mkdir()
    subfolder.mkdir()

    # Create some dummy files in folder and subfolder
    for i in range (0,21):
        file = folder / f'This is file #{i}.txt'
        subfile = subfolder / f'This is file {i} in subfolder'
        CONTENT = f'This is file #{i}'
        file.write_text(CONTENT)
        subfile.write_text(CONTENT)
    return folder


def test_check_filesum(temp_folder):
    files = list(temp_folder.iterdir())
    subfolder = temp_folder / 'subfolder'
    subfiles = list(subfolder.iterdir())
    assert len(files) == 22 # Files + subfolder
    assert len(subfiles) == 21 # Files in subfolder


def test_non_recursive_removal(temp_folder):
    files = list(temp_folder.iterdir())
    subfolder = temp_folder / 'subfolder'
    subfiles = list(subfolder.iterdir())

    assert len (files) == 22 # Before cleaning we should have 22 objects (files + subfolder)
    assert len (subfiles) == 21 # 21 Files in subfolder

    # Try the dry run mode first
    flatcleaner = FlatCleaner(temp_folder,True)
    imageremover(flatcleaner)

    files = list(temp_folder.iterdir())
    subfolder = temp_folder / 'subfolder'
    subfiles = list(subfolder.iterdir())

    assert len (files) == 22 # Everything should still be there
    assert len (subfiles) == 21 # 21 Files in subfolder
    
    # Do the cleaning in sharp mode
    flatcleaner = FlatCleaner(temp_folder,False)
    imageremover(flatcleaner)

    files = list(temp_folder.iterdir())
    assert len(files) == 1 # Only subfolder and it's files should be left

    subfiles = list(subfolder.iterdir())
    assert len(subfiles) == 21 # Files in subfolder still there


def test_recursive_removal(temp_folder):
    files = list(temp_folder.iterdir())
    subfolder = temp_folder / 'subfolder'
    subfiles = list(subfolder.iterdir())


    files = list(temp_folder.iterdir())
    assert len(files) == 22 # Before cleaning we should have 22 objects (files + subfolder)

    subfiles = list(subfolder.iterdir())
    assert len(subfiles) == 21 # Files in subfolder still there

    # Dry run first
    recursivecleaner = RecursiveCleaner(temp_folder,True)
    imageremover(recursivecleaner)

    files = list(temp_folder.iterdir())
    assert len(files) == 22 # The files should be untouched

    subfiles = list(subfolder.iterdir())
    assert len(subfiles) == 21 # Files in subfolder still there


    # Time for sharp removal
    recursivecleaner = RecursiveCleaner(temp_folder,False)
    imageremover(recursivecleaner)

    files = list(temp_folder.iterdir())
    assert len(files) == 0 # All should be wiped


