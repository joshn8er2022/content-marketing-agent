"""
DSPy-powered Content Marketing Agent - Optimized Architecture
40-50% DSPy usage focusing on AI-heavy operations
"""

import dspy
from typing import Dict, List, Optional, Any
import asyncio
import json
from datetime import datetime
import streamlit as st

# Core DSPy Signatures - AI-Heavy Operations Only
class TrendAnalyzer(dspy.Signature):
    """Analyze social media trends and identify content opportunities"""
    
    user_profile: str = dspy.InputField(desc="User expertise, interests, and cultural context")
    raw_trend_data: str = dspy.InputField(desc="Raw trend data from social media platforms")
    platform_focus: str = dspy.InputField(desc="Primary social media platforms to analyze")
    
    trending_topics: str = dspy.OutputField(desc="Top 5 trending topics with relevance scores")
    content_opportunities: str = dspy.OutputField(desc="Specific content ideas with engagement predictions")
    cultural_insights: str = dspy.OutputField(desc="Cultural adaptation recommendations")


class ContentStrategist(dspy.Signature):
    """Generate comprehensive content strategy based on trends and user goals"""
    
    user_goals: str = dspy.InputField(desc="Business goals, target audience, and brand positioning")
    trending_insights: str = dspy.InputField(desc="Current trending topics and opportunities")
    content_type: str = dspy.InputField(desc="Desired content type and platform specifications")
    
    content_strategy: str = dspy.OutputField(desc="Detailed content strategy with hooks and messaging")
    engagement_tactics: str = dspy.OutputField(desc="Specific tactics to maximize engagement")
    success_metrics: str = dspy.OutputField(desc="Expected outcomes and KPIs")


class BilingualContentCreator(dspy.Signature):
    """Create engaging bilingual content optimized for cultural context"""
    
    strategy_brief: str = dspy.InputField(desc="Content strategy and key messaging points")
    language_requirements: str = dspy.InputField(desc="Language preferences and cultural context")
    platform_specs: str = dspy.InputField(desc="Platform requirements and best practices")
    trending_elements: str = dspy.InputField(desc="Trending hashtags, topics, or formats to incorporate")
    
    primary_content: str = dspy.OutputField(desc="Main content text optimized for engagement")
    secondary_content: str = dspy.OutputField(desc="Alternative language version if bilingual")
    hashtags_and_cta: str = dspy.OutputField(desc="Optimized hashtags and call-to-action")


class ConversationManager(dspy.Signature):
    """Manage intelligent conversations about content marketing strategy"""
    
    user_query: str = dspy.InputField(desc="User's question or request for assistance")
    conversation_context: str = dspy.InputField(desc="Previous conversation history and user profile")
    current_trends: str = dspy.InputField(desc="Latest trend data and content opportunities")
    
    response: str = dspy.OutputField(desc="Helpful, actionable response with specific recommendations")
    follow_up_questions: str = dspy.OutputField(desc="Suggested follow-up questions to deepen engagement")
    action_items: str = dspy.OutputField(desc="Specific next steps the user can take")


