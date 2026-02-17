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
        normalized_address = address.strip().lower()
        now = datetime.now()
        if normalized_address in self._cache:
            cache_time = self._cache_timestamps.get(normalized_address)
            if cache_time and (now - cache_time) < self._cache_ttl:
                logger.info(
                    f"Returning cached geocoding result for: {address}"
                )
                return self._cache[normalized_address]
            else:
                # Cache expired, remove it
                del self._cache[normalized_address]
                if normalized_address in self._cache_timestamps:
                    del self._cache_timestamps[normalized_address]

        try:
            # Rate limiting: wait if needed
            if self._last_request_time:
                time_since_last = now - self._last_request_time
                if time_since_last < self._min_request_interval:
                    wait_time = (
                        self._min_request_interval - time_since_last
                    ).total_seconds()
                    logger.debug(
                        f"Rate limiting: waiting {wait_time:.2f} seconds"
                    )
                    await asyncio.sleep(wait_time)

            # Nominatim API request
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

            # Update last request time
            self._last_request_time = datetime.now()

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    lat = float(result["lat"])
                    lon = float(result["lon"])
                    logger.info(
                        f"Geocoding successful: {address} -> ({lat}, {lon})"
                    )
                    # Cache the result
                    self._cache[normalized_address] = (lat, lon)
                    self._cache_timestamps[normalized_address] = (
                        self._last_request_time
                    )
                    return (lat, lon)
                else:
                    logger.warning(f"No results found for address: {address}")
            else:
                logger.error(
                    f"Geocoding failed with status {response.status_code}: "
                    f"{response.text}"
                )

        except httpx.RequestError as e:
            logger.error(f"Geocoding request failed: {e}")
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error parsing geocoding response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in geocoding: {e}")

        return None

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Singleton instance
_geocoding_service: Optional[GeocodingService] = None


def get_geocoding_service() -> GeocodingService:
    """Get or create the geocoding service singleton."""
    global _geocoding_service
    if _geocoding_service is None:
        _geocoding_service = GeocodingService()
    return _geocoding_service


async def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convenience function to geocode an address.

    Args:
        address: The address string to geocode

    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    service = get_geocoding_service()
    return await service.geocode(address)


async def close_geocoding_service():
    """Close the geocoding service."""
    global _geocoding_service
    if _geocoding_service:
        await _geocoding_service.close()
        _geocoding_service = None
