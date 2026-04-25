"""
Simple LangGraph Example

This example demonstrates the basic concepts of LangGraph:
- Creating a graph
- Defining nodes (functions that process state)
- Defining edges (connections between nodes)
- Running the graph with state
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END


# Step 1: Define the State
# The state is a dictionary that gets passed between nodes
class GraphState(TypedDict):
    """State that flows through the graph"""
    message: str
    step_count: int
    result: str


# Step 2: Define Node Functions
# Each node is a function that takes state and returns updated state
def start_node(state: GraphState) -> GraphState:
    """First node - initializes the processing"""
    print(f"🚀 Starting with message: '{state['message']}'")
    return {
        "message": state["message"],
        "step_count": 1,
        "result": f"Started processing: {state['message']}"
    }


def process_node(state: GraphState) -> GraphState:
    """Second node - processes the message"""
    print(f"⚙️  Processing step {state['step_count']}")
    processed = state["message"].upper()
    return {
        "message": state["message"],
        "step_count": state["step_count"] + 1,
        "result": f"Processed: {processed}"
    }


def finish_node(state: GraphState) -> GraphState:
    """Final node - completes the workflow"""
    print(f"✅ Finishing at step {state['step_count']}")
    return {
        "message": state["message"],
        "step_count": state["step_count"] + 1,
        "result": f"Final result: {state['result']} | Total steps: {state['step_count']}"
    }


# Step 3: Build the Graph
def create_simple_graph():
    """Creates and configures a simple LangGraph workflow"""
    
    # Create a new StateGraph with our state type
    workflow = StateGraph(GraphState)
    
    # Add nodes to the graph
    # Each node is a function that processes the state
    workflow.add_node("start", start_node)
    workflow.add_node("process", process_node)
    workflow.add_node("finish", finish_node)
    
    # Define the edges (flow between nodes)
    # This creates a linear flow: start -> process -> finish -> END
    workflow.set_entry_point("start")  # Where the graph starts
    workflow.add_edge("start", "process")  # start connects to process
    workflow.add_edge("process", "finish")  # process connects to finish
    workflow.add_edge("finish", END)  # finish connects to END (terminates)
    
    # Compile the graph into an executable
    app = workflow.compile()
    
    return app


# Step 4: Run the Graph
def run_example():
    """Runs a simple example through the graph"""
    
    # Create the graph
    app = create_simple_graph()
    
    # Initial state
    initial_state = {
        "message": "Hello, LangGraph!",
        "step_count": 0,
        "result": ""
    }
    
    print("=" * 50)
    print("Running LangGraph Example")
    print("=" * 50)
    print()
    
    # Invoke the graph with initial state
    # The graph will execute all nodes in sequence
    final_state = app.invoke(initial_state)
    
    print()
    print("=" * 50)
    print("Final State:")
    print("=" * 50)
    print(f"Message: {final_state['message']}")
    print(f"Step Count: {final_state['step_count']}")
    print(f"Result: {final_state['result']}")
    
    return final_state


if __name__ == "__main__":
    # Run the example
    result = run_example()
    
    print("\n" + "=" * 50)
    print("Graph Explanation:")
    print("=" * 50)
    print("""
    LangGraph allows you to create stateful workflows:
    
    1. State: A TypedDict that flows through all nodes
    2. Nodes: Functions that process and modify the state
    3. Edges: Connections that define the flow between nodes
    4. Execution: The graph runs nodes in sequence based on edges
    
    In this example:
    start → process → finish → END
    
    Each node receives the state, modifies it, and passes it to the next node.
    """)
