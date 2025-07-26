# agents/issue_detection_agent.py

import base64
import json
import random
from typing import Dict, List, Tuple, Optional
import re

class IssueDetectionAgent:
    """
    Agent specialized in detecting and analyzing property issues from images and descriptions
    """
    
    def __init__(self):
        self.issue_database = {
            'water_damage': {
                'keywords': ['water', 'leak', 'stain', 'wet', 'damp', 'moisture'],
                'severity_levels': {
                    'minor': 'Surface discoloration, small stains',
                    'moderate': 'Visible water damage, peeling paint',
                    'severe': 'Structural damage, extensive staining, mold growth'
                },
                'solutions': [
                    "Check for active leaks in pipes above the affected area",
                    "Ensure proper ventilation to prevent mold growth", 
                    "Contact a plumber if leak source is unclear",
                    "Consider waterproofing treatment for recurring issues"
                ],
                'cost_range': '$200-1500'
            },
            'structural_damage': {
                'keywords': ['crack', 'hole', 'foundation', 'wall', 'ceiling'],
                'severity_levels': {
                    'minor': 'Small cosmetic cracks, nail holes',
                    'moderate': 'Visible cracks in walls, settling damage',
                    'severe': 'Large cracks, structural integrity concerns'
                },
                'solutions': [
                    "Monitor crack size and growth over time",
                    "Fill small cracks with appropriate filler",
                    "Consult structural engineer for large cracks",
                    "Address underlying foundation issues if present"
                ],
                'cost_range': '$100-5000+'
            },
            'mold_growth': {
                'keywords': ['mold', 'mould', 'fungus', 'black spots', 'green'],
                'severity_levels': {
                    'minor': 'Small patches, surface mold',
                    'moderate': 'Visible growth, musty odor',
                    'severe': 'Extensive growth, health concerns'
                },
                'solutions': [
                    "Identify and eliminate moisture source",
                    "Use dehumidifier to reduce humidity below 60%",
                    "Clean small areas with bleach solution (1:10 ratio)",
                    "Contact mold remediation specialist for large areas"
                ],
                'cost_range': '$300-3000'
            },
            'electrical_issues': {
                'keywords': ['electrical', 'outlet', 'switch', 'wiring', 'light'],
                'severity_levels': {
                    'minor': 'Non-working outlets, flickering lights',
                    'moderate': 'Multiple electrical issues, overloaded circuits',
                    'severe': 'Exposed wiring, electrical hazards'
                },
                'solutions': [
                    "Check circuit breakers and reset if needed",
                    "Test GFCI outlets and reset buttons",
                    "Replace faulty light bulbs and fixtures",
                    "Contact licensed electrician for wiring issues"
                ],
                'cost_range': '$150-1000'
            },
            'plumbing_issues': {
                'keywords': ['pipe', 'drain', 'toilet', 'faucet', 'sink'],
                'severity_levels': {
                    'minor': 'Dripping faucets, slow drains',
                    'moderate': 'Clogged pipes, running toilets',
                    'severe': 'Burst pipes, sewage backup'
                },
                'solutions': [
                    "Clear minor clogs with plunger or drain snake",
                    "Check and replace worn faucet washers",
                    "Adjust toilet float and flapper mechanisms",
                    "Call plumber for persistent or major issues"
                ],
                'cost_range': '$100-800'
            },
            'cosmetic_damage': {
                'keywords': ['paint', 'scratch', 'dent', 'scuff', 'wear'],
                'severity_levels': {
                    'minor': 'Small scratches, scuff marks',
                    'moderate': 'Peeling paint, multiple marks',
                    'severe': 'Extensive damage, requires refinishing'
                },
                'solutions': [
                    "Touch up small areas with matching paint",
                    "Sand and repaint larger damaged areas",
                    "Use wood filler for dents in wooden surfaces",
                    "Consider professional refinishing for extensive damage"
                ],
                'cost_range': '$50-500'
            }
        }
        
        self.safety_priorities = {
            'electrical_issues': 'HIGH - Potential fire/shock hazard',
            'structural_damage': 'HIGH - Safety and stability concerns',
            'mold_growth': 'MEDIUM - Health implications',
            'water_damage': 'MEDIUM - Can lead to mold and structural issues',
            'plumbing_issues': 'MEDIUM - Water damage potential',
            'cosmetic_damage': 'LOW - Aesthetic concerns only'
        }

    def process_request(self, text: str, image_data: Optional[bytes] = None, context: Dict = None) -> Tuple[str, float]:
        """
        Process user request for issue detection and analysis
        
        Args:
            text: User description of the issue
            image_data: Optional image data for visual analysis
            context: Conversation context
            
        Returns:
            Tuple of (response_text, confidence_score)
        """
        
        if image_data:
            return self._analyze_image_with_context(text, image_data, context)
        else:
            return self._analyze_text_description(text, context)

    def _analyze_image_with_context(self, description: str, image_data: bytes, context: Dict) -> Tuple[str, float]:
        """
        Analyze uploaded image for property issues
        
        This is a simulation - in real implementation, this would use:
        - OpenAI GPT-4 Vision API
        - Google Vision API
        - Custom trained models for specific issues
        """
        
        # Simulate image analysis based on description and common patterns
        detected_issues = self._simulate_image_analysis(description, image_data)
        
        if not detected_issues:
            return self._generate_no_issues_response(), 0.6
        
        # Generate comprehensive analysis report
        response = self._generate_issue_analysis_report(detected_issues, description)
        confidence = self._calculate_confidence(detected_issues, len(description))
        
        return response, confidence

    def _simulate_image_analysis(self, description: str, image_data: bytes) -> List[Dict]:
        """
        Simulate image analysis results based on description keywords
        """
        description_lower = description.lower()
        detected_issues = []
        
        for issue_type, info in self.issue_database.items():
            keyword_matches = sum(1 for keyword in info['keywords'] if keyword in description_lower)
            
            if keyword_matches > 0:
                # Simulate detection confidence based on keyword matches
                confidence = min(0.95, 0.6 + (keyword_matches * 0.1))
                severity = self._determine_severity(description_lower, issue_type)
                
                detected_issues.append({
                    'type': issue_type,
                    'confidence': confidence,
                    'severity': severity,
                    'keywords_matched': keyword_matches
                })
        
        # Sort by confidence
        detected_issues.sort(key=lambda x: x['confidence'], reverse=True)
        return detected_issues[:3]  # Return top 3 most likely issues

    def _determine_severity(self, description: str, issue_type: str) -> str:
        """Determine severity level based on description"""
        severe_indicators = ['extensive', 'large', 'major', 'severe', 'bad', 'terrible', 'everywhere']
        moderate_indicators = ['noticeable', 'visible', 'concerning', 'growing', 'spreading']
        
        if any(indicator in description for indicator in severe_indicators):
            return 'severe'
        elif any(indicator in description for indicator in moderate_indicators):
            return 'moderate'
        else:
            return 'minor'

    def _generate_issue_analysis_report(self, detected_issues: List[Dict], description: str) -> str:
        """Generate comprehensive analysis report"""
        
        if not detected_issues:
            return "No significant issues detected in the uploaded image."
        
        primary_issue = detected_issues[0]
        issue_type = primary_issue['type']
        issue_info = self.issue_database[issue_type]
        
        # Build the response
        response_parts = []
        
        # Header
        response_parts.append("🔍 **Property Issue Analysis Complete**\n")
        
        # Primary issue identification
        issue_name = issue_type.replace('_', ' ').title()
        confidence_pct = int(primary_issue['confidence'] * 100)
        response_parts.append(f"**Primary Issue Detected:** {issue_name} ({confidence_pct}% confidence)")
        response_parts.append(f"**Severity Level:** {primary_issue['severity'].title()}")
        
        # Safety priority
        if issue_type in self.safety_priorities:
            priority = self.safety_priorities[issue_type]
            response_parts.append(f"**Safety Priority:** {priority}")
        
        # Detailed analysis
        response_parts.append("\n**Analysis Details:**")
        severity_description = issue_info['severity_levels'][primary_issue['severity']]
        response_parts.append(f"• {severity_description}")
        
        # Additional issues
        if len(detected_issues) > 1:
            response_parts.append(f"\n**Additional Concerns:**")
            for issue in detected_issues[1:]:
                add_issue_name = issue['type'].replace('_', ' ').title()
                add_confidence = int(issue['confidence'] * 100)
                response_parts.append(f"• {add_issue_name} ({add_confidence}% confidence)")
        
        # Recommended actions
        response_parts.append(f"\n**Recommended Actions:**")
        for i, solution in enumerate(issue_info['solutions'], 1):
            response_parts.append(f"{i}. {solution}")
        
        # Cost estimate
        response_parts.append(f"\n**Estimated Repair Cost:** {issue_info['cost_range']}")
        
        # Next steps
        response_parts.append(f"\n**Next Steps:**")
        if primary_issue['severity'] == 'severe':
            response_parts.append("⚠️ **Immediate attention recommended** - Contact a professional contractor")
        elif primary_issue['severity'] == 'moderate':
            response_parts.append("⏰ **Schedule repair soon** - Issue may worsen if left untreated")
        else:
            response_parts.append("📝 **Monitor and plan** - Can be addressed during routine maintenance")
        
        response_parts.append("\n**Would you like specific guidance on any of these recommendations?**")
        
        return "\n".join(response_parts)

    def _analyze_text_description(self, text: str, context: Dict) -> Tuple[str, float]:
        """
        Analyze text description without image
        """
        text_lower = text.lower()
        
        # Check for issue keywords
        possible_issues = []
        for issue_type, info in self.issue_database.items():
            keyword_matches = sum(1 for keyword in info['keywords'] if keyword in text_lower)
            if keyword_matches > 0:
                possible_issues.append({
                    'type': issue_type,
                    'matches': keyword_matches,
                    'severity': self._determine_severity(text_lower, issue_type)
                })
        
        if possible_issues:
            # Sort by keyword matches
            possible_issues.sort(key=lambda x: x['matches'], reverse=True)
            return self._generate_text_analysis_response(possible_issues, text), 0.7
        else:
            return self._generate_general_guidance_response(text), 0.5

    def _generate_text_analysis_response(self, possible_issues: List[Dict], description: str) -> str:
        """Generate response based on text analysis"""
        
        primary_issue = possible_issues[0]
        issue_type = primary_issue['type']
        issue_info = self.issue_database[issue_type]
        
        response_parts = []
        
        response_parts.append("🔧 **Issue Analysis Based on Description**\n")
        
        issue_name = issue_type.replace('_', ' ').title()
        response_parts.append(f"**Likely Issue:** {issue_name}")
        response_parts.append(f"**Severity Assessment:** {primary_issue['severity'].title()}")
        
        # Quick diagnostic questions
        response_parts.append(f"\n**Diagnostic Questions:**")
        diagnostic_questions = self._get_diagnostic_questions(issue_type)
        for question in diagnostic_questions[:3]:
            response_parts.append(f"• {question}")
        
        # Initial recommendations
        response_parts.append(f"\n**Initial Recommendations:**")
        for i, solution in enumerate(issue_info['solutions'][:3], 1):
            response_parts.append(f"{i}. {solution}")
        
        response_parts.append(f"\n**For more accurate diagnosis, consider uploading a photo of the issue.**")
        response_parts.append(f"\n**Would you like specific guidance on any of these steps?**")
        
        return "\n".join(response_parts)

    def _get_diagnostic_questions(self, issue_type: str) -> List[str]:
        """Get diagnostic questions for specific issue types"""
        
        questions_db = {
            'water_damage': [
                "Is the water damage still actively spreading?",
                "Can you locate the source of the water?",
                "Is there a musty odor in the area?",
                "How long has this damage been present?"
            ],
            'structural_damage': [
                "Are the cracks getting larger over time?",
                "Do doors or windows stick in this area?",
                "Is the crack wider than a coin?",
                "Are there multiple cracks in the same area?"
            ],
            'mold_growth': [
                "What color is the growth you're seeing?",
                "Is there a musty smell in the room?",
                "Is the area frequently damp or humid?",
                "How large is the affected area?"
            ],
            'electrical_issues': [
                "Are circuit breakers tripping frequently?",
                "Do you smell burning or see sparks?",
                "Are outlets warm to the touch?", 
                "Do lights flicker when appliances turn on?"
            ],
            'plumbing_issues': [
                "Is water pressure affected throughout the house?",
                "Can you hear water running when all taps are off?",
                "Is the issue getting worse over time?",
                "Are multiple fixtures affected?"
            ],
            'cosmetic_damage': [
                "Is the damage affecting the underlying material?",
                "How large is the affected area?",
                "Is the damage spreading or stable?",
                "Do you know what caused the damage?"
            ]
        }
        
        return questions_db.get(issue_type, [
            "Can you describe the issue in more detail?",
            "When did you first notice this problem?",
            "Has the issue changed or worsened recently?"
        ])

    def _generate_general_guidance_response(self, text: str) -> str:
        """Generate general guidance when no specific issue is identified"""
        
        response_parts = []
        
        response_parts.append("🔍 **Property Issue Assistance**\n")
        response_parts.append("I'd be happy to help analyze your property issue! For the most accurate assessment, I recommend:")
        response_parts.append("")
        response_parts.append("**Option 1: Upload a Photo**")
        response_parts.append("📸 Share an image of the problem area for visual analysis")
        response_parts.append("")
        response_parts.append("**Option 2: Provide More Details**")
        response_parts.append("• What type of issue are you experiencing? (leak, crack, damage, etc.)")
        response_parts.append("• Where is it located? (bathroom, kitchen, bedroom, etc.)")
        response_parts.append("• When did you first notice it?")
        response_parts.append("• Has it changed or gotten worse?")
        response_parts.append("")
        response_parts.append("**Common Issues I Can Help With:**")
        
        for issue_type, info in list(self.issue_database.items())[:4]:
            issue_name = issue_type.replace('_', ' ').title()
            response_parts.append(f"• {issue_name}: {', '.join(info['keywords'][:3])}")
        
        response_parts.append("")
        response_parts.append("**What specific issue would you like me to help you with?**")
        
        return "\n".join(response_parts)

    def _generate_no_issues_response(self) -> str:
        """Generate response when no issues are detected"""
        
        responses = [
            "🎉 **Good News!** No significant issues detected in the uploaded image.\n\nThe area appears to be in good condition. If you're concerned about something specific, please point it out and I'll take a closer look.",
            
            "✅ **Analysis Complete** - No major problems identified.\n\nThe property appears well-maintained in this area. If you notice something I might have missed, feel free to describe your specific concerns.",
            
            "🔍 **Image Analysis Results** - No obvious issues found.\n\nEverything looks normal in this photo. If you're experiencing problems that aren't visible, please describe them and I can provide guidance."
        ]
        
        return random.choice(responses)

    def _calculate_confidence(self, detected_issues: List[Dict], description_length: int) -> float:
        """Calculate overall confidence score"""
        
        if not detected_issues:
            return 0.3
        
        # Base confidence on primary issue
        base_confidence = detected_issues[0]['confidence']
        
        # Adjust based on description quality
        if description_length > 50:
            base_confidence += 0.1
        elif description_length < 10:
            base_confidence -= 0.1
        
        # Adjust based on number of supporting issues
        if len(detected_issues) > 1:
            base_confidence += 0.05
        
        return min(0.95, max(0.5, base_confidence))

    def get_follow_up_questions(self, issue_type: str, severity: str) -> List[str]:
        """Get relevant follow-up questions for an issue"""
        
        base_questions = self._get_diagnostic_questions(issue_type)
        
        if severity == 'severe':
            base_questions.extend([
                "Do you need emergency professional assistance?",
                "Is the issue affecting other areas of the property?",
                "Are there any safety concerns for occupants?"
            ])
        
        return base_questions[:5]  # Limit to 5 questions

    def estimate_repair_timeline(self, issue_type: str, severity: str) -> str:
        """Estimate repair timeline based on issue type and severity"""
        
        timelines = {
            'water_damage': {
                'minor': '1-2 days',
                'moderate': '3-7 days', 
                'severe': '1-3 weeks'
            },
            'structural_damage': {
                'minor': '1 day',
                'moderate': '1-2 weeks',
                'severe': '2-8 weeks'
            },
            'mold_growth': {
                'minor': '1-3 days',
                'moderate': '1-2 weeks',
                'severe': '2-4 weeks'
            },
            'electrical_issues': {
                'minor': '2-4 hours',
                'moderate': '1-2 days',
                'severe': '3-7 days'
            },
            'plumbing_issues': {
                'minor': '1-4 hours',
                'moderate': '1-2 days', 
                'severe': '2-5 days'
            },
            'cosmetic_damage': {
                'minor': '2-6 hours',
                'moderate': '1-3 days',
                'severe': '1-2 weeks'
            }
        }
        
        return timelines.get(issue_type, {}).get(severity, 'Timeline varies - consult professional')