class ContentOptimizer(dspy.Signature):
    """Optimize existing content for better performance"""
    
    original_content: str = dspy.InputField(desc="Content to be optimized")
    performance_goals: str = dspy.InputField(desc="Desired improvements and target metrics")
    platform_context: str = dspy.InputField(desc="Platform-specific optimization requirements")
    
    optimized_content: str = dspy.OutputField(desc="Improved content with better engagement potential")
    optimization_rationale: str = dspy.OutputField(desc="Explanation of changes made and expected impact")
    ab_test_suggestions: str = dspy.OutputField(desc="Alternative versions for A/B testing")


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
    """Optimized DSPy-powered content marketing agent"""
    
    def __init__(self):
        # Initialize DSPy with OpenAI
        openai_key = self._get_api_key("OPENAI_API_KEY")
        if openai_key:
            dspy.settings.configure(lm=dspy.OpenAI(model="gpt-3.5-turbo", api_key=openai_key))
        
        # Initialize DSPy modules for AI-heavy operations only
        self.trend_analyzer = dspy.ChainOfThought(TrendAnalyzer)
        self.content_strategist = dspy.ChainOfThought(ContentStrategist)
        self.content_creator = dspy.ChainOfThought(BilingualContentCreator)
        self.conversation_manager = dspy.ChainOfThought(ConversationManager)
        self.content_optimizer = dspy.ChainOfThought(ContentOptimizer)
        
        # Simple Python for utilities and caching
        self.trends_cache = {}
        self.cache_timestamp = None
        self.conversation_cache = []
    
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
        """Generate content using DSPy pipeline with trend analysis"""
        
        try:
            # Step 1: Get trend data (simple Python utility)
            trend_data = await self.analyze_trends_with_apify(user_profile)
            
            # Step 2: DSPy Trend Analysis
            user_profile_str = self._format_user_profile(user_profile)
            trend_data_str = self._format_trend_data(trend_data)
            platform_focus = ", ".join(user_profile.get('active_platforms', [platform]))
            
            trend_analysis = self.trend_analyzer(
                user_profile=user_profile_str,
                raw_trend_data=trend_data_str,
                platform_focus=platform_focus
            )
            
            # Step 3: DSPy Content Strategy
            user_goals = self._format_user_goals(user_profile, content_type)
            
            strategy = self.content_strategist(
                user_goals=user_goals,
                trending_insights=trend_analysis.trending_topics,
                content_type=f"{content_type} for {platform}"
            )
            
            # Step 4: DSPy Content Creation
            language_requirements = self._format_language_requirements(language, user_profile)
            platform_specs = self._get_platform_specs(platform)
            trending_elements = self._format_trending_elements(trend_analysis)
            
            content = self.content_creator(
                strategy_brief=strategy.content_strategy,
                language_requirements=language_requirements,
                platform_specs=platform_specs,
                trending_elements=trending_elements
            )
            
            # Step 5: Parse and format results (simple Python)
            return self._format_content_result(content, strategy, trend_analysis, trend_data)
            
        except Exception as e:
            st.error(f"DSPy content generation failed: {str(e)}")
            return self._generate_fallback_content(user_profile, platform, content_type, language, topic)
    
    def _format_user_profile(self, user_profile: Dict) -> str:
        """Simple utility to format user profile for DSPy"""
        return f"""
        Name: {user_profile.get('name', 'Content Creator')}
        Brand: {user_profile.get('brand_name', 'Personal Brand')}
        Expertise: {', '.join(user_profile.get('expertise_areas', []))}
        Cultural Background: {user_profile.get('cultural_background', 'cameroon')}
        Primary Language: {user_profile.get('primary_language', 'en')}
        Active Platforms: {', '.join(user_profile.get('active_platforms', []))}
        """
    
    def _format_trend_data(self, trend_data: Dict) -> str:
        """Simple utility to format trend data for DSPy"""
        trending_topics = trend_data.get('trending_topics', [])[:5]
        return json.dumps({
            'trending_topics': trending_topics,
            'content_opportunities': trend_data.get('content_opportunities', [])[:3],
            'data_sources': trend_data.get('data_sources', {})
        }, indent=2)
    
    def _format_user_goals(self, user_profile: Dict, content_type: str) -> str:
        """Simple utility to format user goals for DSPy"""
        return f"""
        Content Type: {content_type}
        Business Goals: Lead generation and brand awareness
        Target Audience: {user_profile.get('cultural_background', 'cameroon')} professionals interested in {', '.join(user_profile.get('expertise_areas', []))}
        Brand Voice: Professional yet authentic, culturally aware
        Success Metrics: Engagement, shares, comments, lead generation
        """
    
    def _format_language_requirements(self, language: str, user_profile: Dict) -> str:
        """Simple utility to format language requirements for DSPy"""
        cultural_bg = user_profile.get('cultural_background', 'cameroon')
        return f"""
        Primary Language: {language}
        Cultural Context: {cultural_bg}
        Tone: Professional yet warm and authentic
        Cultural Adaptation: Include relevant cultural references and values
        Bilingual: {'Yes' if language == 'bilingual' else 'No'}
        """
    
    def _get_platform_specs(self, platform: str) -> str:
        """Simple utility to get platform specifications"""
        specs = {
            "instagram": "Visual-first, 1-3 sentences, engaging hooks, 5-10 hashtags, stories-friendly",
            "tiktok": "Short-form video script, trending sounds, quick hooks, viral potential",
            "linkedin": "Professional tone, thought leadership, longer form, industry insights",
            "facebook": "Community-focused, shareable, conversation starters, family-friendly",
            "youtube": "Educational or entertaining, longer form, clear value proposition"
        }
        return specs.get(platform, "General social media best practices")
    
    def _format_trending_elements(self, trend_analysis) -> str:
        """Simple utility to format trending elements for DSPy"""
        return f"""
        Trending Topics: {trend_analysis.trending_topics}
        Content Opportunities: {trend_analysis.content_opportunities}
        Cultural Insights: {trend_analysis.cultural_insights}
        """
    
    def _format_content_result(self, content, strategy, trend_analysis, trend_data) -> Dict[str, Any]:
        """Simple utility to format final content result"""
        
        # Parse hashtags from content
        hashtags = self._extract_hashtags(content.hashtags_and_cta)
        cta = self._extract_cta(content.hashtags_and_cta)
        
        return {
            "content_text": content.primary_content,
            "secondary_content": content.secondary_content if content.secondary_content else None,
            "hashtags": hashtags,
            "call_to_action": cta,
            "strategy": strategy.content_strategy,
            "engagement_tactics": strategy.engagement_tactics,
            "trending_topics": trend_analysis.trending_topics,
            "cultural_insights": trend_analysis.cultural_insights,
            "trend_data": trend_data
        }
    
    def _extract_hashtags(self, hashtags_and_cta: str) -> List[str]:
        """Simple utility to extract hashtags"""
        import re
        hashtags = re.findall(r'#\w+', hashtags_and_cta)
        return hashtags[:10]  # Limit to 10 hashtags
    
    def _extract_cta(self, hashtags_and_cta: str) -> str:
        """Simple utility to extract call-to-action"""
        lines = hashtags_and_cta.split('\n')
        for line in lines:
            if not line.startswith('#') and len(line.strip()) > 10:
                return line.strip()
        return "Share your thoughts in the comments!"
    
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
        """Generate intelligent chat response using DSPy conversation management"""
        
        try:
            # Get current trends (simple utility)
            trend_data = await self.analyze_trends_with_apify(user_profile)
            
            # Format context for DSPy (simple utilities)
            conversation_context = self._format_conversation_context(user_profile, conversation_history)
            current_trends = self._format_trends_for_chat(trend_data)
            
            # DSPy Conversation Management
            response = self.conversation_manager(
                user_query=user_message,
                conversation_context=conversation_context,
                current_trends=current_trends
            )
            
            # Format response (simple utility)
            return self._format_chat_response(response)
            
        except Exception as e:
            # Simple fallback
            return self._generate_fallback_chat_response(user_message, user_profile)
    
    def _format_conversation_context(self, user_profile: Dict, conversation_history: List[Dict]) -> str:
        """Simple utility to format conversation context"""
        context = f"""
        User Profile:
        - Name: {user_profile.get('name', 'User')}
        - Expertise: {', '.join(user_profile.get('expertise_areas', []))}
        - Platforms: {', '.join(user_profile.get('active_platforms', []))}
        - Cultural Background: {user_profile.get('cultural_background', 'cameroon')}
        - Primary Language: {user_profile.get('primary_language', 'en')}
        
        Recent Conversation:
        """
        
        # Add last 3 messages for context
        recent_messages = conversation_history[-3:] if conversation_history else []
        for msg in recent_messages:
            context += f"- {msg.get('role', 'unknown')}: {msg.get('content', '')[:100]}...\n"
        
        return context
    
    def _format_trends_for_chat(self, trend_data: Dict) -> str:
        """Simple utility to format trends for chat context"""
        trending_topics = trend_data.get('trending_topics', [])[:3]
        opportunities = trend_data.get('content_opportunities', [])[:2]
        
        trends_summary = "Current Trending Topics:\n"
        for topic in trending_topics:
            trends_summary += f"- {topic.get('topic', 'Unknown')}: {topic.get('engagement_score', 0):.1f}% engagement\n"
        
        trends_summary += "\nContent Opportunities:\n"
        for opp in opportunities:
            trends_summary += f"- {opp.get('topic', 'Unknown')}: {opp.get('engagement_potential', 0):.1f}% potential\n"
        
        return trends_summary
    
    def _format_chat_response(self, response) -> str:
        """Simple utility to format chat response"""
        formatted_response = response.response
        
        if response.follow_up_questions and response.follow_up_questions.strip():
            formatted_response += f"\n\n**💡 Follow-up Questions:**\n{response.follow_up_questions}"
        
        if response.action_items and response.action_items.strip():
            formatted_response += f"\n\n**🎯 Action Items:**\n{response.action_items}"
        
        return formatted_response
    
    def _generate_fallback_chat_response(self, user_message: str, user_profile: Dict) -> str:
        """Simple fallback chat response"""
        expertise = ', '.join(user_profile.get('expertise_areas', ['personal development']))
        
        return f"""I understand you're asking about: "{user_message}"

Based on your expertise in {expertise}, here are some thoughts:

💡 **Quick Suggestion:** Focus on creating authentic content that showcases your knowledge while connecting with your audience's needs.

🎯 **Next Steps:**
- Consider creating educational content around this topic
- Share your personal experience or client success stories
- Engage with your audience by asking questions

Would you like me to help you create some content around this topic?"""
    
    async def optimize_content(
        self, 
        original_content: str, 
        performance_goals: str,
        platform: str,
        user_profile: Dict
    ) -> Dict[str, Any]:
        """Optimize existing content using DSPy"""
        
        try:
            # Format inputs for DSPy
            platform_context = f"""
            Platform: {platform}
            Platform Specs: {self._get_platform_specs(platform)}
            User Profile: {self._format_user_profile(user_profile)}
            """
            
            # DSPy Content Optimization
            optimization = self.content_optimizer(
                original_content=original_content,
                performance_goals=performance_goals,
                platform_context=platform_context
            )
            
            return {
                "optimized_content": optimization.optimized_content,
                "optimization_rationale": optimization.optimization_rationale,
                "ab_test_suggestions": optimization.ab_test_suggestions,
                "original_content": original_content
            }
            
        except Exception as e:
            # Simple fallback optimization
            return {
                "optimized_content": original_content,
                "optimization_rationale": f"Unable to optimize due to: {str(e)}",
                "ab_test_suggestions": "Try different hooks, hashtags, or call-to-actions",
                "original_content": original_content
            }
    
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