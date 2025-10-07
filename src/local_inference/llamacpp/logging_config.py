"""
Logging Configuration for Llama Agents
Provides consistent logging setup across the project
"""

import logging
import sys
from datetime import datetime
from typing import Optional
import json


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        # Add timestamp
        record.timestamp = datetime.now().strftime("%H:%M:%S")
        
        return super().format(record)


def setup_logger(
    name: str = "LlamaAgent",
    level: str = "INFO",
    use_colors: bool = True,
    log_to_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup a logger with consistent formatting
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_colors: Whether to use colored output
        log_to_file: Optional file path to log to
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    if use_colors:
        formatter = ColoredFormatter(
            '%(timestamp)s | %(levelname)s | %(name)s | %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_to_file:
        file_handler = logging.FileHandler(log_to_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


class AgentEventLogger:
    """Specialized logger for agent events with structured logging"""
    
    def __init__(self, name: str = "AgentEvents", level: str = "INFO"):
        self.logger = setup_logger(name, level)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def log_session_start(self, agent_type: str, model_path: str):
        """Log session start"""
        self.logger.info(f"🚀 Session {self.session_id} started - {agent_type}")
        self.logger.info(f"📁 Model: {model_path}")
    
    def log_user_input(self, user_input: str, turn_number: int = 1):
        """Log user input"""
        self.logger.info(f"👤 Turn {turn_number} - User: {user_input}")
    
    def log_agent_response(self, response: str, turn_number: int = 1):
        """Log agent response"""
        self.logger.info(f"🤖 Turn {turn_number} - Agent: {response}")
    
    def log_tool_call(self, tool_name: str, args: dict, turn_number: int = 1):
        """Log tool execution"""
        self.logger.info(f"🔧 Turn {turn_number} - Tool Call: {tool_name}")
        self.logger.debug(f"   Args: {json.dumps(args, indent=2)}")
    
    def log_tool_result(self, tool_name: str, result: str, success: bool = True, turn_number: int = 1):
        """Log tool result"""
        status = "✅" if success else "❌"
        self.logger.info(f"{status} Turn {turn_number} - Tool Result ({tool_name}): {result}")
    
    def log_performance(self, operation: str, duration: float, details: dict = None):
        """Log performance metrics"""
        self.logger.info(f"⏱️  Performance: {operation} took {duration:.2f}s")
        if details:
            self.logger.debug(f"   Details: {json.dumps(details, indent=2)}")
    
    def log_error(self, error: str, context: str = "", turn_number: int = 1):
        """Log errors with context"""
        if context:
            self.logger.error(f"❌ Turn {turn_number} - Error in {context}: {error}")
        else:
            self.logger.error(f"❌ Turn {turn_number} - Error: {error}")
    
    def log_system_event(self, event: str):
        """Log system events"""
        self.logger.info(f"⚙️  System: {event}")
    
    def log_conversation_summary(self, total_turns: int, total_tokens: int, duration: float):
        """Log conversation summary"""
        self.logger.info(f"📊 Session {self.session_id} Summary:")
        self.logger.info(f"   Total turns: {total_turns}")
        self.logger.info(f"   Total tokens: {total_tokens}")
        self.logger.info(f"   Duration: {duration:.2f}s")


# Example usage and testing
if __name__ == "__main__":
    # Test different logging setups
    
    print("=== Basic Logger ===")
    basic_logger = setup_logger("TestLogger", "INFO")
    basic_logger.info("This is a basic log message")
    basic_logger.warning("This is a warning message")
    basic_logger.error("This is an error message")
    
    print("\n=== Agent Event Logger ===")
    agent_logger = AgentEventLogger("TestAgent", "INFO")
    agent_logger.log_session_start("TestAgent", "/path/to/model.gguf")
    agent_logger.log_user_input("Hello, how are you?", 1)
    agent_logger.log_agent_response("I'm doing well, thank you!", 1)
    agent_logger.log_tool_call("get_weather", {"city": "Paris"}, 1)
    agent_logger.log_tool_result("get_weather", "Sunny, 22°C", True, 1)
    agent_logger.log_performance("think", 1.23, {"tokens": 150, "model": "mistral"})
    agent_logger.log_conversation_summary(1, 150, 1.23)
    
    print("\n=== Debug Logger ===")
    debug_logger = setup_logger("DebugLogger", "DEBUG")
    debug_logger.debug("This is a debug message")
    debug_logger.info("This is an info message")
    
    print("\n=== File Logger ===")
    file_logger = setup_logger("FileLogger", "INFO", log_to_file="test.log")
    file_logger.info("This message will be written to test.log")
    print("Check test.log file for the logged message")

