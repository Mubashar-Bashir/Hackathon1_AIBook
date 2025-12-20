import React from 'react';
import Layout from '@theme/Layout';
import RAGMonitor from '../components/RAGMonitor';
import styles from './rag-monitor.module.css';

function RAGMonitorPage() {
  return (
    <Layout title="RAG Pipeline Monitor" description="Real-time monitoring of RAG content pipeline">
      <div className={styles.container}>
        <div className="container margin-vert--lg">
          <div className="row">
            <div className="col col--12">
              <h1 className={styles.title}>RAG Pipeline Monitor</h1>
              <p className={styles.description}>
                Real-time visualization of the RAG content pipeline progress. Monitor document fetching,
                embedding generation, and vector storage processes.
              </p>

              <div className={styles.monitorSection}>
                <RAGMonitor />
              </div>

              <div className={styles.infoSection}>
                <h2>About the RAG Pipeline</h2>
                <div className={styles.infoGrid}>
                  <div className={styles.infoCard}>
                    <h3>Document Fetching</h3>
                    <p>Retrieves content from the textbook website using sitemap or direct URLs. Processes HTML content and extracts text for further processing.</p>
                  </div>
                  <div className={styles.infoCard}>
                    <h3>Embedding Generation</h3>
                    <p>Converts text chunks into vector embeddings using Cohere's embedding models. These embeddings capture semantic meaning for similarity search.</p>
                  </div>
                  <div className={styles.infoCard}>
                    <h3>Vector Storage</h3>
                    <p>Stores embeddings in Qdrant vector database with metadata for fast similarity search during RAG queries.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default RAGMonitorPage;