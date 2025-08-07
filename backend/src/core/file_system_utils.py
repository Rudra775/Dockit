import os, tempfile, shutil, logging

logger = logging.getLogger("doctit_backend")

def create_temp_dir() -> str : 
    """
    Creates a temporary directory for cloning a repository.
    Returns the path to the new directory.
    """
    
    try: 
        temp_dir = tempfile.mkdtemp(prefix='dockit-clone-')
        logger.info(f"New temporary directory created: {temp_dir}")
        return temp_dir
    except OSError as e: 
        logger.error(f"Failed to create a new directory: {e}")
        raise

def cleanup_temp_dir(path: str) : 
    """Removes a directory entirely"""
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            logger.info(f"Cleaned up temporary directoy: {path}")
        except OSError as e:
            logger.error(f"Failed to clean up temporary directoy {path} : {e}")
    
    else: 
        logger.warning(f"Attempted to cleaup non-existing directory: {path}")
        

        
        
            

