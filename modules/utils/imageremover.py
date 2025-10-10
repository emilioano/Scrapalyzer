# For abstract classes
import logging
from abc import ABC, abstractmethod
import os

logger = logging.getLogger(__name__)

class ImageRemover(ABC):
    def __init__(self, cleanfolder, dryrun):
        self.cleanfolder = cleanfolder
        self.dryrun = dryrun

    @abstractmethod
    def wipefolder(self):
        pass

class RecursiveCleaner(ImageRemover):
    def wipefolder(self):
        logger.info(f'Wiping folder with recursive mode, and dryrun mode set as {self.dryrun}')
        # List all subfolders
        for root, dirs, files in os.walk(self.cleanfolder):
            # Get all files in the and remove them
            for filename in files:
                full_path=os.path.join(root, filename)
                try:
                    if self.dryrun:
                        logger.info(f'** Dry run ** Removed {full_path}')
                    else:
                        os.remove(full_path)
                        logger.info(f'Removed {full_path}')
                except Exception as error:
                    logger.info(f'Error when removing file: {error}')
        # When the folders are empty we are allowed to remove them, so let's do that
        for dirs in os.walk(self.cleanfolder):
            # Below to not include the root folder for deletion.
            if dirs[0] != self.cleanfolder:
                try:        
                    if self.dryrun:
                        logger.info(f'** Dry run ** Removed folder {dirs[0]}')
                    else:
                        os.rmdir(dirs[0])
                        logger.info(f'**Removed folder {dirs[0]}')
                except Exception as error:
                    logger.info(f'Unable to remove folder: {error}')

class FlatCleaner(ImageRemover):      
    def wipefolder(self):
        logger.info(f'Wiping folder with flat mode, and dryrun mode set as {self.dryrun}')
        for filename in os.listdir(self.cleanfolder):
            full_path=os.path.join(self.cleanfolder, filename)               
            try:
                #Skip subsfolders
                if os.path.isdir(full_path):
                    continue
                else:
                    if self.dryrun:
                        logger.info(f'** Dry run** Removed {full_path}')
                    else:
                        os.remove(full_path)
                        logger.info(f'Removed {full_path}')
            except Exception as error:
                logger.error(f'Error when removing file: {error}')

def imageremover(cleaner: ImageRemover):
    cleaner.wipefolder()