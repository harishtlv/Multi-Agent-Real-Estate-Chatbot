# agents/tenancy_faq_agent.py

import random
from typing import Dict, List, Tuple, Optional
import re

class TenancyFAQAgent:
    """
    Agent specialized in handling tenancy law questions and rental guidance
    """
    
    def __init__(self):
        self.legal_database = {
            'eviction': {
                'keywords': ['evict', 'eviction', 'kick out', 'remove', 'terminate lease'],
                'general_info': "Eviction laws vary by jurisdiction, but generally require proper notice and legal grounds.",
                'common_grounds': [
                    "Non-payment of rent",
                    "Violation of lease terms", 
                    "Illegal activities on property",
                    "Property damage beyond normal wear",
                    "Lease expiration (in some areas)"
                ],
                'tenant_rights': [
                    "Right to proper written notice (usually 30-60 days)",
                    "Right to cure violations in many cases",
                    "Right to legal representation in court",
                    "Right to remain until court order (no self-help evictions)"
                ]
            },
            'rent_increase': {
                'keywords': ['rent increase', 'raise rent', 'rent hike', 'increase rent'],
                'general_info': "Rent increase regulations vary significantly by location and lease type.",
                'typical_rules': [
                    "Month-to-month: Usually 30 days notice minimum",
                    "Fixed-term lease: Generally no increases during term",
                    "Rent-controlled areas: May have caps on increase amounts",
                    "Some areas require 60-90 days notice for large increases"
                ],
                'tenant_options': [
                    "Review lease agreement for specific terms",
                    "Check local rent control ordinances",
                    "Negotiate with landlord if increase seems excessive",
                    "Consider moving if increase is unaffordable"
                ]
            },
            'security_deposit': {
                'keywords': ['deposit', 'security deposit', 'last month', 'damage deposit'],
                'general_info': "Security deposit laws protect both landlords and tenants.",
                'typical_rules': [
                    "Usually 1-2 months rent maximum",
                    "Must be returned within 14-30 days after move-out",
                    "Can be used for unpaid rent and damage beyond normal wear",
                    "Detailed itemization required for deductions"
                ],
                'tenant_rights': [
                    "Right to pre-move-out inspection in many areas",
                    "Right to written itemization of deductions",
                    "Right to challenge unreasonable deductions",
                    "Right to interest on deposit in some jurisdictions"
                ]
            },
            'repairs_maintenance': {
                'keywords': ['repair', 'maintenance', 'fix', 'broken', 'landlord responsibility'],
                'general_info': "Repair responsibilities are typically divided between landlords and tenants.",
                'landlord_responsibilities': [
                    "Major structural repairs",
                    "Plumbing and electrical systems",
                    "Heating and cooling systems",
                    "Appliances provided by landlord",
                    "Health and safety issues"
                ],
                'tenant_responsibilities': [
                    "Minor repairs and maintenance",
                    "Damage caused by tenant or guests",
                    "Changing light bulbs and filters",
                    "Keeping property clean and sanitary"
                ]
            },
            'lease_termination': {
                'keywords': ['move out', 'terminate lease', 'break lease', 'early termination'],
                'general_info': "Lease termination requires following proper procedures and notice periods.",
                'notice_periods': [
                    "Month-to-month: Usually 30 days notice",
                    "Fixed-term lease: May require payment until end of term",
                    "Some areas allow early termination for specific reasons",
                    "Military deployment often allows early termination"
                ],
                'proper_procedures': [
                    "Provide written notice to landlord",
                    "Continue paying rent through notice period",
                    "Schedule final inspection",
                    "Return keys and property access"
                ]
            },
            'tenant_rights': {
                'keywords': ['tenant rights', 'rights', 'what can landlord do', 'illegal'],
                'general_info': "Tenants have fundamental rights that vary by jurisdiction.",
                'basic_rights': [
                    "Right to quiet enjoyment of property",
                    "Right to habitable living conditions",
                    "Right to privacy (landlord entry restrictions)",
                    "Right to be free from discrimination",
                    "Right to organize tenant associations"
                ],
                'prohibited_actions': [
                    "Self-help evictions (changing locks, utilities shut-off)",
                    "Retaliation for complaints or exercise of rights",
                    "Discrimination based on protected classes",
                    "Entry without proper notice (except emergencies)"
                ]
            }
        }
        
        self.location_specific_notes = {
            'california': {
                'rent_control': True,
                'notice_period': '30 days (60 days for year+ tenancy)',
                'deposit_limit': '2 months rent (unfurnished), 3 months (furnished)',
                'special_rules': ['Just cause eviction requirements', 'Rent increase caps']
            },
            'new_york': {
                'rent_control': True,
                'notice_period': '30 days',
                'deposit_limit': '1 month rent',
                'special_rules': ['Rent stabilization laws', 'Security deposit interest required']
            },
            'texas': {
                'rent_control': False,
                'notice_period': '30 days',
                'deposit_limit': 'No state limit',
                'special_rules': ['Property code requirements', 'Repair and deduct allowed']
            },
            'florida': {
                'rent_control': False,
                'notice_period': '15 days (week-to-week), 30 days (month-to-month)',
                'deposit_limit': 'No state limit',
                'special_rules': ['3-day pay or quit notice', 'Hurricane evacuation protections']
            }
        }

    def process_request(self, text: str, location: Optional[str] = None, context: Dict = None) -> Tuple[str, float]:
        """
        Process tenancy-related questions
        
        Args:
            text: User question
            location: User's location for specific laws
            context: Conversation context
            
        Returns:
            Tuple of (response_text, confidence_score)
        """
        
        # Identify the topic
        topic = self._identify_topic(text)
        
        if topic:
            response = self._generate_topic_response(topic, text, location)
            confidence = self._calculate_confidence(text, topic, location)
            return response, confidence
        else:
            return self._generate_general_guidance_response(text, location), 0.6

    def _identify_topic(self, text: str) -> Optional[str]:
        """Identify the main topic from user text"""
        
        text_lower = text.lower()
        topic_scores = {}
        
        for topic, info in self.legal_database.items():
            score = sum(1 for keyword in info['keywords'] if keyword in text_lower)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        return None

    def _generate_topic_response(self, topic: str, text: str, location: Optional[str]) -> str:
        """Generate detailed response for identified topic"""
        
        topic_info = self.legal_database[topic]
        response_parts = []
        
        # Header
        topic_name = topic.replace('_', ' ').title()
        response_parts.append(f"⚖️ **{topic_name} - Legal Guidance**\n")
        
        # General information
        response_parts.append(f"**Overview:**")
        response_parts.append(f"{topic_info['general_info']}\n")
        
        # Specific information based on topic
        if topic == 'eviction':
            response_parts.append("**Common Legal Grounds for Eviction:**")
            for ground in topic_info['common_grounds']:
                response_parts.append(f"• {ground}")
            
            response_parts.append(f"\n**Your Rights as a Tenant:**")
            for right in topic_info['tenant_rights']:
                response_parts.append(f"• {right}")
                
        elif topic == 'rent_increase':
            response_parts.append("**Typical Rules:**")
            for rule in topic_info['typical_rules']:
                response_parts.append(f"• {rule}")
            
            response_parts.append(f"\n**Your Options:**")
            for option in topic_info['tenant_options']:
                response_parts.append(f"• {option}")
                
        elif topic == 'security_deposit':
            response_parts.append("**Standard Rules:**")
            for rule in topic_info['typical_rules']:
                response_parts.append(f"• {rule}")
            
            response_parts.append(f"\n**Your Rights:**")
            for right in topic_info['tenant_rights']:
                response_parts.append(f"• {right}")
                
        elif topic == 'repairs_maintenance':
            response_parts.append("**Landlord Responsibilities:**")
            for resp in topic_info['landlord_responsibilities']:
                response_parts.append(f"• {resp}")
            
            response_parts.append(f"\n**Tenant Responsibilities:**")
            for resp in topic_info['tenant_responsibilities']:
                response_parts.append(f"• {resp}")
                
        elif topic == 'lease_termination':
            response_parts.append("**Notice Requirements:**")
            for notice in topic_info['notice_periods']:
                response_parts.append(f"• {notice}")
            
            response_parts.append(f"\n**Proper Procedures:**")
            for procedure in topic_info['proper_procedures']:
                response_parts.append(f"• {procedure}")
                
        elif topic == 'tenant_rights':
            response_parts.append("**Basic Tenant Rights:**")
            for right in topic_info['basic_rights']:
                response_parts.append(f"• {right}")
            
            response_parts.append(f"\n**Prohibited Landlord Actions:**")
            for action in topic_info['prohibited_actions']:
                response_parts.append(f"• {action}")
        
        # Location-specific information
        if location:
            location_info = self._get_location_specific_info(location, topic)
            if location_info:
                response_parts.append(f"\n**{location.title()}-Specific Information:**")
                response_parts.append(location_info)
        else:
            response_parts.append(f"\n💡 **Tip:** For more specific guidance, please share your city/state/country.")
        
        # Next steps
        response_parts.append(f"\n**Recommended Next Steps:**")
        next_steps = self._get_next_steps(topic, text)
        for step in next_steps:
            response_parts.append(f"• {step}")
        
        response_parts.append(f"\n**Need more specific guidance on any of these points?**")
        
        return "\n".join(response_parts)

    def _get_location_specific_info(self, location: str, topic: str) -> Optional[str]:
        """Get location-specific legal information"""
        
        location_lower = location.lower()
        
        # Check for known locations
        for loc_key, loc_info in self.location_specific_notes.items():
            if loc_key in location_lower:
                info_parts = []
                
                if topic == 'rent_increase' and loc_info.get('rent_control'):
                    info_parts.append("• Rent control laws may limit increase amounts")
                
                if topic in ['eviction', 'lease_termination']:
                    info_parts.append(f"• Standard notice period: {loc_info['notice_period']}")
                
                if topic == 'security_deposit':
                    info_parts.append(f"• Deposit limit: {loc_info['deposit_limit']}")
                
                if loc_info.get('special_rules'):
                    info_parts.append("• Special local rules apply:")
                    for rule in loc_info['special_rules']:
                        info_parts.append(f"  - {rule}")
                
                return "\n".join(info_parts) if info_parts else None
        
        # Generic location advice
        return f"Please check local housing authority or tenant rights organizations in {location} for specific regulations."

    def _get_next_steps(self, topic: str, text: str) -> List[str]:
        """Get recommended next steps based on topic"""
        
        next_steps_db = {
            'eviction': [
                "Review your lease agreement carefully",
                "Document all communications with landlord",
                "Contact local tenant rights organization",
                "Consult with a tenant attorney if facing eviction"
            ],
            'rent_increase': [
                "Check if proper notice was given",
                "Research local rent control laws",
                "Compare to market rates in your area",
                "Consider negotiating with landlord"
            ],
            'security_deposit': [
                "Document property condition with photos",
                "Keep all receipts and communications",
                "Request itemized list of any deductions",
                "File complaint with housing authority if needed"
            ],
            'repairs_maintenance': [
                "Submit repair requests in writing",
                "Document the issues with photos/videos",
                "Keep records of all communications",
                "Check local habitability standards"
            ],
            'lease_termination': [
                "Review lease for early termination clauses",
                "Give proper written notice",
                "Schedule pre-move-out inspection",
                "Document property condition"
            ],
            'tenant_rights': [
                "Know your local tenant rights laws",
                "Join or contact tenant organizations",
                "Document any violations by landlord",
                "Seek legal advice for serious violations"
            ]
        }
        
        return next_steps_db.get(topic, [
            "Research your local tenant laws",
            "Document everything in writing",
            "Consult with local housing authority",
            "Consider legal consultation if needed"
        ])

    def _calculate_confidence(self, text: str, topic: str, location: Optional[str]) -> float:
        """Calculate confidence score for response"""
        
        base_confidence = 0.8
        
        # Adjust based on topic clarity
        topic_info = self.legal_database[topic]
        keyword_matches = sum(1 for keyword in topic_info['keywords'] if keyword.lower() in text.lower())
        
        if keyword_matches > 2:
            base_confidence += 0.1
        elif keyword_matches == 1:
            base_confidence -= 0.1
        
        # Adjust based on location specificity
        if location:
            if any(loc in location.lower() for loc in self.location_specific_notes.keys()):
                base_confidence += 0.05
        else:
            base_confidence -= 0.05
        
        return min(0.95, max(0.6, base_confidence))

    def _generate_general_guidance_response(self, text: str, location: Optional[str]) -> str:
        """Generate general guidance when no specific topic is identified"""
        
        response_parts = []
        
        response_parts.append("⚖️ **Tenancy Law Guidance**\n")
        response_parts.append("I'm here to help with rental and tenancy questions! I can provide guidance on:")
        response_parts.append("")
        
        # List main topics
        for topic, info in self.legal_database.items():
            topic_name = topic.replace('_', ' ').title()
            response_parts.append(f"**{topic_name}:**")
            response_parts.append(f"• {info['general_info']}")
            response_parts.append("")
        
        response_parts.append("**To get the most helpful advice:**")
        response_parts.append("• Be specific about your situation")
        response_parts.append("• Share your location (city/state/country) for local laws")
        response_parts.append("• Describe any urgent timelines or deadlines")
        response_parts.append("")
        
        if location:
            response_parts.append(f"**Your Location:** {location}")
            response_parts.append("I'll include relevant local information in my responses.")
        else:
            response_parts.append("💡 **Tip:** Share your location for more specific legal guidance.")
        
        response_parts.append("")
        response_parts.append("**What specific tenancy question can I help you with?**")
        
        return "\n".join(response_parts)

    def get_emergency_resources(self, location: Optional[str] = None) -> str:
        """Get emergency tenant resources"""
        
        response_parts = []
        response_parts.append("🚨 **Emergency Tenant Resources**\n")
        
        response_parts.append("**Immediate Help:**")
        response_parts.append("• Contact local housing authority")
        response_parts.append("• Reach out to tenant rights organizations")
        response_parts.append("• Call 211 for local resource referrals")
        response_parts.append("• Contact legal aid societies for free legal help")
        response_parts.append("")
        
        if location:
            response_parts.append(f"**{location}-Specific Resources:**")
            response_parts.append("• Search '[your city] tenant rights organization'")
            response_parts.append("• Look up '[your state] housing authority'")
            response_parts.append("• Contact '[your area] legal aid'")
        else:
            response_parts.append("**How to Find Local Help:**")
            response_parts.append("• Search 'tenant rights [your city]'")
            response_parts.append("• Contact your city's housing department")
            response_parts.append("• Look up state tenant protection agencies")
        
        response_parts.append("")
        response_parts.append("**If facing illegal eviction or harassment:**")
        response_parts.append("• Document everything (photos, messages, recordings if legal)")
        response_parts.append("• File complaints with housing authorities")
        response_parts.append("• Seek immediate legal representation")
        response_parts.append("• Know that self-help evictions are illegal in most places")
        
        return "\n".join(response_parts)

    def generate_document_template(self, document_type: str) -> str:
        """Generate template documents for common tenant needs"""
        
        templates = {
            'repair_request': """
**Repair Request Letter Template**

[Date]

[Landlord Name]
[Landlord Address]

Dear [Landlord Name],

I am writing to formally request repairs to my rental unit at [Property Address], Unit [Number].

**Issues requiring attention:**
• [Describe issue 1 in detail]
• [Describe issue 2 in detail]

These issues affect the habitability of the property and require prompt attention. Please arrange for repairs within a reasonable timeframe as required by law.

I am available to provide access to the unit. Please contact me at [Phone] or [Email] to schedule.

Thank you for your prompt attention to this matter.

Sincerely,
[Your Name]
[Date]

**Keep a copy for your records**
""",
            
            'notice_to_vacate': """
**Notice to Vacate Template**

[Date]

[Landlord Name]
[Landlord Address]

Dear [Landlord Name],

This letter serves as my formal [30/60] day notice to vacate the rental property located at [Property Address], Unit [Number].

**Move-out Details:**
• Last day of occupancy: [Date]
• Final rent payment through: [Date]
• Forwarding address: [New Address]

I request to schedule a pre-move-out inspection and will ensure the property is returned in good condition, normal wear and tear excepted.

Please return my security deposit of $[Amount] to my forwarding address within the timeframe required by law.

Thank you for your cooperation.

Sincerely,
[Your Name]
[Current Date]
""",

            'deposit_demand': """
**Security Deposit Return Demand Letter**

[Date]

[Landlord Name]
[Landlord Address]

Dear [Landlord Name],

I am writing to formally request the return of my security deposit for the property at [Property Address], which I vacated on [Move-out Date].

**Deposit Details:**
• Amount paid: $[Amount]
• Date paid: [Date]
• Days since move-out: [Number]

According to [State] law, security deposits must be returned within [timeframe] days. As this period has passed, I am requesting immediate return of my full deposit.

If deductions were made, please provide an itemized list with receipts as required by law. I believe I am entitled to the full amount as the property was left in good condition.

Please send the deposit to: [Forwarding Address]

I expect resolution within [timeframe] or I may pursue legal remedies available under state law.

Sincerely,
[Your Name]
[Date]
"""
        }
        
        return templates.get(document_type, "Template not found. Available templates: repair_request, notice_to_vacate, deposit_demand")

    def get_legal_resources_by_state(self, state: str) -> str:
        """Get legal resources specific to a state"""
        
        # This would be expanded with real resources in production
        state_resources = {
            'california': {
                'housing_authority': 'California Department of Housing and Community Development',
                'tenant_org': 'Tenants Together',
                'legal_aid': 'California Legal Aid',
                'hotline': '1-866-557-7368'
            },
            'new_york': {
                'housing_authority': 'New York State Division of Housing',
                'tenant_org': 'Met Council on Housing',
                'legal_aid': 'Legal Aid Society',
                'hotline': '311'
            },
            'texas': {
                'housing_authority': 'Texas Department of Housing',
                'tenant_org': 'Texas Tenants Union',
                'legal_aid': 'Texas Legal Aid',
                'hotline': '2-1-1'
            }
        }
        
        state_lower = state.lower()
        if state_lower in state_resources:
            resources = state_resources[state_lower]
            return f"""
**{state.title()} Tenant Resources:**

• **Housing Authority:** {resources['housing_authority']}
• **Tenant Organization:** {resources['tenant_org']}
• **Legal Aid:** {resources['legal_aid']}
• **Hotline:** {resources['hotline']}

**Additional Resources:**
• Search "[your city] tenant rights" for local organizations
• Contact your city hall for housing department information
• Check state bar association for lawyer referrals
"""
        else:
            return f"""
**General Resources for {state.title()}:**

• Contact your state housing authority
• Search "tenant rights {state}" online
• Call 2-1-1 for local resource referrals
• Contact state legal aid organizations
• Check with your city's housing department

**For specific {state.title()} laws:**
• Visit your state government website
• Contact state attorney general's office
• Look up "{state} landlord tenant law"
"""