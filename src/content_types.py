"""
Concrete implementations of different media content types.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from .media import MediaContent, MediaType, ContentRating

class Movie(MediaContent):
    """Movie implementation of media content."""
    
    def __init__(
        self,
        title: str,
        duration_minutes: int,
        release_date: datetime,
        content_rating: ContentRating,
        genres: List[str],
        description: str,
        director: str,
        cast: List[str],
        budget: Optional[float] = None,
        box_office: Optional[float] = None
    ):
        """
        Initialize movie.
        
        Args:
            director: Movie director name
            cast: List of main cast members
            budget: Production budget (optional)
            box_office: Box office earnings (optional)
        """
        super().__init__(title, duration_minutes, release_date, content_rating, genres, description)
        
        if not director or not isinstance(director, str):
            raise ValueError("Director must be a non-empty string")
        if not isinstance(cast, list):
            raise ValueError("Cast must be a list")
            
        self._director = director.strip()
        self._cast = [actor.strip() for actor in cast if actor.strip()]
        self._budget = budget
        self._box_office = box_office
    
    @property
    def director(self) -> str:
        """Get movie director."""
        return self._director
    
    @property
    def cast(self) -> List[str]:
        """Get main cast list."""
        return self._cast.copy()
    
    @property
    def budget(self) -> Optional[float]:
        """Get production budget."""
        return self._budget
    
    @property
    def box_office(self) -> Optional[float]:
        """Get box office earnings."""
        return self._box_office
    
    def get_media_type(self) -> MediaType:
        """Return movie media type."""
        return MediaType.MOVIE
    
    def can_stream(self) -> bool:
        """Check if movie is available for streaming."""
        # Movies are available 90 days after release
        return not self.is_recently_released(90)
    
    def get_streaming_url(self) -> str:
        """Get movie streaming URL."""
        if not self.can_stream():
            raise ValueError("Movie not available for streaming yet")
        return f"https://stream.example.com/movies/{self.title.lower().replace(' ', '-')}"
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get movie-specific metadata."""
        return {
            'type': self.get_media_type().value,
            'director': self.director,
            'cast': self.cast,
            'budget': self.budget,
            'box_office': self.box_office,
            'is_blockbuster': self._is_blockbuster()
        }
    
    def _is_blockbuster(self) -> bool:
        """Determine if movie is a blockbuster (private method)."""
        if self._budget and self._box_office:
            return self._box_office > self._budget * 3  # 3x budget return
        return False

