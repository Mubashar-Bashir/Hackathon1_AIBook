import React, { useState, useEffect, useRef } from 'react';

interface SelectionTooltipProps {
  isOpen: boolean;
  position: { x: number; y: number };
  onAskAI: () => void;
  onClose: () => void;
}

const SelectionTooltip: React.FC<SelectionTooltipProps> = ({
  isOpen,
  position,
  onAskAI,
  onClose
}) => {
  const tooltipRef = useRef<HTMLDivElement>(null);

  // Handle clicks outside the tooltip to close it
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  if (!isOpen) {
    return null;
  }

  return (
    <div
      ref={tooltipRef}
      className="fixed z-50 bg-purple-600 text-white px-4 py-2 rounded-lg shadow-lg flex items-center space-x-2"
      style={{
        left: position.x,
        top: position.y,
        transform: 'translateY(-100%)' // Position above the cursor
      }}
    >
      <button
        onClick={onAskAI}
        className="font-medium hover:text-cyan-200 transition-colors focus:outline-none focus:ring-2 focus:ring-white rounded px-2 py-1"
      >
        Ask AI
      </button>
      <button
        onClick={onClose}
        className="text-sm hover:text-cyan-200 focus:outline-none focus:ring-2 focus:ring-white rounded px-1"
        aria-label="Close tooltip"
      >
        ×
      </button>
    </div>
  );
};

// Hook to manage text selection and tooltip
export const useTextSelection = () => {
  const [tooltip, setTooltip] = useState({
    isOpen: false,
    position: { x: 0, y: 0 },
    selectedText: ''
  });

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedText = selection?.toString().trim() || '';

      if (selectedText) {
        const range = selection?.getRangeAt(0);
        if (range) {
          const rect = range.getBoundingClientRect();
          // Position the tooltip above the selected text
          setTooltip({
            isOpen: true,
            position: {
              x: rect.left + window.scrollX,
              y: rect.top + window.scrollY
            },
            selectedText
          });
        }
      } else {
        setTooltip(prev => ({ ...prev, isOpen: false }));
      }
    };

    const handleMouseUp = () => {
      // Small delay to ensure selection is complete
      setTimeout(handleSelection, 1);
    };

    const handleClick = () => {
      // Check if click is outside any selection
      const selection = window.getSelection();
      if (!selection?.toString().trim()) {
        setTooltip(prev => ({ ...prev, isOpen: false }));
      }
    };

    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('click', handleClick);
    };
  }, []);

  const handleAskAI = () => {
    if (tooltip.selectedText) {
      // Dispatch custom event with selected text
      const event = new CustomEvent('aibook:ask-context', {
        detail: { text: tooltip.selectedText }
      });
      window.dispatchEvent(event);
      setTooltip(prev => ({ ...prev, isOpen: false }));
    }
  };

  const handleCloseTooltip = () => {
    setTooltip(prev => ({ ...prev, isOpen: false }));
  };

  return {
    tooltip,
    handleAskAI,
    handleCloseTooltip
  };
};

export default SelectionTooltip;