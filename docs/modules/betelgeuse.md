# 🔴 Betelgeuse - Social Media Management

<div class="module-card">
  <h2><span class="emoji-icon">🔴</span> Betelgeuse</h2>
  <p>Named after the bright red supergiant star in the Orion constellation, Betelgeuse powers your social media management with advanced features for content scheduling, analytics, and engagement tracking.</p>
</div>

## Overview

The Betelgeuse module provides comprehensive tools for managing your social media presence across multiple platforms. Whether you're a social media manager, content creator, or marketing team, Betelgeuse streamlines your workflow and enhances your social media strategy.

## Key Features

- **Multi-platform Integration**: Seamlessly connect and manage content across Twitter, Instagram, LinkedIn, Facebook, TikTok, and more
- **Content Scheduling**: Plan and schedule posts with customizable publishing times and platform-specific optimizations
- **Analytics Dashboard**: Track engagement, reach, impressions, and other key metrics across all platforms
- **Audience Insights**: Gain valuable data about your audience demographics, behavior, and preferences
- **Automated Responses**: Set up intelligent auto-replies and engagement rules
- **Campaign Management**: Organize posts into campaigns and track performance metrics by campaign

## Installation

Betelgeuse can be installed as part of Nebula Orion or as a standalone module:

```bash
# Full Nebula Orion installation
pip install nebula-orion

# Betelgeuse module only
pip install nebula-orion[betelgeuse]
```

## Basic Usage

### Connecting Platforms

```python
from nebula_orion import betelgeuse

# Initialize the social media manager
sm_manager = betelgeuse.SocialMediaManager()

# Connect social media accounts
sm_manager.connect_platform(
    platform="twitter",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
)

sm_manager.connect_platform(
    platform="instagram",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD"  # Consider using environment variables for credentials
)
```

### Scheduling Posts

```python
# Schedule a basic text post
sm_manager.schedule_post(
    content="Excited to announce our latest feature! Check it out now!",
    platforms=["twitter", "linkedin"],
    schedule_time="2024-03-15 14:00:00"
)

# Schedule a post with media
sm_manager.schedule_post(
    content="Our new product demo is live!",
    media=["path/to/image.jpg", "path/to/video.mp4"],
    platforms=["instagram", "facebook"],
    schedule_time="2024-03-16 10:30:00",
    hashtags=["#ProductLaunch", "#Innovation"]
)
```

### Analyzing Engagement

```python
# Get platform-specific metrics
twitter_metrics = sm_manager.get_engagement_metrics(
    platform="twitter",
    start_date="2024-03-01",
    end_date="2024-03-15"
)
print(f"Twitter engagement: {twitter_metrics.total_engagement}")
print(f"Most engaging post: {twitter_metrics.top_post.content}")

# Get cross-platform metrics
all_metrics = sm_manager.get_engagement_metrics(
    start_date="2024-03-01",
    end_date="2024-03-15"
)
print(f"Best performing platform: {all_metrics.top_platform}")
```

## Advanced Features

### Content Calendar

```python
# Create a content calendar
calendar = sm_manager.create_content_calendar(
    name="Q2 Marketing Campaign",
    start_date="2024-04-01",
    end_date="2024-06-30"
)

# Add posts to the calendar
calendar.add_post(
    content="Weekly tip: Optimize your workflow with Nebula Orion!",
    platforms=["twitter", "linkedin"],
    schedule_pattern="every monday at 10:00"
)

# Add campaign posts
for i, topic in enumerate(["Productivity", "Automation", "Analytics"]):
    calendar.add_post(
        content=f"Learn how Nebula Orion enhances your {topic} workflows",
        platforms=["all"],
        schedule_time=f"2024-04-{15+i} 12:00:00"
    )

# Activate the calendar
calendar.activate()
```

### Audience Targeting

```python
# Define audience segments
sm_manager.create_audience_segment(
    name="Tech Professionals",
    criteria={
        "interests": ["technology", "programming", "data science"],
        "job_titles": ["developer", "engineer", "analyst"],
        "age_range": (25, 45)
    }
)

# Target a specific audience segment
sm_manager.schedule_post(
    content="New developer tools available in our latest release!",
    platforms=["linkedin", "twitter"],
    schedule_time="2024-04-10 09:00:00",
    audience_segment="Tech Professionals"
)
```

### Performance Optimization

```python
# Get optimal posting times
optimal_times = sm_manager.get_optimal_posting_times(
    platform="instagram",
    days=["monday", "wednesday", "friday"]
)
print(f"Best times to post: {optimal_times}")

# Optimize post content
optimized_content = sm_manager.optimize_content(
    original_content="Check out our new product features!",
    platform="twitter",
    optimization_goal="engagement"
)
print(f"Optimized content: {optimized_content}")
```

## Integration with Other Modules

Betelgeuse works seamlessly with other Nebula Orion modules:

### With Bellatrix (AI Toolkit)

```python
from nebula_orion import betelgeuse, bellatrix

# Initialize modules
sm_manager = betelgeuse.SocialMediaManager()
ai_toolkit = bellatrix.AIToolkit()

# Generate AI-powered content and post it
content_ideas = ai_toolkit.generate_content_suggestions(
    topic="industry trends",
    tone="professional",
    length="short"
)

for idea in content_ideas[:3]:  # Take top 3 ideas
    sm_manager.schedule_post(
        content=idea,
        platforms=["linkedin"],
        schedule_time=ai_toolkit.suggest_optimal_time("linkedin")
    )
```

### With Rigel (Video Production)

```python
from nebula_orion import betelgeuse, rigel

# Initialize modules
sm_manager = betelgeuse.SocialMediaManager()
video_pipeline = rigel.VideoProductionPipeline()

# Create video and share it
video_job = video_pipeline.create_job(
    template="social_media_promo",
    duration=30  # seconds
)
video_result = video_job.process()

# Schedule the video across platforms
sm_manager.schedule_post(
    content="Check out our latest product showcase!",
    media=[video_result.output_path],
    platforms=["instagram", "tiktok", "youtube"],
    schedule_time="2024-04-20 18:00:00"
)
```

### With Saiph (Automation)

```python
from nebula_orion import betelgeuse, saiph

# Initialize modules
sm_manager = betelgeuse.SocialMediaManager()
auto_system = saiph.AutomationSystem()

# Create an automated workflow
workflow = auto_system.create_workflow("Social Media Campaign")

workflow.add_task(
    "Monitor engagement",
    action=lambda: sm_manager.get_engagement_metrics(last_days=1),
    trigger="daily at 08:00",
    condition=lambda metrics: metrics.total_engagement < 100
)

workflow.add_task(
    "Boost underperforming posts",
    action=lambda metrics: sm_manager.boost_post(metrics.lowest_engagement_post.id),
    depends_on=["Monitor engagement"]
)

# Activate the workflow
workflow.activate()
```

## API Reference

For complete API documentation, see the [Betelgeuse API Reference](../api/betelgeuse.md).

## Examples and Tutorials

- [Creating a Social Media Content Calendar](../tutorials/betelgeuse/content-calendar.md)
- [Measuring Campaign Performance](../tutorials/betelgeuse/campaign-analytics.md)
- [Automating Social Media Responses](../tutorials/betelgeuse/automated-responses.md)
