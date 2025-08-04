import asyncio
import httpx
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class ApifyClient:
    """Client for interacting with Apify API for web scraping and data collection"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("APIFY_API_TOKEN")
        self.base_url = "https://api.apify.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.session = httpx.AsyncClient(timeout=300.0)  # 5 minute timeout
    
    async def run_actor(
        self, 
        actor_id: str, 
        input_data: Dict[str, Any],
        wait_for_finish: bool = True,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Run an Apify actor with given input data"""
        
        url = f"{self.base_url}/acts/{actor_id}/runs"
        
        # Add synchronous parameter if waiting for finish
        params = {}
        if wait_for_finish:
            params["waitForFinish"] = timeout
        
        try:
            response = await self.session.post(
                url, 
                headers=self.headers,
                json=input_data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            print(f"Error running actor {actor_id}: {e}")
            return {"error": str(e)}
    
    async def get_dataset_items(self, dataset_id: str, limit: int = 1000) -> List[Dict]:
        """Get items from a dataset"""
        
        url = f"{self.base_url}/datasets/{dataset_id}/items"
        params = {"limit": limit, "format": "json"}
        
        try:
            response = await self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            print(f"Error fetching dataset {dataset_id}: {e}")
            return []
    
    async def get_run_status(self, run_id: str) -> Dict[str, Any]:
        """Get the status of a running actor"""
        
        url = f"{self.base_url}/actor-runs/{run_id}"
        
        try:
            response = await self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            print(f"Error getting run status {run_id}: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """Close the HTTP session"""
        await self.session.aclose()


class ApifyTrendAnalyzer:
    """Enhanced trend analyzer using Apify actors for social media scraping"""
    
    def __init__(self):
        self.client = ApifyClient()
        
        # Popular Apify actors for social media scraping
        self.actors = {
            "instagram_scraper": "apify/instagram-scraper",
            "tiktok_scraper": "clockworks/free-tiktok-scraper", 
            "youtube_scraper": "bernardo/youtube-scraper",
            "twitter_scraper": "quacker/twitter-scraper",
            "google_trends": "lukaskrivka/google-trends-scraper",
            "linkedin_scraper": "voyager/linkedin-scraper"
        }
    
    async def scrape_instagram_trends(
        self, 
        hashtags: List[str], 
        max_posts: int = 50
    ) -> List[Dict]:
        """Scrape Instagram posts for trending content analysis"""
        
        input_data = {
            "hashtags": hashtags,
            "resultsLimit": max_posts,
            "searchLimit": 1,
            "addParentData": False
        }
        
        result = await self.client.run_actor(
            self.actors["instagram_scraper"],
            input_data
        )
        
        if "data" in result and "defaultDatasetId" in result["data"]:
            dataset_id = result["data"]["defaultDatasetId"]
            return await self.client.get_dataset_items(dataset_id)
        
        return []
    
    async def scrape_tiktok_trends(
        self, 
        keywords: List[str], 
        max_videos: int = 30
    ) -> List[Dict]:
        """Scrape TikTok for trending videos and hashtags"""
        
        results = []
        
        for keyword in keywords:
            input_data = {
                "searchQueries": [keyword],
                "resultsPerPage": max_videos,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False
            }
            
            result = await self.client.run_actor(
                self.actors["tiktok_scraper"],
                input_data
            )
            
            if "data" in result and "defaultDatasetId" in result["data"]:
                dataset_id = result["data"]["defaultDatasetId"]
                items = await self.client.get_dataset_items(dataset_id)
                results.extend(items)
        
        return results
    
    async def scrape_youtube_trends(
        self, 
        search_terms: List[str], 
        max_videos: int = 25
    ) -> List[Dict]:
        """Scrape YouTube for trending videos and topics"""
        
        input_data = {
            "searchKeywords": search_terms,
            "maxResults": max_videos,
            "uploadDate": "week",  # Last week's videos
            "sortBy": "viewCount"
        }
        
        result = await self.client.run_actor(
            self.actors["youtube_scraper"],
            input_data
        )
        
        if "data" in result and "defaultDatasetId" in result["data"]:
            dataset_id = result["data"]["defaultDatasetId"]
            return await self.client.get_dataset_items(dataset_id)
        
        return []
    
    async def scrape_google_trends(
        self, 
        keywords: List[str], 
        geo: str = "CM"  # Cameroon
    ) -> List[Dict]:
        """Scrape Google Trends for keyword popularity"""
        
        input_data = {
            "searchTerms": keywords,
            "timeRange": "today 7-d",  # Last 7 days
            "geo": geo,
            "category": 0,  # All categories
            "searchType": "web"
        }
        
        result = await self.client.run_actor(
            self.actors["google_trends"],
            input_data
        )
        
        if "data" in result and "defaultDatasetId" in result["data"]:
            dataset_id = result["data"]["defaultDatasetId"]
            return await self.client.get_dataset_items(dataset_id)
        
        return []
    
    async def analyze_competitor_content(
        self, 
        competitor_handles: List[str], 
        platform: str = "instagram"
    ) -> List[Dict]:
        """Analyze competitor content for insights"""
        
        if platform == "instagram":
            input_data = {
                "usernames": competitor_handles,
                "resultsLimit": 20,
                "searchLimit": 1
            }
            
            result = await self.client.run_actor(
                self.actors["instagram_scraper"],
                input_data
            )
            
            if "data" in result and "defaultDatasetId" in result["data"]:
                dataset_id = result["data"]["defaultDatasetId"]
                return await self.client.get_dataset_items(dataset_id)
        
        return []
    
    async def comprehensive_trend_analysis(
        self,
        user_interests: List[str],
        expertise_areas: List[str],
        cultural_context: str = "cameroon",
        competitor_handles: List[str] = None
    ) -> Dict[str, Any]:
        """Perform comprehensive trend analysis using Apify"""
        
        try:
            # Combine interests and expertise for search terms
            search_terms = user_interests + expertise_areas
            
            # Run multiple scraping tasks concurrently
            tasks = [
                self.scrape_google_trends(search_terms, "CM"),
                self.scrape_instagram_trends([f"#{term.replace(' ', '')}" for term in search_terms]),
                self.scrape_tiktok_trends(search_terms),
                self.scrape_youtube_trends(search_terms)
            ]
            
            # Add competitor analysis if provided
            if competitor_handles:
                tasks.append(self.analyze_competitor_content(competitor_handles))
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            google_trends = results[0] if not isinstance(results[0], Exception) else []
            instagram_data = results[1] if not isinstance(results[1], Exception) else []
            tiktok_data = results[2] if not isinstance(results[2], Exception) else []
            youtube_data = results[3] if not isinstance(results[3], Exception) else []
            competitor_data = results[4] if len(results) > 4 and not isinstance(results[4], Exception) else []
            
            # Process and analyze the data
            trending_topics = self._extract_trending_topics(
                google_trends, instagram_data, tiktok_data, youtube_data
            )
            
            content_opportunities = self._identify_content_opportunities(
                trending_topics, user_interests, expertise_areas
            )
            
            competitor_insights = self._analyze_competitor_insights(competitor_data)
            
            return {
                "trending_topics": trending_topics,
                "content_opportunities": content_opportunities,
                "competitor_insights": competitor_insights,
                "data_sources": {
                    "google_trends_count": len(google_trends),
                    "instagram_posts_count": len(instagram_data),
                    "tiktok_videos_count": len(tiktok_data),
                    "youtube_videos_count": len(youtube_data),
                    "competitor_posts_count": len(competitor_data)
                },
                "analysis_timestamp": datetime.now().isoformat()
            }
        
        finally:
            await self.client.close()
    
    def _extract_trending_topics(
        self, 
        google_trends: List[Dict],
        instagram_data: List[Dict],
        tiktok_data: List[Dict],
        youtube_data: List[Dict]
    ) -> List[Dict]:
        """Extract and rank trending topics from scraped data"""
        
        topics = []
        
        # Process Google Trends
        for trend in google_trends:
            topics.append({
                "topic": trend.get("keyword", ""),
                "platform": "google",
                "engagement_score": trend.get("interest", 0),
                "relevance_score": 0,
                "source_data": trend
            })
        
        # Process Instagram data
        for post in instagram_data:
            hashtags = post.get("hashtags", [])
            likes = post.get("likesCount", 0)
            comments = post.get("commentsCount", 0)
            
            engagement_score = likes + (comments * 5)  # Weight comments more
            
            for hashtag in hashtags[:3]:  # Top 3 hashtags
                topics.append({
                    "topic": hashtag,
                    "platform": "instagram",
                    "engagement_score": engagement_score,
                    "relevance_score": 0,
                    "source_data": post
                })
        
        # Process TikTok data
        for video in tiktok_data:
            title = video.get("text", "")
            likes = video.get("diggCount", 0)
            shares = video.get("shareCount", 0)
            
            engagement_score = likes + (shares * 10)  # Weight shares more
            
            topics.append({
                "topic": title[:50] + "..." if len(title) > 50 else title,
                "platform": "tiktok",
                "engagement_score": engagement_score,
                "relevance_score": 0,
                "source_data": video
            })
        
        # Process YouTube data
        for video in youtube_data:
            title = video.get("title", "")
            views = video.get("viewCount", 0)
            likes = video.get("likeCount", 0)
            
            engagement_score = (views / 1000) + (likes * 2)  # Normalize views
            
            topics.append({
                "topic": title,
                "platform": "youtube",
                "engagement_score": engagement_score,
                "relevance_score": 0,
                "source_data": video
            })
        
        # Sort by engagement score and return top topics
        return sorted(topics, key=lambda x: x["engagement_score"], reverse=True)[:20]
    
    def _identify_content_opportunities(
        self, 
        trending_topics: List[Dict],
        user_interests: List[str],
        expertise_areas: List[str]
    ) -> List[Dict]:
        """Identify specific content opportunities from trending topics"""
        
        opportunities = []
        
        for topic in trending_topics[:10]:  # Top 10 topics
            # Calculate relevance score
            relevance_score = 0
            topic_text = topic["topic"].lower()
            
            for interest in user_interests:
                if interest.lower() in topic_text:
                    relevance_score += 2
            
            for expertise in expertise_areas:
                if expertise.lower() in topic_text:
                    relevance_score += 3
            
            if relevance_score > 0:  # Only include relevant topics
                opportunities.append({
                    "topic": topic["topic"],
                    "platform": topic["platform"],
                    "engagement_potential": min(topic["engagement_score"] / 1000 * 100, 100),
                    "relevance_score": relevance_score,
                    "opportunity_type": self._classify_opportunity_type(topic),
                    "suggested_approach": self._suggest_content_approach(topic),
                    "source_data": topic["source_data"]
                })
        
        return sorted(opportunities, key=lambda x: x["relevance_score"], reverse=True)
    
    def _analyze_competitor_insights(self, competitor_data: List[Dict]) -> Dict[str, Any]:
        """Analyze competitor content for insights"""
        
        if not competitor_data:
            return {"insights": [], "top_hashtags": [], "content_types": []}
        
        # Extract hashtags
        all_hashtags = []
        content_types = []
        
        for post in competitor_data:
            hashtags = post.get("hashtags", [])
            all_hashtags.extend(hashtags)
            
            # Determine content type
            if post.get("videoUrl"):
                content_types.append("video")
            else:
                content_types.append("image")
        
        # Count hashtag frequency
        hashtag_counts = {}
        for hashtag in all_hashtags:
            hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Count content types
        content_type_counts = {}
        for content_type in content_types:
            content_type_counts[content_type] = content_type_counts.get(content_type, 0) + 1
        
        return {
            "insights": [
                f"Competitors posted {len(competitor_data)} pieces of content",
                f"Most popular content type: {max(content_type_counts, key=content_type_counts.get) if content_type_counts else 'N/A'}",
                f"Average hashtags per post: {len(all_hashtags) / len(competitor_data) if competitor_data else 0:.1f}"
            ],
            "top_hashtags": [{"hashtag": tag, "count": count} for tag, count in top_hashtags],
            "content_types": content_type_counts
        }
    
    def _classify_opportunity_type(self, topic: Dict) -> str:
        """Classify the type of content opportunity"""
        
        topic_text = topic["topic"].lower()
        
        if any(word in topic_text for word in ["how", "tutorial", "guide", "tips"]):
            return "educational"
        elif any(word in topic_text for word in ["challenge", "trend", "viral"]):
            return "viral_trend"
        elif any(word in topic_text for word in ["motivation", "inspiration", "success"]):
            return "motivational"
        else:
            return "general"
    
    def _suggest_content_approach(self, topic: Dict) -> str:
        """Suggest how to approach creating content for this topic"""
        
        approaches = {
            "educational": "Create a step-by-step tutorial or guide",
            "viral_trend": "Put your unique spin on this trending topic",
            "motivational": "Share personal story or client success related to this topic",
            "general": "Connect this topic to your expertise and provide unique insights"
        }
        
        opportunity_type = self._classify_opportunity_type(topic)
        return approaches.get(opportunity_type, approaches["general"])


# Example usage
async def main():
    """Example usage of Apify trend analyzer"""
    
    analyzer = ApifyTrendAnalyzer()
    
    result = await analyzer.comprehensive_trend_analysis(
        user_interests=["personal development", "business", "health"],
        expertise_areas=["life coaching", "entrepreneurship"],
        cultural_context="cameroon",
        competitor_handles=["@example_competitor1", "@example_competitor2"]
    )
    
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())