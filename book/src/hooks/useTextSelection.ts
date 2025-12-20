import { useState, useEffect, useCallback } from 'react';
import { TooltipState } from '../components/Chat/types';

const useTextSelection = () => {
  const [tooltipState, setTooltipState] = useState<TooltipState>({
    isVisible: false,
    position: { x: 0, y: 0 },
    selectedText: '',
    targetElement: null
  });

  // Function to handle text selection
  const handleTextSelection = useCallback(() => {
    const selection = window.getSelection();
    if (!selection) return;

    const selectedText = selection.toString().trim();

    // Implement 200 character limit with truncation (T015, T023)
    if (selectedText && selectedText.length > 0) {
      const truncatedText = selectedText.length > 200
        ? selectedText.substring(0, 200) + '...'
        : selectedText;

      // Get the position for tooltip
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      setTooltipState({
        isVisible: true,
        position: {
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY - 40 // Position above the selected text
        },
        selectedText: truncatedText,
        targetElement: range.startContainer.parentElement
      });
    } else {
      // Hide tooltip if no text is selected
      setTooltipState(prev => ({
        ...prev,
        isVisible: false
      }));
    }
  }, []);

  // Function to handle tooltip click - dispatch custom event (T014, T026)
  const handleTooltipClick = useCallback(() => {
    if (tooltipState.selectedText) {
      // Dispatch custom event with selected text
      const event = new CustomEvent('aibook:open-with-context', {
        detail: { selectedText: tooltipState.selectedText }
      });
      window.dispatchEvent(event);

      // Hide the tooltip after click
      setTooltipState(prev => ({
        ...prev,
        isVisible: false
      }));
    }
  }, [tooltipState.selectedText]);

  // Function to hide tooltip
  const hideTooltip = useCallback(() => {
    setTooltipState(prev => ({
      ...prev,
      isVisible: false
    }));
  }, []);

  // Add event listeners when component mounts
  useEffect(() => {
    const handleMouseUp = () => {
      // Add a small delay to ensure selection is complete
      setTimeout(handleTextSelection, 10);
    };

    const handleClickOutside = (event: MouseEvent) => {
      // Hide tooltip if clicking outside of it
      const target = event.target as HTMLElement;
      if (target && !target.closest('.selection-tooltip')) {
        hideTooltip();
      }
    };

    // Add event listeners
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('click', handleClickOutside);

    // Cleanup event listeners on unmount
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('click', handleClickOutside);
    };
  }, [handleTextSelection, hideTooltip]);

  return {
    tooltipState,
    handleTooltipClick,
    hideTooltip
  };
};

export default useTextSelection;