import streamlit as st
import base64
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
from dataclasses import dataclass
import pandas as pd

# Import our agent modules
from agents.agent_router import AgentRouter
from agents.issue_detection_agent import IssueDetectionAgent
from agents.tenancy_faq_agent import TenancyFAQAgent
from utils.conversation_manager import ConversationManager
from utils.image_processor import ImageProcessor

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Real Estate Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class Message:
    id: str
    type: str  # 'user' or 'bot'
    content: str
    agent: Optional[str] = None
    image_data: Optional[str] = None
    image_name: Optional[str] = None
    confidence: Optional[float] = None
    timestamp: Optional[datetime] = None

class RealEstateChatbotApp:
    def __init__(self):
        self.setup_session_state()
        self.agent_router = AgentRouter()
        self.issue_agent = IssueDetectionAgent()
        self.tenancy_agent = TenancyFAQAgent()
        self.conversation_manager = ConversationManager()
        self.image_processor = ImageProcessor()

    def setup_session_state(self):
        """Initialize session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                Message(
                    id="welcome",
                    type="bot",
                    agent="router",
                    content="""👋 **Welcome to your Multi-Agent Real Estate Assistant!**

I'm here to help with property issues and tenancy questions. I have two specialized agents:

🔍 **Issue Detection Agent**: Upload images for property issue analysis (water damage, cracks, mold, etc.)
⚖️ **Tenancy FAQ Agent**: Get guidance on rental laws, tenant rights, and landlord responsibilities

