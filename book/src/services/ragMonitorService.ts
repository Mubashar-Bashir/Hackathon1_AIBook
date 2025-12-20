/**
 * RAG Monitor Service
 * Provides functions to interact with the RAG monitoring API
 */

interface RAGProgressUpdate {
  job_id: string;
  status: string;
  step: string;
  progress: number;
  total: number;
  completed: number;
  errors: number;
  message: string;
  metadata: any;
}

interface RAGStatus {
  current_job_id: string | null;
  status: string;
  progress: number;
  current_step: number;
  total_steps: number;
  step_details: {
    fetching: StepDetails;
    embedding: StepDetails;
    storing: StepDetails;
  };
  metadata: {
    total_documents: number;
    total_chunks: number;
    total_embeddings: number;
    start_time: string | null;
    end_time: string | null;
  };
  active_connections: any[];
}

interface StepDetails {
  status: string;
  progress: number;
  total: number;
  completed: number;
  errors: number;
}

interface VectorStats {
  collection_name: string;
  total_vectors: number;
  status: string;
  error?: string;
}

class RAGMonitorService {
  private baseUrl: string;
  private ws: WebSocket | null = null;

  constructor() {
    this.baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  }

  /**
   * Get current RAG pipeline status
   */
  async getRAGStatus(): Promise<RAGStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/api/monitor/rag-status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching RAG status:', error);
      throw error;
    }
  }

  /**
   * Get vector store statistics
   */
  async getVectorStats(): Promise<VectorStats> {
    try {
      const response = await fetch(`${this.baseUrl}/api/monitor/vector-stats`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching vector stats:', error);
      throw error;
    }
  }

  /**
   * Connect to WebSocket for real-time updates
   */
  connectWebSocket(onMessage: (data: RAGProgressUpdate) => void, onError?: (error: Event) => void): WebSocket {
    const wsUrl = `${this.baseUrl.replace('http', 'ws')}/api/monitor/rag-progress`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('Connected to RAG monitor WebSocket');
    };

    this.ws.onmessage = (event) => {
      try {
        const data: RAGProgressUpdate = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) {
        onError(error);
      }
    };

    this.ws.onclose = () => {
      console.log('Disconnected from RAG monitor WebSocket');
      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        this.connectWebSocket(onMessage, onError);
      }, 5000);
    };

    return this.ws;
  }

  /**
   * Disconnect from WebSocket
   */
  disconnectWebSocket() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Trigger a content pipeline job
   */
  async triggerContentPipeline(base_url: string, sitemap_url?: string, urls?: string[]): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/content/fetch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          base_url,
          sitemap_url,
          urls
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error triggering content pipeline:', error);
      throw error;
    }
  }
}

export default new RAGMonitorService();