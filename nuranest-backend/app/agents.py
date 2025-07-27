import os
import logging
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.symptom_classifier import classify_symptom
from app.timeline_parser import extract_week
from app.timeline_checker import check_symptoms_by_week
from app.triage_engine import run_triage_questions
from app.combo_checker import infer_symptom_combinations

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Global variable to hold the agent instance for tool access
_agent_instance = None

@tool
def pregnancy_search_tool(query: str) -> str:
    """Search for pregnancy health information from medical sources. Input should be a clear question about pregnancy health, nutrition, or care."""
    global _agent_instance
    try:
        print("\n📚 Searching medical documents...")
        if _agent_instance is None or _agent_instance.retriever is None:
            return "Sorry, the search system is not properly initialized."
        
        docs = _agent_instance.retriever.invoke(query)

        results = []
        for i, doc in enumerate(docs[:3], 1):
            source = doc.metadata.get('source', None)
            filename = (
                source.split('/')[-1] if source and '/' in source else source
            )
            filename = (
                filename.split('\\')[-1] if filename and '\\' in filename else filename or "Unknown source"
            )
            print(f"📄 Found in: {filename}")
            
            content = doc.page_content.strip().replace("\n", " ")
            if len(content) > 300:
                content = content[:300] + "..."
            
            results.append(f"**Source {i}** ({filename}):\n{content}")

        return "\n\n---\n\n".join(results) if results else "No relevant information found."
    except Exception as e:
        logger.error(f"❌ Error during document search: {e}")
        return "Sorry, I couldn't search the pregnancy database right now."

class PregnancyHealthAgent:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.llm = None
        self.agent_executor = None

    def _initialize_retriever(self):
        try:
            print("🔍 Loading vectorstore and embeddings...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            # Use the existing vectorstore path
            db_path = "vectorstore_local"
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"FAISS DB not found at {db_path}")
            self.vectorstore = FAISS.load_local(db_path, self.embeddings, allow_dangerous_deserialization=True)
            self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            print("✅ Vectorstore loaded successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to load vectorstore: {e}")
            raise

    def initialize_system(self):
        try:
            print("🚀 Initializing Pregnancy Health AI System...")
            global _agent_instance
            _agent_instance = self
            self._initialize_retriever()

            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")

            self.llm = ChatGroq(
                model_name="llama3-8b-8192",
                groq_api_key=groq_api_key,
                temperature=0.1,
                max_tokens=2000,
            )

            # Create the agent
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a specialized pregnancy health assistant. You ONLY answer questions related to pregnancy, maternal health, and prenatal care.

IMPORTANT RULES:
1. ONLY answer pregnancy-related questions (prenatal care, nutrition, complications, exercise, etc.)
2. If asked about non-pregnancy topics, politely redirect to pregnancy health
3. Use the pregnancy_search_tool ONLY for pregnancy-related questions
4. Provide clear, direct answers based on medical information
5. Always include a medical disclaimer for pregnancy health advice
6. Write in a natural, conversational tone - never mention "tool results" or "search results"

Example responses:
- Pregnancy question: "💡 During pregnancy, it's recommended to..."
- Non-pregnancy question: "I'm a pregnancy health assistant. I can help you with questions about pregnancy, prenatal care, maternal health, and related topics. What would you like to know about pregnancy health?"

