import ipaddress

import httpx


class GeoService:
    def lookup(self, ip_address: str | None) -> dict:
        if not ip_address:
            return {}

        try:
            ip = ipaddress.ip_address(ip_address)

            if ip.is_private or ip.is_loopback:
                return {}
        except ValueError:
            return {}

        result = self._provider_a(ip_address)

        if result:
            return result

        result = self._provider_b(ip_address)

        if result:
            return result

        return {}

    def _provider_a(self, ip_address: str) -> dict | None:
        try:
            response = httpx.get(
                f"http://ip-api.com/json/{ip_address}",
                timeout=3.0,
            )

            response.raise_for_status()
            data = response.json()

            if data.get("status") != "success":
                return None

            return {
                "country": data.get("country"),
                "city": data.get("city"),
                "provider": "ip-api",
            }

        except (httpx.HTTPError, ValueError):
            return None

    def _provider_b(self, ip_address: str) -> dict | None:
        try:
            response = httpx.get(
                f"https://ipapi.co/{ip_address}/json/",
                timeout=3.0,
            )

            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                return None

            return {
                "country": data.get("country_name"),
                "city": data.get("city"),
                "provider": "ipapi",
            }

        except (httpx.HTTPError, ValueError):
            return None