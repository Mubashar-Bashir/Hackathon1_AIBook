import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import styles from './PersonalizationToggle.module.css';

interface PersonalizationToggleProps {
  content: string;
  chapterId: string;
  onContentChange: (content: string) => void;
}

const PersonalizationToggle: React.FC<PersonalizationToggleProps> = ({
  content,
  chapterId,
  onContentChange
}) => {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isClient, setIsClient] = useState(false);

  // Mark as client-side after mounting
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Don't render anything during SSR to avoid auth context issues
  if (!isClient) {
    return null;
  }

  const { isAuthenticated, user } = useAuth();

  useEffect(() => {
    // Reset to original content when personalization is turned off
    if (!isPersonalized) {
      onContentChange(content);
    }
  }, [isPersonalized, content, onContentChange]);

  const handleToggle = async () => {
    if (!isAuthenticated) {
      setError('Please log in to use personalization features');
      return;
    }

    if (!isPersonalized) {
      // Turn on personalization
      setIsProcessing(true);
      setError(null);

      try {
        const backendUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
        const response = await fetch(`${backendUrl}/api/personalization/apply`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            content,
            user_background: user?.background, // Use user's background level
            personalization_type: 'all'
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to personalize content');
        }

        const data = await response.json();
        onContentChange(data.personalized_content);
        setIsPersonalized(true);
      } catch (err) {
        console.error('Personalization error:', err);
        setError(err instanceof Error ? err.message : 'Failed to personalize content');
      } finally {
        setIsProcessing(false);
      }
    } else {
      // Turn off personalization
      onContentChange(content);
      setIsPersonalized(false);
    }
  };

  // Show login notice if not authenticated
  if (!isAuthenticated) {
    return (
      <div className={styles.personalizationNotice}>
        <p>
          <a href="/login">Log in</a> to personalize this content based on your background.
        </p>
      </div>
    );
  }

  return (
    <div className={styles.personalizationToggle}>
      <div className={styles.toggleContainer}>
        <label className={styles.toggleLabel}>
          <input
            type="checkbox"
            checked={isPersonalized}
            onChange={handleToggle}
            disabled={isProcessing}
            className={styles.toggleCheckbox}
          />
          <span className={styles.toggleSlider}></span>
          <span className={styles.toggleText}>
            {isProcessing
              ? 'Personalizing...'
              : isPersonalized
                ? 'Personalized Content'
                : 'Personalize Content'}
          </span>
        </label>
      </div>

      {error && (
        <div className={styles.personalizationError}>
          {error}
        </div>
      )}
    </div>
  );
};

export default PersonalizationToggle;