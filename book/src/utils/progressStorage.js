const PROGRESS_STORAGE_KEY = 'bookProgress';

export const saveProgress = (bookId, chapterId, percentage) => {
  if (typeof window === 'undefined') return; // Ensure this runs only in browser

  try {
    const storedProgress = localStorage.getItem(PROGRESS_STORAGE_KEY);
    const allProgress = storedProgress ? JSON.parse(storedProgress) : {};

    if (!allProgress[bookId]) {
      allProgress[bookId] = { chapters: {}, overallPercentage: 0 };
    }
    if (!allProgress[bookId].chapters[chapterId]) {
      allProgress[bookId].chapters[chapterId] = { percentage: 0, lastReadAt: null };
    }

    allProgress[bookId].chapters[chapterId].percentage = percentage;
    allProgress[bookId].chapters[chapterId].lastReadAt = new Date().toISOString();

    // Recalculate overall percentage for the book (simple average for now)
    const chapterPercentages = Object.values(allProgress[bookId].chapters).map(c => c.percentage);
    const overall = chapterPercentages.reduce((sum, p) => sum + p, 0) / chapterPercentages.length;
    allProgress[bookId].overallPercentage = Math.round(overall);

    localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(allProgress));
    console.log(`Progress saved for ${bookId}/${chapterId}: ${percentage}%`);
  } catch (error) {
    console.error("Error saving progress to localStorage:", error);
  }
};

export const loadProgress = (bookId, chapterId) => {
  if (typeof window === 'undefined') return 0; // Ensure this runs only in browser

  try {
    const storedProgress = localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (storedProgress) {
      const allProgress = JSON.parse(storedProgress);
      if (allProgress[bookId] && allProgress[bookId].chapters[chapterId]) {
        return allProgress[bookId].chapters[chapterId].percentage;
      }
    }
  } catch (error) {
    console.error("Error loading progress from localStorage:", error);
  }
  return 0; // Default if no progress found
};

export const loadBookOverallProgress = (bookId) => {
  if (typeof window === 'undefined') return 0;

  try {
    const storedProgress = localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (storedProgress) {
      const allProgress = JSON.parse(storedProgress);
      if (allProgress[bookId]) {
        return allProgress[bookId].overallPercentage;
      }
    }
  } catch (error) {
    console.error("Error loading overall book progress from localStorage:", error);
  }
  return 0;
};

export const loadAllUserProgress = () => {
  if (typeof window === 'undefined') return {};

  try {
    const storedProgress = localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (storedProgress) {
      return JSON.parse(storedProgress);
    }
  } catch (error) {
    console.error("Error loading all user progress from localStorage:", error);
  }
  return {};
};
