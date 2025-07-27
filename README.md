# Multi-Agent Real Estate Chatbot

**Developer:** Harish

A sophisticated multi-agentic chatbot system for real estate assistance, featuring specialized agents for property issue detection and tenancy guidance.

## 🏠 System Overview

This application implements a multi-agent architecture with two specialized virtual agents:

- **🔍 Agent 1 (Issue Detection)**: Analyzes property images and provides troubleshooting guidance
- **⚖️ Agent 2 (Tenancy FAQ)**: Offers legal guidance on rental laws and tenant rights
- **🏠 Agent Router**: Intelligently routes requests to the appropriate specialist

## ✨ Key Features

### Multi-Modal Analysis
- **Image Upload & Analysis**: Upload property photos for visual issue detection
- **Text-Based Queries**: Ask questions about tenancy laws and property maintenance
- **Combined Context**: Agents can work together on complex issues

### Intelligent Routing
- **Automatic Detection**: Smart routing based on content analysis and image presence
- **Context Awareness**: Maintains conversation history across agent switches
- **Fallback Handling**: Asks clarifying questions when intent is unclear

### Specialized Knowledge
- **Property Issues**: Water damage, structural problems, mold, electrical, plumbing
- **Legal Guidance**: Eviction laws, rent increases, security deposits, tenant rights
- **Location-Specific**: Tailored advice based on user's geographic location

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- OpenAI API key
- Git

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd multi-agent-real-estate-chatbot
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env file and add your API keys
```

5. **Run the application:**
```bash
streamlit run main.py
```

6. **Open your browser:**
Navigate to `http://localhost:8501`

## 🔧 Configuration

### Required Environment Variables

Create a `.env` file with the following:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for enhanced image analysis)
GOOGLE_VISION_API_KEY=your_google_vision_api_key_here
AZURE_VISION_KEY=your_azure_vision_key_here
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint_here

# Application settings
DEBUG=False
LOG_LEVEL=INFO
```

### API Key Setup

1. **OpenAI API Key** (Required):
   - Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Create a new API key
   - Add to your `.env` file

2. **Google Vision API** (Optional):
   - Enable Vision API in Google Cloud Console
   - Create service account and download credentials
   - Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

3. **Azure Vision API** (Optional):
   - Create Computer Vision resource in Azure Portal
   - Copy key and endpoint to `.env` file

## 🏗️ Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Agent Router   │────│ Conversation    │
│                 │    │                 │    │ Manager         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                    ┌───────────┴───────────┐
            ┌─────────────────┐    ┌─────────────────┐
            │    Agent 1      │    │    Agent 2      │
            │ Issue Detection │    │  Tenancy FAQ    │
            └─────────────────┘    └─────────────────┘
                     │                       │
            ┌─────────────────┐    ┌─────────────────┐
            │ Image Processor │    │ Legal Database  │
            └─────────────────┘    └─────────────────┘
```

### Agent Routing Logic

The system uses intelligent routing based on:

1. **Image Presence**: Automatically routes to Issue Detection Agent
2. **Keyword Analysis**: Matches text against specialized vocabularies
3. **Pattern Recognition**: Uses regex patterns for complex queries
4. **Context Awareness**: Considers conversation history
5. **Confidence Scoring**: Routes to highest confidence agent

### File Structure

```
multi-agent-real-estate-chatbot/
├── main.py                     # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── agents/
│   ├── __init__.py
│   ├── agent_router.py        # Central routing logic
│   ├── issue_detection_agent.py  # Property issue analysis
│   └── tenancy_faq_agent.py   # Legal guidance agent
├── utils/
│   ├── __init__.py
│   ├── conversation_manager.py # Context management
│   ├── image_processor.py     # Image handling utilities
│   └── response_formatter.py  # Response formatting
├── logs/                      # Application logs
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Development environment
└── README.md                  # This file
```

## 🎯 Agent Capabilities

### Issue Detection Agent (Agent 1)

**Detects and analyzes:**
- Water damage and leaks
- Structural issues (cracks, foundation problems)
- Mold and moisture problems
- Electrical issues
- Plumbing problems
- Cosmetic damage

**Provides:**
- Severity assessment (Minor/Moderate/Severe)
- Step-by-step repair guidance
- Cost estimates
- Safety recommendations
- Professional referral advice

**Example Interaction:**
```
User: [Uploads image of water stain] "What's wrong with my ceiling?"

Agent 1: 🔍 Issue Detection Analysis Complete

Primary Issue Detected: Water Damage (92% confidence)
Severity Level: Moderate

Analysis Details:
• Visible water staining and possible mold growth
• Paint peeling due to moisture exposure

Recommended Actions:
1. Check for active leaks above this area
2. Ensure proper ventilation to prevent mold spread
3. Contact a qualified contractor for assessment

Estimated Cost: $300-800
```

### Tenancy FAQ Agent (Agent 2)

**Covers topics:**
- Eviction procedures and tenant rights
- Rent increase regulations
- Security deposit laws
- Repair and maintenance responsibilities
- Lease termination procedures
- Tenant rights and protections

**Provides:**
- Location-specific legal guidance
- Template documents (repair requests, notices)
- Step-by-step procedures
- Resource referrals
- Timeline expectations

**Example Interaction:**
```
User: "Can my landlord evict me without notice?"

Agent 2: ⚖️ Tenancy Legal Guidance

Overview: Eviction laws vary by jurisdiction, but generally require proper notice and legal grounds.

Your Rights as a Tenant:
• Right to proper written notice (usually 30-60 days)
• Right to cure violations in many cases
• Right to legal representation in court
• Right to remain until court order

Location-Specific Advice: For more precise guidance, could you tell me your city/state?
```

