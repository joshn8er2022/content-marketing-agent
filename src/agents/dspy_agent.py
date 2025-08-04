"""
DSPy-powered Content Marketing Agent with real trend analysis
"""

import dspy
from typing import Dict, List, Optional, Any
import asyncio
import json
from datetime import datetime
import streamlit as st

# DSPy Signatures for the agent
class TrendAnalyzer(dspy.Signature):
    """Analyze current social media trends and identify content opportunities"""
    
    user_interests: str = dspy.InputField(desc="User's expertise areas and interests")
    cultural_context: str = dspy.InputField(desc="Cultural background (e.g., Cameroonian, bilingual)")
    platform: str = dspy.InputField(desc="Target social media platform")
    raw_trend_data: str = dspy.InputField(desc="Raw trend data from social media platforms")
    
    trending_topics: str = dspy.OutputField(desc="Top 5 trending topics relevant to user")
    content_opportunities: str = dspy.OutputField(desc="Specific content ideas with high engagement potential")
    optimal_timing: str = dspy.OutputField(desc="Best posting times and frequency recommendations")


class ContentStrategist(dspy.Signature):
    """Generate personalized content strategy based on trends and user profile"""
    
    user_profile: str = dspy.InputField(desc="User's brand, expertise, and target audience")
    trending_topics: str = dspy.InputField(desc="Current trending topics relevant to user")
    content_type: str = dspy.InputField(desc="Type of content to create (educational, motivational, etc.)")
    platform: str = dspy.InputField(desc="Target platform specifications")
    
    content_strategy: str = dspy.OutputField(desc="Detailed content strategy with hooks and messaging")
    target_outcome: str = dspy.OutputField(desc="Expected engagement and business outcomes")
    key_messages: str = dspy.OutputField(desc="Core messages to communicate")


class BilingualContentCreator(dspy.Signature):
    """Create engaging bilingual content optimized for specific platforms"""
    
    content_strategy: str = dspy.InputField(desc="Content strategy and key messages")
    language: str = dspy.InputField(desc="Target language (en, fr, or bilingual)")
    platform: str = dspy.InputField(desc="Platform specifications and requirements")
    cultural_context: str = dspy.InputField(desc="Cultural adaptation requirements")
    trending_elements: str = dspy.InputField(desc="Trending hashtags, topics, or formats to incorporate")
    
    content_text: str = dspy.OutputField(desc="Complete content with captions and descriptions")
    hashtags: str = dspy.OutputField(desc="Relevant hashtags optimized for platform and culture")
    call_to_action: str = dspy.OutputField(desc="Compelling call-to-action based on business goals")


class ChatAssistant(dspy.Signature):
    """Provide helpful responses about content marketing and social media strategy"""
    
    user_message: str = dspy.InputField(desc="User's question or request")
    user_context: str = dspy.InputField(desc="User's profile and previous conversation context")
    current_trends: str = dspy.InputField(desc="Current trending topics and opportunities")
    
    response: str = dspy.OutputField(desc="Helpful, actionable response with specific recommendations")
    suggested_actions: str = dspy.OutputField(desc="Specific next steps the user can take")


