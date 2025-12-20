import React, { useState, useEffect } from 'react';
import { useChatContext } from './ChatContext';
import ChatWindow from './ChatWindow';
import usePageContext from '../../hooks/usePageContext';
import useSelectedText from '../../hooks/useSelectedText';

const LessonAssistant = () => {
  const {
    isOpen,
    toggleChat,
    setContext,
    setPosition,
    position,
    context: currentContext
  } = useChatContext();

  const { pageTitle, pageRoute } = usePageContext();
  const selectedText = useSelectedText();
  const [isMinimized, setIsMinimized] = useState(false);

  // Update context when page context or selected text changes
  useEffect(() => {
    // Only update if the context values have actually changed
    if (currentContext.pageTitle !== pageTitle ||
        currentContext.pageRoute !== pageRoute ||
        currentContext.selectedText !== selectedText) {
      setContext({
        pageTitle,
        pageRoute,
        selectedText,
        lastUpdated: new Date()
      });
    }
  }, [pageTitle, pageRoute, selectedText, setContext, currentContext.pageTitle, currentContext.pageRoute, currentContext.selectedText]);

  // Set initial position if not set
  useEffect(() => {
    if (!position.x && !position.y) {
      setPosition({
        x: window.innerWidth - 320, // Position from right
        y: window.innerHeight - 200  // Position from bottom
      });
    }
  }, [setPosition, position]);

  // Handle window resize to keep chat within bounds
  useEffect(() => {
    const handleResize = () => {
      if (position.x && position.y) {
        setPosition({
          x: Math.min(position.x, window.innerWidth - 320),
          y: Math.min(position.y, window.innerHeight - 200)
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [position, setPosition]);

  // Handle keyboard navigation - allow opening/closing with keyboard
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Allow opening chat with Alt+Shift+C
      if (e.altKey && e.shiftKey && e.key === 'C') {
        e.preventDefault();
        toggleChat();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleChat]);

  if (isMinimized) {
    return (
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 9999,
          width: '40px',
          height: '40px',
          backgroundColor: 'purple',
          color: 'white',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.3)'
        }}
        onClick={() => setIsMinimized(false)}
      >
        M
      </div>
    );
  }

  if (!isOpen) {
    return (
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 9999,
          width: '64px',
          height: '64px',
          backgroundColor: '#7e22ce', // purple-700
          color: 'white',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0,0,0,0.3)'
        }}
        onClick={toggleChat}
      >
        🤖
      </div>
    );
  }

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 9999,
        width: '320px',
        height: '500px',
        backgroundColor: 'white',
        borderRadius: '16px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
        border: '1px solid #e2e8f0',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}
    >
      {/* Header */}
      <div style={{
        backgroundColor: '#7e22ce', // purple-700
        color: 'white',
        padding: '16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '12px',
            height: '12px',
            backgroundColor: '#4ade80', // green-400
            borderRadius: '50%',
            animation: 'pulse 2s infinite'
          }}></div>
          <h3 style={{ fontWeight: '600', fontSize: '14px' }}>{pageTitle || 'Current Lesson'}</h3>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setIsMinimized(true)}
            style={{
              padding: '4px',
              background: 'rgba(255,255,255,0.2)',
              borderRadius: '50%',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
            </svg>
          </button>
          <button
            onClick={toggleChat}
            style={{
              padding: '4px',
              background: 'rgba(255,255,255,0.2)',
              borderRadius: '50%',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Assistant Section */}
      <div style={{
        background: 'linear-gradient(to bottom, #ede9fe, #ddd6fe)', // purple-100 to purple-200
        padding: '16px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        {/* Assistant Avatar */}
        <div style={{ marginBottom: '16px' }}>
          <div style={{
            width: '64px',
            height: '64px',
            background: 'linear-gradient(to right, #8b5cf6, #a855f7)', // purple-500 to purple-600
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontSize: '24px',
            fontWeight: 'bold',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
          }}>
            AI
          </div>
        </div>

        {/* Prompt Bubble */}
        <div style={{
          textAlign: 'center',
          marginBottom: '16px'
        }}>
          <div style={{
            display: 'inline-block',
            backgroundColor: 'rgba(255,255,255,0.8)',
            backdropFilter: 'blur(4px)',
            borderRadius: '16px',
            padding: '8px 16px',
            fontSize: '14px',
            color: '#374151',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            Ask me about Physical AI & Robotics!
          </div>
        </div>
      </div>

      {/* Chat Window - Using existing ChatWindow component */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <ChatWindow onClose={toggleChat} />
      </div>
    </div>
  );
};

export default LessonAssistant;