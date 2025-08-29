import streamlit as st
import requests
import json
import re
from datetime import datetime
import time
import os

# Add imports for Groq
try:
    from groq import Groq
except ImportError:
    st.error("Please install the groq package: pip install groq")
    st.stop()

st.set_page_config(
    page_title="🤖 Agentic AI Study Helper", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .tool-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .quiz-question {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #2196f3;
        color: #1565c0;
        font-size: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .quiz-question strong {
        color: #0d47a1;
    }
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        animation: fadeIn 0.5s ease-in;
    }
    .notes-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .notes-section h3 {
        color: #495057;
        margin-bottom: 1rem;
    }
    .notes-section p, .notes-section li {
        color: #212529;
        line-height: 1.6;
    }
    .key-point {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        color: #856404;
        transition: transform 0.2s ease;
    }
    .key-point:hover {
        transform: translateX(5px);
    }
    .important-term {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 0.6rem 1rem;
        margin: 0.3rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 500;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .api-status {
        background: #e8f5e8;
        color: #2e7d32;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ===== ENHANCED TOOLS =====
class StudyTools:
    @staticmethod
    def call_groq_api(prompt, max_tokens=1500, temperature=0.7):
        """Call Groq API with improved error handling"""
        try:
            # Get API key from session state
            api_key = st.session_state.get('groq_api_key')
            if not api_key:
                st.error("Please enter your Groq API key in the sidebar")
                return None

            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Clean prompt to remove emojis and special characters that might cause encoding issues
            clean_prompt = StudyTools._clean_text_for_api(prompt)
            
            # Call the API with rate limiting consideration
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a knowledgeable and helpful AI study assistant. Provide clear, accurate, and well-structured educational content. Use plain text without emojis in your responses."
                    },
                    {
                        "role": "user", 
                        "content": clean_prompt
                    }
                ],
                model="llama3-8b-8192",
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content

        except UnicodeEncodeError as e:
            st.error("Text encoding error. Retrying with cleaned text...")
            # Try again with more aggressive text cleaning
            try:
                ascii_prompt = prompt.encode('ascii', 'ignore').decode('ascii')
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a helpful AI study assistant. Provide clear educational content using only standard ASCII characters."
                        },
                        {
                            "role": "user", 
                            "content": ascii_prompt
                        }
                    ],
                    model="llama3-8b-8192",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=1,
                    stream=False
                )
                return response.choices[0].message.content
            except Exception as retry_error:
                st.error(f"API call failed after retry: {retry_error}")
                return None
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg:
                st.error("Rate limit exceeded. Please wait a moment before trying again.")
                st.info("Tip: Groq free tier has rate limits. Consider upgrading for higher limits.")
            elif "api key" in error_msg or "authentication" in error_msg:
                st.error("Invalid API key. Please check your Groq API key.")
            elif "quota" in error_msg:
                st.error("API quota exceeded. Please check your Groq account limits.")
            else:
                st.error(f"Error calling Groq API: {e}")
            return None

    @staticmethod
    def _clean_text_for_api(text):
        """Clean text to remove emojis and problematic characters for API calls"""
        import re
        
        # Remove emojis and special Unicode characters
        emoji_pattern = re.compile("["
                                 u"\U0001F600-\U0001F64F"  # emoticons
                                 u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                 u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                 u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                 u"\U00002702-\U000027B0"
                                 u"\U000024C2-\U0001F251"
                                 u"\U0001F900-\U0001F9FF"  # supplemental symbols
                                 "]+", flags=re.UNICODE)
        
        # Remove emojis
        text = emoji_pattern.sub(r'', text)
        
        # Replace common markdown symbols that might cause issues
        replacements = {
            '📖': 'Overview',
            '🔑': 'Key Points',
            '📚': 'Important Terms',
            '💡': 'Key Facts',
            '🌐': 'Connections',
            '🎯': 'Study Tips',
            '❓': 'Review Questions',
            '##': 'Section:',
            '•': '-'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Ensure ASCII compatibility
        try:
            text = text.encode('ascii', 'ignore').decode('ascii')
        except:
            pass
            
        return text

    @staticmethod
    def search_wikipedia(query, max_retries=3):
        """Enhanced Wikipedia search with better error handling and retries"""
        for attempt in range(max_retries):
            try:
                # Clean the query
                clean_query = query.strip().replace(' ', '_')
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{clean_query}"
                
                headers = {
                    'User-Agent': 'StudyHelper/2.0 (https://streamlit.io; educational-use)',
                    'Accept': 'application/json'
                }
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    extract = data.get('extract', 'No summary available.')
                    
                    # Filter out disambiguation pages
                    if 'may refer to:' in extract.lower() or len(extract) < 100:
                        # Try to get more specific content
                        search_url = f"https://en.wikipedia.org/w/api.php"
                        search_params = {
                            'action': 'query',
                            'format': 'json',
                            'list': 'search',
                            'srsearch': query,
                            'srlimit': 5
                        }
                        
                        search_response = requests.get(search_url, params=search_params, timeout=10)
                        if search_response.status_code == 200:
                            search_data = search_response.json()
                            if search_data.get('query', {}).get('search'):
                                # Get the first search result
                                first_result = search_data['query']['search'][0]
                                return StudyTools.search_wikipedia(first_result['title'])
                    
                    page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
                    
                    return {
                        'success': True,
                        'content': extract,
                        'url': page_url,
                        'title': data.get('title', query),
                        'thumbnail': data.get('thumbnail', {}).get('source', '')
                    }
                elif response.status_code == 404:
                    return {
                        'success': False,
                        'content': f"No Wikipedia article found for '{query}'. Try a different search term or check the spelling.",
                        'error': "Not Found"
                    }
                else:
                    if attempt == max_retries - 1:
                        return {
                            'success': False,
                            'content': f"Could not fetch information about '{query}' (HTTP {response.status_code})",
                            'error': f"HTTP {response.status_code}"
                        }
                    time.sleep(1)  # Wait before retry
                    
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'content': "Request timed out. Please check your internet connection and try again.",
                        'error': "Timeout"
                    }
                time.sleep(2)
            except Exception as e:
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'content': f"Error searching Wikipedia: {str(e)}",
                        'error': str(e)
                    }
                time.sleep(1)
        
        return {
            'success': False,
            'content': "Failed to retrieve information after multiple attempts.",
            'error': "Max retries exceeded"
        }
    
    @staticmethod
    def generate_enhanced_quiz_with_ai(content, topic, difficulty="medium", num_questions=5):
        """Generate better quiz questions using Groq AI"""
        if not content or len(content.strip()) < 50:
            return StudyTools.generate_basic_quiz(content, difficulty, num_questions)
        
        try:
            difficulty_instructions = {
                "easy": "Create simple recall questions, fill-in-the-blanks, and basic true/false questions that test basic understanding.",
                "medium": "Create questions that require understanding and explanation of concepts, asking 'how' and 'why' questions.",
                "hard": "Create analytical questions that require critical thinking, comparison, synthesis, and application of knowledge."
            }
            
            prompt = f"""
            Create exactly {num_questions} {difficulty} level educational quiz questions about: "{topic}"
            
            Content to base questions on:
            {content}
            
            Requirements:
            {difficulty_instructions[difficulty]}
            
            Format Requirements:
            - Number each question clearly (Q1:, Q2:, etc.)
            - Make questions varied (multiple choice, short answer, essay, true/false)
            - Ensure questions test different aspects of the topic
            - Focus on the most important concepts from the content
            - Make questions specific to the content provided
            - Avoid generic questions
            - Use plain text without emojis or special characters
            
            Example format:
            Q1: [Specific question based on content]
            Q2: [Different type of question]
            Q3: [Another variation]
            
            Create exactly {num_questions} questions now:
            """
            
            with st.spinner("AI is crafting personalized quiz questions..."):
                response_text = StudyTools.call_groq_api(prompt, max_tokens=1200, temperature=0.5)
            
            if response_text:
                # Parse the response into individual questions
                questions = []
                lines = response_text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    # Look for question patterns
                    if (line and (line.lower().startswith('q') or 
                                 re.match(r'^[0-9]+[\.\):]', line) or
                                 line.lower().startswith('question'))):
                        # Clean up the question
                        cleaned_question = re.sub(r'^(Q[0-9]+[:.]?|[0-9]+[\.\):]|Question [0-9]+[:.]?)\s*', '', line)
                        if cleaned_question and len(cleaned_question) > 10:
                            questions.append(cleaned_question)
                
                # If we didn't get enough questions, fill with basic ones
                if len(questions) < num_questions:
                    basic_questions = StudyTools.generate_basic_quiz(content, difficulty, num_questions - len(questions))
                    questions.extend(basic_questions)
                
                return questions[:num_questions] if questions else StudyTools.generate_basic_quiz(content, difficulty, num_questions)
            else:
                return StudyTools.generate_basic_quiz(content, difficulty, num_questions)
            
        except Exception as e:
            st.warning(f"AI quiz generation encountered an issue: {e}. Using basic quiz generation.")
            return StudyTools.generate_basic_quiz(content, difficulty, num_questions)

    @staticmethod
    def generate_basic_quiz(content, difficulty="medium", num_questions=5):
        """Generate quiz questions based on content (fallback method)"""
        if not content or len(content.split()) < 10:
            return ["Not enough content to generate meaningful quiz questions. Please search for a topic first."]
        
        # Extract key information
        sentences = [s.strip() for s in content.split('. ') if len(s.strip()) > 20]
        key_sentences = sentences[:min(10, len(sentences))]
        
        questions = []
        
        # Generate content-specific questions
        for i, sentence in enumerate(key_sentences[:num_questions]):
            if difficulty == "easy":
                if i % 3 == 0:
                    questions.append(f"Fill in the blank: {sentence.replace(sentence.split()[-3], '______')}")
                elif i % 3 == 1:
                    questions.append(f"True or False: {sentence}")
                else:
                    questions.append(f"What is mentioned about {sentence.split()[0] if sentence.split() else 'the topic'}?")
            
            elif difficulty == "medium":
                if i % 3 == 0:
                    questions.append(f"Explain the significance of: {sentence[:60]}...")
                elif i % 3 == 1:
                    questions.append(f"How does this relate to the main topic: {sentence[:50]}...?")
                else:
                    questions.append(f"What are the key characteristics mentioned in: {sentence[:70]}...?")
            
            else:  # hard
                if i % 3 == 0:
                    questions.append(f"Analyze and evaluate: {sentence[:60]}...")
                elif i % 3 == 1:
                    questions.append(f"What are the implications of: {sentence[:50]}...?")
                else:
                    questions.append(f"How would you apply this knowledge: {sentence[:60]}...?")
        
        # Fill with generic questions if needed
        while len(questions) < num_questions:
            generic_questions = [
                "What is the main concept discussed in this topic?",
                "How does this topic relate to real-world applications?",
                "What are the most important points to remember?",
                "What questions does this information raise?",
                "How might this knowledge be useful in practice?"
            ]
            questions.append(generic_questions[len(questions) % len(generic_questions)])
        
        return questions[:num_questions]
    
    @staticmethod
    def generate_enhanced_notes_with_ai(content, topic):
        """Generate comprehensive study notes using Groq AI"""
        if not content or len(content.strip()) < 50:
            return StudyTools.create_basic_notes(content)
        
        try:
            prompt = f"""
            Create comprehensive, well-structured study notes for the topic: "{topic}"
            
            Source content:
            {content}
            
            Create detailed study notes with these sections:
            
            Overview
            A clear, concise summary (2-3 sentences) of the main concept
            
            Key Points
            5-8 detailed bullet points covering the most important aspects from the content
            
            Important Terms and Concepts
            5-7 key terms with clear definitions and explanations
            
            Key Facts and Details
            4-6 specific facts, data points, or important details worth remembering
            
            Connections and Applications
            How this topic relates to other subjects, real-world applications, or broader concepts
            
            Study Tips
            Specific suggestions for remembering this information (mnemonics, analogies, etc.)
            
            Review Questions
            3-4 self-assessment questions to test understanding
            
            Make the notes comprehensive, student-friendly, and well-organized.
            Focus specifically on the content provided, not generic information.
            Use plain text formatting without emojis or special unicode characters.
            """
            
            with st.spinner("AI is creating comprehensive study notes..."):
                response_text = StudyTools.call_groq_api(prompt, max_tokens=2000, temperature=0.4)
            
            if response_text:
                return {
                    'enhanced': True,
                    'content': response_text
                }
            else:
                return StudyTools.create_basic_notes(content)
            
        except Exception as e:
            st.warning(f"AI notes generation encountered an issue: {e}. Using basic notes generation.")
            return StudyTools.create_basic_notes(content)

    @staticmethod
    def create_basic_notes(content):
        """Create structured study notes (fallback method)"""
        if not content:
            return {
                'enhanced': False,
                'content': "No content available for notes generation."
            }
        
        sentences = [s.strip() for s in content.split('. ') if s.strip()]
        
        # Extract key information
        key_points = []
        important_terms = set()
        
        for sentence in sentences:
            if len(sentence.split()) > 8:
                key_points.append(sentence)
            
            # Extract capitalized terms (potential important concepts)
            words = sentence.split()
            for word in words:
                clean_word = re.sub(r'[^\w]', '', word)
                if (clean_word.istitle() and len(clean_word) > 3 and 
                    clean_word not in ['The', 'This', 'That', 'These', 'Those', 'When', 'Where', 'What', 'How']):
                    important_terms.add(clean_word)
        
        # Create formatted notes
        notes_content = f"""
Overview
{'. '.join(sentences[:2]) + '.' if len(sentences) >= 2 else sentences[0] if sentences else 'No overview available.'}

Key Points
"""
        for i, point in enumerate(key_points[:6], 1):
            notes_content += f"- {point}\n"
        
        notes_content += f"""
Important Terms
"""
        for term in sorted(list(important_terms))[:8]:
            notes_content += f"- {term}\n"
        
        notes_content += f"""
Summary
{'. '.join(sentences[:3]) + '.' if len(sentences) >= 3 else content[:200] + '...'}

Study Tips
- Review the key points regularly
- Create connections between important terms
- Practice explaining the concept in your own words
- Look for real-world examples and applications
"""
        
        return {
            'enhanced': False,
            'content': notes_content
        }
    
    @staticmethod
    def get_related_topics(topic):
        """Suggest related topics for further study"""
        try:
            # Use Wikipedia's opensearch API for suggestions
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': topic,
                'limit': 8,
                'format': 'json'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = data[1] if len(data) > 1 else []
                
                # Filter and enhance suggestions
                filtered_suggestions = []
                for suggestion in suggestions[:6]:
                    if suggestion.lower() != topic.lower():
                        filtered_suggestions.append(suggestion)
                
                return filtered_suggestions
            
        except Exception as e:
            st.warning(f"Could not fetch related topics: {e}")
        
        # Fallback suggestions
        return [
            f"History of {topic}",
            f"Applications of {topic}",
            f"{topic} fundamentals",
            f"Advanced {topic}",
            f"{topic} in practice"
        ]

