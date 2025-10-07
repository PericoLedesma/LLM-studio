# Terminal Logging Guide for Llama Agents

This guide shows you different approaches to implement logging of events in the terminal for your Llama agents.

## Quick Start

### 1. Simple Print-Based Logging (Easiest)

```python
def log_user_input(user_input: str):
    print(f"👤 User: {user_input}")

def log_agent_response(response: str):
    print(f"🤖 Agent: {response}")

def log_tool_call(tool_name: str, args: dict):
    print(f"🔧 Tool Call: {tool_name}")
    print(f"   Args: {json.dumps(args, indent=2)}")

def log_tool_result(tool_name: str, result: str):
    print(f"✅ Tool Result ({tool_name}): {result}")

def log_error(error: str):
    print(f"❌ Error: {error}")
```

### 2. Using TerminalLogger (Recommended for Development)

```python
from terminal_logger import TerminalLogger

logger = TerminalLogger(show_timestamp=True, show_colors=True)

# Usage
logger.user_input("What's the weather?")
logger.tool_call("get_weather", {"city": "Paris"})
logger.tool_result("get_weather", "Sunny, 22°C", True)
logger.agent_response("The weather is sunny!")
logger.performance("think", 1.23)
```

### 3. Using Python's Built-in Logging (Most Professional)

```python
from logging_config import setup_logger

logger = setup_logger("MyAgent", "INFO", use_colors=True)

logger.info("🚀 Agent started")
logger.info("👤 User: Hello")
logger.info("🤖 Agent: Hi there!")
logger.warning("⚠️ Warning message")
logger.error("❌ Error occurred")
```

### 4. Using AgentEventLogger (Best for Agent Systems)

```python
from logging_config import AgentEventLogger

event_logger = AgentEventLogger("MyAgent", "INFO")

event_logger.log_session_start("MyAgent", "/path/to/model.gguf")
event_logger.log_user_input("Hello", 1)
event_logger.log_tool_call("get_weather", {"city": "Paris"}, 1)
event_logger.log_tool_result("get_weather", "Sunny", True, 1)
event_logger.log_agent_response("The weather is sunny!", 1)
event_logger.log_performance("think", 1.23)
```

## Integration Examples

### Adding Logging to Your Existing Agent

```python
class MyAgent:
    def __init__(self, model_path: str):
        self.llm = LlamaAgentWrapper(model_path)
        self.logger = TerminalLogger()
        self.turn_count = 0
    
    def think(self, user_input: str) -> str:
        self.turn_count += 1
        start_time = time.time()
        
        # Log user input
        self.logger.user_input(user_input)
        
        try:
            # Your existing logic here
            response = self.llm.chat_completion(messages)
            
            # Log response
            self.logger.agent_response(response)
            
            # Log performance
            duration = time.time() - start_time
            self.logger.performance("think", duration)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in think: {str(e)}")
            return "Sorry, I encountered an error."
```

### Logging Tool Execution

```python
def execute_tool(self, tool_name: str, args: dict) -> str:
    self.logger.tool_call(tool_name, args)
    
    try:
        start_time = time.time()
        result = self.tools[tool_name](**args)
        duration = time.time() - start_time
        
        self.logger.tool_result(tool_name, str(result), True)
        self.logger.performance(f"tool_{tool_name}", duration)
        
        return str(result)
        
    except Exception as e:
        self.logger.tool_result(tool_name, str(e), False)
        return f"Error: {str(e)}"
```

## Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about program execution
- **WARNING**: Something unexpected happened, but the program is still working
- **ERROR**: A serious problem occurred
- **CRITICAL**: A very serious error occurred

## Configuration Options

### Environment-Based Logging

```python
import os

# Set log level based on environment
log_level = os.getenv("LOG_LEVEL", "INFO")
debug_mode = os.getenv("DEBUG", "false").lower() == "true"

logger = setup_logger("MyAgent", log_level)
```

### File Logging

```python
# Log to both console and file
logger = setup_logger("MyAgent", "INFO", log_to_file="agent.log")
```

### Colored Output

```python
# Enable/disable colors
logger = TerminalLogger(show_colors=True)  # Default
logger = TerminalLogger(show_colors=False)  # For CI/CD
```

## Best Practices

1. **Use appropriate log levels**: Don't log everything as INFO
2. **Include context**: Add relevant information like turn numbers, user IDs, etc.
3. **Log performance**: Track timing for optimization
4. **Handle errors gracefully**: Always log errors with context
5. **Use structured logging**: Include JSON data for complex objects
6. **Consider log rotation**: For production systems with file logging

## Example Output

```
14:30:15 | INFO | LlamaAgent | 🚀 Session 20241201_143015 started - LlamaAgent
14:30:15 | INFO | LlamaAgent | 📁 Model: /path/to/model.gguf
14:30:15 | INFO | LlamaAgent | ⚙️ System: Initialized with 3 tools
14:30:16 | INFO | LlamaAgent | 👤 Turn 1 - User: What's the weather in Paris?
14:30:16 | INFO | LlamaAgent | 🔧 Turn 1 - Tool Call: get_weather
14:30:16 | DEBUG | LlamaAgent |    Args: {"city": "Paris"}
14:30:17 | INFO | LlamaAgent | ✅ Turn 1 - Tool Result (get_weather): Sunny, 22°C
14:30:17 | INFO | LlamaAgent | 🤖 Turn 1 - Agent: The weather in Paris is sunny with a temperature of 22°C.
14:30:17 | INFO | LlamaAgent | ⏱️ Performance: think took 1.23s
```

## Files in This Directory

- `logging_example.py` - Comprehensive examples of different logging approaches
- `logging_config.py` - Professional logging configuration with colors and file support
- `terminal_logger.py` - Simple terminal logger with emojis and colors
- `logging_demo.py` - Interactive demo showing all logging methods
- `LOGGING_GUIDE.md` - This guide

## Running the Demo

```bash
# Run the interactive demo
python logging_demo.py

# Test individual components
python terminal_logger.py
python logging_config.py
```

Choose the logging approach that best fits your needs and integrate it into your existing agent code!
