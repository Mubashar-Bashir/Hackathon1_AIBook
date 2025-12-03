# Tasks: Docusaurus Frontend Features and Design Implementation

This document outlines the actionable, testable steps required to implement the Docusaurus frontend features and design as specified in `AIBook/specs/docusaurus-frontend/spec.md` and planned in `AIBook/specs/docusaurus-frontend/plan.md`.

## 1. Theme and Styling Implementation

*   [ ] **Task 1.1: Define Global CSS Variables for Theming**
    *   Define CSS variables for primary/secondary colors, text colors, background colors, and typography in `AIBook/book/src/css/custom.css`.
    *   Ensure variables support both light and dark modes.
    *   **Acceptance Criteria:** CSS variables are defined and can be toggled by Docusaurus's default theme switch.

*   [ ] **Task 1.2: Implement Custom Typography**
    *   Import chosen fonts (if any) and apply them to headings, body text, and code blocks via `AIBook/book/src/css/custom.css`.
    *   **Acceptance Criteria:** Fonts are correctly applied across the site.

*   [ ] **Task 1.3: Basic Docusaurus Theme Overrides**
    *   Adjust basic Docusaurus styling (e.g., link colors, button styles) in `AIBook/book/src/css/custom.css` to match the defined aesthetic.
    *   **Acceptance Criteria:** Core Docusaurus UI elements reflect the desired theme.

*   [ ] **Task 1.4 (Optional): Integrate Tailwind CSS**
    *   Install Tailwind CSS and configure Docusaurus PostCSS to process Tailwind directives.
    *   **Acceptance Criteria:** Tailwind utility classes can be used in React components and Markdown/MDX.

## 2. Main Page Layout Implementation

*   [ ] **Task 2.1: Create Custom Homepage Component**
    *   Create `AIBook/book/src/pages/index.js` (or `.tsx`) as a custom React component for the homepage.
    *   **Acceptance Criteria:** The custom component is rendered as the site's homepage.

*   [ ] **Task 2.2: Design Hero Section**
    *   Implement a hero section with a title, tagline, and a call-to-action button.
    *   **Acceptance Criteria:** Hero section is visually appealing and responsive.

*   [ ] **Task 2.3: Placeholder Sections for Book Categories**
    *   Add placeholder sections to highlight different book categories or featured content.
    *   **Acceptance Criteria:** Sections are structured for future content.

## 3. Navigation Components Implementation

*   [ ] **Task 3.1: Configure Docusaurus Sidebar Structure**
    *   Ensure `AIBook/book/sidebars.ts` (or `sidebars.js`) correctly defines the hierarchical structure for documentation/book content.
    *   **Acceptance Criteria:** Left sidebar displays correct book/chapter navigation.

*   [ ] **Task 3.2: Customize Navbar**
    *   Update `docusaurus.config.ts` to include relevant links (Home, Books, About) in the navbar.
    *   (Optional) Swizzle `Navbar` component for advanced layout/login button integration.
    *   **Acceptance Criteria:** Navbar contains desired links and is consistent with the theme.

*   [ ] **Task 3.3: Enable In-Page Table of Contents (TOC)**
    *   Verify that Docusaurus's default TOC is enabled and functioning on content pages.
    *   **Acceptance Criteria:** TOC appears on relevant pages for easy navigation.

## 4. Book Tracking/Completion Dashboard Implementation (Client-Side MVP)

*   [ ] **Task 4.1: Create `ProgressStorage` Utility (Client-Side)**
    *   Develop a utility (e.g., `AIBook/book/src/utils/progressStorage.js`) to save and retrieve user progress from `localStorage`.
    *   **Acceptance Criteria:** Functions for `saveProgress(bookId, chapterId, percentage)` and `loadProgress(bookId, chapterId)` are functional.

*   [ ] **Task 4.2: Develop `ProgressIndicator` Component**
    *   Create `AIBook/book/src/components/ProgressIndicator.js` (or `.tsx`) to display a progress bar for a single chapter/book.
    *   **Acceptance Criteria:** Component renders a progress bar based on input `percentage`.

*   [ ] **Task 4.3: Integrate Progress Tracking into DocItem**
    *   Swizzle the `DocItem` component (if necessary) or find an alternative way to inject logic to update progress when a user views a chapter/page.
    *   Use `ProgressStorage` to save progress when a user scrolls to the end or spends a certain amount of time on a page.
    *   **Acceptance Criteria:** Viewing a chapter updates its progress in `localStorage`.

*   [ ] **Task 4.4: Develop `UserDashboard` Component (Client-Side)**
    *   Create `AIBook/book/src/components/UserDashboard.js` (or `.tsx`) to display aggregated progress across multiple books/chapters from `localStorage`.
    *   **Acceptance Criteria:** Dashboard displays a list of books with their overall progress.

*   [ ] **Task 4.5: Integrate `UserDashboard` into Homepage**
    *   Embed the `UserDashboard` component into `AIBook/book/src/pages/index.js` (or `.tsx`).
    *   **Acceptance Criteria:** Homepage displays the user's progress dashboard.

## 5. Tutorials Integration

*   [ ] **Task 5.1: Define Tutorial Content Structure**
    *   Establish a clear directory structure for tutorial content within `AIBook/book/docs/tutorials/` (e.g., `docs/tutorials/robot-arm-kinematics/index.mdx`).
    *   **Acceptance Criteria:** A sample tutorial file is created with appropriate headings and code blocks.

*   [ ] **Task 5.2: Basic Static Code Block Styling**
    *   Ensure code blocks within tutorials are well-formatted and readable (Docusaurus Prism integration).
    *   **Acceptance Criteria:** Code examples are rendered correctly and are easy to read.

## 6. Reference Links Management

*   [ ] **Task 6.1: Consistent Link Styling**
    *   Define styles for internal and external links in `AIBook/book/src/css/custom.css` (e.g., color, hover effects, external link icon).
    *   **Acceptance Criteria:** All links across the site have a consistent visual style.

## 7. General Quality Assurance

*   [ ] **Task 7.1: Conduct Local Review of Theme and Layout**
    *   Manually review the site in development mode (`npm start`) to ensure design consistency and responsiveness.
    *   **Acceptance Criteria:** Key design elements are consistent and site is responsive on various screen sizes.

*   [ ] **Task 7.2: Verify Basic Book Tracking Functionality**
    *   Test saving and loading progress for a few chapters to `localStorage`.
    *   **Acceptance Criteria:** Progress is correctly saved and retrieved locally.

*   [ ] **Task 7.3: Initial Content Structure Setup**
    *   Create placeholder Markdown/MDX files for the first few chapters/modules in `AIBook/book/docs/` to provide an initial content structure.
    *   **Acceptance Criteria:** Basic book structure is visible in the sidebar.
