"""
Base media classes and interfaces for the digital library system.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum

class MediaType(Enum):
    """Enumeration of supported media types."""
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    MUSIC = "music"
    PODCAST = "podcast"

class ContentRating(Enum):
    """Content rating classifications."""
    G = "G"           # General Audiences
    PG = "PG"         # Parental Guidance
    PG_13 = "PG-13"   # Parents Strongly Cautioned
    R = "R"           # Restricted
    NC_17 = "NC-17"   # Adults Only
    UNRATED = "Unrated"

class MediaContent(ABC):
    """
    Abstract base class for all media content.
    
    This class defines the common interface and attributes that all
    media types must implement.
    """
    
    def __init__(
        self,
        title: str,
        duration_minutes: int,
        release_date: datetime,
        content_rating: ContentRating,
        genres: List[str],
        description: str
    ):
        """
        Initialize media content.
        
        Args:
            title: The title of the media content
            duration_minutes: Duration in minutes
            release_date: When the content was released
            content_rating: Age/content rating
            genres: List of genre tags
            description: Content description
            
        Raises:
            ValueError: If any required field is invalid
        """
        # Validate inputs
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError("Duration must be a positive integer")
            
        if not isinstance(genres, list) or not genres:
            raise ValueError("Genres must be a non-empty list")
            
        # Protected attributes (use properties for access)
        self._title = title.strip()
        self._duration_minutes = duration_minutes
        self._release_date = release_date
        self._content_rating = content_rating
        self._genres = [genre.strip().lower() for genre in genres]
        self._description = description.strip()
        self._view_count = 0
        self._average_rating = 0.0
        self._ratings = []
        self._created_at = datetime.now()
    
    # Properties for controlled access to attributes
    @property
    def title(self) -> str:
        """Get the media title."""
        return self._title
    
    @property
    def duration_minutes(self) -> int:
        """Get duration in minutes."""
        return self._duration_minutes
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration string."""
        hours, minutes = divmod(self._duration_minutes, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    
    @property
    def release_date(self) -> datetime:
        """Get release date."""
        return self._release_date
    
    @property
    def content_rating(self) -> ContentRating:
        """Get content rating."""
        return self._content_rating
    
    @property
    def genres(self) -> List[str]:
        """Get list of genres."""
        return self._genres.copy()  # Return copy to prevent external modification
    
    @property
    def description(self) -> str:
        """Get content description."""
        return self._description
    
    @property
    def view_count(self) -> int:
        """Get total view count."""
        return self._view_count
    
    @property
    def average_rating(self) -> float:
        """Get average user rating."""
        return self._average_rating
    
    # Abstract methods that subclasses must implement
    @abstractmethod
    def get_media_type(self) -> MediaType:
        """Return the specific media type."""
        pass
    
    @abstractmethod
    def can_stream(self) -> bool:
        """Check if content is available for streaming."""
        pass
    
    @abstractmethod
    def get_streaming_url(self) -> str:
        """Get the streaming URL for this content."""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get media-specific metadata."""
        pass
    
    # Common methods for all media types
    def add_view(self) -> None:
        """Record a view of this content."""
        self._view_count += 1
    
    def add_rating(self, rating: float) -> None:
        """
        Add a user rating.
        
        Args:
            rating: Rating from 1.0 to 5.0
            
        Raises:
            ValueError: If rating is out of range
        """
        if not isinstance(rating, (int, float)) or not (1.0 <= rating <= 5.0):
            raise ValueError("Rating must be between 1.0 and 5.0")
        
        self._ratings.append(float(rating))
        self._average_rating = sum(self._ratings) / len(self._ratings)
    
    def matches_genre(self, genre: str) -> bool:
        """Check if content matches a specific genre."""
        return genre.lower().strip() in self._genres
    
    def is_recently_released(self, days: int = 30) -> bool:
        """Check if content was released within specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        return self._release_date >= cutoff_date
    
    def __str__(self) -> str:
        """String representation of media content."""
        return f"{self.title} ({self.release_date.year}) - {self.duration_formatted}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"{self.__class__.__name__}("
            f"title='{self.title}', "
            f"duration={self.duration_minutes}, "
            f"rating={self.content_rating.value})"
        )

    def is_age_appropriate(self, user_age: int) -> bool:
        """
        Check if content is appropriate for user's age.
        
        Args:
            user_age: User's age in years
            
        Returns:
            bool: True if age-appropriate
        """
        rating = self.content_rating
        if rating == ContentRating.G or rating == ContentRating.UNRATED:
            return True
        if rating == ContentRating.PG:
            return True  # Guidance, but no strict age
        if rating == ContentRating.PG_13:
            return user_age >= 13
        if rating == ContentRating.R:
            return user_age >= 17
        if rating == ContentRating.NC_17:
            return user_age >= 18
        return True
    
    def matches_search(self, query: str) -> bool:
        """
        Check if content matches search query.
        
        Args:
            query: Search string
            
        Returns:
            bool: True if content matches query
        """
        q = query.lower().strip()
        if q in self.title.lower():
            return True
        if q in self.description.lower():
            return True
        if any(q in genre for genre in self.genres):
            return True
        return False