"""
Main entry point module for the Simple To-Do List App.
Initializes application components, sets up logging, and manages the CLI interface
with comprehensive error handling and performance monitoring.

Version: 1.0
Python: 3.6+
"""

import os  # version: 3.6+
import sys  # version: 3.6+
import signal  # version: 3.6+
import time  # version: 3.6+
from typing import Optional

from .interfaces.cli_interface import CLIInterface
from .config.settings import load_config, get_config
from .logging.logger import get_logger
from .exceptions.storage_exceptions import FileAccessError
from .constants.messages import ERROR_MESSAGES, INFO_MESSAGES

# Constants for application initialization
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
DEFAULT_PERMISSIONS = 0o600
STARTUP_TIMEOUT = 5000  # milliseconds

# Global variables for cleanup
cli_interface: Optional[CLIInterface] = None
logger = None

def signal_handler(signum: int, frame) -> None:
    """
    Handles system signals for graceful shutdown.
    
    Args:
        signum: Signal number received
        frame: Current stack frame
    """
    logger.info(f"Received signal {signum}, initiating graceful shutdown")
    if cli_interface:
        cleanup(cli_interface)
    sys.exit(EXIT_SUCCESS)

def setup_data_directory() -> bool:
    """
    Creates and configures the data directory with appropriate permissions.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config = get_config()
        data_dir = config['DATA_DIR']
        
        # Create directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, mode=DEFAULT_PERMISSIONS)
        
        # Set secure permissions
        os.chmod(data_dir, DEFAULT_PERMISSIONS)
        
        # Verify directory is writable
        if not os.access(data_dir, os.W_OK):
            raise FileAccessError(f"Data directory {data_dir} is not writable")
            
        logger.debug(f"Data directory setup complete: {data_dir}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup data directory: {str(e)}")
        return False

def cleanup(interface: CLIInterface) -> None:
    """
    Performs cleanup operations before application exit.
    
    Args:
        interface: CLIInterface instance to cleanup
    """
    try:
        # Cleanup CLI interface
        interface.cleanup()
        
        # Flush logs
        if logger:
            for handler in logger.handlers:
                handler.flush()
                handler.close()
                
        logger.info("Cleanup completed successfully")
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}", file=sys.stderr)

def main() -> int:
    """
    Main entry point function that initializes and runs the application.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    global cli_interface, logger
    
    try:
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start startup timer
        start_time = time.time()
        
        # Load configuration
        config = load_config()
        if not config:
            print(ERROR_MESSAGES['system_error'], file=sys.stderr)
            return EXIT_FAILURE
            
        # Initialize logger
        logger = get_logger()
        logger.info("Application startup initiated")
        
        # Set up data directory
        if not setup_data_directory():
            logger.error("Failed to setup data directory")
            return EXIT_FAILURE
            
        # Check startup time
        startup_time = (time.time() - start_time) * 1000
        if startup_time > STARTUP_TIMEOUT:
            logger.warning(f"Slow startup detected: {startup_time:.2f}ms")
            
        # Initialize CLI interface
        storage_path = os.path.join(config['DATA_DIR'], config['TASKS_FILE'])
        cli_interface = CLIInterface(storage_path)
        
        # Run main interface loop
        logger.info("Starting main application loop")
        exit_code = cli_interface.run()
        
        # Perform cleanup
        cleanup(cli_interface)
        
        # Log final status
        logger.info(f"Application exiting with code {exit_code}")
        return exit_code
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        if cli_interface:
            cleanup(cli_interface)
        return EXIT_SUCCESS
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        if cli_interface:
            cleanup(cli_interface)
        return EXIT_FAILURE

if __name__ == '__main__':
    sys.exit(main())