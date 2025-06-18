"""
Tests for logging configuration.
"""
import logging
import pytest
from pathlib import Path
from src.utils.logging_config import configure_logging

@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file for testing."""
    return tmp_path / "test.log"

def test_configure_logging_stderr_only():
    """Test logging configuration without file output."""
    configure_logging(log_level="INFO")
    root_logger = logging.getLogger()
    
    # Check log level
    assert root_logger.getEffectiveLevel() == logging.INFO
    
    # Check handlers
    handlers = root_logger.handlers
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)

def test_configure_logging_with_file(temp_log_file):
    """Test logging configuration with file output."""
    configure_logging(log_level="DEBUG", log_file=temp_log_file)
    root_logger = logging.getLogger()
    
    # Check log level
    assert root_logger.getEffectiveLevel() == logging.DEBUG
    
    # Check handlers
    handlers = root_logger.handlers
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    assert any(isinstance(h, logging.FileHandler) for h in handlers)
    
    # Test logging to file
    test_message = "Test log message"
    logging.info(test_message)
    
    log_content = temp_log_file.read_text()
    assert test_message in log_content

def test_configure_logging_invalid_directory():
    """Test logging configuration with invalid log directory."""
    invalid_path = Path("/nonexistent/directory/test.log")
    
    with pytest.raises(Exception):
        configure_logging(log_level="INFO", log_file=invalid_path)
