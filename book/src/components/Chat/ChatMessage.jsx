import React from 'react';

const ChatMessage = ({ message }) => {
  const isUser = message.sender === 'user';
  const isSystem = message.sender === 'system';

  return (
    <div className={`chat ${isUser ? 'chat-end' : 'chat-start'} mb-4`}>
      {!isUser && !isSystem && (
        <div className="chat-image avatar">
          <div className="w-10 bg-purple-500 rounded-full flex items-center justify-center text-white">
            <span>🤖</span>
          </div>
        </div>
      )}
      <div className={`chat-bubble ${isSystem ? 'chat-bubble-info' : isUser ? 'chat-bubble-primary' : 'chat-bubble-secondary'} text-white`}>
        <div className="text-sm">{message.content}</div>
        <div className="text-xs mt-1 opacity-80">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;