**How can I assist you today?**""",
                    timestamp=datetime.now()
                )
            ]
        
        if 'current_agent' not in st.session_state:
            st.session_state.current_agent = 'router'
        
        if 'conversation_context' not in st.session_state:
            st.session_state.conversation_context = {}
        
        if 'user_location' not in st.session_state:
            st.session_state.user_location = None

    def render_sidebar(self):
        """Render the sidebar with agent status and settings"""
        st.sidebar.header("🏠 Real Estate Assistant")
        
        # Agent Status
        st.sidebar.subheader("Agent Status")
        
        agents_status = {
            'router': {'name': '🏠 Main Assistant', 'active': st.session_state.current_agent == 'router'},
            'agent1': {'name': '🔍 Issue Detective', 'active': st.session_state.current_agent == 'agent1'},
            'agent2': {'name': '⚖️ Legal Advisor', 'active': st.session_state.current_agent == 'agent2'}
        }
        
        for agent_id, info in agents_status.items():
            if info['active']:
                st.sidebar.success(f"**Active:** {info['name']}")
            else:
                st.sidebar.info(f"Standby: {info['name']}")
        
        # User Settings
        st.sidebar.subheader("Settings")
        
        # Location setting for tenancy laws
        location = st.sidebar.text_input(
            "Your Location (City, State/Country)",
            value=st.session_state.user_location or "",
            help="This helps provide location-specific tenancy law guidance"
        )
        if location != st.session_state.user_location:
            st.session_state.user_location = location
        
        # Conversation stats
        st.sidebar.subheader("Session Stats")
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m.type == 'user'])
        st.sidebar.metric("Total Messages", total_messages)
        st.sidebar.metric("Your Messages", user_messages)
        
        # Clear conversation
        if st.sidebar.button("🗑️ Clear Conversation"):
            self.clear_conversation()

    def clear_conversation(self):
        """Clear the conversation history"""
        st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
        st.session_state.current_agent = 'router'
        st.session_state.conversation_context = {}
        st.rerun()

    def render_message(self, message: Message):
        """Render a single message in the chat"""
        if message.type == 'user':
            with st.chat_message("user", avatar="👤"):
                if message.image_data:
                    st.image(message.image_data, caption=message.image_name, width=300)
                st.write(message.content)
        else:
            # Determine avatar based on agent
            avatar_map = {
                'router': '🏠',
                'agent1': '🔍',
                'agent2': '⚖️'
            }
            avatar = avatar_map.get(message.agent, '🤖')
            
            with st.chat_message("assistant", avatar=avatar):
                # Show agent name and confidence
                if message.agent and message.agent != 'router':
                    agent_names = {
                        'agent1': 'Issue Detection Agent',
                        'agent2': 'Tenancy FAQ Agent'
                    }
                    agent_name = agent_names.get(message.agent, 'Assistant')
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.caption(f"**{agent_name}**")
                    if message.confidence:
                        with col2:
                            st.caption(f"Confidence: {message.confidence:.0%}")
                
                st.write(message.content)

    def process_user_input(self, user_input: str, uploaded_image=None) -> Message:
        """Process user input and generate bot response"""
        
        # Create user message
        image_data = None
        image_name = None
        
        if uploaded_image:
            image_data = uploaded_image.getvalue()
            image_name = uploaded_image.name
        
        user_message = Message(
            id=f"user_{int(time.time())}",
            type="user",
            content=user_input,
            image_data=image_data,
            image_name=image_name,
            timestamp=datetime.now()
        )
        
        # Add user message to session
        st.session_state.messages.append(user_message)
        
        # Route to appropriate agent
        target_agent = self.agent_router.route_request(
            user_input, 
            has_image=uploaded_image is not None,
            context=st.session_state.conversation_context
        )
        
        st.session_state.current_agent = target_agent
        
        # Generate response based on agent
        if target_agent == 'agent1':
            response_content, confidence = self.issue_agent.process_request(
                user_input, 
                image_data, 
                st.session_state.conversation_context
            )
        elif target_agent == 'agent2':
            response_content, confidence = self.tenancy_agent.process_request(
                user_input,
                location=st.session_state.user_location,
                context=st.session_state.conversation_context
            )
        else:  # router or clarification
            response_content, confidence = self.agent_router.generate_clarification_response(
                user_input,
                st.session_state.conversation_context
            )
        
        # Create bot response message
        bot_message = Message(
            id=f"bot_{int(time.time())}",
            type="bot",
            content=response_content,
            agent=target_agent,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        return bot_message

    def render_chat_interface(self):
        """Render the main chat interface"""
        st.header("💬 Real Estate Assistant Chat")
        
        # Display messages
        for message in st.session_state.messages:
            self.render_message(message)
        
        # Chat input area
        st.subheader("Send Message")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            user_input = st.text_area(
                "Type your message here...",
                placeholder="Ask about property issues, upload an image, or ask tenancy questions...",
                height=100,
                key="user_input"
            )
        
        with col2:
            st.write("**Upload Image** (Optional)")
            uploaded_image = st.file_uploader(
                "Choose an image...",
                type=['png', 'jpg', 'jpeg'],
                help="Upload property images for issue detection"
            )
            
            if uploaded_image:
                st.image(uploaded_image, caption="Preview", width=200)
        
        # Send button
        if st.button("Send Message", type="primary", use_container_width=True):
            if user_input.strip() or uploaded_image:
                with st.spinner("Processing your request..."):
                    bot_response = self.process_user_input(user_input, uploaded_image)
                    st.session_state.messages.append(bot_response)
                    
                    # Clear input
                    st.session_state.user_input = ""
                    st.rerun()
            else:
                st.warning("Please enter a message or upload an image.")

    def render_example_interactions(self):
        """Render example interactions to help users understand capabilities"""
        st.subheader("💡 Example Interactions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🔍 Issue Detection Examples:**")
            examples_issues = [
                "Upload a photo of water damage on ceiling",
                "Show me a crack in the wall",
                "What's wrong with this broken fixture?",
                "Analyze mold growth in bathroom"
            ]
            
            for example in examples_issues:
                if st.button(example, key=f"issue_{example}"):
                    st.session_state.user_input = example
                    st.rerun()
        
        with col2:
            st.write("**⚖️ Tenancy FAQ Examples:**")
            examples_tenancy = [
                "Can my landlord evict me without notice?",
                "How much notice do I need to give before moving out?",
                "What are my rights regarding rent increases?",
                "Who is responsible for property maintenance?"
            ]
            
            for example in examples_tenancy:
                if st.button(example, key=f"tenancy_{example}"):
                    st.session_state.user_input = example
                    st.rerun()

    def render_analytics_dashboard(self):
        """Render analytics and insights dashboard"""
        st.subheader("📊 Session Analytics")
        
        if len(st.session_state.messages) > 1:
            # Message analysis
            messages_df = pd.DataFrame([
                {
                    'Type': msg.type,
                    'Agent': msg.agent or 'Unknown',
                    'Has_Image': bool(msg.image_data),
                    'Confidence': msg.confidence,
                    'Length': len(msg.content),
                    'Timestamp': msg.timestamp
                }
                for msg in st.session_state.messages[1:]  # Skip welcome message
            ])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                agent_counts = messages_df[messages_df['Type'] == 'bot']['Agent'].value_counts()
                st.write("**Agent Usage:**")
                for agent, count in agent_counts.items():
                    agent_names = {
                        'agent1': 'Issue Detection',
                        'agent2': 'Tenancy FAQ',
                        'router': 'Main Assistant'
                    }
                    st.write(f"• {agent_names.get(agent, agent)}: {count}")
            
            with col2:
                avg_confidence = messages_df['Confidence'].dropna().mean()
                image_count = messages_df['Has_Image'].sum()
                st.metric("Average Confidence", f"{avg_confidence:.1%}" if not pd.isna(avg_confidence) else "N/A")
                st.metric("Images Uploaded", int(image_count))
            
            with col3:
                response_times = []  # Would need to track actual response times
                st.metric("Total Interactions", len(messages_df))
                st.metric("User Messages", len(messages_df[messages_df['Type'] == 'user']))

    def run(self):
        """Main application runner"""
        st.title("🏠 Multi-Agent Real Estate Assistant")
        st.markdown("*Powered by AI agents specialized in property issues and tenancy guidance*")
        
        # Render sidebar
        self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["💬 Chat", "💡 Examples", "📊 Analytics"])
        
        with tab1:
            self.render_chat_interface()
        
        with tab2:
            self.render_example_interactions()
        
        with tab3:
            self.render_analytics_dashboard()

# Main execution
if __name__ == "__main__":
    app = RealEstateChatbotApp()
    app.run()