# ===== MAIN APPLICATION =====
class StudyHelper:
    def __init__(self):
        self.tools = StudyTools()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        defaults = {
            'study_history': [],
            'current_content': "",
            'current_topic': "",
            'show_quiz': False,
            'show_notes': False,
            'show_related': False,
            'groq_api_key': ""
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def display_header(self):
        """Display the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🤖 Agentic AI Study Helper</h1>
            <p>Your intelligent study companion powered by Groq AI - Research, Learn, and Test your knowledge!</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_sidebar(self):
        """Display sidebar with options and history"""
        with st.sidebar:
            st.header("🎯 Study Configuration")

            # Groq API Key input with validation
            groq_api_key = st.text_input(
                "🔑 Enter Groq API Key:",
                type="password",
                value=st.session_state.get('groq_api_key', ''),
                help="Get your free API key from console.groq.com"
            )
            
            if groq_api_key:
                st.session_state['groq_api_key'] = groq_api_key
                st.markdown('<div class="api-status">✅ API Key Configured</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ Please enter your Groq API key to enable AI features</div>', unsafe_allow_html=True)

            st.divider()

            # Study mode selection
            study_mode = st.selectbox(
                "📚 Select Study Mode:",
                ["📖 Research & Learn", "📝 Quiz Mode", "📋 Study Notes", "🔗 Related Topics"],
                help="Choose how you want to study your topic"
            )
            
            # Advanced options
            with st.expander("⚙️ Advanced Options"):
                difficulty = st.selectbox(
                    "📊 Difficulty Level:",
                    ["easy", "medium", "hard"],
                    index=1,
                    help="Select the complexity level for quizzes and content"
                )
                
                num_questions = st.slider(
                    "❓ Number of Quiz Questions:", 
                    min_value=3, 
                    max_value=15, 
                    value=5,
                    help="How many questions to generate for quizzes"
                )
            
            st.divider()
            
            # Study history
            st.header("📚 Recent Studies")
            if st.session_state.study_history:
                for i, item in enumerate(st.session_state.study_history[-5:]):
                    with st.expander(f"📖 {item['topic'][:25]}{'...' if len(item['topic']) > 25 else ''}"):
                        st.write(f"**🕒 Time:** {item['timestamp']}")
                        st.write(f"**📋 Mode:** {item['mode']}")
                        if st.button(f"🔄 Study Again", key=f"restudy_{i}"):
                            return study_mode, difficulty, num_questions, item['topic']
            else:
                st.info("No recent studies")
            
            if st.button("🗑️ Clear History", help="Remove all study history"):
                st.session_state.study_history = []
                st.rerun()
            
            return study_mode, difficulty, num_questions, None
    
    def add_to_history(self, topic, mode):
        """Add study session to history"""
        # Avoid duplicates
        existing_topics = [item['topic'] for item in st.session_state.study_history]
        if topic not in existing_topics:
            st.session_state.study_history.append({
                'topic': topic,
                'mode': mode,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        # Keep only last 20 items
        st.session_state.study_history = st.session_state.study_history[-20:]
    
    def research_mode(self, topic):
        """Research and learning mode with enhanced display"""
        st.header(f"📖 Researching: {topic}")
        
        with st.spinner("🔍 Searching Wikipedia for comprehensive information..."):
            result = self.tools.search_wikipedia(topic)
        
        if result['success']:
            st.session_state.current_content = result['content']
            st.session_state.current_topic = topic
            
            # Success message with animation
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success(f"✅ Successfully found detailed information about: **{result['title']}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display content in an attractive format
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("### 📄 Content Summary")
                st.markdown(f"**📊 Length:** {len(result['content'])} characters")
                st.markdown("---")
                st.write(result['content'])
            
            with col2:
                if result.get('thumbnail'):
                    st.image(result['thumbnail'], width=200)
                
                if result.get('url'):
                    st.markdown(f"**📖 Source:** [Wikipedia Article]({result['url']})")
                
                st.markdown("**🔧 Available Actions:**")
                if st.button("📝 Generate Quiz", use_container_width=True):
                    st.session_state.show_quiz = True
                    st.rerun()
                
                if st.button("📋 Create Notes", use_container_width=True):
                    st.session_state.show_notes = True
                    st.rerun()
                
                if st.button("🔗 Related Topics", use_container_width=True):
                    st.session_state.show_related = True
                    st.rerun()
            
        else:
            st.error(f"❌ {result['content']}")
            if result.get('error') == 'Not Found':
                st.info("💡 **Suggestions:**")
                st.info("• Check the spelling of your search term")
                st.info("• Try more general or specific terms")
                st.info("• Use alternative names or synonyms")
    
    def quiz_mode(self, difficulty, num_questions):
        """Enhanced quiz generation mode"""
        if not st.session_state.current_content:
            st.warning("⚠️ Please research a topic first to generate a quiz!")
            return
        
        st.header(f"📝 Interactive Quiz: {st.session_state.current_topic}")
        
        # Display quiz metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Difficulty", difficulty.capitalize())
        with col2:
            st.metric("❓ Questions", num_questions)
        with col3:
            st.metric("📄 Content Length", f"{len(st.session_state.current_content)} chars")
        
        st.divider()
        
        # Generate quiz questions
        questions = self.tools.generate_enhanced_quiz_with_ai(
            st.session_state.current_content, 
            st.session_state.current_topic,
            difficulty, 
            num_questions
        )
        
        # Display questions with enhanced styling
        st.markdown("### 🎯 Quiz Questions")
        answers = {}
        
        for i, question in enumerate(questions, 1):
            st.markdown(f"""
            <div class="quiz-question">
                <strong>Question {i}:</strong> {question}
            </div>
            """, unsafe_allow_html=True)
            
            # Answer input with dynamic height based on question type
            if "essay" in question.lower() or "explain" in question.lower() or "analyze" in question.lower():
                height = 150
            else:
                height = 80
            
            answers[f"q{i}"] = st.text_area(
                f"Your answer for Question {i}:", 
                key=f"answer_{i}", 
                height=height,
                placeholder="Type your answer here..."
            )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("📊 Submit Quiz", type="primary", use_container_width=True):
                completed_answers = sum(1 for ans in answers.values() if ans.strip())
                st.success(f"✅ Quiz submitted! You answered {completed_answers}/{len(questions)} questions.")
                
                if completed_answers == len(questions):
                    st.balloons()
                    st.info("🎉 Great job completing all questions! Review your answers against the source material.")
                else:
                    st.warning(f"📝 You have {len(questions) - completed_answers} unanswered questions remaining.")
        
        with col2:
            if st.button("🔄 Generate New Quiz", use_container_width=True):
                st.rerun()
    
    def notes_mode(self):
        """Enhanced study notes generation mode"""
        if not st.session_state.current_content:
            st.warning("⚠️ Please research a topic first to create study notes!")
            return
        
        st.header(f"📋 Study Notes: {st.session_state.current_topic}")
        
        # Notes type selection
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("**Choose your notes style:**")
        with col2:
            notes_type = st.selectbox(
                "", 
                ["🧠 AI Enhanced (Recommended)", "📝 Basic Structure"], 
                key="notes_type",
                help="AI Enhanced provides comprehensive, structured notes using Groq AI"
            )
        
        if notes_type == "🧠 AI Enhanced (Recommended)":
            if not st.session_state.get('groq_api_key'):
                st.error("🔑 Please enter your Groq API key in the sidebar to use AI-enhanced notes.")
                return
            
            notes_result = self.tools.generate_enhanced_notes_with_ai(
                st.session_state.current_content, 
                st.session_state.current_topic
            )
            
            if notes_result.get('enhanced'):
                st.markdown('<div class="notes-section">', unsafe_allow_html=True)
                st.markdown(notes_result['content'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download option
                st.download_button(
                    label="💾 Download Notes",
                    data=notes_result['content'],
                    file_name=f"{st.session_state.current_topic}_notes.md",
                    mime="text/markdown"
                )
            else:
                self._display_basic_notes(notes_result)
        else:
            notes = self.tools.create_basic_notes(st.session_state.current_content)
            st.markdown('<div class="notes-section">', unsafe_allow_html=True)
            st.markdown(notes['content'])
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _display_basic_notes(self, notes_result):
        """Display basic notes with enhanced styling"""
        st.markdown('<div class="notes-section">', unsafe_allow_html=True)
        st.markdown(notes_result['content'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    def related_topics_mode(self):
        """Enhanced related topics suggestion mode"""
        if not st.session_state.current_topic:
            st.warning("⚠️ Please research a topic first to find related topics!")
            return
        
        st.header(f"🔗 Topics Related to: {st.session_state.current_topic}")
        
        with st.spinner("🔍 Discovering related topics..."):
            related = self.tools.get_related_topics(st.session_state.current_topic)
        
        if related:
            st.markdown("### 📚 Suggested Topics for Further Study:")
            
            # Display in a grid layout
            cols = st.columns(2)
            for i, topic in enumerate(related):
                with cols[i % 2]:
                    with st.container():
                        st.markdown(f"**📖 {topic}**")
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"Explore this related topic")
                        with col2:
                            if st.button("🔍 Study", key=f"study_{i}_{topic}"):
                                self.research_mode(topic)
                                self.add_to_history(topic, "Related Topic Research")
                                st.rerun()
                        st.divider()
        else:
            st.info("No related topics found. Try searching for a different topic.")
    
    def display_usage_tips(self):
        """Display helpful usage tips"""
        with st.expander("💡 Usage Tips & Help"):
            st.markdown("""
            ### 🚀 Getting Started
            1. **Get a Groq API Key**: Visit [console.groq.com](https://console.groq.com) to get your free API key
            2. **Enter your API key** in the sidebar (it's stored securely in your session)
            3. **Search for any topic** you want to learn about
            
            ### 🎯 Study Modes
            - **📖 Research & Learn**: Get comprehensive information from Wikipedia
            - **📝 Quiz Mode**: Generate personalized quizzes based on your content
            - **📋 Study Notes**: Create structured, comprehensive study notes
            - **🔗 Related Topics**: Discover connected topics for deeper learning
            
            ### ⚙️ Pro Tips
            - Use **specific topic names** for better results (e.g., "Photosynthesis" vs "plants")
            - Try different **difficulty levels** to match your learning needs
            - Use the **study history** to quickly revisit topics
            - **Download your notes** for offline studying
            
            ### 🔧 Troubleshooting
            - If you get rate limit errors, wait a few moments before trying again
            - For "API key" errors, double-check your Groq API key
            - If Wikipedia search fails, try alternative topic names
            """)
    
    def run(self):
        """Main application runner"""
        self.display_header()
        
        # Check if this is first run
        if not st.session_state.get('groq_api_key'):
            st.info("👋 **Welcome!** Please enter your Groq API key in the sidebar to get started. It's free at console.groq.com")
        
        # Sidebar
        sidebar_result = self.display_sidebar()
        if len(sidebar_result) == 4:
            study_mode, difficulty, num_questions, restudy_topic = sidebar_result
        else:
            study_mode, difficulty, num_questions = sidebar_result
            restudy_topic = None
        
        # Main content area
        col1, col2 = st.columns([4, 1])
        
        with col1:
            topic_input = st.text_input(
                "🎯 Enter a topic to study:",
                placeholder="e.g., Machine Learning, Photosynthesis, Ancient Rome, Quantum Physics...",
                value=restudy_topic if restudy_topic else ""
            )
        
        with col2:
            st.write("")  # Spacing for alignment
            search_button = st.button("🔍 Start Learning", type="primary", use_container_width=True)
        
        # Usage tips
        self.display_usage_tips()
        
        # Process user input
        if (search_button and topic_input) or restudy_topic:
            current_topic = topic_input or restudy_topic
            self.add_to_history(current_topic, study_mode)
            
            if "Research" in study_mode:
                self.research_mode(current_topic)
            elif "Quiz" in study_mode:
                st.session_state.current_topic = current_topic
                # First research, then show quiz
                self.research_mode(current_topic)
                if st.session_state.current_content:
                    st.divider()
                    self.quiz_mode(difficulty, num_questions)
            elif "Notes" in study_mode:
                st.session_state.current_topic = current_topic
                self.research_mode(current_topic)
                if st.session_state.current_content:
                    st.divider()
                    self.notes_mode()
            elif "Related" in study_mode:
                st.session_state.current_topic = current_topic
                self.research_mode(current_topic)
                if st.session_state.current_content:
                    st.divider()
                    self.related_topics_mode()
        
        # Handle mode-specific displays for current content
        if st.session_state.current_content:
            if study_mode == "📝 Quiz Mode" and not search_button:
                st.divider()
                self.quiz_mode(difficulty, num_questions)
            
            elif study_mode == "📋 Study Notes" and not search_button:
                st.divider()
                self.notes_mode()
            
            elif study_mode == "🔗 Related Topics" and not search_button:
                st.divider()
                self.related_topics_mode()
        
        # Handle action button states from research mode
        if st.session_state.get('show_quiz'):
            st.divider()
            self.quiz_mode(difficulty, num_questions)
            st.session_state.show_quiz = False
        
        if st.session_state.get('show_notes'):
            st.divider()
            self.notes_mode()
            st.session_state.show_notes = False
        
        if st.session_state.get('show_related'):
            st.divider()
            self.related_topics_mode()
            st.session_state.show_related = False

# ===== RUN APPLICATION =====
if __name__ == "__main__":
    try:
        app = StudyHelper()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page and try again. If the problem persists, check your internet connection and API key.")