"""
Llama.cpp Agent Example
Shows how to integrate llama.cpp into agent architecture with tools
"""

import json
import time
from typing import Dict, List, Any
from llama_agent_wrapper import LlamaAgentWrapper
from logging_config import AgentEventLogger


class LlamaAgent:
    """
    Agent that uses llama.cpp for local inference with tool capabilities
    """
    
    def __init__(self, model_path: str, tools: List[Dict] = None, log_level: str = "INFO"):
        """
        Initialize the agent
        
        Args:
            model_path: Path to GGUF model
            tools: List of available tools
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.llm = LlamaAgentWrapper(model_path)
        self.tools = tools or []
        self.conversation_history = []
        self.turn_count = 0
        
        # Setup event logging
        self.event_logger = AgentEventLogger("LlamaAgent", log_level)
        self.event_logger.log_session_start("LlamaAgent", model_path)
        self.event_logger.log_system_event(f"Initialized with {len(self.tools)} tools")
    
    def add_tool(self, name: str, description: str, func):
        """Add a tool to the agent"""
        self.tools.append({
            "name": name,
            "description": description,
            "function": func
        })
        self.event_logger.log_system_event(f"Added tool: {name}")
    
    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Execute a tool by name with given arguments"""
        for tool in self.tools:
            if tool["name"] == tool_name:
                try:
                    start_time = time.time()
                    result = tool["function"](**args)
                    duration = time.time() - start_time
                    
                    self.event_logger.log_tool_result(tool_name, str(result), True, self.turn_count)
                    self.event_logger.log_performance(f"tool_{tool_name}", duration)
                    
                    return str(result)
                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)}"
                    self.event_logger.log_tool_result(tool_name, error_msg, False, self.turn_count)
                    return error_msg
        return f"Tool {tool_name} not found"
    
    def think(self, user_input: str) -> str:
        """
        Main agent reasoning loop
        """
        start_time = time.time()
        self.turn_count += 1
        
        # Log user input
        self.event_logger.log_user_input(user_input, self.turn_count)
        
        try:
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Create system prompt with tool descriptions
            system_prompt = self._create_system_prompt()
            
            # Prepare messages for LLM
            messages = [{"role": "system", "content": system_prompt}] + self.conversation_history
            
            # Get LLM response
            response = self.llm.chat_completion(messages, max_tokens=512)
            assistant_response = response["choices"][0]["message"]["content"]
            
            # Check if response contains tool calls
            tool_calls = self._extract_tool_calls(assistant_response)
            
            if tool_calls:
                # Log tool calls
                for tool_call in tool_calls:
                    self.event_logger.log_tool_call(tool_call["name"], tool_call["args"], self.turn_count)
                
                # Execute tools and get results
                tool_results = []
                for tool_call in tool_calls:
                    result = self.execute_tool(tool_call["name"], tool_call["args"])
                    tool_results.append(f"Tool {tool_call['name']} result: {result}")
                
                # Create follow-up message with tool results
                tool_results_text = "\n".join(tool_results)
                follow_up_messages = messages + [
                    {"role": "assistant", "content": assistant_response},
                    {"role": "user", "content": f"Tool results: {tool_results_text}\n\nPlease provide a final answer based on these results."}
                ]
                
                # Get final response
                final_response = self.llm.chat_completion(follow_up_messages, max_tokens=512)
                final_answer = final_response["choices"][0]["message"]["content"]
                
                # Update conversation history
                self.conversation_history.append({"role": "assistant", "content": final_answer})
                
                # Log final response
                self.event_logger.log_agent_response(final_answer, self.turn_count)
                
                # Log performance
                duration = time.time() - start_time
                self.event_logger.log_performance("think_with_tools", duration, {
                    "tools_used": len(tool_calls),
                    "total_tokens": response["usage"]["total_tokens"] + final_response["usage"]["total_tokens"]
                })
                
                return final_answer
            else:
                # No tools needed, return direct response
                self.conversation_history.append({"role": "assistant", "content": assistant_response})
                
                # Log response
                self.event_logger.log_agent_response(assistant_response, self.turn_count)
                
                # Log performance
                duration = time.time() - start_time
                self.event_logger.log_performance("think_direct", duration, {
                    "total_tokens": response["usage"]["total_tokens"]
                })
                
                return assistant_response
                
        except Exception as e:
            self.event_logger.log_error(str(e), "think method", self.turn_count)
            return "Sorry, I encountered an error processing your request."
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with tool descriptions"""
        base_prompt = """You are a helpful AI assistant with access to tools. 
When you need to use a tool, respond with a JSON object in this format:
{"tool_calls": [{"name": "tool_name", "args": {"arg1": "value1"}}]}

Available tools:"""
        
        for tool in self.tools:
            base_prompt += f"\n- {tool['name']}: {tool['description']}"
        
        base_prompt += "\n\nIf you don't need tools, respond normally with text."
        return base_prompt
    
    def _extract_tool_calls(self, response: str) -> List[Dict]:
        """Extract tool calls from LLM response"""
        try:
            # Look for JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                if "tool_calls" in parsed:
                    return parsed["tool_calls"]
        except (json.JSONDecodeError, KeyError):
            pass
        
        return []


# Example tools
def get_weather(city: str) -> str:
    """Get weather for a city (mock implementation)"""
    return f"The weather in {city} is sunny with 22°C"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression (mock implementation)"""
    try:
        # Simple eval for demo - in production, use a safer math parser
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except:
        return f"Could not calculate {expression}"

def search_web(query: str) -> str:
    """Search the web (mock implementation)"""
    return f"Search results for '{query}': This is a mock search result."


# Example usage
if __name__ == "__main__":
    # Initialize agent with model
    agent = LlamaAgent(
        model_path="/Users/pedrorodriguezdeledesmajimenez/scripts/llm_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    )
    
    # Add tools
    agent.add_tool("get_weather", "Get current weather for a city", get_weather)
    agent.add_tool("calculate", "Calculate mathematical expressions", calculate)
    agent.add_tool("search_web", "Search the internet for information", search_web)
    
    # Test the agent
    print("🤖 Llama Agent Ready!")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        print("Agent: ", end="")
        response = agent.think(user_input)
        print(response)
        print()
