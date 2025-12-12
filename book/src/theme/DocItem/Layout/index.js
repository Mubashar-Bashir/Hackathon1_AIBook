import React, { useState, useEffect } from 'react';
import DocItemLayout from '@theme-original/DocItem/Layout';
import TranslationToggle from '@site/src/components/TranslationToggle';
import PersonalizationToggle from '@site/src/components/PersonalizationToggle';

// Enhanced layout for documentation items that includes translation and personalization
export default function DocItemLayoutEnhancer(props) {
  const [originalContent, setOriginalContent] = useState('');
  const [currentContent, setCurrentContent] = useState('');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const handleContentChange = (newContent) => {
    setCurrentContent(newContent);
  };

  // Safely access metadata - check if props.content exists
  const metadata = (props.content && props.content.metadata) ? props.content.metadata : {};

  return (
    <>
      <DocItemLayout {...props} />

      {/* Only render enhanced controls on client side to avoid SSR issues */}
      {isClient && (
        <div style={{
          marginTop: '30px',
          paddingTop: '20px',
          borderTop: '1px solid #e0e0e0',
          backgroundColor: '#f9f9f9',
          borderRadius: '8px',
          padding: '15px'
        }}>
          <h4>Enhance this content:</h4>

          <div style={{
            display: 'flex',
            gap: '15px',
            flexWrap: 'wrap',
            alignItems: 'center'
          }}>
            <div style={{ flex: '1', minWidth: '250px' }}>
              <PersonalizationToggle
                content={originalContent}
                chapterId={metadata?.frontMatter?.id || metadata?.unversionedId || ''}
                onContentChange={handleContentChange}
              />
            </div>

            <div style={{ flex: '1', minWidth: '250px' }}>
              <TranslationToggle
                content={originalContent}
                chapterId={metadata?.frontMatter?.id || metadata?.unversionedId || ''}
                onContentChange={handleContentChange}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}