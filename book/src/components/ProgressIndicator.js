import React from 'react';
import clsx from 'clsx';

import styles from './ProgressIndicator.module.css';

function ProgressIndicator({ percentage, label }) {
  const progress = Math.max(0, Math.min(100, percentage)); // Ensure percentage is between 0 and 100

  return (
    <div className={styles.progressContainer} role="progressbar" aria-valuenow={progress} aria-valuemin="0" aria-valuemax="100">
      {label && <span className={styles.progressLabel}>{label}</span>}
      <div className={styles.progressBarBackground}>
        <div
          className={clsx(styles.progressBarFill, {
            [styles.isComplete]: progress === 100,
          })}
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <span className={styles.progressText}>{progress}%</span>
    </div>
  );
}

export default ProgressIndicator;
