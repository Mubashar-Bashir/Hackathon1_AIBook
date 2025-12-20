import React, { useState, useEffect } from 'react';
import { useChatContext } from './ChatContext';
import ChatContextDisplay from './ChatContextDisplay';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatWindow = ({ onClose }) => {
  const { context, messages, setMessages, isLoading: contextIsLoading, setIsLoading } = useChatContext();
  const [isMinimized, setIsMinimized] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);

  // Listen for the custom event to handle context from text selection
  useEffect(() => {
    const handleContextOpen = (e) => {
      const contextText = e.detail.text;
      // Add a specialized "System" message or pre-fill the input
      setMessages(prev => [...prev, {
        id: `system-${Date.now()}`,
        role: 'system',
        content: `Context selected: "${contextText}"`,
        sender: 'system',
        timestamp: new Date()
      }]);
    };

    window.addEventListener('aibook:ask-context', handleContextOpen);
    return () => window.removeEventListener('aibook:ask-context', handleContextOpen);
  }, [setMessages]);

  if (isMinimized) {
    return (
      <div className="bg-gradient-to-r from-violet-600 to-purple-600 text-white p-2 rounded-lg shadow-lg cursor-pointer" onClick={() => setIsMinimized(false)}>
        <div className="flex items-center justify-between">
          <span className="font-bold">AI Assistant</span>
          <span className="text-sm">({context.pageTitle || 'Page'})</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-b from-violet-700 via-purple-600 to-indigo-900 text-white rounded-lg shadow-2xl flex flex-col w-96 h-[500px] max-h-[80vh] transition-all duration-300 relative">
      {/* Mascot Character - Peeking over the top */}
      <div className="absolute -top-8 left-4 z-10">
        <div className="w-16 h-16 rounded-full bg-white flex items-center justify-center border-4 border-purple-300">
          <span className="text-2xl">🤖</span>
        </div>
      </div>

      {/* Chat Header */}
      <div className="bg-violet-800 bg-opacity-80 p-4 rounded-t-lg flex justify-between items-center backdrop-blur-sm">
        <div className="flex items-center">
          <h3 className="font-bold text-lg">AI Assistant</h3>
          {context.pageTitle && (
            <span className="ml-2 text-xs opacity-80 truncate max-w-[100px]">{context.pageTitle}</span>
          )}
        </div>
        <div className="flex space-x-2">
          <button
            className="text-white hover:text-cyan-200 cursor-pointer text-xl"
            onClick={() => setIsMinimized(true)}
            aria-label="Minimize chat"
          >
            −
          </button>
          <button
            className="text-white hover:text-cyan-200 cursor-pointer text-xl"
            onClick={onClose}
            aria-label="Close chat"
          >
            ×
          </button>
        </div>
      </div>

      {/* Suggestions - Only show when no messages exist */}
      {showSuggestions && messages.length === 0 && (
        <div className="p-3 overflow-x-auto whitespace-nowrap flex space-x-2">
          <button
            className="bg-violet-500 hover:bg-violet-400 px-3 py-1 rounded-full text-sm whitespace-nowrap transition-colors flex-shrink-0"
            onClick={() => {
              setMessages(prev => [...prev, {
                id: `suggestion-${Date.now()}-1`,
                content: 'SDD Methodology',
                sender: 'user',
                timestamp: new Date()
              }]);
              setShowSuggestions(false);
            }}
          >
            SDD Methodology
          </button>
          <button
            className="bg-violet-500 hover:bg-violet-400 px-3 py-1 rounded-full text-sm whitespace-nowrap transition-colors flex-shrink-0"
            onClick={() => {
              setMessages(prev => [...prev, {
                id: `suggestion-${Date.now()}-2`,
                content: 'AI-Native Level 4',
                sender: 'user',
                timestamp: new Date()
              }]);
              setShowSuggestions(false);
            }}
          >
            AI-Native Level 4
          </button>
          <button
            className="bg-violet-500 hover:bg-violet-400 px-3 py-1 rounded-full text-sm whitespace-nowrap transition-colors flex-shrink-0"
            onClick={() => {
              setMessages(prev => [...prev, {
                id: `suggestion-${Date.now()}-3`,
                content: 'Agentic Loops',
                sender: 'user',
                timestamp: new Date()
              }]);
              setShowSuggestions(false);
            }}
          >
            Agentic Loops
          </button>
        </div>
      )}

      {/* Context Display */}
      <ChatContextDisplay />

      {/* Messages */}
      <MessageList />

      {/* Input Area */}
      <MessageInput />
    </div>
  );
};

export default ChatWindow;