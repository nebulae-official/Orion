# Quick Start Guide

This guide will help you get up and running with Nebula Orion quickly. We'll explore the basics of each module to give you a solid foundation.

## Basic Usage

After [installing Nebula Orion](installation.md), you can import and use it in your Python projects:

```python
import nebula_orion

# Print the welcome message
print(nebula_orion.hello())
```

## Module Overview

Nebula Orion is organized into four main modules, each named after a star in the Orion constellation. Let's explore the basics of each module:

### 🔴 Betelgeuse - Social Media Management

```python
from nebula_orion import betelgeuse

# Initialize the social media manager
sm_manager = betelgeuse.SocialMediaManager()

# Schedule a post across platforms
sm_manager.schedule_post(
    content="Check out our latest update! 🚀",
    platforms=["twitter", "linkedin"],
    schedule_time="2024-03-15 14:00:00"
)

# Analyze engagement metrics
metrics = sm_manager.get_engagement_metrics(
    platform="twitter",
    start_date="2024-03-01",
    end_date="2024-03-15"
)
print(f"Total engagement: {metrics.total_engagement}")
```

### 🤖 Bellatrix - AI Toolkit

```python
from nebula_orion import bellatrix

# Initialize the AI toolkit
ai = bellatrix.AIToolkit()

# Analyze content sentiment
sentiment = ai.analyze_sentiment("Great news! Our latest feature is now live!")
print(f"Sentiment score: {sentiment.score}, Classification: {sentiment.classification}")

# Generate content suggestions
suggestions = ai.generate_content_suggestions(
    topic="machine learning",
    tone="informative",
    length="medium"
)
for suggestion in suggestions:
    print(f"- {suggestion}")
```

### 🎥 Rigel - Video Production

```python
from nebula_orion import rigel

# Initialize the video pipeline
video_pipeline = rigel.VideoProductionPipeline()

# Set up a processing job
job = video_pipeline.create_job(
    input_file="raw_footage.mp4",
    output_format="mp4",
    resolution="1080p"
)

# Add processing steps
job.add_step(rigel.ColorGrading(preset="cinematic"))
job.add_step(rigel.AddWatermark(image="logo.png", position="bottom-right"))
job.add_step(rigel.ExportWithSubtitles(subtitle_file="captions.srt"))

# Run the job
result = job.process()
print(f"Video processed successfully: {result.output_path}")
```

### ⚙️ Saiph - Automation System

```python
from nebula_orion import saiph

# Initialize the automation system
auto_system = saiph.AutomationSystem()

# Create a workflow
workflow = auto_system.create_workflow("Content Publication")

# Add tasks to the workflow
workflow.add_task(
    "Create content",
    assigned_to="content_team",
    duration="2d"
)
workflow.add_task(
    "Review content",
    assigned_to="editorial_team",
    duration="1d",
    depends_on=["Create content"]
)
workflow.add_task(
    "Publish content",
    assigned_to="publishing_team",
    duration="4h",
    depends_on=["Review content"]
)

# Start the workflow
workflow.start()

# Check status
status = workflow.get_status()
print(f"Workflow progress: {status.progress}%")
```

## Combining Modules

One of the powerful features of Nebula Orion is the ability to combine modules for integrated workflows:

```python
from nebula_orion import betelgeuse, bellatrix, rigel, saiph

# Create a content workflow
def create_content_workflow():
    # Use AI to generate content ideas
    ai = bellatrix.AIToolkit()
    content_ideas = ai.generate_content_suggestions(topic="technology trends")

    # Create a video for the best idea
    video_pipeline = rigel.VideoProductionPipeline()
    job = video_pipeline.create_job(template="explainer_video")
    job.set_script(content_ideas[0])
    video_path = job.process().output_path

    # Schedule social media posts with the video
    sm_manager = betelgeuse.SocialMediaManager()
    sm_manager.schedule_post(
        content="Check out our latest tech trend analysis! #TechTrends",
        media=[video_path],
        platforms=["twitter", "linkedin", "instagram"]
    )

    # Set up an automation to track engagement
    auto_system = saiph.AutomationSystem()
    tracking = auto_system.create_tracking_task(
        "Monitor video engagement",
        metrics=["views", "likes", "shares"],
        notification_threshold=1000
    )

    return tracking

# Execute the workflow
tracking_task = create_content_workflow()
print(f"Content workflow initiated. Tracking ID: {tracking_task.id}")
```

## Configuration

For more advanced usage, you can configure Nebula Orion through a configuration file. Create a file named `orion_config.yaml` in your project:

```yaml
# orion_config.yaml
api_keys:
  twitter: "your_twitter_api_key"
  openai: "your_openai_api_key"

storage:
  type: "s3"
  bucket: "orion-assets"
  region: "us-west-2"

processing:
  default_resolution: "1080p"
  threads: 4
```

Then load it in your application:

```python
from nebula_orion import config

# Load configuration
config.load_from_file("orion_config.yaml")
```

## Next Steps

Now that you understand the basics of Nebula Orion, explore these resources:

- [Configuration Guide](configuration.md) - Learn about advanced configuration options
- [Module Documentation](../modules/overview.md) - Detailed documentation for each module
- [API Reference](../api/nebula_orion.md) - Complete API reference
- [Tutorials](../tutorials/basic-usage.md) - Step-by-step tutorials for common use cases
