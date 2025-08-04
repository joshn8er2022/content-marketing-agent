#!/usr/bin/env python3
"""
Content Marketing Agent - Streamlit App
AI-powered content creation assistant for culturally-aware, trend-driven social media marketing
"""

import streamlit as st
import os
from datetime import datetime

# For Streamlit Cloud deployment, get API keys from secrets
def get_api_key(key_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        return st.secrets[key_name]
    except:
        return os.getenv(key_name, "")

# Simple content generation without complex imports
def generate_content(profile, platform, content_type, topic, language):
    """Generate content based on user inputs"""
    
    # Content templates based on type
    templates = {
        "educational": {
            "en": "🎯 {topic} Tips for {expertise}\n\nHere's what I've learned from helping clients:\n\n✨ Tip 1: Start with clarity - know exactly what you want\n✨ Tip 2: Take consistent action daily\n✨ Tip 3: Surround yourself with supportive people\n\nYour journey is unique! 💪\n\nWhat's your biggest challenge? Share below! 👇",
            "fr": "🎯 Conseils {topic} pour {expertise}\n\nVoici ce que j'ai appris en aidant mes clients:\n\n✨ Conseil 1: Commencez par la clarté - sachez ce que vous voulez\n✨ Conseil 2: Prenez des mesures cohérentes quotidiennement\n✨ Conseil 3: Entourez-vous de personnes qui vous soutiennent\n\nVotre parcours est unique! 💪\n\nQuel est votre plus grand défi? Partagez ci-dessous! 👇"
        },
        "motivational": {
            "en": "🌟 Monday Motivation for {expertise}!\n\nRemember: Every expert was once a beginner.\n\nYour current struggles are building your future strength. 💪\n\nIn our community, we believe in:\n✨ Progress over perfection\n✨ Growth through challenges\n✨ Supporting each other's journey\n\nWhat's one small step you're taking today? 👇",
            "fr": "🌟 Motivation du lundi pour {expertise}!\n\nRappelez-vous: Chaque expert était autrefois débutant.\n\nVos difficultés actuelles construisent votre force future. 💪\n\nDans notre communauté, nous croyons en:\n✨ Le progrès plutôt que la perfection\n✨ La croissance à travers les défis\n✨ Le soutien mutuel dans notre parcours\n\nQuelle petite étape prenez-vous aujourd'hui? 👇"
        },
        "promotional": {
            "en": "🎯 Ready to transform your {expertise_lower}?\n\nI'm here to help you:\n✅ Overcome your biggest challenges\n✅ Create lasting positive change\n✅ Build the life you truly want\n\nWith years of experience helping people like you, I understand your journey.\n\n💬 DM me 'READY' to start your transformation!\n\n#Transformation #{expertise_tag}",
            "fr": "🎯 Prêt(e) à transformer votre {expertise_lower}?\n\nJe suis là pour vous aider à:\n✅ Surmonter vos plus grands défis\n✅ Créer un changement positif durable\n✅ Construire la vie que vous voulez vraiment\n\nAvec des années d'expérience aidant des gens comme vous, je comprends votre parcours.\n\n💬 Envoyez-moi 'PRÊT' pour commencer votre transformation!\n\n#Transformation #{expertise_tag}"
        },
        "entertainment": {
            "en": "😄 Fun fact about {expertise}:\n\nDid you know that small daily habits create 80% of your results?\n\nIt's like building a house - one brick at a time! 🏠\n\nHere's my favorite simple habit:\n{topic} for just 5 minutes every morning.\n\nWhat's your favorite simple habit? Share below! 👇\n\n#{expertise_tag} #SmallHabits #BigResults",
            "fr": "😄 Fait amusant sur {expertise}:\n\nSaviez-vous que les petites habitudes quotidiennes créent 80% de vos résultats?\n\nC'est comme construire une maison - une brique à la fois! 🏠\n\nVoici ma simple habitude préférée:\n{topic} pendant seulement 5 minutes chaque matin.\n\nQuelle est votre habitude simple préférée? Partagez ci-dessous! 👇\n\n#{expertise_tag} #PetitesHabitudes #GrandsRésultats"
        }
    }
    
    # Get template
    template = templates.get(content_type, templates["educational"])
    content_template = template.get(language, template["en"])
    
    # Fill in variables
    expertise = profile['expertise_areas'][0] if profile['expertise_areas'] else "Personal Development"
    expertise_lower = expertise.lower()
    expertise_tag = expertise.replace(' ', '')
    topic_text = topic or "Success"
    
    content = content_template.format(
        topic=topic_text,
        expertise=expertise,
        expertise_lower=expertise_lower,
        expertise_tag=expertise_tag
    )
    
    # Add cultural elements for Cameroon
    if profile.get('cultural_background') == 'cameroon':
        cultural_hashtags = {
            "en": ["#CameroonPride", "#AfricanWisdom", "#CommunityFirst"],
            "fr": ["#FiertéCamerounaise", "#SagesseAfricaine", "#CommunautéDAbord"]
        }
        
        hashtags = cultural_hashtags.get(language, cultural_hashtags["en"])
        content += f"\n\n{' '.join(hashtags[:2])}"
    
    # Add platform-specific hashtags
    platform_hashtags = {
        "instagram": ["#InstaMotivation", "#SelfImprovement"],
        "tiktok": ["#MotivationTok", "#SelfGrowth"],
        "linkedin": ["#ProfessionalDevelopment", "#Leadership"],
        "facebook": ["#Motivation", "#PersonalGrowth"],
        "youtube": ["#SelfImprovement", "#MotivationalContent"]
    }
    
    if platform in platform_hashtags:
        content += f" {' '.join(platform_hashtags[platform][:2])}"
    
    return content

def main():
    """Main Streamlit app"""
    
    st.set_page_config(
        page_title="Content Marketing Agent",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Content Marketing Agent")
    st.markdown("*Your AI-powered content creation assistant for culturally-aware, trend-driven social media marketing*")
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'content_pieces' not in st.session_state:
        st.session_state.content_pieces = []
    
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
        
        if st.sidebar.button("🔄 Reset Profile"):
            st.session_state.user_profile = None
            st.rerun()
        
        # Main content
        st.markdown("## 📊 Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Platforms", len(profile['active_platforms']))
        
        with col2:
            st.metric("Content Created", len(st.session_state.content_pieces))
        
        with col3:
            st.metric("Expertise Areas", len(profile['expertise_areas']))
        
        # Content creation section
        st.markdown("## ✍️ Create Content")
        
        with st.form("content_creation"):
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
                topic = st.text_input("Topic (Optional)", placeholder="Leave blank for AI suggestion")
                
                language = st.selectbox(
                    "Language",
                    options=["en", "fr", "bilingual"],
                    format_func=lambda x: {"en": "English", "fr": "French", "bilingual": "Both"}[x]
                )
            
            create_content = st.form_submit_button("🚀 Generate Content", type="primary")
            
            if create_content:
                with st.spinner("Creating content..."):
                    try:
                        # Generate content using our simple function
                        content_text = generate_content(profile, platform, content_type, topic, language)
                        
                        # Handle bilingual content
                        if language == 'bilingual':
                            # Create both English and French versions
                            en_content = generate_content(profile, platform, content_type, topic, 'en')
                            fr_content = generate_content(profile, platform, content_type, topic, 'fr')
                            content_text = f"{en_content}\n\n---\n\n{fr_content}"
                        
                        # Create content piece
                        content_piece = {
                            "id": f"content_{len(st.session_state.content_pieces) + 1}",
                            "platform": platform,
                            "content_type": content_type,
                            "language": language,
                            "text": content_text,
                            "topic": topic or "AI Generated",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        
                        st.session_state.content_pieces.append(content_piece)
                        st.success("✅ Content created successfully!")
                        
                    except Exception as e:
                        st.error(f"Error creating content: {str(e)}")
                        # Simple fallback
                        content_text = f"🎯 {topic or 'Success Tips'}\n\nFocus on progress, not perfection! 💪\n\n#{profile['expertise_areas'][0].replace(' ', '') if profile['expertise_areas'] else 'Success'}"
                        
                        content_piece = {
                            "id": f"content_{len(st.session_state.content_pieces) + 1}",
                            "platform": platform,
                            "content_type": content_type,
                            "language": language,
                            "text": content_text,
                            "topic": topic or "Simple",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        
                        st.session_state.content_pieces.append(content_piece)
                        st.success("✅ Content created successfully!")
        
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