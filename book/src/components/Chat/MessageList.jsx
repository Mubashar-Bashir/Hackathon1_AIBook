import React, { useRef, useEffect } from 'react';
import { useChatContext } from './ChatContext';
import ChatMessage from './ChatMessage';

const MessageList = () => {
  const { messages, isLoading } = useChatContext();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex-1 overflow-y-auto p-4 bg-violet-900 bg-opacity-30">
      {messages.length === 0 && !isLoading ? (
        <div className="text-center text-violet-200 italic py-8">
          No messages yet. Start a conversation!
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="chat chat-start mb-4">
              <div className="chat-image avatar">
                <div className="w-10 bg-purple-500 rounded-full flex items-center justify-center text-white">
                  <span>🤖</span>
                </div>
              </div>
              <div className="chat-bubble chat-bubble-secondary text-white">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;