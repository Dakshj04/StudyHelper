# 🤖 Agentic AI Study Helper

> Your intelligent study companion powered by Groq AI - Research, Learn, and Test your knowledge!

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-API-green.svg)](https://console.groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### 📖 Research & Learn
- **Wikipedia Integration**: Automatically fetch comprehensive information on any topic
- **Smart Content Processing**: Advanced text analysis and extraction
- **Enhanced Search**: Disambiguation handling and fallback mechanisms
- **Rich Content Display**: Beautiful formatting with thumbnails and source links

### 📝 Interactive Quizzes
- **AI-Generated Questions**: Personalized quizzes based on your content using Groq AI
- **Multiple Difficulty Levels**: Easy, Medium, and Hard complexity options
- **Varied Question Types**: Multiple choice, short answer, essay, and true/false
- **Smart Question Creation**: Content-specific questions that test understanding

### 📋 Study Notes
- **AI-Enhanced Notes**: Comprehensive, structured notes with multiple sections
- **Organized Content**: Overview, key points, terms, facts, and study tips
- **Download Feature**: Export notes as markdown files for offline study
- **Fallback Generation**: Basic notes when AI is unavailable

### 🔗 Related Topics
- **Topic Discovery**: Find related subjects for deeper learning
- **Wikipedia Suggestions**: Intelligent topic recommendations
- **One-Click Study**: Instantly research suggested topics

### 🎯 Advanced Features
- **Study History**: Track and revisit previously studied topics
- **Session Management**: Persistent state across interactions
- **Error Recovery**: Robust error handling with graceful fallbacks
- **Rate Limit Awareness**: Smart handling of API limitations

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agentic-ai-study-helper.git
   cd agentic-ai-study-helper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Get started**
   - Open your browser to `http://localhost:8501`
   - Enter your Groq API key in the sidebar
   - Start learning!

## 📦 Dependencies

```txt
streamlit>=1.28.0
groq>=0.4.0
requests>=2.31.0
```

## 🔑 API Setup

### Getting Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it into the app's sidebar

**Note**: Groq offers a generous free tier perfect for educational use!

## 📚 Usage Guide

### Basic Workflow

1. **Enter API Key**: Add your Groq API key in the sidebar
2. **Choose Study Mode**: Select from Research, Quiz, Notes, or Related Topics
3. **Search Topic**: Enter any subject you want to learn about
4. **Interact**: Generate quizzes, create notes, or explore related topics

### Study Modes

#### 📖 Research & Learn
```
Perfect for: Initial topic exploration
Input: Any topic (e.g., "Machine Learning", "Photosynthesis")
Output: Comprehensive Wikipedia summary with source links
Actions: Generate quiz, create notes, find related topics
```

#### 📝 Quiz Mode
```
Perfect for: Testing your knowledge
Prerequisites: Previously researched content
Options: 3-15 questions, Easy/Medium/Hard difficulty
Output: Personalized questions with answer tracking
```

#### 📋 Study Notes
```
Perfect for: Organized learning materials
Features: AI-enhanced or basic structured notes
Sections: Overview, key points, terms, facts, study tips
Export: Download as markdown file
```

#### 🔗 Related Topics
```
Perfect for: Expanding your knowledge
Input: Previously studied topic
Output: Curated list of related subjects
Action: One-click research on related topics
```

### Pro Tips

- **Use Specific Topics**: "Photosynthesis" works better than "plants"
- **Try Different Difficulties**: Match complexity to your learning level
- **Utilize Study History**: Quickly revisit previous topics
- **Download Notes**: Keep offline copies for review
- **Explore Related Topics**: Discover connections between subjects

## 🛠️ Technical Details

### Architecture

```
┌─────────────────┐
│   Streamlit UI  │ ← User Interface Layer
├─────────────────┤
│   StudyHelper   │ ← Main Application Logic
├─────────────────┤
│   StudyTools    │ ← Core Functionality
├─────────────────┤
│ External APIs   │ ← Groq AI + Wikipedia
└─────────────────┘
```

### Key Components

- **StudyHelper**: Main application controller
- **StudyTools**: Core functionality (API calls, content processing)
- **Session State**: Persistent data across interactions
- **Error Handling**: Robust error recovery and user feedback

### API Integration

- **Groq AI**: Content generation and enhancement
- **Wikipedia API**: Research and content retrieval
- **Rate Limiting**: Intelligent handling of API limits
- **Encoding Safety**: Unicode and emoji handling

## 🎨 Customization

### Styling
The app uses custom CSS for a modern, professional look:
- Gradient backgrounds and smooth animations
- Responsive design for different screen sizes
- Color-coded sections for better organization
- Hover effects and interactive elements

### Configuration
Key settings can be modified in the code:
- Default difficulty levels
- Number of quiz questions
- API timeout values
- Content processing parameters

## 🔧 Troubleshooting

### Common Issues

**"Please enter your Groq API key"**
- Solution: Add your API key in the sidebar
- Check: Verify key is correct at console.groq.com

**"Rate limit exceeded"**
- Solution: Wait a few moments before retrying
- Note: Free tier has generous but limited requests

**"No Wikipedia article found"**
- Solution: Try different search terms
- Tip: Use more specific or general terms

**"API quota exceeded"**
- Solution: Check your Groq account usage
- Option: Upgrade to higher tier if needed

### Error Recovery
The app includes automatic:
- Text encoding fixes for special characters
- Fallback to basic functionality when AI fails
- Retry mechanisms for network issues
- Graceful degradation for missing features

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Areas for Contribution
- **New Features**: Additional study modes or tools
- **UI Improvements**: Better styling or user experience
- **API Integration**: Support for other AI services
- **Performance**: Optimization and caching
- **Documentation**: Tutorials and examples

## 📈 Roadmap

### Upcoming Features
- [ ] **Flashcard Generation**: Create interactive flashcards
- [ ] **Study Schedules**: Spaced repetition reminders
- [ ] **Progress Tracking**: Learning analytics and insights
- [ ] **Multi-language Support**: Study in different languages
- [ ] **Collaborative Features**: Share notes and quizzes
- [ ] **Advanced Search**: Filter by difficulty, topic type
- [ ] **Custom Content**: Upload your own study materials

### Performance Improvements
- [ ] **Caching System**: Store frequently accessed content
- [ ] **Batch Processing**: Handle multiple topics efficiently
- [ ] **Async Operations**: Faster content loading
- [ ] **Database Integration**: Persistent user data

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast, reliable AI inference
- **Wikipedia**: For comprehensive educational content
- **Streamlit**: For the amazing web app framework
- **OpenAI**: For inspiration in AI-powered education

## 📞 Support

### Getting Help
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact us at support@studyhelper.com

### Resources
- **Documentation**: Full API documentation available
- **Tutorials**: Step-by-step guides and examples
- **Community**: Join our Discord server for real-time help

---

<div align="center">

**Made with ❤️ for learners everywhere**

[Report Bug](https://github.com/yourusername/agentic-ai-study-helper/issues) • [Request Feature](https://github.com/yourusername/agentic-ai-study-helper/issues) • [Documentation](https://github.com/yourusername/agentic-ai-study-helper/wiki)

</div>