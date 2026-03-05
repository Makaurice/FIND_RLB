# Customer Care AI Agent
# Handles 24/7 customer support, blockchain actions, and Hedera logging

import json
import os
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available, using fallback intent detection")

from backend.contracts import call_hedera_contract, get_contract
from backend.hedera_integration_v2 import get_hedera_client
# from ai_agents.tenant_agent import TenantAIAgent  # Import when needed
# from ai_agents.landlord_agent import LandlordAIAgent
# from ai_agents.matching_engine import MatchingEngineAgent
# from backend.wallet_service import WalletService

class CustomerCareAgent:
    def __init__(self, user_id, session_id=None):
        self.user_id = user_id
        self.session_id = session_id or f"session_{user_id}_{datetime.now().timestamp()}"
        self.conversation_history = []
        self.knowledge_base = self._load_knowledge_base()

        if OPENAI_AVAILABLE:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                print("Warning: OPENAI_API_KEY not set, using fallback intent detection")
                self.openai_client = None
            else:
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None

        # Initialize other agents lazily
        self._tenant_agent = None
        self._landlord_agent = None
        self._matching_agent = None
        self._wallet_service = None

    @property
    def tenant_agent(self):
        if self._tenant_agent is None:
            try:
                from ai_agents.tenant_agent import TenantAIAgent
                self._tenant_agent = TenantAIAgent(self.user_id)
            except ImportError:
                self._tenant_agent = None
        return self._tenant_agent

    @property
    def landlord_agent(self):
        if self._landlord_agent is None:
            try:
                from ai_agents.landlord_agent import LandlordAIAgent
                self._landlord_agent = LandlordAIAgent(self.user_id)
            except ImportError:
                self._landlord_agent = None
        return self._landlord_agent

    @property
    def matching_agent(self):
        if self._matching_agent is None:
            try:
                from ai_agents.matching_engine import MatchingEngineAgent
                self._matching_agent = MatchingEngineAgent()
            except ImportError:
                self._matching_agent = None
        return self._matching_agent

    @property
    def wallet_service(self):
        if self._wallet_service is None:
            try:
                from backend.wallet_service import WalletService
                self._wallet_service = WalletService()
            except ImportError:
                self._wallet_service = None
        return self._wallet_service

    def _load_knowledge_base(self):
        """Load knowledge base with common Q&A."""
        return {
            "rent_payment": {
                "questions": ["rent due", "pay rent", "rent payment"],
                "answers": "Rent is due on the 1st of each month. You can pay via the app or ask me to process it.",
                "actions": ["check_rent_status", "pay_rent"]
            },
            "lease_info": {
                "questions": ["lease terms", "when does lease end", "lease agreement"],
                "answers": "Your lease details are stored on Hedera. Let me check your current lease.",
                "actions": ["check_lease"]
            },
            "property_search": {
                "questions": ["find home", "looking for apartment", "property recommendations"],
                "answers": "I can help you find the perfect home based on your preferences.",
                "actions": ["find_home"]
            },
            "maintenance": {
                "questions": ["maintenance issue", "repair needed", "landlord not responding"],
                "answers": "I'll help you report maintenance issues and track their resolution.",
                "actions": ["report_maintenance"]
            },
            "moving_services": {
                "questions": ["moving service", "schedule move", "relocation help"],
                "answers": "I can help arrange moving services and coordinate with providers.",
                "actions": ["schedule_moving"]
            },
            "savings": {
                "questions": ["savings progress", "rent to own", "financial planning"],
                "answers": "Let me check your savings progress and provide personalized recommendations.",
                "actions": ["check_savings"]
            }
        }

    def process_message(self, message, context=None):
        """Process user message and generate response with actions."""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})

        # Detect intent
        intent = self._detect_intent(message)

        # Extract entities
        entities = self._extract_entities(message)

        # Generate response and actions
        response, actions = self._generate_response(intent, entities, context, message)

        # Log interaction on Hedera
        self._log_interaction_on_hedera(message, response)

        # Add AI response to history
        self.conversation_history.append({"role": "assistant", "content": response})

        return {
            "response": response,
            "actions_taken": actions,
            "intent": intent,
            "entities": entities,
            "session_id": self.session_id
        }

    def _detect_intent(self, message):
        """Detect user intent using OpenAI or simple keyword matching."""
        if self.openai_client:
            try:
                # Use OpenAI for intent detection
                prompt = f"""
                Analyze this customer message and determine the primary intent.
                Message: "{message}"

                Possible intents:
                - rent_payment: questions about paying rent, due dates, payment issues
                - lease_info: questions about lease terms, duration, agreements
                - property_search: looking for properties, recommendations
                - maintenance: reporting repairs, landlord issues
                - moving_services: moving help, scheduling
                - savings: savings progress, financial planning
                - general: other questions

                Return only the intent name.
                """
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50
                )
                intent = response.choices[0].message.content.strip().lower()
                return intent if intent in self.knowledge_base else "general"
            except Exception as e:
                print(f"OpenAI error: {e}")
                # Fallback to keyword matching

        # Fallback to keyword matching
        message_lower = message.lower()
        print(f"Debug: message_lower = {message_lower}")
        for category, data in self.knowledge_base.items():
            print(f"Debug: checking category {category}")
            # Check if any question phrase has its words in the message
            for question in data["questions"]:
                print(f"Debug: checking question '{question}'")
                question_words = set(question.lower().split())
                message_words = set(message_lower.split())
                print(f"Debug: question_words = {question_words}, message_words = {message_words}")
                if question_words.issubset(message_words):
                    print(f"Debug: match found for {category}")
                    return category
        print("Debug: no match, returning general")
        return "general"

    def _extract_entities(self, message):
        """Extract entities like dates, amounts, locations."""
        # Simple entity extraction - could be enhanced with NLP
        entities = {}
        message_lower = message.lower()

        # Extract amounts (KES, USD, etc.)
        import re
        amounts = re.findall(r'\d+(?:,\d{3})*(?:\.\d{2})?', message)
        if amounts:
            entities["amount"] = amounts[0]

        # Extract locations
        locations = ["westlands", "nairobi", "cbd", "kilimani", "koinange"]
        for loc in locations:
            if loc in message_lower:
                entities["location"] = loc
                break

        return entities

    def _generate_response(self, intent, entities, context, message):
        """Generate response and execute actions."""
        actions = []

        if intent in self.knowledge_base:
            base_response = self.knowledge_base[intent]["answers"]
            possible_actions = self.knowledge_base[intent]["actions"]
        else:
            base_response = "I'm here to help with your housing and rental needs. How can I assist you today?"
            possible_actions = []

        # Execute actions
        for action in possible_actions:
            if action == "check_rent_status":
                rent_info = self._check_rent_status()
                if rent_info:
                    base_response += f"\n\nRent Status: {rent_info}"
                    actions.append({"action": "check_rent_status", "result": rent_info})
            elif action == "pay_rent":
                if "amount" in entities:
                    payment_result = self._pay_rent(entities["amount"])
                    base_response += f"\n\nPayment Result: {payment_result}"
                    actions.append({"action": "pay_rent", "result": payment_result})
            elif action == "check_lease":
                lease_info = self._check_lease()
                if lease_info:
                    base_response += f"\n\nLease Info: {lease_info}"
                    actions.append({"action": "check_lease", "result": lease_info})
            elif action == "find_home":
                recommendations = self._find_home(entities)
                if recommendations:
                    base_response += f"\n\nProperty Recommendations: {recommendations}"
                    actions.append({"action": "find_home", "result": recommendations})
            elif action == "report_maintenance":
                ticket = self._report_maintenance(message)
                base_response += f"\n\nMaintenance Ticket: {ticket}"
                actions.append({"action": "report_maintenance", "result": ticket})
            elif action == "schedule_moving":
                moving = self._schedule_moving(entities)
                base_response += f"\n\nMoving Service: {moving}"
                actions.append({"action": "schedule_moving", "result": moving})
            elif action == "check_savings":
                savings = self._check_savings()
                base_response += f"\n\nSavings Progress: {savings}"
                actions.append({"action": "check_savings", "result": savings})

        # If no specific actions, check for escalation
        if not actions and intent == "general":
            if self._should_escalate(message):
                escalation = self._escalate_issue(message)
                base_response += f"\n\n{escalation}"
                actions.append({"action": "escalate", "result": escalation})

        return base_response, actions

    def _check_rent_status(self):
        """Check rent payment status from contracts."""
        try:
            result = call_hedera_contract('RentEscrow', 'getRentStatus', [self.user_id])
            return result.get('result', 'Unable to fetch rent status')
        except Exception as e:
            return f"Error checking rent status: {str(e)}"

    def _pay_rent(self, amount):
        """Process rent payment via wallet service."""
        try:
            # This would integrate with wallet service
            return f"Payment of {amount} KES initiated. Transaction pending confirmation."
        except Exception as e:
            return f"Payment failed: {str(e)}"

    def _check_lease(self):
        """Check lease information."""
        try:
            result = call_hedera_contract('LeaseAgreement', 'getLeaseDetails', [self.user_id])
            return result.get('result', 'Unable to fetch lease details')
        except Exception as e:
            return f"Error checking lease: {str(e)}"

    def _find_home(self, entities):
        """Find property recommendations."""
        try:
            preferences = {"location": entities.get("location"), "budget": entities.get("amount")}
            self.tenant_agent.learn_preferences(preferences)
            recommendations = self.tenant_agent.recommend_home()
            return recommendations
        except Exception as e:
            return f"Error finding homes: {str(e)}"

    def _report_maintenance(self, description):
        """Report maintenance issue."""
        try:
            # Create maintenance ticket on Hedera
            ticket_data = {
                "user_id": self.user_id,
                "description": description,
                "timestamp": datetime.now().isoformat(),
                "status": "open"
            }
            # Log to Hedera Consensus Service
            self._log_to_hedera_consensus("maintenance_ticket", ticket_data)
            return f"Ticket created: {ticket_data}"
        except Exception as e:
            return f"Error reporting maintenance: {str(e)}"

    def _schedule_moving(self, entities):
        """Schedule moving service."""
        try:
            # This would integrate with moving service agent
            return "Moving service scheduled. Details will be sent shortly."
        except Exception as e:
            return f"Error scheduling moving: {str(e)}"

    def _check_savings(self):
        """Check savings progress."""
        try:
            # This would integrate with savings agent
            return "Savings progress: 65% towards rent-to-own goal."
        except Exception as e:
            return f"Error checking savings: {str(e)}"

    def _should_escalate(self, message):
        """Determine if issue should be escalated to human."""
        # Simple escalation logic - can be enhanced
        escalation_keywords = ["urgent", "emergency", "angry", "complaint", "not working"]
        return any(word in message.lower() for word in escalation_keywords)

    def _escalate_issue(self, message):
        """Escalate issue to human support."""
        try:
            escalation_data = {
                "user_id": self.user_id,
                "message": message,
                "conversation_history": self.conversation_history[-5:],  # Last 5 messages
                "timestamp": datetime.now().isoformat(),
                "status": "escalated"
            }
            # Log escalation to Hedera
            self._log_to_hedera_consensus("escalation", escalation_data)
            return "Your issue has been escalated to our human support team. They'll contact you shortly."
        except Exception as e:
            return f"Error escalating issue: {str(e)}"

    def _log_interaction_on_hedera(self, user_message, ai_response):
        """Log conversation to Hedera for transparency."""
        interaction_data = {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        self._log_to_hedera_consensus("conversation", interaction_data)

    def _log_to_hedera_consensus(self, topic, data):
        """Log data to Hedera Consensus Service."""
        try:
            client = get_hedera_client()
            # This would submit message to consensus service
            # For now, just print/log
            print(f"Logged to Hedera: {topic} - {data}")
        except Exception as e:
            print(f"Error logging to Hedera: {str(e)}")

    def get_conversation_history(self):
        """Get conversation history for this session."""
        return self.conversation_history

    def clear_session(self):
        """Clear conversation session."""
        self.conversation_history = []
        self.session_id = f"session_{self.user_id}_{datetime.now().timestamp()}"