class TVShow(MediaContent):
    """TV Show implementation with seasons and episodes."""
    
    def __init__(
        self,
        title: str,
        duration_minutes: int,  # Average episode duration
        release_date: datetime,
        content_rating: ContentRating,
        genres: List[str],
        description: str,
        seasons: int,
        total_episodes: int,
        status: str = "ongoing"  # ongoing, completed, cancelled
    ):
        """Initialize TV show."""
        super().__init__(title, duration_minutes, release_date, content_rating, genres, description)
        
        if not isinstance(seasons, int) or seasons <= 0:
            raise ValueError("Seasons must be a positive integer")
        if not isinstance(total_episodes, int) or total_episodes <= 0:
            raise ValueError("Total episodes must be a positive integer")
        if status not in ['ongoing', 'completed', 'cancelled']:
            raise ValueError("Status must be 'ongoing', 'completed', or 'cancelled'")
            
        self._seasons = seasons
        self._total_episodes = total_episodes
        self._status = status
    
    @property
    def seasons(self) -> int:
        """Get number of seasons."""
        return self._seasons
    
    @property
    def total_episodes(self) -> int:
        """Get total episode count."""
        return self._total_episodes
    
    @property
    def status(self) -> str:
        """Get show status."""
        return self._status
    
    @property
    def average_episode_duration(self) -> int:
        """Get average episode duration."""
        return self.duration_minutes
    
    @property
    def total_runtime_minutes(self) -> int:
        """Get total runtime for all episodes."""
        return self.duration_minutes * self._total_episodes
    
    def get_media_type(self) -> MediaType:
        """Return TV show media type."""
        return MediaType.TV_SHOW
    
    def can_stream(self) -> bool:
        """TV shows are always available for streaming."""
        return True
    
    def get_streaming_url(self) -> str:
        """Get TV show streaming URL."""
        return f"https://stream.example.com/shows/{self.title.lower().replace(' ', '-')}"
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get TV show metadata."""
        return {
            'type': self.get_media_type().value,
            'seasons': self.seasons,
            'total_episodes': self.total_episodes,
            'status': self.status,
            'average_episode_duration': self.average_episode_duration,
            'total_runtime_hours': round(self.total_runtime_minutes / 60, 1)
        }


class Music(MediaContent):
    """Music implementation of media content."""
    
    def __init__(
        self,
        title: str,
        duration_minutes: int,
        release_date: datetime,
        content_rating: ContentRating,
        genres: List[str],
        description: str,
        artist: str,
        album: str,
        track_number: int,
        is_explicit: bool = False
    ):
        """
        Initialize music track.
        
        Args:
            artist: Name of the artist
            album: Album name
            track_number: Track number in the album
            is_explicit: Whether the track has explicit content
        """
        super().__init__(title, duration_minutes, release_date, content_rating, genres, description)
        
        if not artist or not isinstance(artist, str):
            raise ValueError("Artist must be a non-empty string")
        if not album or not isinstance(album, str):
            raise ValueError("Album must be a non-empty string")
        if not isinstance(track_number, int) or track_number <= 0:
            raise ValueError("Track number must be a positive integer")
            
        self._artist = artist.strip()
        self._album = album.strip()
        self._track_number = track_number
        self._is_explicit = is_explicit
    
    @property
    def artist(self) -> str:
        """Get artist name."""
        return self._artist
    
    @property
    def album(self) -> str:
        """Get album name."""
        return self._album
    
    @property
    def track_number(self) -> int:
        """Get track number."""
        return self._track_number
    
    @property
    def is_explicit(self) -> bool:
        """Check if track has explicit content."""
        return self._is_explicit
    
    def get_media_type(self) -> MediaType:
        """Return music media type."""
        return MediaType.MUSIC
    
    def can_stream(self) -> bool:
        """Music tracks are always available for streaming."""
        return True
    
    def get_streaming_url(self) -> str:
        """Get music streaming URL."""
        return f"https://stream.example.com/music/{self.title.lower().replace(' ', '-')}"
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get music-specific metadata."""
        return {
            'type': self.get_media_type().value,
            'artist': self.artist,
            'album': self.album,
            'track_number': self.track_number,
            'is_explicit': self.is_explicit
        }


class Podcast(MediaContent):
    """Podcast implementation of media content."""

    def __init__(
        self,
        title: str,
        duration_minutes: int,
        release_date: datetime,
        content_rating: ContentRating,
        genres: List[str],
        description: str,
        host: str,
        episode_number: int,
        season_number: int,
        transcript_available: bool = False
    ):
        """
        Initialize podcast episode.

        Args:
            host: Host name
            episode_number: Episode number in the season
            season_number: Season number
            transcript_available: Whether transcript is available
        """
        super().__init__(title, duration_minutes, release_date, content_rating, genres, description)
        if not host or not isinstance(host, str):
            raise ValueError("Host must be a non-empty string")
        if not isinstance(episode_number, int) or episode_number <= 0:
            raise ValueError("Episode number must be a positive integer")
        if not isinstance(season_number, int) or season_number <= 0:
            raise ValueError("Season number must be a positive integer")
        self._host = host.strip()
        self._episode_number = episode_number
        self._season_number = season_number
        self._transcript_available = transcript_available

    @property
    def host(self) -> str:
        """Get host name."""
        return self._host

    @property
    def episode_number(self) -> int:
        """Get episode number."""
        return self._episode_number

    @property
    def season_number(self) -> int:
        """Get season number."""
        return self._season_number

    @property
    def transcript_available(self) -> bool:
        """Check if transcript is available."""
        return self._transcript_available

    def get_media_type(self) -> MediaType:
        """Return podcast media type."""
        return MediaType.PODCAST

    def can_stream(self) -> bool:
        """Podcasts are always available for streaming."""
        return True

    def get_streaming_url(self) -> str:
        """Get podcast streaming URL."""
        return (
            f"https://stream.example.com/podcasts/"
            f"{self.host.lower().replace(' ', '-')}/"
            f"{self.title.lower().replace(' ', '-')}/"
            f"s{self.season_number}e{self.episode_number}"
        )

    def get_metadata(self) -> Dict[str, Any]:
        """Get podcast-specific metadata."""
        return {
            'type': self.get_media_type().value,
            'host': self.host,
            'episode_number': self.episode_number,
            'season_number': self.season_number,
            'transcript_available': self.transcript_available
        }
