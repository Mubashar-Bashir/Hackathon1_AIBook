import React, { useState } from 'react';
import { useChatContext } from './ChatContext';

const MessageInput = () => {
  const [inputValue, setInputValue] = useState('');
  const { addMessage, context, setIsLoading } = useChatContext();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // In a real implementation, this would call the backend
    // For now, we'll simulate the process
    const userMessage = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent',
      contextInfo: context
    };

    // Add user message immediately
    addMessage(userMessage);
    setInputValue('');

    // Show loading state to simulate AI "thinking"
    setIsLoading(true);

    // Simulate bot response after a delay (mock API)
    setTimeout(() => {
      const botMessage = {
        id: (Date.now() + 1).toString(),
        content: "In AIBOOK, this concept is a core pillar of Spec-Driven Development. Let's dive deeper!",
        sender: 'assistant',
        timestamp: new Date(),
        status: 'sent',
        contextInfo: context
      };
      addMessage(botMessage);
      setIsLoading(false); // Remove loading state
    }, 1500);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="p-4 bg-violet-800 bg-opacity-50">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about the textbook..."
          className="flex-1 input input-bordered input-sm bg-white bg-opacity-20 text-white placeholder:text-violet-200 focus:outline-none focus:ring-2 focus:ring-cyan-300 border-violet-400"
          disabled={false} // Can be enabled when backend is connected
        />
        <button
          type="submit"
          className="btn bg-cyan-500 hover:bg-cyan-400 text-white border-cyan-500"
          disabled={!inputValue.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default MessageInput;