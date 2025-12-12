import React from 'react';
import { loadAllUserProgress, loadBookOverallProgress } from '../utils/progressStorage';
import ProgressIndicator from './ProgressIndicator';

import styles from './UserDashboard.module.css';

function UserDashboard() {
  const allProgress = loadAllUserProgress();
  const bookIds = Object.keys(allProgress);

  if (bookIds.length === 0) {
    return (
      <div className={styles.dashboardContainer}>
        <p>Start reading a book to see your progress here!</p>
      </div>
    );
  }

  return (
    <div className={styles.dashboardContainer}>
      {bookIds.map(bookId => {
        const overallProgress = loadBookOverallProgress(bookId);
        // Basic title extraction - would need more robust mapping for real titles
        const bookTitle = bookId.replace('AIBook', 'Physical AI & Humanoid Robotics Textbook').replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

        return (
          <div key={bookId} className={styles.bookProgressItem}>
            <h3>{bookTitle}</h3>
            <ProgressIndicator percentage={overallProgress} label="Overall Progress" />
            {/* Optionally, display chapter-level progress here */}
          </div>
        );
      })}
    </div>
  );
}

export default UserDashboard;
