import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

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
        const response = await fetch('http://localhost:8000/personalization/personalize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`
          },
          body: JSON.stringify({
            chapterId,
            userId: user?.userId,
            content
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to personalize content');
        }

        const data = await response.json();
        onContentChange(data.personalizedContent);
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

  if (!isAuthenticated) {
    return (
      <div className="personalization-notice">
        <p>
          <a href="/login">Log in</a> to personalize this content based on your background.
        </p>
      </div>
    );
  }

  return (
    <div className="personalization-toggle">
      <div className="toggle-container">
        <label className="toggle-label">
          <input
            type="checkbox"
            checked={isPersonalized}
            onChange={handleToggle}
            disabled={isProcessing}
            className="toggle-checkbox"
          />
          <span className="toggle-slider"></span>
          <span className="toggle-text">
            {isProcessing
              ? 'Personalizing...'
              : isPersonalized
                ? 'Personalized Content'
                : 'Personalize Content'}
          </span>
        </label>
      </div>

      {error && (
        <div className="personalization-error">
          {error}
        </div>
      )}

      <style jsx>{`
        .personalization-toggle {
          margin: 20px 0;
          padding: 15px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background-color: #f9f9f9;
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

        .personalization-notice {
          margin: 20px 0;
          padding: 15px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background-color: #fff3cd;
          color: #856404;
        }

        .personalization-notice a {
          color: #16b28f;
          text-decoration: none;
          font-weight: bold;
        }

        .personalization-notice a:hover {
          text-decoration: underline;
        }

        .personalization-error {
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

export default PersonalizationToggle;