import React, { useState, useEffect } from 'react';
import styles from './RAGMonitor.module.css';

const RAGMonitor = () => {
  const [ws, setWs] = useState(null);
  const [status, setStatus] = useState({
    current_job_id: null,
    status: 'idle',
    progress: 0,
    current_step: 0,
    total_steps: 3,
    step_details: {
      fetching: { status: 'pending', progress: 0, total: 0, completed: 0, errors: 0 },
      embedding: { status: 'pending', progress: 0, total: 0, completed: 0, errors: 0 },
      storing: { status: 'pending', progress: 0, total: 0, completed: 0, errors: 0 }
    },
    metadata: {
      total_documents: 0,
      total_chunks: 0,
      total_embeddings: 0,
      start_time: null,
      end_time: null
    }
  });
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    const websocket = new WebSocket('ws://localhost:8000/api/monitor/rag-progress');

    websocket.onopen = () => {
      console.log('Connected to RAG monitor');
      setIsConnected(true);
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(prevStatus => ({
        ...prevStatus,
        current_job_id: data.job_id,
        status: data.status,
        progress: data.progress,
        step_details: {
          ...prevStatus.step_details,
          [data.step]: {
            ...prevStatus.step_details[data.step],
            progress: data.progress,
            total: data.total,
            completed: data.completed,
            errors: data.errors,
            status: data.status === 'completed' ? 'completed' :
                   prevStatus.step_details[data.step].status === 'pending' ? 'in_progress' :
                   prevStatus.step_details[data.step].status
          }
        },
        metadata: data.metadata
      }));
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    websocket.onclose = () => {
      console.log('Disconnected from RAG monitor');
      setIsConnected(false);
    };

    setWs(websocket);

    // Cleanup on unmount
    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  const getStepStatus = (stepName) => {
    const step = status.step_details[stepName];
    if (step.status === 'completed') return 'completed';
    if (step.status === 'in_progress') return 'in-progress';
    return 'pending';
  };

  const getStepIcon = (stepName) => {
    const status = getStepStatus(stepName);
    switch(status) {
      case 'completed': return '✓';
      case 'in-progress': return '🔄';
      default: return '○';
    }
  };

  const getStepColor = (stepName) => {
    const status = getStepStatus(stepName);
    switch(status) {
      case 'completed': return '#00ff8c'; // cyber green
      case 'in-progress': return '#00f0ff'; // cyber cyan
      default: return '#666';
    }
  };

  const getProgressPercentage = (stepName) => {
    const step = status.step_details[stepName];
    return step.total > 0 ? Math.round((step.completed / step.total) * 100) : 0;
  };

  const [baseURL, setBaseURL] = useState('https://book-20sb9ub9v-mubashar-bashirs-projects.vercel.app');
  const [sitemapURL, setSitemapURL] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [pipelineStatus, setPipelineStatus] = useState('');

  const triggerContentPipeline = async () => {
    if (!baseURL) {
      alert('Please enter a base URL');
      return;
    }

    setIsProcessing(true);
    setPipelineStatus('Starting pipeline...');

    try {
      const response = await fetch('http://localhost:8000/api/content/fetch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          base_url: baseURL,
          sitemap_url: sitemapURL || null
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPipelineStatus('Pipeline started successfully!');

      // Update the monitoring status
      setStatus(prevStatus => ({
        ...prevStatus,
        status: 'fetching',
        progress: 0,
        current_step: 1,
        step_details: {
          fetching: { status: 'in_progress', progress: 0, total: 0, completed: 0, errors: 0 },
          embedding: { status: 'pending', progress: 0, total: 0, completed: 0, errors: 0 },
          storing: { status: 'pending', progress: 0, total: 0, completed: 0, errors: 0 }
        }
      }));
    } catch (error) {
      console.error('Error triggering content pipeline:', error);
      setPipelineStatus(`Error: ${(error as Error).message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className={styles.ragMonitorContainer}>
      <div className={styles.monitorHeader}>
        <h2>RAG Pipeline Monitor</h2>
        <div className={`${styles.connectionStatus} ${isConnected ? styles.connected : styles.disconnected}`}>
          {isConnected ? '● Connected' : '● Disconnected'}
        </div>
      </div>

      {/* Pipeline Control Panel */}
      <div className={styles.controlPanel}>
        <h3>Start Content Pipeline</h3>
        <div className={styles.inputGroup}>
          <label htmlFor="baseURL" className={styles.label}>Base URL:</label>
          <input
            type="url"
            id="baseURL"
            value={baseURL}
            onChange={(e) => setBaseURL(e.target.value)}
            placeholder="Enter base URL to crawl (e.g., https://example.com)"
            className={styles.input}
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="sitemapURL" className={styles.label}>Sitemap URL (optional):</label>
          <input
            type="url"
            id="sitemapURL"
            value={sitemapURL}
            onChange={(e) => setSitemapURL(e.target.value)}
            placeholder="Enter sitemap URL if available (e.g., https://example.com/sitemap.xml)"
            className={styles.input}
          />
        </div>
        <button
          onClick={triggerContentPipeline}
          disabled={isProcessing}
          className={`${styles.startButton} ${isProcessing ? styles.disabled : ''}`}
        >
          {isProcessing ? 'Processing...' : 'Start Pipeline'}
        </button>
        {pipelineStatus && (
          <div className={styles.pipelineStatusMessage}>
            {pipelineStatus}
          </div>
        )}
      </div>

      <div className={styles.pipelineStatus}>
        <div className={styles.statusCard}>
          <h3>Overall Pipeline Status</h3>
          <div className={styles.statusText}>
            <span className={styles.statusValue}>{status.status}</span>
            <span className={styles.progressValue}>{status.progress}%</span>
          </div>
          <div className={styles.progressBar}>
            <div
              className={styles.progressFill}
              style={{
                width: `${status.progress}%`,
                background: `linear-gradient(90deg, #00f0ff, #00ff8c)`
              }}
            ></div>
          </div>
        </div>

        <div className={styles.metadataCard}>
          <h3>Processing Metadata</h3>
          <div className={styles.metadataGrid}>
            <div className={styles.metadataItem}>
              <span className={styles.metadataLabel}>Total Documents:</span>
              <span className={styles.metadataValue}>{status.metadata.total_documents}</span>
            </div>
            <div className={styles.metadataItem}>
              <span className={styles.metadataLabel}>Total Chunks:</span>
              <span className={styles.metadataValue}>{status.metadata.total_chunks}</span>
            </div>
            <div className={styles.metadataItem}>
              <span className={styles.metadataLabel}>Total Embeddings:</span>
              <span className={styles.metadataValue}>{status.metadata.total_embeddings}</span>
            </div>
            <div className={styles.metadataItem}>
              <span className={styles.metadataLabel}>Start Time:</span>
              <span className={styles.metadataValue}>
                {status.metadata.start_time ? new Date(status.metadata.start_time).toLocaleTimeString() : 'N/A'}
              </span>
            </div>
            <div className={styles.metadataItem}>
              <span className={styles.metadataLabel}>End Time:</span>
              <span className={styles.metadataValue}>
                {status.metadata.end_time ? new Date(status.metadata.end_time).toLocaleTimeString() : 'N/A'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.pipelineSteps}>
        <h3>Pipeline Steps</h3>

        {/* Fetching Step */}
        <div className={styles.stepCard}>
          <div className={styles.stepHeader}>
            <div className={styles.stepIcon} style={{color: getStepColor('fetching')}}>
              {getStepIcon('fetching')}
            </div>
            <div className={styles.stepTitle}>Document Fetching</div>
            <div className={styles.stepStatus}>{getStepStatus('fetching')}</div>
          </div>
          <div className={styles.stepDetails}>
            <div className={styles.stepProgress}>
              <div className={styles.progressInfo}>
                <span>Progress: {status.step_details.fetching.completed}/{status.step_details.fetching.total}</span>
                <span>Errors: {status.step_details.fetching.errors}</span>
              </div>
              <div className={styles.progressBar}>
                <div
                  className={styles.progressFill}
                  style={{
                    width: `${getProgressPercentage('fetching')}%`,
                    background: getStepColor('fetching')
                  }}
                ></div>
              </div>
              <div className={styles.progressPercentage}>{getProgressPercentage('fetching')}%</div>
            </div>
          </div>
        </div>

        {/* Embedding Step */}
        <div className={styles.stepCard}>
          <div className={styles.stepHeader}>
            <div className={styles.stepIcon} style={{color: getStepColor('embedding')}}>
              {getStepIcon('embedding')}
            </div>
            <div className={styles.stepTitle}>Embedding Generation</div>
            <div className={styles.stepStatus}>{getStepStatus('embedding')}</div>
          </div>
          <div className={styles.stepDetails}>
            <div className={styles.stepProgress}>
              <div className={styles.progressInfo}>
                <span>Progress: {status.step_details.embedding.completed}/{status.step_details.embedding.total}</span>
                <span>Errors: {status.step_details.embedding.errors}</span>
              </div>
              <div className={styles.progressBar}>
                <div
                  className={styles.progressFill}
                  style={{
                    width: `${getProgressPercentage('embedding')}%`,
                    background: getStepColor('embedding')
                  }}
                ></div>
              </div>
              <div className={styles.progressPercentage}>{getProgressPercentage('embedding')}%</div>
            </div>
          </div>
        </div>

        {/* Storing Step */}
        <div className={styles.stepCard}>
          <div className={styles.stepHeader}>
            <div className={styles.stepIcon} style={{color: getStepColor('storing')}}>
              {getStepIcon('storing')}
            </div>
            <div className={styles.stepTitle}>Vector Storage</div>
            <div className={styles.stepStatus}>{getStepStatus('storing')}</div>
          </div>
          <div className={styles.stepDetails}>
            <div className={styles.stepProgress}>
              <div className={styles.progressInfo}>
                <span>Progress: {status.step_details.storing.completed}/{status.step_details.storing.total}</span>
                <span>Errors: {status.step_details.storing.errors}</span>
              </div>
              <div className={styles.progressBar}>
                <div
                  className={styles.progressFill}
                  style={{
                    width: `${getProgressPercentage('storing')}%`,
                    background: getStepColor('storing')
                  }}
                ></div>
              </div>
              <div className={styles.progressPercentage}>{getProgressPercentage('storing')}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RAGMonitor;