import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatbotResponse {
  responseText: string;
  sources: string[];
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [currentChapterId, setCurrentChapterId] = useState<string>('');
  const [isClient, setIsClient] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isAuthenticated, user } = useAuth();

  // Mark as client-side after mounting
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Get current chapter ID from URL or page context (only in browser)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const path = window.location.pathname;
      if (path.includes('/docs/')) {
        // Extract chapter ID from URL (e.g., /docs/physical-ai/chapter3 -> physical-ai/chapter3)
        const chapterPath = path.split('/docs/')[1]?.split('/')[0];
        if (chapterPath) {
          setCurrentChapterId(chapterPath);
        }
      }
    }
  }, []);

  // Detect selected text (only in browser)
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleSelection = () => {
      const selectedText = window.getSelection()?.toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading || typeof window === 'undefined') return;

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Determine if we're using context-based query
      const useContext = selectedText && selectedText.trim() !== '';
      const userId = isAuthenticated ? user?.userId : undefined;

      let response: Response;
      let requestBody: any;

      if (useContext) {
        // Use context-specific endpoint
        requestBody = {
          queryText: inputText,
          contextText: selectedText || '',
          chapterId: currentChapterId || 'unknown',
          userId: userId
        };

        response = await fetch('http://localhost:8000/chatbot/ask-with-context', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify(requestBody)
        });
      } else {
        // Use general endpoint
        requestBody = {
          queryText: inputText,
          userId: userId
        };

        response = await fetch('http://localhost:8000/chatbot/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify(requestBody)
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data: ChatbotResponse = await response.json();

      // Add bot response to chat
      const botMessage: ChatMessage = {
        id: Date.now().toString(),
        text: data.responseText + (data.sources.length > 0 ? `\n\nSources: ${data.sources.join(', ')}` : ''),
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        text: `Error: ${error instanceof Error ? error.message : 'Failed to get response from chatbot'}`,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setSelectedText(null); // Clear selected text after using it
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  // Don't render anything on the server side
  if (!isClient) {
    return null;
  }

  return (
    <div className="chatbot-container">
      {/* Chatbot button */}
      <button
        className="chatbot-button"
        onClick={toggleChatbot}
        aria-label="Open chatbot"
      >
        🤖
      </button>

      {/* Chatbot popup */}
      {isOpen && (
        <div className="chatbot-popup">
          <div className="chatbot-header">
            <h3>AI Textbook Assistant</h3>
            <button
              className="chatbot-close"
              onClick={toggleChatbot}
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook.</p>
                <p>You can ask me questions about the content, or select text and ask me about it specifically.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`chatbot-message ${message.sender}-message`}
                >
                  <div className="message-content">
                    {message.text}
                  </div>
                  <div className="message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message bot-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className="selected-text-preview">
              <strong>Context:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
            </div>
          )}

          <div className="chatbot-input-area">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={selectedText ? "Ask about selected text..." : "Ask a question about the textbook..."}
              className="chatbot-input"
              rows={3}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              className="chatbot-send-button"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      )}

      <style jsx>{`
        .chatbot-container {
          position: fixed;
          bottom: 20px;
          right: 20px;
          z-index: 1000;
        }

        .chatbot-button {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background-color: #16b28f;
          color: white;
          border: none;
          font-size: 24px;
          cursor: pointer;
          box-shadow: 0 4px 8px rgba(0,0,0,0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
        }

        .chatbot-button:hover {
          transform: scale(1.05);
          box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }

        .chatbot-popup {
          position: absolute;
          bottom: 70px;
          right: 0;
          width: 350px;
          height: 500px;
          background-color: white;
          border-radius: 10px;
          box-shadow: 0 8px 16px rgba(0,0,0,0.2);
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        .chatbot-header {
          background-color: #16b28f;
          color: white;
          padding: 15px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .chatbot-close {
          background: none;
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          padding: 0;
          margin: 0;
          width: 30px;
          height: 30px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .chatbot-messages {
          flex: 1;
          overflow-y: auto;
          padding: 15px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .chatbot-welcome {
          color: #666;
          font-style: italic;
          text-align: center;
          padding: 20px 0;
        }

        .chatbot-message {
          max-width: 80%;
          padding: 10px 15px;
          border-radius: 18px;
          position: relative;
        }

        .user-message {
          align-self: flex-end;
          background-color: #e3f2fd;
          border-bottom-right-radius: 5px;
        }

        .bot-message {
          align-self: flex-start;
          background-color: #f5f5f5;
          border-bottom-left-radius: 5px;
        }

        .message-content {
          word-wrap: break-word;
        }

        .message-timestamp {
          font-size: 0.7em;
          color: #999;
          text-align: right;
          margin-top: 5px;
        }

        .typing-indicator {
          display: flex;
          align-items: center;
        }

        .typing-indicator span {
          height: 8px;
          width: 8px;
          background-color: #999;
          border-radius: 50%;
          display: inline-block;
          margin: 0 2px;
          animation: typing 1.4s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(1) {
          animation-delay: -0.32s;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: -0.16s;
        }

        @keyframes typing {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }

        .selected-text-preview {
          background-color: #fff3cd;
          border: 1px solid #ffeaa7;
          border-radius: 5px;
          padding: 8px 12px;
          margin: 10px 15px 0;
          font-size: 0.9em;
          color: #856404;
        }

        .chatbot-input-area {
          padding: 15px;
          border-top: 1px solid #eee;
          display: flex;
          flex-direction: column;
        }

        .chatbot-input {
          width: 100%;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 5px;
          resize: none;
          margin-bottom: 10px;
          font-family: inherit;
        }

        .chatbot-send-button {
          align-self: flex-end;
          padding: 8px 15px;
          background-color: #16b28f;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
        }

        .chatbot-send-button:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
};

export default Chatbot;