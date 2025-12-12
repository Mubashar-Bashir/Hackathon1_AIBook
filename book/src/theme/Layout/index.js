import React from 'react';
import DefaultLayout from '@theme-original/Layout';
import { useLocation } from '@docusaurus/router';

// Function to detect if we're on a documentation page
function useIsDocPage() {
  const location = useLocation();
  return location.pathname.startsWith('/docs/');
}

// Wrapper layout that adds translation and personalization functionality
export default function Layout(props) {
  const isDocPage = useIsDocPage();

  return (
    <DefaultLayout {...props}>
      <>
        {props.children}

        {/* Add translation and personalization toggles for documentation pages only */}
        {isDocPage && (
          <div className="content-enhancement-controls" style={{
            position: 'sticky',
            bottom: '20px',
            zIndex: 100,
            padding: '10px',
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderRadius: '8px',
            boxShadow: '0 -2px 10px rgba(0,0,0,0.1)',
            display: 'flex',
            gap: '10px',
            justifyContent: 'center'
          }}>
            <div>Personalization Toggle Placeholder</div>
            <div>Translation Toggle Placeholder</div>
          </div>
        )}
      </>
    </DefaultLayout>
  );
}