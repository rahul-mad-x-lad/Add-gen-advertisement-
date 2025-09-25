from typing import Dict, Any, Optional
import fal_client
import os
import time

def generate_video_from_image(
    image_url: str,
    prompt: str,
    model: str = "fal-ai/minimax-video/image-to-video",
    api_key: Optional[str] = None,
    duration: Optional[int] = None,
    fps: Optional[int] = None,
    aspect_ratio: Optional[str] = None,
    motion_strength: Optional[float] = None,
    seed: Optional[int] = None,
    webhook_url: Optional[str] = None,
    sync: bool = True
) -> Dict[str, Any]:
    """
    Generate a video from an image using fal AI models.
    
    Args:
        image_url: URL of the input image
        prompt: Text description for video generation
        model: fal AI model to use for video generation
        api_key: fal AI API key (uses FAL_KEY env var if not provided)
        duration: Video duration in seconds
        fps: Frames per second
        aspect_ratio: Video aspect ratio
        motion_strength: Strength of motion (0.0 to 1.0)
        seed: Random seed for reproducible results
        webhook_url: Optional webhook URL for async results
        sync: Whether to wait for results or return immediately
    
    Returns:
        Dict containing the API response with video URL
    """
    
    # Set API key if provided
    if api_key:
        os.environ["FAL_KEY"] = api_key
    elif not os.getenv("FAL_KEY"):
        raise ValueError("FAL_KEY environment variable or api_key parameter must be set")
    
    # Prepare request arguments
    arguments = {
        "image_url": image_url,
        "prompt": prompt
    }
    
    # Add optional parameters based on model capabilities
    if duration is not None:
        arguments["duration"] = duration
    if fps is not None:
        arguments["fps"] = fps
    if aspect_ratio is not None:
        arguments["aspect_ratio"] = aspect_ratio
    if motion_strength is not None:
        arguments["motion_strength"] = motion_strength
    if seed is not None:
        arguments["seed"] = seed
    
    try:
        print(f"Generating video with model: {model}")
        print(f"Image URL: {image_url}")
        print(f"Prompt: {prompt}")
        print(f"Arguments: {arguments}")
        
        if sync:
            # Use subscribe for synchronous operation with progress tracking
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    print(f"Progress: {update.logs}")
                    for log in update.logs:
                        print(f"Log: {log.get('message', '')}")
            
            result = fal_client.subscribe(
                model,
                arguments=arguments,
                with_logs=True,
                on_queue_update=on_queue_update
            )
            
            print(f"Video generation completed!")
            print(f"Result: {result}")
            return result
            
        else:
            # Use submit for asynchronous operation
            handler = fal_client.submit(
                model,
                arguments=arguments,
                webhook_url=webhook_url
            )
            
            return {
                "request_id": handler.request_id,
                "status": "submitted",
                "message": "Video generation started. Use request_id to check status."
            }
            
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        raise Exception(f"Video generation failed: {str(e)}")

def check_video_status(
    model: str,
    request_id: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check the status of a video generation request.
    
    Args:
        model: fal AI model used for generation
        request_id: Request ID from submit operation
        api_key: fal AI API key
    
    Returns:
        Dict containing status information
    """
    if api_key:
        os.environ["FAL_KEY"] = api_key
    
    try:
        status = fal_client.status(model, request_id, with_logs=True)
        print(f"Status check result: {status}")
        return status
    except Exception as e:
        raise Exception(f"Status check failed: {str(e)}")

def get_video_result(
    model: str,
    request_id: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the result of a video generation request.
    
    Args:
        model: fal AI model used for generation
        request_id: Request ID from submit operation
        api_key: fal AI API key
    
    Returns:
        Dict containing the video generation result
    """
    if api_key:
        os.environ["FAL_KEY"] = api_key
    
    try:
        result = fal_client.result(model, request_id)
        print(f"Video generation result: {result}")
        return result
    except Exception as e:
        raise Exception(f"Result retrieval failed: {str(e)}")

def upload_image_for_video(
    image_path: str,
    api_key: Optional[str] = None
) -> str:
    """
    Upload an image file to fal and get a URL for video generation.
    
    Args:
        image_path: Path to the image file
        api_key: fal AI API key
    
    Returns:
        URL of the uploaded image
    """
    if api_key:
        os.environ["FAL_KEY"] = api_key
    
    try:
        url = fal_client.upload_file(image_path)
        print(f"Image uploaded successfully: {url}")
        return url
    except Exception as e:
        raise Exception(f"Image upload failed: {str(e)}")

# Available video generation models
VIDEO_MODELS = {
    "minimax": {
        "id": "fal-ai/minimax-video/image-to-video",
        "name": "MiniMax Video",
        "description": "Generate video clips from images using MiniMax Video model",
        "max_duration": 6,
        "supports_fps": True,
        "supports_motion_strength": True
    },
    "luma": {
        "id": "fal-ai/luma-dream-machine",
        "name": "Luma Dream Machine v1.5",
        "description": "Generate video clips using Luma Dream Machine v1.5",
        "max_duration": 5,
        "supports_fps": False,
        "supports_motion_strength": False
    },
    "kling": {
        "id": "fal-ai/kling-video/v1/standard",
        "name": "Kling 1.0",
        "description": "Generate video clips using Kling 1.0",
        "max_duration": 10,
        "supports_fps": True,
        "supports_motion_strength": True
    }
}

def get_available_models() -> Dict[str, Dict[str, Any]]:
    """
    Get information about available video generation models.
    
    Returns:
        Dict containing model information
    """
    return VIDEO_MODELS
