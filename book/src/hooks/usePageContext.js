import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook to get current page context (title and route)
 * Optimized for performance to work with AIBOOK's Docusaurus setup
 * @returns {Object} Object containing pageTitle and pageRoute
 */
const usePageContext = () => {
  const [context, setContext] = useState({
    pageTitle: typeof document !== 'undefined' ? document.title : '',
    pageRoute: typeof window !== 'undefined' ? window.location.pathname : ''
  });

  // Memoize the update function to prevent recreation on every render
  const updateContext = useCallback(() => {
    setContext(prevContext => {
      const newPageTitle = document.title;
      const newPageRoute = window.location.pathname;

      // Only update if something actually changed
      if (prevContext.pageTitle !== newPageTitle || prevContext.pageRoute !== newPageRoute) {
        return {
          pageTitle: newPageTitle,
          pageRoute: newPageRoute
        };
      }
      return prevContext;
    });
  }, []);

  useEffect(() => {
    // Set up a more robust observer for title changes
    let titleObserver = null;
    const titleElement = typeof document !== 'undefined' ? document.querySelector('title') : null;

    if (titleElement && typeof MutationObserver !== 'undefined') {
      titleObserver = new MutationObserver(updateContext);
      titleObserver.observe(titleElement, { childList: true });
    }

    // Listen for popstate events (browser navigation)
    window.addEventListener('popstate', updateContext);

    // Listen for hashchange events (URL fragment changes)
    window.addEventListener('hashchange', updateContext);

    // Listen for custom events that might indicate page changes
    document.addEventListener('DOMContentLoaded', updateContext);
    window.addEventListener('load', updateContext);

    // For SPAs, also listen to potential custom events
    window.addEventListener('locationchange', updateContext);

    // Initial update
    updateContext();

    // Check for title changes periodically as a fallback, but with reduced frequency for performance
    const titleCheckInterval = setInterval(() => {
      if (document.title !== context.pageTitle) {
        updateContext();
      }
    }, 2000); // Check every 2 seconds instead of 1 second for performance

    // Cleanup
    return () => {
      if (titleObserver) {
        titleObserver.disconnect();
      }
      window.removeEventListener('popstate', updateContext);
      window.removeEventListener('hashchange', updateContext);
      document.removeEventListener('DOMContentLoaded', updateContext);
      window.removeEventListener('load', updateContext);
      window.removeEventListener('locationchange', updateContext);
      clearInterval(titleCheckInterval);
    };
  }, [updateContext]); // Use the memoized callback

  return context;
};

export default usePageContext;