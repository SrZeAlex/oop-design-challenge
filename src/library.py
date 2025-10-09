"""
Media library management system with advanced OOP patterns.
"""

from typing import List, Dict, Optional, Set, Callable
from datetime import datetime
from .media import MediaContent, MediaType, ContentRating
from .content_types import Movie, TVShow

class SearchFilter:
    """Encapsulates search and filtering logic."""
    
    def __init__(self):
        self.genres: Set[str] = set()
        self.media_types: Set[MediaType] = set()
        self.content_ratings: Set[ContentRating] = set()
        self.min_rating: Optional[float] = None
        self.max_duration: Optional[int] = None
        self.recently_released_days: Optional[int] = None
    
    def add_genre_filter(self, genre: str) -> 'SearchFilter':
        """Add genre filter (fluent interface)."""
        self.genres.add(genre.lower().strip())
        return self
    
    def add_type_filter(self, media_type: MediaType) -> 'SearchFilter':
        """Add media type filter."""
        self.media_types.add(media_type)
        return self
    
    def set_rating_filter(self, min_rating: float) -> 'SearchFilter':
        """Set minimum rating filter."""
        if not (1.0 <= min_rating <= 5.0):
            raise ValueError("Rating must be between 1.0 and 5.0")
        self.min_rating = min_rating
        return self
    
    def matches(self, content: MediaContent) -> bool:
        """Check if content matches all filters."""
        # Genre filter
        if self.genres and not any(content.matches_genre(genre) for genre in self.genres):
            return False
        
        # Media type filter
        if self.media_types and content.get_media_type() not in self.media_types:
            return False
        
        # Content rating filter
        if self.content_ratings and content.content_rating not in self.content_ratings:
            return False
        
        # Rating filter
        if self.min_rating and content.average_rating < self.min_rating:
            return False
        
        # Duration filter
        if self.max_duration and content.duration_minutes > self.max_duration:
            return False
        
        # Recently released filter
        if self.recently_released_days and not content.is_recently_released(self.recently_released_days):
            return False
        
        return True

class MediaLibrary:
    """
    Media library with advanced search and management capabilities.
    
    Demonstrates composition, encapsulation, and polymorphism.
    """
    
    def __init__(self, name: str):
        """
        Initialize media library.
        
        Args:
            name: Library name
        """
        self._name = name
        self._content: List[MediaContent] = []
        self._content_by_type: Dict[MediaType, List[MediaContent]] = {
            media_type: [] for media_type in MediaType
        }
        self._total_views = 0
        self._created_at = datetime.now()
    
    @property
    def name(self) -> str:
        """Get library name."""
        return self._name
    
    @property
    def total_content(self) -> int:
        """Get total number of content items."""
        return len(self._content)
    
    @property
    def total_views(self) -> int:
        """Get total views across all content."""
        return sum(content.view_count for content in self._content)
    
    def add_content(self, content: MediaContent) -> None:
        """
        Add media content to library.
        
        Args:
            content: Media content to add
            
        Raises:
            ValueError: If content already exists
        """
        if content in self._content:
            raise ValueError(f"Content '{content.title}' already exists in library")
        
        self._content.append(content)
        self._content_by_type[content.get_media_type()].append(content)
    
    def remove_content(self, title: str) -> bool:
        """
        Remove content by title.
        
        Args:
            title: Title of content to remove
            
        Returns:
            bool: True if content was removed
        """
        for content in self._content:
            if content.title.lower() == title.lower():
                self._content.remove(content)
                self._content_by_type[content.get_media_type()].remove(content)
                return True
        return False
    
    def get_content_by_type(self, media_type: MediaType) -> List[MediaContent]:
        """Get all content of specific type."""
        return self._content_by_type[media_type].copy()
    
    def search(self, query: str = "", filters: Optional[SearchFilter] = None) -> List[MediaContent]:
        """
        Search content with optional filters.
        
        Args:
            query: Search query string
            filters: Search filters to apply
            
        Returns:
            List of matching content
        """
        results = []
        
        for content in self._content:
            # Text search
            if query and not content.matches_search(query):
                continue
            
            # Apply filters
            if filters and not filters.matches(content):
                continue
            
            results.append(content)
        
        return results
    
    def get_top_rated(self, limit: int = 10) -> List[MediaContent]:
        """Get top-rated content."""
        return sorted(
            [c for c in self._content if c.average_rating > 0],
            key=lambda x: x.average_rating,
            reverse=True
        )[:limit]
    
    def get_most_viewed(self, limit: int = 10) -> List[MediaContent]:
        """Get most viewed content."""
        return sorted(
            self._content,
            key=lambda x: x.view_count,
            reverse=True
        )[:limit]
    
    def get_recently_added(self, days: int = 7) -> List[MediaContent]:
        """Get recently added content."""
        cutoff = datetime.now() - timedelta(days=days)
        return [c for c in self._content if c._created_at >= cutoff]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics."""
        stats = {
            'total_content': self.total_content,
            'total_views': self.total_views,
            'content_by_type': {
                media_type.value: len(content_list)
                for media_type, content_list in self._content_by_type.items()
            },
            'average_rating': 0.0,
            'total_runtime_hours': 0
        }
        
        if self._content:
            # Calculate average rating across all content
            rated_content = [c for c in self._content if c.average_rating > 0]
            if rated_content:
                stats['average_rating'] = sum(c.average_rating for c in rated_content) / len(rated_content)
            
            # Calculate total runtime
            total_minutes = sum(c.duration_minutes for c in self._content)
            stats['total_runtime_hours'] = round(total_minutes / 60, 1)
        
        return stats
