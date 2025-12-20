import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import styles from './TranslationToggle.module.css';

interface TranslationToggleProps {
  content: string;
  chapterId: string;
  onContentChange: (content: string) => void;
}

const TranslationToggle: React.FC<TranslationToggleProps> = ({
  content,
  chapterId,
  onContentChange
}) => {
  const [isTranslated, setIsTranslated] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentLang, setCurrentLang] = useState('en');
  const [isClient, setIsClient] = useState(false);

  // Mark as client-side after mounting
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Don't render anything during SSR to avoid auth context issues
  if (!isClient) {
    return null;
  }

  const { isAuthenticated } = useAuth();

  useEffect(() => {
    // Reset to original content when translation is turned off
    if (!isTranslated) {
      onContentChange(content);
      setCurrentLang('en');
    }
  }, [isTranslated, content, onContentChange]);

  const handleToggle = async () => {
    if (!isAuthenticated) {
      setError('Please log in to use translation features');
      return;
    }

    if (!isTranslated) {
      // Translate to Urdu
      setIsProcessing(true);
      setError(null);

      try {
        const backendUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
        const response = await fetch(`${backendUrl}/api/translation/translate-chapter`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify({
            chapter_content: content,
            target_language: 'ur'
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to translate content');
        }

        const data = await response.json();
        onContentChange(data.translated_content);
        setIsTranslated(true);
        setCurrentLang('ur');
      } catch (err) {
        console.error('Translation error:', err);
        setError(err instanceof Error ? err.message : 'Failed to translate content');
      } finally {
        setIsProcessing(false);
      }
    } else {
      // Translate back to English
      setIsProcessing(true);
      setError(null);

      try {
        const response = await fetch('http://localhost:8000/api/translation/translate-chapter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify({
            chapter_content: content, // This is already the Urdu content
            target_language: 'en'
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to translate content');
        }

        const data = await response.json();
        onContentChange(data.translated_content);
        setIsTranslated(false);
        setCurrentLang('en');
      } catch (err) {
        console.error('Translation error:', err);
        setError(err instanceof Error ? err.message : 'Failed to translate content');
      } finally {
        setIsProcessing(false);
      }
    }
  };

  if (!isAuthenticated) {
    return (
      <div className={styles.translationNotice}>
        <p>
          <a href="/login">Log in</a> to translate this content to Urdu.
        </p>
      </div>
    );
  }

  return (
    <div className={styles.translationToggle}>
      <div className={styles.toggleContainer}>
        <label className={styles.toggleLabel}>
          <input
            type="checkbox"
            checked={isTranslated}
            onChange={handleToggle}
            disabled={isProcessing}
            className={styles.toggleCheckbox}
          />
          <span className={styles.toggleSlider}></span>
          <span className={styles.toggleText}>
            {isProcessing
              ? 'Translating...'
              : isTranslated
                ? 'Urdu Translation'
                : 'Translate to Urdu'}
          </span>
        </label>
      </div>

      {error && (
        <div className={styles.translationError}>
          {error}
        </div>
      )}
    </div>
  );
};

export default TranslationToggle;