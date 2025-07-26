# agents/agent_router.py

import re
from typing import Dict, List, Tuple, Optional
import json

class AgentRouter:
    """
    Central router that determines which agent should handle incoming requests
    """
    
    def __init__(self):
        self.tenancy_keywords = [
            'landlord', 'tenant', 'rent', 'deposit', 'evict', 'eviction', 'lease', 
            'notice', 'rights', 'law', 'legal', 'contract', 'agreement', 'rental',
            'tenancy', 'move out', 'move in', 'security deposit', 'rent increase',
            'repair responsibility', 'maintenance', 'utilities', 'subletting',
            'termination', 'breach', 'violation', 'dispute', 'court'
        ]
        
        self.issue_keywords = [
            'damage', 'broken', 'crack', 'leak', 'leaking', 'mold', 'mould',
            'repair', 'fix', 'problem', 'issue', 'maintenance', 'water damage',
            'electrical', 'plumbing', 'heating', 'cooling', 'hvac', 'paint',
            'ceiling', 'wall', 'floor', 'window', 'door', 'fixture', 'stain',
            'smell', 'odor', 'noise', 'insulation', 'ventilation'
        ]
        
        self.clarification_responses = [
            "I'd like to help you with the right specialist! Could you clarify what type of assistance you need?",
            "To provide the best help, could you tell me if you have a property issue to inspect or a tenancy question?",
            "I can help with both property issues and rental questions. What specific situation are you dealing with?"
        ]

    def route_request(self, text: str, has_image: bool = False, context: Dict = None) -> str:
        """
        Route the request to the appropriate agent
        
        Args:
            text: User input text
            has_image: Whether an image was uploaded
            context: Conversation context
            
        Returns:
            Agent identifier ('agent1', 'agent2', or 'router')
        """
        
        # Priority 1: If image is uploaded, likely an issue detection request
        if has_image:
            return 'agent1'
        
        # Priority 2: Analyze text content
        text_lower = text.lower()
        
        # Count keyword matches
        tenancy_score = sum(1 for keyword in self.tenancy_keywords if keyword in text_lower)
        issue_score = sum(1 for keyword in self.issue_keywords if keyword in text_lower)
        
        # Enhanced pattern matching
        tenancy_patterns = [
            r'can\s+(my\s+)?landlord',
            r'tenant\s+rights?',
            r'rent\s+increase',
            r'security\s+deposit',
            r'evict(ion)?',
            r'lease\s+agreement',
            r'notice\s+period',
            r'move\s+out',
            r'terminate\s+lease'
        ]
        
        issue_patterns = [
            r'what\'?s\s+wrong\s+with',
            r'fix\s+this',
            r'repair\s+needed',
            r'damage\s+to',
            r'problem\s+with',
            r'issue\s+with',
            r'broken\s+\w+',
            r'leak(ing)?',
            r'crack\s+in'
        ]
        
        # Check for pattern matches
        for pattern in tenancy_patterns:
            if re.search(pattern, text_lower):
                tenancy_score += 2
        
        for pattern in issue_patterns:
            if re.search(pattern, text_lower):
                issue_score += 2
        
        # Decision logic
        if tenancy_score > issue_score and tenancy_score > 0:
            return 'agent2'
        elif issue_score > tenancy_score and issue_score > 0:
            return 'agent1'
        elif issue_score == tenancy_score and issue_score > 0:
            # Equal scores - check context or ask for clarification
            if context and 'last_agent' in context:
                return context['last_agent']
            return 'router'
        else:
            # No clear indicators
            return 'router'

    def generate_clarification_response(self, text: str, context: Dict = None) -> Tuple[str, float]:
        """
        Generate a clarification response when routing is unclear
        
        Args:
            text: User input
            context: Conversation context
            
        Returns:
            Tuple of (response_text, confidence_score)
        """
        import random
        
        base_response = random.choice(self.clarification_responses)
        
        # Add specific guidance based on partial matches
        text_lower = text.lower()
        suggestions = []
        
        if any(word in text_lower for word in ['photo', 'image', 'picture', 'show', 'look']):
            suggestions.append("📸 **Upload an image** if you have a property issue that needs visual inspection")
        
        if any(word in text_lower for word in ['question', 'ask', 'know', 'tell']):
            suggestions.append("❓ **Ask a question** about tenancy laws, rental rights, or landlord responsibilities")
        
        if not suggestions:
            suggestions = [
                "🔍 **Property Issues:** Upload images of damage, leaks, cracks, or broken fixtures",
                "⚖️ **Tenancy Questions:** Ask about rental laws, tenant rights, or lease agreements"
            ]
        
        full_response = f"{base_response}\n\n" + "\n".join(suggestions)
        full_response += "\n\n**How would you like to proceed?**"
        
        return full_response, 1.0

    def analyze_conversation_flow(self, messages: List[Dict]) -> Dict:
        """
        Analyze conversation flow for insights
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Analysis results
        """
        agent_usage = {'agent1': 0, 'agent2': 0, 'router': 0}
        topics = []
        
        for msg in messages:
            if msg.get('type') == 'bot' and msg.get('agent'):
                agent_usage[msg['agent']] = agent_usage.get(msg['agent'], 0) + 1
        
        return {
            'agent_usage': agent_usage,
            'total_messages': len(messages),
            'dominant_agent': max(agent_usage, key=agent_usage.get),
            'conversation_type': self._determine_conversation_type(agent_usage)
        }
    
    def _determine_conversation_type(self, agent_usage: Dict) -> str:
        """Determine the primary conversation type"""
        if agent_usage['agent1'] > agent_usage['agent2']:
            return 'issue_focused'
        elif agent_usage['agent2'] > agent_usage['agent1']:
            return 'tenancy_focused'
        else:
            return 'mixed'

    def get_routing_explanation(self, text: str, has_image: bool, chosen_agent: str) -> str:
        """
        Provide explanation for why a particular agent was chosen
        
        Args:
            text: User input
            has_image: Whether image was present
            chosen_agent: The agent that was selected
            
        Returns:
            Explanation string
        """
        explanations = {
            'agent1': "🔍 **Routed to Issue Detection Agent** - ",
            'agent2': "⚖️ **Routed to Tenancy FAQ Agent** - ",
            'router': "🏠 **Handled by Main Assistant** - "
        }
        
        reasons = []
        
        if has_image:
            reasons.append("image uploaded for analysis")
        
        text_lower = text.lower()
        if any(word in text_lower for word in self.issue_keywords):
            reasons.append("property issue keywords detected")
        
        if any(word in text_lower for word in self.tenancy_keywords):
            reasons.append("tenancy-related terms found")
        
        if not reasons:
            reasons.append("request needs clarification")
        
        explanation = explanations[chosen_agent] + ", ".join(reasons)
        return explanation