import React from 'react';
import { useLocation } from '@docusaurus/router';
import { useEffect } from 'react';
import { saveProgress } from '../utils/progressStorage';

function Root({ children }) {
  const location = useLocation();

  useEffect(() => {
    // This effect runs on every route change
    const path = location.pathname;
    if (path.startsWith('/AIBook/docs/')) {
      const parts = path.split('/');
      const bookId = 'AIBook'; // Assuming 'AIBook' is the main book ID
      let chapterId = parts[parts.length - 1];

      // Simple heuristic: if the path ends with a directory name, use that as chapterId
      // Otherwise, if it ends with a file name, remove the extension
      if (chapterId.includes('.md') || chapterId.includes('.mdx')) {
        chapterId = chapterId.split('.')[0];
      }

      // Simulate 100% completion for now, could be based on scroll position later
      saveProgress(bookId, chapterId, 100);
    }
  }, [location]);

  return <>{children}</>;
}

export default Root;