## 🔄 Usage Examples

### Property Issue Analysis

1. **Upload an Image:**
   - Click the camera icon
   - Select property photo
   - Add description (optional)
   - Send message

2. **Text-Only Issues:**
   - Describe problem: "I have a leak in my bathroom"
   - Agent will ask follow-up questions
   - Provides troubleshooting steps

### Tenancy Questions

1. **Legal Queries:**
   - Ask about rights: "What notice does landlord need to give?"
   - Get location-specific advice
   - Receive template documents

2. **Emergency Situations:**
   - Get immediate guidance for urgent issues
   - Access to emergency resources
   - Legal referral information

## 🧪 Testing

### Run Unit Tests
```bash
python -m pytest tests/ -v
```

### Test Coverage
```bash
python -m pytest tests/ --cov=agents --cov=utils --cov-report=html
```

### Manual Testing Scenarios

1. **Image Analysis Test:**
   - Upload various property images
   - Test with different issue types
   - Verify confidence scores

2. **Routing Test:**
   - Try mixed queries (image + tenancy question)
   - Test clarification scenarios
   - Verify agent switching

3. **Location Test:**
   - Set different locations
   - Verify location-specific responses
   - Test unknown locations

## 🚀 Deployment

### Local Development
```bash
streamlit run main.py
```

### Docker Deployment
```bash
# Build image
docker build -t real-estate-bot .

# Run container
docker run -p 8501:8501 --env-file .env real-estate-bot
```

### Docker Compose
```bash
docker-compose up -d
```

### Cloud Deployment

**Streamlit Cloud:**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets (API keys) in dashboard
4. Deploy automatically

**Heroku:**
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
git push heroku main
```

**AWS/GCP/Azure:**
- Use Docker image with container services
- Set environment variables in cloud console
- Configure load balancing for production

## 📊 Performance Metrics

### Response Times
- Text queries: < 3 seconds
- Image analysis: < 10 seconds
- Agent routing: < 1 second

### Accuracy Targets
- Issue detection: > 90% accuracy
- Agent routing: > 95% correct routing
- Legal information: Verified against current laws

### Scalability
- Concurrent users: 100+ (with proper infrastructure)
- Image processing: Optimized for 10MB max files
- Memory usage: < 2GB per instance

## 🔒 Security Considerations

### Data Privacy
- Images processed in memory only
- No persistent storage of user images
- API keys encrypted in environment variables
- Session data cleared on browser close

### API Security
- Rate limiting on API endpoints
- Input validation and sanitization
- Secure image processing pipeline
- Error handling without data exposure

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API Key not found"**
   ```bash
   # Check .env file exists and contains:
   OPENAI_API_KEY=your_actual_key_here
   ```

2. **"Image upload failed"**
   - Check file size (max 10MB)
   - Verify image format (PNG, JPG, JPEG, GIF, BMP)
   - Ensure stable internet connection

3. **"Agent routing not working"**
   - Check for typos in agent keywords
   - Verify conversation context is maintained
   - Review agent routing logs

4. **"Streamlit won't start"**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r requirements.txt
   
   # Clear Streamlit cache
   streamlit cache clear
   ```

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Logs

Check application logs:
```bash
tail -f logs/app.log
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Install development dependencies: `pip install -r requirements.txt`
4. Make changes and add tests
5. Run tests: `pytest`
6. Submit pull request

### Code Style

- Use Black for formatting: `black .`
- Use flake8 for linting: `flake8 .`
- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include type hints

### Testing Guidelines

- Write unit tests for all new features
- Test both success and failure scenarios  
- Mock external API calls
- Achieve >90% code coverage

## 📈 Future Enhancements

### Phase 2 Features
- **Mobile App**: Native iOS/Android applications
- **Voice Interface**: Speech-to-text input and audio responses
- **Document Analysis**: OCR for lease agreements and legal documents
- **Video Analysis**: Short video clips for complex property issues

### Advanced AI Features
- **Predictive Maintenance**: ML models for issue prediction
- **Custom Training**: Fine-tuned models for specific property types
- **Multi-Language**: Support for Spanish, Chinese, and other languages
- **Expert Network**: Integration with human professionals

### Integration Opportunities
- **Property Management Systems**: API integrations
- **Legal Databases**: Real-time law updates
- **Service Marketplaces**: Connect with contractors and lawyers
- **IoT Devices**: Smart home sensor integration

## 📞 Support

### Contact Information
- **Developer**: [Your Name] - [your.email@example.com]
- **Project Repository**: [GitHub URL]
- **Documentation**: [Documentation URL]

### Getting Help

1. **Check Documentation**: Review this README and code comments
2. **Search Issues**: Look through existing GitHub issues
3. **Create Issue**: Submit detailed bug report or feature request
4. **Email Support**: Contact developer directly for urgent issues

### Streamlit from Google Colab:

```python
npm install -g localtunnel
streamlit run app.py &>/content/logs.txt & npx localtunnel --port 8501
```

### Feedback

We welcome feedback on:
- User experience and interface design
- Agent accuracy and response quality
- Feature requests and improvements
- Bug reports and technical issues

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision API
- Streamlit for the web framework
- Google Cloud Vision for image analysis capabilities
- Legal databases and tenant rights organizations for guidance

---

**Built with ❤️ for better real estate experiences**