class DSPyContentAgent:
    """Main DSPy-powered content marketing agent"""
    
    def __init__(self):
        # Initialize DSPy with OpenAI
        openai_key = self._get_api_key("OPENAI_API_KEY")
        if openai_key:
            dspy.settings.configure(lm=dspy.OpenAI(model="gpt-3.5-turbo", api_key=openai_key))
        
        # Initialize DSPy modules
        self.trend_analyzer = dspy.ChainOfThought(TrendAnalyzer)
        self.content_strategist = dspy.ChainOfThought(ContentStrategist)
        self.content_creator = dspy.ChainOfThought(BilingualContentCreator)
        self.chat_assistant = dspy.ChainOfThought(ChatAssistant)
        
        # Cache for trends to avoid repeated API calls
        self.trends_cache = {}
        self.cache_timestamp = None
    
    def _get_api_key(self, key_name: str) -> str:
        """Get API key from Streamlit secrets or environment"""
        try:
            return st.secrets[key_name]
        except:
            import os
            return os.getenv(key_name, "")
    
    async def analyze_trends_with_apify(self, user_profile: Dict) -> Dict[str, Any]:
        """Analyze trends using Apify data"""
        
        # Check cache first (cache for 30 minutes)
        current_time = datetime.now()
        if (self.cache_timestamp and 
            (current_time - self.cache_timestamp).seconds < 1800 and
            self.trends_cache):
            return self.trends_cache
        
        try:
            from ..api.apify_integration import ApifyTrendAnalyzer
            
            # Initialize Apify analyzer
            apify_analyzer = ApifyTrendAnalyzer()
            
            # Get trend data
            trend_data = await apify_analyzer.comprehensive_trend_analysis(
                user_interests=user_profile.get('expertise_areas', []),
                expertise_areas=user_profile.get('expertise_areas', []),
                cultural_context=user_profile.get('cultural_background', 'cameroon')
            )
            
            # Cache the results
            self.trends_cache = trend_data
            self.cache_timestamp = current_time
            
            return trend_data
            
        except Exception as e:
            st.warning(f"Apify trend analysis unavailable: {str(e)}")
            # Fallback to simulated trend data
            return self._get_fallback_trends(user_profile)
    
    def _get_fallback_trends(self, user_profile: Dict) -> Dict[str, Any]:
        """Fallback trend data when Apify is unavailable"""
        
        expertise = user_profile.get('expertise_areas', ['Personal Development'])[0]
        
        return {
            "trending_topics": [
                {
                    "topic": f"{expertise} Tips",
                    "platform": "instagram",
                    "engagement_score": 85.0,
                    "relevance_score": 9.2
                },
                {
                    "topic": "Monday Motivation",
                    "platform": "tiktok", 
                    "engagement_score": 92.0,
                    "relevance_score": 8.8
                },
                {
                    "topic": "Success Mindset",
                    "platform": "linkedin",
                    "engagement_score": 78.0,
                    "relevance_score": 9.0
                }
            ],
            "content_opportunities": [
                {
                    "topic": f"5 {expertise} Mistakes to Avoid",
                    "engagement_potential": 88.5,
                    "suggested_approach": "Educational carousel post with personal examples"
                },
                {
                    "topic": "Behind the Scenes: My Daily Routine",
                    "engagement_potential": 82.3,
                    "suggested_approach": "Authentic video showing your process"
                }
            ],
            "optimal_timing": {
                "instagram": ["Tuesday-Thursday: 11 AM - 1 PM", "Evening: 7 PM - 9 PM"],
                "tiktok": ["Tuesday-Thursday: 6 AM - 10 AM", "Weekend: 9 AM - 12 PM"]
            }
        }
    
    async def generate_content_with_trends(
        self, 
        user_profile: Dict, 
        platform: str, 
        content_type: str, 
        language: str,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate content using real trend analysis"""
        
        try:
            # Get current trends
            trend_data = await self.analyze_trends_with_apify(user_profile)
            
            # Prepare inputs for DSPy
            user_interests = ", ".join(user_profile.get('expertise_areas', []))
            cultural_context = f"{user_profile.get('cultural_background', 'cameroon')}, {language}"
            
            # Convert trend data to string for DSPy
            trending_topics_str = json.dumps(trend_data.get('trending_topics', [])[:3], indent=2)
            
            # Step 1: Analyze trends
            trend_analysis = self.trend_analyzer(
                user_interests=user_interests,
                cultural_context=cultural_context,
                platform=platform,
                raw_trend_data=trending_topics_str
            )
            
            # Step 2: Create content strategy
            user_profile_str = f"""
            Name: {user_profile.get('name', 'Content Creator')}
            Brand: {user_profile.get('brand_name', 'Personal Brand')}
            Expertise: {user_interests}
            Cultural Background: {user_profile.get('cultural_background', 'cameroon')}
            Target Audience: Professionals interested in {user_interests}
            """
            
            strategy = self.content_strategist(
                user_profile=user_profile_str,
                trending_topics=trend_analysis.trending_topics,
                content_type=content_type,
                platform=platform
            )
            
            # Step 3: Create content
            trending_elements = f"""
            Trending Topics: {trend_analysis.trending_topics}
            Content Opportunities: {trend_analysis.content_opportunities}
            Optimal Timing: {trend_analysis.optimal_timing}
            """
            
            content = self.content_creator(
                content_strategy=strategy.content_strategy,
                language=language,
                platform=platform,
                cultural_context=cultural_context,
                trending_elements=trending_elements
            )
            
            return {
                "content_text": content.content_text,
                "hashtags": content.hashtags.split() if content.hashtags else [],
                "call_to_action": content.call_to_action,
                "strategy": strategy.content_strategy,
                "trending_topics": trend_analysis.trending_topics,
                "optimal_timing": trend_analysis.optimal_timing,
                "trend_data": trend_data
            }
            
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            # Fallback to simple content generation
            return self._generate_fallback_content(user_profile, platform, content_type, language, topic)
    
    def _generate_fallback_content(
        self, 
        user_profile: Dict, 
        platform: str, 
        content_type: str, 
        language: str,
        topic: Optional[str]
    ) -> Dict[str, Any]:
        """Fallback content generation when DSPy fails"""
        
        expertise = user_profile.get('expertise_areas', ['Personal Development'])[0]
        name = user_profile.get('name', 'Content Creator')
        
        templates = {
            "educational": {
                "en": f"🎯 {topic or 'Success'} Tips from {name}\n\nAs a {expertise.lower()} expert, here's what I've learned:\n\n✨ Focus on progress, not perfection\n✨ Consistency beats intensity\n✨ Your mindset shapes your reality\n\nWhat's your biggest challenge right now? 👇",
                "fr": f"🎯 Conseils {topic or 'Succès'} de {name}\n\nEn tant qu'expert en {expertise.lower()}, voici ce que j'ai appris:\n\n✨ Concentrez-vous sur le progrès, pas la perfection\n✨ La cohérence bat l'intensité\n✨ Votre état d'esprit façonne votre réalité\n\nQuel est votre plus grand défi en ce moment? 👇"
            }
        }
        
        content_template = templates.get(content_type, templates["educational"])
        content_text = content_template.get(language, content_template["en"])
        
        hashtags = [f"#{expertise.replace(' ', '')}", "#Success", "#Motivation"]
        if user_profile.get('cultural_background') == 'cameroon':
            hashtags.extend(["#CameroonPride", "#AfricanWisdom"])
        
        return {
            "content_text": content_text,
            "hashtags": hashtags,
            "call_to_action": "Share your thoughts in the comments!",
            "strategy": f"Educational content about {expertise} with personal touch",
            "trending_topics": f"Current focus on {expertise} and personal development",
            "optimal_timing": "Post during peak engagement hours for your audience"
        }
    
    async def chat_response(
        self, 
        user_message: str, 
        user_profile: Dict, 
        conversation_history: List[Dict]
    ) -> str:
        """Generate chat response using DSPy"""
        
        try:
            # Get current trends for context
            trend_data = await self.analyze_trends_with_apify(user_profile)
            
            # Prepare context
            user_context = f"""
            User Profile:
            - Name: {user_profile.get('name', 'User')}
            - Expertise: {', '.join(user_profile.get('expertise_areas', []))}
            - Platforms: {', '.join(user_profile.get('active_platforms', []))}
            - Cultural Background: {user_profile.get('cultural_background', 'cameroon')}
            
            Recent Conversation:
            {json.dumps(conversation_history[-3:], indent=2) if conversation_history else 'No previous conversation'}
            """
            
            current_trends = json.dumps(trend_data.get('trending_topics', [])[:3], indent=2)
            
            # Generate response
            response = self.chat_assistant(
                user_message=user_message,
                user_context=user_context,
                current_trends=current_trends
            )
            
            return f"{response.response}\n\n**Suggested Actions:**\n{response.suggested_actions}"
            
        except Exception as e:
            # Fallback response
            return f"I understand you're asking about: {user_message}\n\nBased on your expertise in {', '.join(user_profile.get('expertise_areas', ['personal development']))}, I'd recommend focusing on creating authentic content that showcases your knowledge while connecting with your audience's needs.\n\nWould you like me to help you create some content around this topic?"
    
    def get_trend_summary(self, trend_data: Dict) -> str:
        """Get a formatted summary of current trends"""
        
        if not trend_data:
            return "No trend data available"
        
        summary = "📈 **Current Trends:**\n\n"
        
        trending_topics = trend_data.get('trending_topics', [])
        for i, topic in enumerate(trending_topics[:3], 1):
            summary += f"{i}. **{topic.get('topic', 'Unknown')}** ({topic.get('platform', 'general')})\n"
            summary += f"   Engagement: {topic.get('engagement_score', 0):.1f}% | Relevance: {topic.get('relevance_score', 0):.1f}/10\n\n"
        
        opportunities = trend_data.get('content_opportunities', [])
        if opportunities:
            summary += "💡 **Content Opportunities:**\n\n"
            for i, opp in enumerate(opportunities[:2], 1):
                summary += f"{i}. {opp.get('topic', 'Content Idea')}\n"
                summary += f"   Potential: {opp.get('engagement_potential', 0):.1f}%\n\n"
        
        return summary