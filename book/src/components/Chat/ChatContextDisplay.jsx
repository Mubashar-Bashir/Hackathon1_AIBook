import React from 'react';
import { useChatContext } from './ChatContext';

const ChatContextDisplay = () => {
  const { context } = useChatContext();

  if (!context.selectedText) {
    return null;
  }

  return (
    <div className="border-b border-base-300 bg-base-100 p-3 text-sm">
      <div className="font-medium text-primary">Context:</div>
      <div className="truncate max-w-[260px] text-ellipsis" title={context.selectedText}>
        "{context.selectedText.substring(0, 60)}{context.selectedText.length > 60 ? '...' : ''}"
      </div>
    </div>
  );
};

export default ChatContextDisplay;