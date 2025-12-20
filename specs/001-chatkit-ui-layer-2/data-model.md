# Data Model: AIBOOK ChatKit UI Frontend (Layer-2)

## Core Entities

### SelectedText
- **id**: string (unique identifier for the selection session)
- **content**: string (the actual selected text, max 200 characters)
- **timestamp**: Date (when the text was selected)
- **position**: {x: number, y: number} (coordinates for tooltip positioning)
- **context**: string (additional context about where the selection occurred)

### ChatState
- **isOpen**: boolean (whether the chat widget is visible)
- **selectedText**: SelectedText (the text that triggered the chat)
- **messages**: Array<ChatMessage> (conversation history)
- **isLoading**: boolean (whether the chat is loading)
- **error**: string | null (any error messages)

### ChatMessage
- **id**: string (unique message identifier)
- **content**: string (the message text)
- **sender**: 'user' | 'ai' (who sent the message)
- **timestamp**: Date (when the message was sent)
- **status**: 'sent' | 'delivered' | 'error' (message delivery status)

### TooltipState
- **isVisible**: boolean (whether the tooltip is shown)
- **position**: {x: number, y: number} (coordinates for tooltip positioning)
- **selectedText**: string (the currently selected text)
- **targetElement**: HTMLElement | null (the element where text was selected)

## Validation Rules

### SelectedText Validation
- **contentMaxLength**: 200 characters maximum
- **contentRequired**: Must not be empty or whitespace only
- **positionValid**: Coordinates must be positive numbers

### ChatMessage Validation
- **contentRequired**: Message content must not be empty
- **senderValid**: Must be either 'user' or 'ai'
- **timestampRequired**: Must have a valid timestamp

### ChatState Validation
- **messagesMax**: Maximum 50 messages in history
- **selectedTextValid**: If provided, must be a valid SelectedText object

## State Transitions

### ChatState Transitions
1. **Initial** → **Idle**: Component mounts, no selection made
2. **Idle** → **TextSelected**: User selects text, tooltip appears
3. **TextSelected** → **ChatOpened**: User clicks tooltip, chat opens
4. **ChatOpened** → **ChatActive**: Chat is ready for interaction
5. **ChatActive** → **MessageSending**: User sends a message
6. **MessageSending** → **MessageReceived**: AI responds
7. **AnyState** → **Error**: Error occurs during operation
8. **AnyState** → **Closed**: Chat is closed

### TooltipState Transitions
1. **Hidden** → **Detecting**: User begins text selection
2. **Detecting** → **Visible**: Text selection completed, tooltip shows
3. **Visible** → **Hidden**: User clicks tooltip or selects elsewhere

## Relationships

### SelectedText → ChatState
- One SelectedText can initiate one ChatState
- SelectedText is embedded in ChatState as the initial context

### ChatState → ChatMessage
- One ChatState contains many ChatMessage objects
- Messages are ordered chronologically in the messages array

### ChatMessage → ChatState
- Each ChatMessage belongs to one ChatState
- Messages are part of the conversation history

## TypeScript Interfaces

```typescript
interface SelectedText {
  id: string;
  content: string;
  timestamp: Date;
  position: { x: number; y: number };
  context: string;
}

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  status: 'sent' | 'delivered' | 'error';
}

interface ChatState {
  isOpen: boolean;
  selectedText: SelectedText | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
}

interface TooltipState {
  isVisible: boolean;
  position: { x: number; y: number };
  selectedText: string;
  targetElement: HTMLElement | null;
}
```

## UI State Management

### Global State (Context)
- **ChatContext**: Manages the overall chat state across components
- **TooltipContext**: Manages tooltip visibility and positioning

### Local State (Component)
- **ChatWidget**: Manages input field, message list, and loading states
- **SelectionTooltip**: Manages visibility, positioning, and click handling
- **Mascot**: Manages animation states and visibility

## Event Flow

1. **Text Selection**: Browser Selection API detects text selection
2. **Position Calculation**: Coordinates calculated for tooltip placement
3. **State Update**: TooltipState updated to show tooltip
4. **User Interaction**: User clicks tooltip
5. **Context Transfer**: SelectedText passed to ChatState
6. **Chat Initialization**: ChatWidget opens with initial message
7. **Message Exchange**: User and AI exchange messages
8. **State Management**: ChatState updated with each message