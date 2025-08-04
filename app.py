#!/usr/bin/env python3
"""
Content Marketing Agent - Streamlit App
AI-powered content creation assistant with real trend analysis and chat interface
"""

import streamlit as st
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
import json

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# For Streamlit Cloud deployment, get API keys from secrets
def get_api_key(key_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        return st.secrets[key_name]
    except:
        return os.getenv(key_name, "")

# Initialize the DSPy agent (AI-heavy operations only)
@st.cache_resource
def get_dspy_agent():
    """Initialize and cache the DSPy agent for AI operations"""
    try:
        from agents.dspy_agent import DSPyContentAgent
        return DSPyContentAgent()
    except Exception as e:
        st.error(f"Error initializing DSPy agent: {e}")
        return None

# Initialize content helpers (simple Python utilities)
@st.cache_resource
def get_content_helpers():
    """Initialize content helper utilities"""
    try:
        from utils.content_helpers import ContentFormatter, PlatformOptimizer, TrendDataProcessor, ConversationHelper
        return {
            'formatter': ContentFormatter(),
            'optimizer': PlatformOptimizer(),
            'trend_processor': TrendDataProcessor(),
            'conversation_helper': ConversationHelper()
        }
    except Exception as e:
        st.error(f"Error initializing content helpers: {e}")
        return None

# Async wrapper for Streamlit
def run_async(coro):
    """Run async function in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

def main():
    """Main Streamlit app"""
    
    st.set_page_config(
        page_title="Content Marketing Agent",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Content Marketing Agent")
    st.markdown("*Your AI-powered content creation assistant with real-time trend analysis*")
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'content_pieces' not in st.session_state:
        st.session_state.content_pieces = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_trends' not in st.session_state:
        st.session_state.current_trends = None
    
    # Initialize DSPy agent and content helpers
    agent = get_dspy_agent()
    helpers = get_content_helpers()
    
    # Check if user has completed setup
    if st.session_state.user_profile is None:
        st.markdown("## 🚀 Welcome! Let's Set Up Your Content Marketing Assistant")
        st.markdown("Complete the form below to personalize your AI assistant for your unique needs and cultural context.")
        
        # Simple setup form
        with st.form("simple_setup"):
            st.markdown("### Basic Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name *")
                brand_name = st.text_input("Brand Name *")
                age = st.number_input("Age", min_value=18, max_value=100, value=60)
            
            with col2:
                primary_language = st.selectbox(
                    "Primary Language *",
                    options=["en", "fr"],
                    format_func=lambda x: {"en": "English", "fr": "French"}[x]
                )
                cultural_background = st.selectbox(
                    "Cultural Background",
                    options=["cameroon", "other"],
                    format_func=lambda x: {"cameroon": "Cameroon", "other": "Other"}[x]
                )
            
            expertise_areas = st.multiselect(
                "Areas of Expertise *",
                options=[
                    "Business Coaching", "Life Coaching", "Health & Wellness", 
                    "Finance", "Marketing", "Education", "Personal Development"
                ]
            )
            
            active_platforms = st.multiselect(
                "Active Social Media Platforms *",
                options=["instagram", "tiktok", "youtube", "linkedin", "facebook"],
                format_func=lambda x: x.title()
            )
            
            submitted = st.form_submit_button("🚀 Create Profile", type="primary")
            
            if submitted:
                if name and brand_name and expertise_areas and active_platforms:
                    # Create a simple user profile
                    st.session_state.user_profile = {
                        "name": name,
                        "brand_name": brand_name,
                        "age": age,
                        "primary_language": primary_language,
                        "cultural_background": cultural_background,
                        "expertise_areas": expertise_areas,
                        "active_platforms": active_platforms
                    }
                    st.success("✅ Profile created successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields marked with *")
    
    else:
        # Main dashboard
        profile = st.session_state.user_profile
        
        # Sidebar
        st.sidebar.title("🎯 Your Profile")
        st.sidebar.write(f"**{profile['name']}**")
        st.sidebar.write(f"Brand: {profile['brand_name']}")
        st.sidebar.write(f"Language: {profile['primary_language'].upper()}")
        st.sidebar.write(f"Platforms: {len(profile['active_platforms'])}")
        
        # Sidebar navigation
        st.sidebar.markdown("---")
        page = st.sidebar.selectbox(
            "Navigate to:",
            ["📊 Dashboard", "💬 Chat Assistant", "✍️ Create Content", "📈 Trend Analysis"]
        )
        
        if st.sidebar.button("🔄 Reset Profile"):
            st.session_state.user_profile = None
            st.rerun()
        
        # Main content based on selected page
        if page == "📊 Dashboard":
            render_dashboard(profile, agent, helpers)
        elif page == "💬 Chat Assistant":
            render_chat_interface(profile, agent, helpers)
        elif page == "✍️ Create Content":
            render_content_creation(profile, agent, helpers)
        elif page == "📈 Trend Analysis":
            render_trend_analysis(profile, agent, helpers)


def render_dashboard(profile, agent, helpers):
    """Render the main dashboard"""
    
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Platforms", len(profile['active_platforms']))
    
    with col2:
        st.metric("Content Created", len(st.session_state.content_pieces))
    
    with col3:
        st.metric("Expertise Areas", len(profile['expertise_areas']))
    
    with col4:
        st.metric("Chat Messages", len(st.session_state.chat_history))
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Analyze Current Trends", use_container_width=True, type="primary"):
            with st.spinner("Analyzing trends with Apify..."):
                if agent:
                    trends = run_async(agent.analyze_trends_with_apify(profile))
                    st.session_state.current_trends = trends
                    st.success("✅ Trends analyzed!")
                    st.rerun()
    
    with col2:
        if st.button("💬 Start Chat Session", use_container_width=True):
            st.session_state.page = "💬 Chat Assistant"
            st.rerun()
    
    with col3:
        if st.button("✍️ Create Content Now", use_container_width=True):
            st.session_state.page = "✍️ Create Content"
            st.rerun()
    
    # Show current trends if available
    if st.session_state.current_trends and helpers:
        st.markdown("## 📈 Current Trends Summary")
        # Use simple Python utility instead of DSPy for trend summary
        trend_summary = helpers['trend_processor'].summarize_trends(
            st.session_state.current_trends.get('trending_topics', [])
        )
        st.markdown(trend_summary)
    
    # Recent content
    if st.session_state.content_pieces:
        st.markdown("## 📝 Recent Content")
        
        for content in st.session_state.content_pieces[-3:]:  # Show last 3
            with st.expander(f"📱 {content['platform'].title()} - {content['topic']} ({content['created_at']})"):
                st.write("**Content:**")
                st.write(content['text'])
                
                if content.get('hashtags'):
                    st.write("**Hashtags:**", " ".join(content['hashtags']))
                
                if st.button("📋 Copy Content", key=f"copy_dash_{content['id']}"):
                    st.code(content['text'])


def render_chat_interface(profile, agent, helpers):
    """Render the enhanced chat interface with DSPy conversation management"""
    
    st.markdown("## 💬 Chat with Your Content Marketing Assistant")
    st.markdown("Ask me anything about content strategy, trends, or social media marketing!")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Assistant:** {message['content']}")
            st.markdown("---")
    
    # Chat input
    user_input = st.text_input(
        "Ask me anything:",
        placeholder="e.g., 'What content should I post today?' or 'How can I improve engagement?'",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        send_button = st.button("Send", type="primary")
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate response using DSPy conversation management
        with st.spinner("Thinking..."):
            if agent and helpers:
                try:
                    # Use DSPy for intelligent response generation
                    response = run_async(agent.chat_response(
                        user_input, 
                        profile, 
                        st.session_state.chat_history
                    ))
                    
                    # Use simple utility to extract intent for follow-up suggestions
                    intent = helpers['conversation_helper'].extract_intent(user_input)
                    follow_ups = helpers['conversation_helper'].generate_follow_up_questions(intent, profile)
                    
                    # Add follow-up suggestions to response
                    if follow_ups:
                        response += f"\n\n**💡 You might also want to ask:**\n"
                        for i, question in enumerate(follow_ups[:2], 1):
                            response += f"{i}. {question}\n"
                    
                except Exception as e:
                    response = helpers['conversation_helper'].generate_fallback_response(user_input, profile) if helpers else f"I understand you're asking about: {user_input}\n\nBased on your expertise, I'd recommend creating authentic content that showcases your knowledge."
            else:
                response = "I'm here to help with your content marketing! Let me know what you'd like to create or discuss."
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        st.rerun()
    
    # Quick action buttons
    st.markdown("### 🎯 Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What should I post today?"):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': "What should I post today?",
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
    
    with col2:
        if st.button("How to improve engagement?"):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': "How can I improve my social media engagement?",
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
    
    with col3:
        if st.button("Best posting times?"):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': "What are the best times to post on social media?",
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()


def render_content_creation(profile, agent, helpers):
    """Render the enhanced content creation interface with DSPy and utilities"""
    
    st.markdown("## ✍️ AI-Powered Content Creation")
    st.markdown("Create trend-aware, culturally-relevant content using real-time data analysis")
    
    # Show current trends first
    if not st.session_state.current_trends:
        st.info("💡 **Tip:** Analyze current trends first for better content recommendations!")
        if st.button("📈 Analyze Trends Now", type="primary"):
            with st.spinner("Analyzing trends with Apify..."):
                if agent:
                    trends = run_async(agent.analyze_trends_with_apify(profile))
                    st.session_state.current_trends = trends
                    st.success("✅ Trends analyzed!")
                    st.rerun()
    else:
        st.success("✅ Using current trend data for content creation")
        
        # Show trend summary using simple utility
        with st.expander("📈 Current Trends Summary"):
            if helpers:
                trend_summary = helpers['trend_processor'].summarize_trends(
                    st.session_state.current_trends.get('trending_topics', [])
                )
                st.markdown(trend_summary)
        
    # Content creation form
    with st.form("enhanced_content_creation"):
        col1, col2 = st.columns(2)
        
        with col1:
            platform = st.selectbox(
                "Target Platform",
                options=profile['active_platforms'],
                format_func=lambda x: x.title()
            )
            
            content_type = st.selectbox(
                "Content Type",
                options=["educational", "motivational", "promotional", "entertainment"]
            )
        
        with col2:
            topic = st.text_input("Topic (Optional)", placeholder="Leave blank for trend-based suggestion")
            
            language = st.selectbox(
                "Language",
                options=["en", "fr", "bilingual"],
                format_func=lambda x: {"en": "English", "fr": "French", "bilingual": "Both"}[x]
            )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            use_trends = st.checkbox("Use current trend data", value=True)
            include_cta = st.checkbox("Include call-to-action", value=True)
            cultural_adaptation = st.checkbox("Apply cultural adaptation", value=True)
        
        create_content = st.form_submit_button("🚀 Generate AI Content", type="primary")
        
        if create_content:
            with st.spinner("Creating trend-aware content with DSPy..."):
                if agent and use_trends:
                    try:
                        # Use DSPy agent for advanced content generation
                        content_result = run_async(agent.generate_content_with_trends(
                            profile, platform, content_type, language, topic
                        ))
                        
                        # Use simple utilities to format and enhance content
                        if helpers:
                            # Add cultural hashtags using utility
                            hashtags = content_result.get('hashtags', [])
                            hashtags = helpers['formatter'].add_cultural_hashtags(
                                hashtags, profile.get('cultural_background', 'cameroon'), language
                            )
                            
                            # Optimize hashtags for platform
                            hashtags = helpers['optimizer'].optimize_hashtags_for_platform(hashtags, platform)
                            
                            # Format content piece using utility
                            content_piece = helpers['formatter'].format_content_piece({
                                "platform": platform,
                                "content_type": content_type,
                                "language": language,
                                "text": content_result['content_text'],
                                "hashtags": hashtags,
                                "call_to_action": content_result.get('call_to_action', ''),
                                "topic": topic or "AI Generated",
                                "trend_based": True
                            })
                            
                            # Add DSPy-generated insights
                            content_piece.update({
                                "strategy": content_result.get('strategy', ''),
                                "engagement_tactics": content_result.get('engagement_tactics', ''),
                                "trending_topics": content_result.get('trending_topics', ''),
                                "cultural_insights": content_result.get('cultural_insights', '')
                            })
                        else:
                            # Fallback formatting
                            content_piece = {
                                "id": f"content_{len(st.session_state.content_pieces) + 1}",
                                "platform": platform,
                                "content_type": content_type,
                                "language": language,
                                "text": content_result['content_text'],
                                "hashtags": content_result.get('hashtags', []),
                                "call_to_action": content_result.get('call_to_action', ''),
                                "topic": topic or "AI Generated",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "trend_based": True
                            }
                        
                        st.session_state.content_pieces.append(content_piece)
                        st.success("✅ AI-powered content created with trend analysis!")
                        
                        # Show additional insights
                        st.markdown("### 📊 Content Insights")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Strategy Used:**")
                            st.write(content_result.get('strategy', 'Standard content strategy'))
                            
                            if content_result.get('engagement_tactics'):
                                st.markdown("**Engagement Tactics:**")
                                st.write(content_result.get('engagement_tactics', ''))
                        
                        with col2:
                            st.markdown("**Trending Elements:**")
                            st.write(content_result.get('trending_topics', 'General trending topics'))
                            
                            if content_result.get('cultural_insights'):
                                st.markdown("**Cultural Insights:**")
                                st.write(content_result.get('cultural_insights', ''))
                        
                        # Show platform best practices
                        if helpers:
                            with st.expander("📱 Platform Best Practices"):
                                practices = helpers['optimizer'].get_platform_best_practices(platform)
                                for key, value in practices.items():
                                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                        
                    except Exception as e:
                        st.error(f"DSPy generation failed: {str(e)}")
                        # Fallback to simple generation
                        create_simple_content(profile, platform, content_type, language, topic, helpers)
                else:
                    # Simple content generation
                    create_simple_content(profile, platform, content_type, language, topic, helpers)


def create_simple_content(profile, platform, content_type, language, topic, helpers=None):
    """Fallback simple content creation with utility enhancements"""
    
    expertise = profile['expertise_areas'][0] if profile['expertise_areas'] else "Personal Development"
    name = profile['name']
    
    templates = {
        "educational": {
            "en": f"🎯 {topic or 'Success'} Tips from {name}\n\nAs a {expertise.lower()} expert, here's what I've learned:\n\n✨ Focus on progress, not perfection\n✨ Consistency beats intensity\n✨ Your mindset shapes your reality\n\nWhat's your biggest challenge right now? 👇",
            "fr": f"🎯 Conseils {topic or 'Succès'} de {name}\n\nEn tant qu'expert en {expertise.lower()}, voici ce que j'ai appris:\n\n✨ Concentrez-vous sur le progrès, pas la perfection\n✨ La cohérence bat l'intensité\n✨ Votre état d'esprit façonne votre réalité\n\nQuel est votre plus grand défi en ce moment? 👇"
        },
        "motivational": {
            "en": f"🌟 Monday Motivation from {name}!\n\nRemember: Every expert was once a beginner.\n\nYour current struggles are building your future strength. 💪\n\nWhat's one small step you're taking today? 👇",
            "fr": f"🌟 Motivation du lundi de {name}!\n\nRappelez-vous: Chaque expert était autrefois débutant.\n\nVos difficultés actuelles construisent votre force future. 💪\n\nQuelle petite étape prenez-vous aujourd'hui? 👇"
        }
    }
    
    content_template = templates.get(content_type, templates["educational"])
    content_text = content_template.get(language, content_template["en"])
    
    # Handle bilingual
    if language == 'bilingual':
        en_content = content_template["en"]
        fr_content = content_template["fr"]
        content_text = f"{en_content}\n\n---\n\n{fr_content}"
    
    hashtags = [f"#{expertise.replace(' ', '')}", "#Success", "#Motivation"]
    
    # Use utilities if available
    if helpers:
        # Add cultural hashtags using utility
        hashtags = helpers['formatter'].add_cultural_hashtags(
            hashtags, profile.get('cultural_background', 'cameroon'), language
        )
        
        # Optimize for platform
        hashtags = helpers['optimizer'].optimize_hashtags_for_platform(hashtags, platform)
        
        # Format content piece using utility
        content_piece = helpers['formatter'].format_content_piece({
            "platform": platform,
            "content_type": content_type,
            "language": language,
            "text": content_text,
            "hashtags": hashtags,
            "call_to_action": "Share your thoughts in the comments!",
            "topic": topic or "Simple Content",
            "trend_based": False
        })
    else:
        # Fallback formatting
        if profile.get('cultural_background') == 'cameroon':
            hashtags.extend(["#CameroonPride", "#AfricanWisdom"])
        
        content_piece = {
            "id": f"content_{len(st.session_state.content_pieces) + 1}",
            "platform": platform,
            "content_type": content_type,
            "language": language,
            "text": content_text,
            "hashtags": hashtags,
            "call_to_action": "Share your thoughts in the comments!",
            "topic": topic or "Simple Content",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "trend_based": False
        }
    
    st.session_state.content_pieces.append(content_piece)
    st.success("✅ Content created successfully!")


def render_trend_analysis(profile, agent, helpers):
    """Render the trend analysis interface with DSPy analysis and utility processing"""
    
    st.markdown("## 📈 Real-Time Trend Analysis")
    st.markdown("Powered by Apify for accurate, up-to-date social media insights")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🔄 Refresh Trend Analysis", type="primary", use_container_width=True):
            with st.spinner("Analyzing trends across platforms..."):
                if agent:
                    trends = run_async(agent.analyze_trends_with_apify(profile))
                    st.session_state.current_trends = trends
                    st.success("✅ Trends updated!")
                    st.rerun()
    
    with col2:
        if st.session_state.current_trends:
            last_update = st.session_state.current_trends.get('analysis_timestamp', 'Unknown')
            st.info(f"Last updated: {last_update[:16] if last_update != 'Unknown' else 'Unknown'}")
    
    if st.session_state.current_trends:
        trends = st.session_state.current_trends
        
        # Trending Topics
        st.markdown("### 🔥 Trending Topics")
        
        trending_topics = trends.get('trending_topics', [])
        
        # Use utility to filter and process trends
        if helpers and trending_topics:
            # Filter relevant trends using utility
            relevant_trends = helpers['trend_processor'].filter_relevant_trends(
                trending_topics, profile, min_relevance=1.0
            )
            
            for i, topic in enumerate(relevant_trends[:5], 1):
                with st.expander(f"{i}. {topic.get('topic', 'Unknown Topic')} ({topic.get('platform', 'general')})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Engagement Score", f"{topic.get('engagement_score', 0):.1f}%")
                    
                    with col2:
                        st.metric("Relevance Score", f"{topic.get('relevance_score', 0):.1f}/10")
                    
                    with col3:
                        if st.button(f"Create Content", key=f"create_{i}"):
                            # Pre-fill content creation with this topic
                            st.session_state.suggested_topic = topic.get('topic', '')
                            st.info(f"💡 Topic '{topic.get('topic', '')}' saved! Go to Create Content to use it.")
                    
                    # Show why this trend is relevant
                    if topic.get('relevance_score', 0) > 5:
                        st.success(f"🎯 High relevance to your {', '.join(profile.get('expertise_areas', []))} expertise")
        elif trending_topics:
            # Fallback display without utility processing
            for i, topic in enumerate(trending_topics[:5], 1):
                with st.expander(f"{i}. {topic.get('topic', 'Unknown Topic')} ({topic.get('platform', 'general')})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Engagement Score", f"{topic.get('engagement_score', 0):.1f}%")
                    
                    with col2:
                        st.metric("Relevance Score", f"{topic.get('relevance_score', 0):.1f}/10")
                    
                    if st.button(f"Create Content About This", key=f"create_{i}"):
                        st.session_state.suggested_topic = topic.get('topic', '')
                        st.info(f"💡 Topic '{topic.get('topic', '')}' saved!")
        
        # Content Opportunities
        st.markdown("### 💡 Content Opportunities")
        
        opportunities = trends.get('content_opportunities', [])
        if opportunities:
            for i, opp in enumerate(opportunities[:3], 1):
                st.markdown(f"**{i}. {opp.get('topic', 'Content Idea')}**")
                st.write(f"📊 Engagement Potential: {opp.get('engagement_potential', 0):.1f}%")
                st.write(f"💡 Approach: {opp.get('suggested_approach', 'Create engaging content')}")
                st.markdown("---")
        
        # Data Sources
        st.markdown("### 📊 Data Sources")
        
        data_sources = trends.get('data_sources', {})
        if data_sources:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Instagram Posts", data_sources.get('instagram_posts_count', 0))
            
            with col2:
                st.metric("TikTok Videos", data_sources.get('tiktok_videos_count', 0))
            
            with col3:
                st.metric("YouTube Videos", data_sources.get('youtube_videos_count', 0))
            
            with col4:
                st.metric("Google Trends", data_sources.get('google_trends_count', 0))
    
    else:
        st.info("No trend data available. Click 'Refresh Trend Analysis' to get started!")
        
        # Show what trend analysis provides
        st.markdown("### 🎯 What You'll Get:")
        st.markdown("""
        - **Real-time trending topics** from Instagram, TikTok, YouTube
        - **Engagement predictions** for your content ideas
        - **Cultural relevance scoring** for Cameroonian audience
        - **Optimal posting times** based on your audience
        - **Content opportunities** with high viral potential
        - **Competitor insights** and successful content patterns
        """)
        
        # Display created content
        if st.session_state.content_pieces:
            st.markdown("## 📝 Your Content")
            
            for i, content in enumerate(reversed(st.session_state.content_pieces[-5:])):  # Show last 5
                with st.expander(f"📱 {content['platform'].title()} - {content['topic']} ({content['created_at']})"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.text_area(
                            "Content",
                            value=content['text'],
                            height=200,
                            key=f"content_{content['id']}"
                        )
                    
                    with col2:
                        st.write("**Platform:**", content['platform'].title())
                        st.write("**Type:**", content['content_type'].title())
                        st.write("**Language:**", content['language'].upper())
                        
                        if st.button("📋 Copy", key=f"copy_{content['id']}"):
                            st.code(content['text'])
        
        # Tips section
        st.markdown("## 💡 Tips for Success")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("""
            **Content Creation Tips:**
            - Post consistently on your chosen platforms
            - Engage with your audience's comments
            - Use relevant hashtags for your niche
            - Share personal stories and experiences
            """)
        
        with tips_col2:
            st.markdown("""
            **Cultural Considerations:**
            - Respect local customs and values
            - Use appropriate greetings for your audience
            - Consider time zones for posting
            - Adapt content for bilingual audiences
            """)

if __name__ == "__main__":
    main()