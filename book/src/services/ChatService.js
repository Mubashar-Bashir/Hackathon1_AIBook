/**
 * Chat Service Implementation for AIBOOK
 * Provides chat functionality integrated with AIBOOK's backend
 */

// In-memory storage for messages and context
let messages = [];
let context = {
  pageTitle: '',
  pageRoute: '',
  selectedText: '',
  lastUpdated: new Date()
};

// Initialize with more realistic mock messages
const initialMessages = [
  {
    id: '1',
    content: 'Hello! I\'m your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?',
    sender: 'assistant',
    timestamp: new Date(Date.now() - 300000), // 5 minutes ago
    status: 'read',
    contextInfo: null
  },
  {
    id: '2',
    content: 'I can provide information about the textbook content and help answer your questions about Physical AI and Robotics.',
    sender: 'assistant',
    timestamp: new Date(Date.now() - 240000), // 4 minutes ago
    status: 'read',
    contextInfo: null
  },
  {
    id: '3',
    content: 'You can ask me about specific concepts, select text to ask about, or get explanations of complex topics.',
    sender: 'assistant',
    timestamp: new Date(Date.now() - 180000), // 3 minutes ago
    status: 'read',
    contextInfo: null
  }
];

// Initialize messages with initial data
messages = [...initialMessages];

export class ChatService {
  /**
   * Get initial messages
   * @returns {Promise<ChatMessage[]>} Promise resolving to array of chat messages
   */
  static async getInitialMessages() {
    return new Promise((resolve, reject) => {
      try {
        setTimeout(() => {
          resolve([...messages]);
        }, 100); // Simulate network delay
      } catch (error) {
        console.error('Error getting initial messages:', error);
        reject(error);
      }
    });
  }

  /**
   * Send a message to the backend
   * @param {string} content - Content of the message to send
   * @param {LocalContextData} [currentContext] - Current context to include with the message
   * @returns {Promise<ChatMessage>} Promise resolving to the sent message
   */
  static async sendMessage(content, currentContext = null) {
    return new Promise((resolve, reject) => {
      try {
        if (!content || typeof content !== 'string' || content.trim().length === 0) {
          throw new Error('Message content is required and must be a non-empty string');
        }

        const newMessage = {
          id: Date.now().toString(),
          content: content.trim(),
          sender: 'user',
          timestamp: new Date(),
          status: 'sent',
          contextInfo: currentContext || { ...context }
        };

        messages.push(newMessage);

        // Simulate API call to AIBOOK backend
        // In a real implementation, this would connect to AIBOOK's backend
        setTimeout(() => {
          const assistantResponse = {
            id: (Date.now() + 1).toString(),
            content: `I received your message: "${content.trim()}". Based on the context of page "${currentContext?.pageTitle || context.pageTitle}", I can provide more specific assistance about Physical AI & Humanoid Robotics.`,
            sender: 'assistant',
            timestamp: new Date(),
            status: 'sent',
            contextInfo: currentContext || { ...context }
          };
          messages.push(assistantResponse);
        }, 800); // Slightly longer delay to simulate backend processing

        setTimeout(() => {
          resolve(newMessage);
        }, 200); // Simulate network delay
      } catch (error) {
        console.error('Error sending message:', error);
        reject(error);
      }
    });
  }

  /**
   * Get current context
   * @returns {Promise<LocalContextData>} Promise resolving to current context data
   */
  static async getCurrentContext() {
    return new Promise((resolve, reject) => {
      try {
        setTimeout(() => {
          resolve({ ...context });
        }, 50); // Simulate async operation
      } catch (error) {
        console.error('Error getting current context:', error);
        reject(error);
      }
    });
  }

  /**
   * Update context when page changes
   * @param {LocalContextData} newContext - New context data to update
   */
  static updateContext(newContext) {
    context = {
      ...context,
      ...newContext,
      lastUpdated: new Date()
    };
  }

  /**
   * Reset messages for testing purposes
   */
  static resetMessages() {
    messages = [...initialMessages];
  }
}

export default ChatService;