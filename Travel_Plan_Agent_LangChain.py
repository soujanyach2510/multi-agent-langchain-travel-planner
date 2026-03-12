import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

st.title("Travel Agent Architecture")

input_text = st.text_area('enter your requirements',height=200)
button = st.button("Run the agents")

if button:
    if input_text:
        llm = Ollama(model='llama3.1',temperature=0.2)
         #ClientAgent
        Client_template="""You are the Client Requirements Agent.
        Goal:
        Extract trip requirements from the user's input WITHOUT inventing details.
        If required details are missing, ask clarifying questions.

        User input: {question}

        Output rules:
        1) Do NOT assume missing info.
        2) Return output in TWO sections exactly:

        SECTION A: REQUIREMENTS (JSON)
        Return a JSON object with keys:
        - destination
        - start_date
        - end_date
        - duration_days
        - travelers_count
        - traveler_type (solo/couple/family/friends)
        - budget_total (with currency)
        - style (relaxation/adventure/culture/mixed)
        - pace (slow/moderate/fast)
        - must_do
        - avoid
        - constraints (diet, mobility, kids, etc.)
        - lodging_preference
        - transport_preference
        - departure_city
        - notes

        If unknown, set the value to null or [].

        SECTION B: CLARIFYING QUESTIONS
        Ask 3–8 precise questions ONLY for missing high-impact fields (dates, destination, budget, travelers). """
        Client_propmt=PromptTemplate(template=Client_template,input_variables=['question'])
        client_chain = Client_propmt|llm
        st.subheader("🔍 Agent 1 is on the go! ")
        client_response = client_chain.invoke({'question':input_text})
        #st.markdown(client_response)


        # Building trip_planner agent
        trip_template="""You are a Trip Planner Agent.

        Task:
        Create a realistic itinerary using ONLY the requirements provided below.
        If key fields are null (destination/dates/budget), produce a draft itinerary with assumptions listed clearly.

        Requirements JSON:
        {client_response}

        Rules:
        - Be realistic: include travel time buffers, meal times, rest time.
        - Avoid hallucinating specific prices, opening hours, or exact ticket rules.
        - Provide options: give 2 alternatives per day (Plan A / Plan B) when possible.
        - Keep it memorable: 1 "highlight moment" per day.

        Output format:
        1) Trip Summary (destination, duration, style, budget approach)
        2) Assumptions (ONLY if requirements have nulls)
        3) Day-by-Day Itinerary:
        For each day:
        - Morning / Afternoon / Evening
        - Meals
        - Local transport notes
        - Estimated daily cost range (low/high) in relative terms (Budget/Moderate/Premium), not exact dollars
        4) Packing & Prep Checklist

        """
        trip_prompt=PromptTemplate(template=trip_template,input_variables=["client_response"])

        trip_chain=trip_prompt|llm

        st.subheader("🔍 Agent 2 is on the go! ")
        trip_planner_output=trip_chain.invoke({"client_response":client_response})
        #st.markdown(research_output)


        # Building Critic agent
        
        critic_template="""You are a Senior Review Agent.

        Input itinerary:
        {trip_planner_output}

        Task:
        Improve clarity and feasibility.
        - Remove redundancy and generic filler.
        - Ensure each day has logical flow (location clustering).
        - Ensure pacing matches a typical traveler (not exhausting).
        - Add small practical tips (local etiquette, safety, timing buffers) WITHOUT making up facts.

        Output format:
        1) Revised Itinerary (final)
        2) Top 5 Improvements Made (bullet list)

        """

        critic_prompt=PromptTemplate(template=critic_template,input_variables=["trip_planner_output"])

        critic_chain=critic_prompt|llm

        st.subheader("🔍 Agent 3 is on the go! and here is the output:\n")
        critic_output=critic_chain.invoke({"trip_planner_output":trip_planner_output})
        st.markdown(critic_output)



