"""
Geocoding service using Nominatim OpenStreetMap API.
"""
import httpx
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class GeocodingService:
    """Service for geocoding addresses to coordinates using Nominatim."""
    
    def __init__(self, base_url: str = "https://nominatim.openstreetmap.org"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": "Hackathon-Dashboard/1.0 (contact@example.com)"
            },
            timeout=30.0
        )
    
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
        
        try:
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
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    lat = float(result["lat"])
                    lon = float(result["lon"])
                    logger.info(
                        f"Geocoding successful: {address} -> ({lat}, {lon})"
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