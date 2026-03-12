# Agentic Travel Planner 
An AI-powered travel planning assistant that transforms free-form trip requests into structured travel requirements, generates day-by-day itineraries, and refines them through a multi-step review workflow.

This project is built with **LangChain**, **Ollama**, and **Streamlit** to demonstrate how agent-style LLM pipelines can be used for real-world planning tasks.

---

## Features

- Accepts natural language travel requirements
- Extracts structured trip details from unstructured input
- Identifies missing information and asks clarifying questions
- Generates realistic day-by-day itineraries
- Adds travel pacing, meal planning, and transport notes
- Reviews and improves the itinerary in a final refinement step
- Simple Streamlit interface for quick interaction

---

## How It Works

The application follows a 3-step agent workflow:

### 1. Requirements Extraction Agent
This agent reads the user’s input and converts it into structured trip requirements such as:

- destination
- start and end dates
- duration
- travelers count
- travel style
- budget
- transport and lodging preferences
- must-do activities
- constraints

If important details are missing, it asks clarifying questions instead of inventing information.

---

### 2. Trip Planner Agent
This agent takes the structured requirements and creates a day-by-day itinerary.

It includes:

- trip summary
- assumptions when data is missing
- morning / afternoon / evening plans
- meal suggestions
- local transport notes
- daily cost range in relative terms
- packing and preparation checklist

---

### 3. Review Agent
This final agent improves the generated itinerary by:

- removing redundancy
- improving flow and readability
- balancing daily pacing
- adding practical travel tips
- refining the overall final output
