# 🤖 Agentic AI Study Helper

An intelligent study companion powered by AI that helps you research, learn, and test your knowledge on any topic. Built with Streamlit and Google's Gemini AI.

## ✨ Features

- **📖 Research & Learn Mode**
  - Search Wikipedia articles on any topic
  - Get concise, well-structured summaries
  - Access original sources with direct links
  
- **📝 Quiz Generation**
  - AI-powered quiz questions based on content
  - Multiple difficulty levels (easy, medium, hard)
  - Customizable number of questions
  - Various question types (multiple choice, short answer, essay)

- **📋 Smart Study Notes**
  - AI-enhanced comprehensive notes generation
  - Basic note-taking with key points extraction
  - Important terms highlighting
  - Structured summaries and key concepts
  
- **🔗 Related Topics**
  - Discover connected subjects
  - Expand your knowledge breadth
  - One-click navigation to related topics

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Streamlit
- Internet connection for API access

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd study-helper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
   - Get a Google Gemini API key from Google Cloud Console
   - Update the `.env` file:
```properties
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## 🎯 Usage

1. **Start Learning**
   - Enter any topic in the search box
   - Click "Start Learning" to begin
   - Choose your study mode from the sidebar

2. **Study Modes**
   - Research & Learn: Get detailed information about your topic
   - Quiz Mode: Test your knowledge
   - Study Notes: Generate comprehensive notes
   - Related Topics: Explore connected subjects

3. **Customize Experience**
   - Adjust difficulty levels
   - Set number of quiz questions
   - Choose between AI-enhanced or basic notes
   - Track your study history

## 🛠️ Technology Stack

- [Streamlit](https://streamlit.io/) - Frontend interface
- [Google Gemini AI](https://ai.google.dev/) - AI-powered content generation
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) - Content sourcing
- [Python](https://www.python.org/) - Backend logic

## 📝 Note

- API keys should be kept secure and not shared
- Some features require active internet connection
- Content is sourced from Wikipedia and processed by AI

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the intelligent features
- Wikipedia for providing the knowledge base
- Streamlit for the interactive web interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.