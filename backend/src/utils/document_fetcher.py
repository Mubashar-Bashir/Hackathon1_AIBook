"""
Document Fetcher Service for RAG Content Pipeline

This module provides functionality to fetch content from Vercel/GitHub using sitemap/XML,
crawl URLs, and extract text content for the RAG system.
"""

import asyncio
import logging
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class ContentFetchResult(BaseModel):
    """Result of content fetching operation"""
    url: str
    title: str
    content: str
    status: str
    error: Optional[str] = None


class DocumentFetcher:
    """Service to fetch content from Vercel/GitHub via sitemap/XML"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AIBook-RAG-Bot/1.0'
        })
        self.logger = logging.getLogger(__name__)

    def get_sitemap_urls(self, sitemap_url: Optional[str] = None) -> List[str]:
        """
        Extract URLs from sitemap.xml
        """
        if not sitemap_url:
            sitemap_url = urljoin(self.base_url, 'sitemap.xml')

        try:
            response = self.session.get(sitemap_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            urls = []

            # Handle both sitemap index and regular sitemap
            sitemap_tags = soup.find_all('sitemap')
            if sitemap_tags:
                # This is a sitemap index, get URLs from all included sitemaps
                for sitemap_tag in sitemap_tags:
                    loc = sitemap_tag.find('loc')
                    if loc:
                        included_sitemap_url = loc.text.strip()
                        urls.extend(self._parse_regular_sitemap(included_sitemap_url))
            else:
                # This is a regular sitemap
                urls = self._parse_regular_sitemap(sitemap_url)

            return urls
        except Exception as e:
            self.logger.error(f"Error fetching sitemap from {sitemap_url}: {e}")
            return []

    def _parse_regular_sitemap(self, sitemap_url: str) -> List[str]:
        """Parse a regular sitemap for URLs"""
        try:
            response = self.session.get(sitemap_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')
            urls = []

            for url_tag in soup.find_all('url'):
                loc = url_tag.find('loc')
                if loc:
                    url = loc.text.strip()
                    # Only include URLs from the same domain
                    if self._is_same_domain(url):
                        urls.append(url)

            return urls
        except Exception as e:
            self.logger.error(f"Error parsing sitemap {sitemap_url}: {e}")
            return []

    def _is_same_domain(self, url: str) -> bool:
        """Check if URL is from the same domain as base_url"""
        base_domain = urlparse(self.base_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain

    def extract_content_from_url(self, url: str) -> ContentFetchResult:
        """
        Extract text content from a specific URL
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else urlparse(url).path.split('/')[-1]

            # Extract main content - prioritize content in main/article tags or with content-related classes
            main_content = soup.find('main') or soup.find('article')
            if not main_content:
                # Look for common content containers
                content_selectors = [
                    '[role="main"]',
                    '.main-content',
                    '.content',
                    '.docs-content',
                    '.markdown',
                    '.doc-content'
                ]
                for selector in content_selectors:
                    main_content = soup.select_one(selector)
                    if main_content:
                        break

            if main_content:
                content = main_content.get_text(separator=' ', strip=True)
            else:
                # Fallback to body content
                body = soup.find('body')
                if body:
                    content = body.get_text(separator=' ', strip=True)
                else:
                    content = soup.get_text(separator=' ', strip=True)

            # Clean up excessive whitespace
            import re
            content = re.sub(r'\s+', ' ', content).strip()

            return ContentFetchResult(
                url=url,
                title=title,
                content=content,
                status='success'
            )
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {e}")
            return ContentFetchResult(
                url=url,
                title='',
                content='',
                status='error',
                error=str(e)
            )

    def fetch_content_from_sitemap(self, sitemap_url: Optional[str] = None) -> List[ContentFetchResult]:
        """
        Fetch all content from URLs listed in sitemap
        """
        urls = self.get_sitemap_urls(sitemap_url)
        results = []

        for url in urls:
            result = self.extract_content_from_url(url)
            results.append(result)

        return results

    def fetch_content_from_urls(self, urls: List[str]) -> List[ContentFetchResult]:
        """
        Fetch content from a list of specific URLs
        """
        results = []

        for url in urls:
            result = self.extract_content_from_url(url)
            results.append(result)

        return results


# Async version for better performance
async def async_fetch_content_from_urls(fetcher: DocumentFetcher, urls: List[str]) -> List[ContentFetchResult]:
    """
    Asynchronously fetch content from a list of URLs
    """
    import aiohttp

    results = []

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=fetcher.timeout)) as session:
        async def fetch_single_url(url: str):
            try:
                async with session.get(url) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')

                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()

                    # Get title
                    title_tag = soup.find('title')
                    title = title_tag.get_text().strip() if title_tag else urlparse(url).path.split('/')[-1]

                    # Extract main content
                    main_content = soup.find('main') or soup.find('article')
                    if not main_content:
                        content_selectors = [
                            '[role="main"]',
                            '.main-content',
                            '.content',
                            '.docs-content',
                            '.markdown',
                            '.doc-content'
                        ]
                        for selector in content_selectors:
                            main_element = soup.select_one(selector)
                            if main_element:
                                main_content = main_element
                                break

                    if main_content:
                        text_content = main_content.get_text(separator=' ', strip=True)
                    else:
                        body = soup.find('body')
                        if body:
                            text_content = body.get_text(separator=' ', strip=True)
                        else:
                            text_content = soup.get_text(separator=' ', strip=True)

                    # Clean up excessive whitespace
                    import re
                    text_content = re.sub(r'\s+', ' ', text_content).strip()

                    return ContentFetchResult(
                        url=url,
                        title=title,
                        content=text_content,
                        status='success'
                    )
            except Exception as e:
                logging.error(f"Error extracting content from {url}: {e}")
                return ContentFetchResult(
                    url=url,
                    title='',
                    content='',
                    status='error',
                    error=str(e)
                )

        tasks = [fetch_single_url(url) for url in urls]
        results = await asyncio.gather(*tasks)

    return results


if __name__ == "__main__":
    # Example usage
    fetcher = DocumentFetcher("https://book-20sb9ub9v-mubashar-bashirs-projects.vercel.app")

    # Try to get URLs from sitemap
    urls = fetcher.get_sitemap_urls()
    print(f"Found {len(urls)} URLs in sitemap")

    if urls:
        # Fetch content from first few URLs as a test
        results = fetcher.fetch_content_from_urls(urls[:3])
        for result in results:
            print(f"URL: {result.url}")
            print(f"Title: {result.title}")
            print(f"Status: {result.status}")
            print(f"Content length: {len(result.content)}")
            print("---")