"""
Geocoding service using Nominatim OpenStreetMap API.
"""
import httpx
from typing import Optional, Tuple, Dict
import logging
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class GeocodingService:
    """Service for geocoding addresses to coordinates using Nominatim."""

    def __init__(self, base_url: str = "https://nominatim.openstreetmap.org"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": (
                    "HackathonHub/1.0 "
                    "(https://github.com/oklabflensburg/hackathonhub; "
                    "info@oklabflensburg.de)"
                ),
                "Referer": "https://hackathonhub.oklabflensburg.de"
            },
            timeout=30.0
        )
        # Cache for geocoding results to avoid repeated requests
        self._cache: Dict[str, Tuple[float, float]] = {}
        self._cache_timestamps: Dict[str, datetime] = {}
        self._cache_ttl = timedelta(hours=24)  # Cache for 24 hours
        # Rate limiting: maximum 1 request per second
        self._last_request_time: Optional[datetime] = None
        # Slightly more than 1 second to be safe
        self._min_request_interval = timedelta(seconds=1.1)

    async def geocode(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Geocode an address to latitude/longitude coordinates.

        Args:
            address: The address string to geocode

        Returns:
            Tuple of (latitude, longitude) or None if geocoding fails
        """
        if not address or address.lower() == "virtual":
            logger.info(
                f"Skipping geocoding for virtual or empty address: {address}"
            )
            return None

        # Check cache first
        cache_key = address.lower().strip()
        if cache_key in self._cache:
            cache_time = self._cache_timestamps.get(cache_key)
            if cache_time and datetime.now() - cache_time < self._cache_ttl:
                logger.debug(f"Using cached geocoding result for: {address}")
                return self._cache[cache_key]
            else:
                # Cache expired
                del self._cache[cache_key]
                if cache_key in self._cache_timestamps:
                    del self._cache_timestamps[cache_key]

        # Rate limiting
        await self._rate_limit()

        try:
            # Make request to Nominatim
            params = {
                "q": address,
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }

            logger.info(f"Geocoding address: {address}")
            response = await self.client.get(
                f"{self.base_url}/search",
                params=params
            )
            response.raise_for_status()

            data = response.json()
            if not data:
                logger.warning(f"No results found for address: {address}")
                return None

            # Extract coordinates from first result
            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])

            logger.info(
                f"Geocoded '{address}' to coordinates: ({lat}, {lon})"
            )

            # Cache the result
            self._cache[cache_key] = (lat, lon)
            self._cache_timestamps[cache_key] = datetime.now()

            return (lat, lon)

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error geocoding address '{address}': {e.response.status_code}"
            )
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error geocoding address '{address}': {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            logger.error(
                f"Error parsing geocoding response for '{address}': {e}"
            )
            return None
        except Exception as e:
            logger.error(f"Unexpected error geocoding address '{address}': {e}")
            return None

    async def _rate_limit(self) -> None:
        """Rate limit requests to 1 per second."""
        if self._last_request_time:
            time_since_last = datetime.now() - self._last_request_time
            if time_since_last < self._min_request_interval:
                wait_time = (
                    self._min_request_interval - time_since_last
                ).total_seconds()
                logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
                await asyncio.sleep(wait_time)

        self._last_request_time = datetime.now()

    async def reverse_geocode(
        self,
        lat: float,
        lon: float
    ) -> Optional[str]:
        """
        Reverse geocode coordinates to an address.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Address string or None if reverse geocoding fails
        """
        # Rate limiting
        await self._rate_limit()

        try:
            params = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "zoom": 18,  # Most detailed level
                "addressdetails": 1
            }

            logger.info(f"Reverse geocoding coordinates: ({lat}, {lon})")
            response = await self.client.get(
                f"{self.base_url}/reverse",
                params=params
            )
            response.raise_for_status()

            data = response.json()
            if not data:
                logger.warning(
                    f"No results found for coordinates: ({lat}, {lon})"
                )
                return None

            # Extract display name
            address = data.get("display_name", "")
            logger.info(
                f"Reverse geocoded ({lat}, {lon}) to address: {address}"
            )

            return address

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error reverse geocoding ({lat}, {lon}): "
                f"{e.response.status_code}"
            )
            return None
        except httpx.RequestError as e:
            logger.error(
                f"Request error reverse geocoding ({lat}, {lon}): {e}"
            )
            return None
        except Exception as e:
            logger.error(
                f"Unexpected error reverse geocoding ({lat}, {lon}): {e}"
            )
            return None

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    def __del__(self) -> None:
        """Ensure client is closed on destruction."""
        try:
            asyncio.create_task(self.close())
        except Exception:
            pass


# Singleton instance
geocoding_service = GeocodingService()