Focus on being a helpful pregnancy health expert."""),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            agent = create_openai_tools_agent(self.llm, [pregnancy_search_tool], prompt)
            self.agent_executor = AgentExecutor(agent=agent, tools=[pregnancy_search_tool], verbose=False, max_iterations=3)
            
            print("✅ Pregnancy AI system is ready!")
            return True
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            return False

    def process_question(self, query: str) -> dict:
        try:
            print("🤔 Processing your question...")
                
            # 1. Step: LLM-generated final answer (chat-style)
            result = self.agent_executor.invoke({"input": query})
            final_response = result.get("output", "").strip()

            if not final_response:
                return {
                    "message": "I couldn't find a specific answer to your question.",
                    "risk_table": [],
                    "raw_response": ""
                }
        
            # 2. Step: Symptom parsing (example using regex or rule-based)
            symptoms = classify_symptom(query)
            symptom_combinations = infer_symptom_combinations(query)  # Like "headache + swelling" → preeclampsia
            week = extract_week(query)
            timeline_results = check_symptoms_by_week(week, query) if week else [] # e.g., "6 weeks" → ectopic risk

            print("detected symptoms:", symptoms)
            print("detected combinations:", symptom_combinations)
            print("timeline results:", timeline_results)

            # 4. Step: Risk Table (structured response)
            risk_table = []
            if symptom_combinations:
                for combo, risk in symptom_combinations:
                    risk_table.append({
                        "Symptoms": combo,
                        "Risk Condition": risk,
                        "Recommended Action": "Seek immediate medical attention" if risk.lower() in ["preeclampsia", "ectopic pregnancy"] else "Monitor and consult OB-GYN"
                    })

            # # Format the response professionally
            formatted_response = self._format_response(final_response)

            # 5. Step: Construct structured response
            response_payload = {
                "message": formatted_response,
                "risk_table": risk_table,
                "symptoms": symptoms,
                "symptom_combinations": symptom_combinations,
                "timeline_results": timeline_results,
                "raw_response": result,
            }

            

            return response_payload
            # return response_payload
        except Exception as e:
            logger.error(f"❌ Error processing question: {e}")
            return {
                "message": "Sorry, an error occurred while processing your question.",
                "risk_table": [],
                "raw_response": "",
                "timeline_results": [],
                "symptom_combinations": [],
                "symptoms": [],
            }    
    def get_sources_for_question(self, query: str) -> list:
        """Get sources used for a question (for terminal display)"""
        try:
            if not self.retriever:
                return []
            
            docs = self.retriever.invoke(query)
            sources = []
            
            for i, doc in enumerate(docs[:3], 1):
                source = doc.metadata.get('source', 'Unknown source')
                filename = source.split('/')[-1] if '/' in source else source
                filename = filename.split('\\')[-1] if '\\' in filename else filename
                sources.append(filename)
            
            return sources
        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            return []

    def _format_response(self, response: str) -> str:
        """Format the response in a professional manner"""
        # Remove any "tool results" language
        response = response.replace("Based on the results from the tool", "")
        response = response.replace("Based on the tool results", "")
        response = response.replace("Based on the search results", "")
        response = response.replace("According to the tool results", "")
        response = response.replace("The tool results show", "")
        response = response.replace("call, it is", "it is")
        response = response.replace("call it is", "it is")
        
        # Clean up the response
        lines = response.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Format bullet points
            if line.startswith('*'):
                line = f"• {line[1:].strip()}"
            elif line.startswith('-'):
                line = f"• {line[1:].strip()}"
            elif line.startswith('•'):
                line = line.strip()
                
            # Format headers and important points
            if line.endswith(':') and not line.startswith('•'):
                line = f"📋 {line}"
            elif any(keyword in line.lower() for keyword in ['recommended', 'important', 'should', 'must', 'avoid']):
                line = f"💡 {line}"
                
            formatted_lines.append(line)
        
        # Join lines with proper spacing
        formatted_text = ' '.join(formatted_lines)
        
        # Clean up multiple spaces and improve readability
        formatted_text = ' '.join(formatted_text.split())
        
        # Add medical disclaimer only for pregnancy-related content
        if ("pregnancy" in formatted_text.lower() or "prenatal" in formatted_text.lower() or "maternal" in formatted_text.lower()) and "consult" not in formatted_text.lower() and "healthcare" not in formatted_text.lower():
            formatted_text += " ⚠️ **Medical Disclaimer:** This information is for educational purposes only. Always consult with your healthcare provider for personalized medical advice."
        
        return formatted_text
        


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏥 I'M NURANEST: PREGNANCY AI ASSISTANT")
    print("=" * 60)
    print("📚 Knowledge Base: WHO, NIH, CDC, NHS, Mayo Clinic")
    print("🤖 Powered by: Groq Llama3-8b")
    print("🔍 Ask me anything about pregnancy health!")
    print("💡 Type 'exit' to quit")
    print("=" * 60)
    
    agent = PregnancyHealthAgent()
    if agent.initialize_system():
        print("✅ System ready! You can start asking questions.")
        while True:
            try:
                question = input("\n🧠 You: ").strip()
                if question.lower() in ["exit", "quit"]:
                    print("👋 Thank you for using Pregnancy AI Assistant!")
                    break
                if not question:
                    continue

                full_context = ""

                # extract week if applicable
                week = extract_week(question)
                timeline_results = check_symptoms_by_week(week, question) if week else []

                # symptom classification
                classifications = classify_symptom(question)
                combination_results = infer_symptom_combinations(question)

                if timeline_results.__contains__(question) or combination_results.__contains__(question) or classifications.__contains__(question):
                    print("⚠️ High-risk symptoms detected! Immediate medical attention is recommended.")
                    # Process the question with the agent
                    response = agent.process_question(question)
                else:
                    # Ask more questions proactively from the user
                    user_data = run_triage_questions(question)
                    # 🧠 Merge responses
                    full_context = " ".join(user_data.values()).lower()

                    # extract week if applicable
                    week = extract_week(full_context)
                    timeline_results = check_symptoms_by_week(week, full_context) if week else []

                    # symptom classification
                    classifications = classify_symptom(full_context)
                    combination_results = infer_symptom_combinations(full_context)

                    response = agent.process_question(full_context)
                
                

                response_json = {
                    "status": "success",
                    "response": {
                        "chatbot_answer": response,
                        "symptom_combinations": combination_results,
                        "timeline_conditions": timeline_results,
                        "combination_inferences": combination_results, 
                        },
                "confidence_score": response.get("confidence_score", None),
                # "timestamp": datetime.now().isoformat(),
                "processing_time": response.get("processing_time", 0.0),
                "risk_table": response.get("risk_table", []),
                }
                print(json.dumps(response_json, indent=2))

                # Show classification results
                if classifications:
                    print("\n⚠️ Symptom Risk Summary:")
                    for c in classifications:
                        print(f"- '{c['matched_phrase']}' → Risk: {c['risk']}, Condition: {c['condition']}")
                        print(f"  Suggested Action: {c['action']}")

                if week and timeline_results:
                    print("\n📅 Timeline-Aware Risk(s):")
                    for res in timeline_results:
                        print(f"- Week {week}: '{res['symptom']}' → {res['condition']} ({res['risk']})")
                        print(f"  Action: {res['action']}")

                if combination_results:
                    print("\n🧩 Inferred Risk Combination(s):")
                    for res in combination_results:
                        print(f"- Symptoms: {', '.join(res['matched_symptoms'])} → {res['condition']} ({res['risk']})")
                        print(f"  Urgent Action: {res['action']}")
                else:
                    print("\n✅ No high-risk symptom combinations detected.")

                # Show sources used
                if full_context == "":
                    print("\n🔍 No sources used for this question.")
                    sources = agent.get_sources_for_question(question)
                    if sources:
                        print(f"\n📚 Sources used:")
                        for i, source in enumerate(sources, 1):
                            print(f"  {i}. {source}")
                
                    print("\n" + "-" * 60)
                else:
                    sources = agent.get_sources_for_question(full_context)
                    if sources:
                        print(f"\n📚 Sources used:")
                        for i, source in enumerate(sources, 1):
                            print(f"  {i}. {source}")
                
                    print("\n" + "-" * 60)
                
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
                print(f"\n❌ Sorry, I encountered an error: {e}")
                print("💡 Please try asking your question again.")
    else:
        print("❌ Failed to initialize the AI system. Please check your configuration.")
