# Quickstart: AIBOOK ChatKit UI Frontend (Layer-2)

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Docusaurus 3.x project set up
- OpenAI ChatKit account (for production use)

## ChatKit Setup

Before implementing the UI, you need to set up ChatKit in your product following the official documentation: https://platform.openai.com/docs/guides/chatkit

### Key Setup Steps:
1. Create an OpenAI account and navigate to the ChatKit dashboard
2. Create a new ChatKit project
3. Obtain your API keys and project configuration
4. Set up your client authentication method
5. Configure your rate limits and usage settings

## Installation

### 1. Install Dependencies

```bash
npm install @openai/chatkit-react
npm install @radix-ui/react-* # shadcn/ui components as needed
```

### 2. Create Component Structure

Create the following directory and files:

```
src/
├── components/
│   └── Chatbot/
│       ├── ChatContainer.tsx
│       ├── ChatWidget.tsx
│       ├── SelectionTooltip.tsx
│       ├── Mascot.tsx
│       └── types.ts
├── hooks/
│   └── useTextSelection.ts
└── client-modules/
    └── Root.js
```

### 3. Create TypeScript Types

In `src/components/Chatbot/types.ts`:

```typescript
export interface SelectedText {
  id: string;
  content: string;
  timestamp: Date;
  position: { x: number; y: number };
  context: string;
}

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
}

export interface ChatState {
  isOpen: boolean;
  selectedText: SelectedText | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}

export interface TooltipState {
  isVisible: boolean;
  position: { x: number; y: number };
  selectedText: string;
  targetElement: HTMLElement | null;
}
```

### 4. Implement Core Components

#### ChatContainer.tsx (SSR Safe Wrapper)
```tsx
import { BrowserOnly } from '@docusaurus/core/lib/client/exports/BrowserOnly';

const ChatContainer = () => {
  return (
    <BrowserOnly fallback={<div />}>
      {() => {
        const ChatWidget = require('./ChatWidget').default;
        return <ChatWidget />;
      }}
    </BrowserOnly>
  );
};

export default ChatContainer;
```

#### SelectionTooltip.tsx
```tsx
import React, { useState, useEffect } from 'react';
import { TooltipState } from './types';

const SelectionTooltip = ({ onAskAI }: { onAskAI: (text: string) => void }) => {
  const [state, setState] = useState<TooltipState>({
    isVisible: false,
    position: { x: 0, y: 0 },
    selectedText: '',
    targetElement: null
  });

  // Implementation for detecting text selection and showing tooltip
  // ...

  return state.isVisible ? (
    <div
      className="fixed bg-violet-600 text-white px-4 py-2 rounded-full shadow-lg cursor-pointer hover:bg-violet-700 transition-colors z-50"
      style={{ left: state.position.x, top: state.position.y }}
      onClick={() => onAskAI(state.selectedText)}
    >
      Ask AI
    </div>
  ) : null;
};

export default SelectionTooltip;
```

### 5. Integrate with Docusaurus Root

In `src/client-modules/Root.js`:

```js
import React from 'react';
import ChatContainer from '../components/Chatbot/ChatContainer';

export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatContainer />
    </>
  );
}
```

### 6. ChatKit SDK Integration

For the actual ChatKit integration, you'll need to implement the proper initialization following the ChatKit documentation:

```tsx
import { useChatKit } from '@openai/chatkit-react';

// For development, use mock initialization
const useMockChatKit = () => {
  // Mock implementation for UI development
  return {
    messages: [],
    sendMessage: () => {},
    isConnected: true,
    // Add other required properties for the UI
  };
};

// In production, replace with actual ChatKit initialization
const useActualChatKit = () => {
  // Follow the official ChatKit setup guide:
  // https://platform.openai.com/docs/guides/chatkit
  return useChatKit({
    // Configuration based on your ChatKit setup
  });
};
```

### 7. Mock SDK Initialization (For UI Development)

For UI development without a live backend, create a mock implementation:

```tsx
// In your ChatWidget component
const mockGetClientSecret = () => {
  return "mock-client-secret"; // This is safe for UI development
};

// Mock chat functionality for UI development
const useMockChat = () => {
  // Implementation that simulates ChatKit behavior for UI development
  // This allows UI development without a live ChatKit backend
};
```

## Running the Application

1. Start your Docusaurus development server:
```bash
npm run start
```

2. The chatbot widget should appear in the bottom-right corner
3. Select text anywhere on the page to see the "Ask AI" tooltip
4. Click the tooltip to open the chat with the selected text as context

## Testing

### Unit Tests
```bash
npm run test
```

### Accessibility Testing
- Test keyboard navigation
- Verify ARIA labels
- Check screen reader compatibility

### Responsive Testing
- Test on mobile devices
- Verify tooltip positioning
- Check chat widget layout on different screen sizes