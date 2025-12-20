import React, { createContext, useContext, useReducer } from 'react';
import ChatService from '../../services/ChatService';

// Define the initial state based on the data model
const initialState = {
  isOpen: false,
  minimized: false,
  position: { x: null, y: null },
  messages: [],
  context: {
    pageTitle: '',
    pageRoute: '',
    selectedText: '',
    lastUpdated: new Date()
  },
  isVisible: false,
  unreadCount: 0,
  isLoading: false
};

// Define the reducer to handle state changes
const chatReducer = (state, action) => {
  switch (action.type) {
    case 'SET_OPEN':
      return {
        ...state,
        isOpen: true,
        isVisible: true,
        unreadCount: 0
      };
    case 'SET_CLOSED':
      return {
        ...state,
        isOpen: false,
        isVisible: false
      };
    case 'SET_MINIMIZED':
      return {
        ...state,
        minimized: action.minimized
      };
    case 'SET_POSITION':
      return {
        ...state,
        position: action.position
      };
    case 'SET_MESSAGES':
      return {
        ...state,
        messages: action.messages
      };
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.message],
        unreadCount: state.isOpen ? state.unreadCount : state.unreadCount + 1
      };
    case 'SET_CONTEXT':
      return {
        ...state,
        context: {
          ...state.context,
          ...action.context
        }
      };
    case 'SET_UNREAD_COUNT':
      return {
        ...state,
        unreadCount: action.count
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.isLoading
      };
    case 'RESET_CHAT':
      return initialState;
    default:
      return state;
  }
};

// Create the context
const ChatContext = createContext();

// Provider component
export const ChatServiceProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Actions
  const openChat = () => {
    dispatch({ type: 'SET_OPEN' });
  };

  const closeChat = () => {
    dispatch({ type: 'SET_CLOSED' });
  };

  const toggleChat = () => {
    if (state.isOpen) {
      closeChat();
    } else {
      openChat();
    }
  };

  const minimizeChat = (minimized) => {
    dispatch({ type: 'SET_MINIMIZED', minimized });
  };

  const setPosition = (position) => {
    dispatch({ type: 'SET_POSITION', position });
  };

  const setMessages = (messages) => {
    dispatch({ type: 'SET_MESSAGES', messages });
  };

  const addMessage = (message) => {
    dispatch({ type: 'ADD_MESSAGE', message });
  };

  const setContext = (context) => {
    dispatch({ type: 'SET_CONTEXT', context });
  };

  const setUnreadCount = (count) => {
    dispatch({ type: 'SET_UNREAD_COUNT', count });
  };

  const resetChat = () => {
    dispatch({ type: 'RESET_CHAT' });
  };

  const setIsLoading = (isLoading) => {
    dispatch({ type: 'SET_LOADING', isLoading });
  };

  // Load initial messages when provider mounts
  React.useEffect(() => {
    const loadInitialMessages = async () => {
      try {
        const initialMessages = await ChatService.getInitialMessages();
        setMessages(initialMessages);
      } catch (error) {
        console.error('Error loading initial messages:', error);
        // Still set initial state to ensure the chat context works even if service fails
        setMessages([]);
      }
    };

    loadInitialMessages();
  }, []);

  const value = {
    ...state,
    openChat,
    closeChat,
    toggleChat,
    minimizeChat,
    setPosition,
    setMessages,
    addMessage,
    setContext,
    setUnreadCount,
    resetChat,
    setIsLoading
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatServiceProvider');
  }
  return context;
};

export default ChatContext;