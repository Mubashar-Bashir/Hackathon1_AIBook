import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook to detect and return currently selected text
 * Optimized for performance to ensure <500ms text detection
 * @returns {string} The currently selected text
 */
const useSelectedText = () => {
  const [selectedText, setSelectedText] = useState('');

  // Memoize the handler to prevent recreation on every render
  const handleSelectionChange = useCallback(() => {
    // Get the currently selected text
    let text = '';

    if (window.getSelection) {
      const selection = window.getSelection();
      text = selection.toString().trim();
    } else if (document.selection && document.selection.type !== 'Control') {
      // For older IE
      text = document.selection.createRange().text.trim();
    }

    // Only update if the selection has actually changed to prevent unnecessary re-renders
    if (text !== selectedText) {
      setSelectedText(text);
    }
  }, [selectedText]);

  useEffect(() => {
    // Add event listeners for selection changes
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('keyup', handleSelectionChange);

    // Also check for touch events on mobile devices
    document.addEventListener('touchend', handleSelectionChange);

    // Initial check in case text is already selected
    handleSelectionChange();

    // Cleanup event listeners
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
      document.removeEventListener('touchend', handleSelectionChange);
    };
  }, [handleSelectionChange]); // Use the memoized callback

  return selectedText;
};

export default useSelectedText;