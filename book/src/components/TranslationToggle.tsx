import React, { useState, useEffect } from 'react';

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
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsClient(true);

    // Check if we're in the browser and initialize auth state
    if (typeof window !== 'undefined' && window.location) {
      // Simulate auth check - in a real app, you'd check actual auth state
      try {
        // Check for auth tokens in localStorage
        const token = localStorage.getItem('authToken');
        if (token) {
          setIsAuthenticated(true);
        }
      } catch {
        setIsAuthenticated(false);
      }
    }
  }, []);

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
        const response = await fetch('http://localhost:8000/translate/chapter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify({
            text: content,
            source_lang: 'en',
            target_lang: 'ur'
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to translate content');
        }

        const data = await response.json();
        onContentChange(data.translated_text);
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
        const response = await fetch('http://localhost:8000/translate/chapter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify({
            text: content, // This is already the Urdu content
            source_lang: 'ur',
            target_lang: 'en'
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to translate content');
        }

        const data = await response.json();
        onContentChange(data.translated_text);
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

  // Don't render anything during SSR
  if (!isClient) {
    return null;
  }

  if (!isAuthenticated) {
    return (
      <div className="translation-notice">
        <p>
          <a href="/login">Log in</a> to translate this content to Urdu.
        </p>
      </div>
    );
  }

  return (
    <div className="translation-toggle">
      <div className="toggle-container">
        <label className="toggle-label">
          <input
            type="checkbox"
            checked={isTranslated}
            onChange={handleToggle}
            disabled={isProcessing}
            className="toggle-checkbox"
          />
          <span className="toggle-slider"></span>
          <span className="toggle-text">
            {isProcessing
              ? 'Translating...'
              : isTranslated
                ? 'Urdu Translation'
                : 'Translate to Urdu'}
          </span>
        </label>
      </div>

      {error && (
        <div className="translation-error">
          {error}
        </div>
      )}

      <style jsx>{`
        .translation-toggle {
          margin: 20px 0;
          padding: 15px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background-color: #f0f8ff;
        }

        .toggle-container {
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .toggle-label {
          display: flex;
          align-items: center;
          cursor: pointer;
          user-select: none;
          font-weight: 500;
        }

        .toggle-checkbox {
          opacity: 0;
          width: 0;
          height: 0;
        }

        .toggle-slider {
          position: relative;
          cursor: pointer;
          width: 50px;
          height: 24px;
          background-color: #ccc;
          border-radius: 24px;
          transition: background-color 0.3s;
          margin-right: 10px;
        }

        .toggle-slider:before {
          position: absolute;
          content: "";
          height: 18px;
          width: 18px;
          left: 3px;
          bottom: 3px;
          background-color: white;
          border-radius: 50%;
          transition: transform 0.3s;
        }

        .toggle-checkbox:checked + .toggle-slider {
          background-color: #16b28f;
        }

        .toggle-checkbox:checked + .toggle-slider:before {
          transform: translateX(26px);
        }

        .toggle-text {
          font-size: 14px;
        }

        .translation-notice {
          margin: 20px 0;
          padding: 15px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background-color: #fff3cd;
          color: #856404;
        }

        .translation-notice a {
          color: #16b28f;
          text-decoration: none;
          font-weight: bold;
        }

        .translation-notice a:hover {
          text-decoration: underline;
        }

        .translation-error {
          margin-top: 10px;
          padding: 10px;
          border: 1px solid #f5c6cb;
          border-radius: 4px;
          background-color: #f8d7da;
          color: #721c24;
          font-size: 14px;
        }
      `}</style>
    </div>
  );
};

export default TranslationToggle;