# Project Constitution: Physical AI & Humanoid Robotics Textbook

## 1. Core Principles

-   **User-Centric Design**: All features and content must prioritize the learning experience of the student.
-   **Clarity & Accessibility**: Information should be clear, concise, and accessible to a diverse audience, including those new to Physical AI.
-   **Technical Accuracy**: Content and code must be technically correct and reflect current best practices in AI and Robotics.
-   **Efficiency & Performance**: The textbook platform and embedded tools should be performant and responsive.
-   **Security by Design**: All components, especially authentication and data handling, must adhere to robust security standards.
-   **Maintainability & Scalability**: The Docusaurus structure, RAG backend, and associated services should be easy to maintain and scale for future content or features.
-   **Modularity & Reusability**: Components should be designed for modularity to facilitate extension and reuse.

## 2. Code Quality & Standards

-   **Readability**: Code must be clean, well-structured, and easy to understand with meaningful variable/function names.
-   **Consistency**: Adhere to established style guides (e.g., Prettier, ESLint for JavaScript; Black, Flake8 for Python).
-   **Simplicity**: Prefer the simplest solution that meets the requirements; avoid over-engineering.
-   **Documentation**: Critical functions, APIs, and complex logic should be documented inline.
-   **Version Control**: Adhere to Git best practices (clear commit messages, feature branches).

## 3. Testing & Validation

-   **Unit Tests**: All critical functions and components must have unit tests.
-   **Integration Tests**: Test the interaction between different modules (e.g., chatbot with RAG backend).
-   **End-to-End Tests**: Verify user journeys (e.g., reading a chapter, asking a question, signing up).
-   **Content Validation**: Ensure textbook content is accurate and complete as per course details.
-   **Performance Testing**: Verify that critical operations (chatbot response, page load, personalization/translation) meet defined performance criteria.

## 4. Architectural Principles

-   **Separation of Concerns**: Clearly define boundaries between Docusaurus frontend, RAG backend (FastAPI), database (Neon), vector store (Qdrant), and authentication (BetterAuth).
-   **Loose Coupling**: Components should be as independent as possible to allow for easier changes and updates.
-   **API-First Design**: Define clear API contracts for communication between services (e.g., frontend to RAG backend).
-   **Cloud-Native**: Design for deployment on cloud platforms (GitHub Pages, serverless functions) where applicable.

## 5. Security & Privacy

-   **Authentication & Authorization**: Implement robust mechanisms for user authentication and restrict access based on roles/permissions.
-   **Data Protection**: Encrypt sensitive data (e.g., user background info) at rest and in transit.
-   **Input Validation**: Validate all user inputs to prevent injection attacks and other vulnerabilities.
-   **Dependency Management**: Regularly audit and update third-party dependencies to mitigate known vulnerabilities.

## 6. Documentation & Knowledge Sharing

-   **Feature Specifications (`spec.md`)**: Clearly define "what" is being built and "why".
-   **Implementation Plans (`plan.md`)**: Document "how" the feature will be built, including architectural decisions.
-   **Task Lists (`tasks.md`)**: Break down implementation into actionable, testable steps.
-   **Prompt History Records (`history/prompts/`)**: Capture all significant AI interactions for traceability and learning.
-   **Architectural Decision Records (`history/adr/`)**: Document significant architectural choices and their rationale.
-   **User Documentation**: The textbook itself serves as primary user documentation.

## 7. Technical Writing Principles for Textbook Content

To ensure the highest quality and effectiveness of the "Physical AI & Humanoid Robotics" textbook, all content creation will adhere to the following principles:

### A. Pre-Writing & Planning

-   **Understand the Topic Thoroughly**: Deep dive into each subject, conducting research to gain expertise during the writing process.
-   **Teach First**: Prioritize creating content that effectively teaches the topic, potentially drawing from prior presentations or articles.
-   **Detailed Plan**: Develop a comprehensive plan of chapters and parts, accepting that it may evolve.
-   **Start with Strong Topics**: Begin writing sections where understanding is already strong, leveraging existing knowledge or materials.
-   **Consider Constant Style Elements**: Define and maintain a consistent style throughout the book.
-   **Introduction Last**: Write introductions for the book and each part only after the main content is complete.
-   **Read, Then Write**: Review existing exemplary technical books to identify effective techniques (analogies, diagrams, code examples) and avoid redundant content.
-   **Learner Persona**: Start with a clear learner persona to tailor content effectively.
-   **Differentiate Content**: Research existing resources to identify gaps and offer unique insights that improve upon current offerings.

### B. Writing & Content Creation

-   **Avoid Common Mistakes**:
    -   **No Banal Advice**: Provide specific, actionable insights, not generic statements.
    -   **Write for Longevity**: Focus on principles and generalizations that remain relevant for three to five years, rather than highly specific, rapidly obsolete details.
    -   **Target Audience Appropriately**: Avoid unnecessary introductory chapters for topics the audience already knows.
    -   **Credit Sources**: Always attribute ideas and code examples, including those derived from AI tools.
    -   **Authentic Voice**: Write in your own voice, as an expert, rather than trying to mimic a perceived "expert" tone.
    -   **Be Concise**: Avoid unnecessary words or lengthy explanations. "Don’t say in a paragraph what you can say in five words."
    -   **Sparing Exclamations & Emphasis**: Use exclamation marks sparingly, and be judicious with bold, italics, and underlining.
-   **Outline First**: Always begin with a clear outline for each chapter/section.
-   **Running Style Guide**: Maintain a list of stylistic conventions to ensure consistency.
-   **Use TODOs**: Employ "TODOs" to track remaining tasks and unfinished sections within the content.
-   **Reader-First Mindset**: Always write with the reader's comprehension as the primary goal.
-   **Compelling Openers & Resounding Endings**: Craft engaging beginnings and conclusive endings for chapters and sections.
-   **Flow & Conflict**: For narrative sections, fill the story with appropriate conflict and tension (e.g., challenges in robotics development).
-   **Drafting Focus**: Turn off the "internal editor" during the first draft to maintain flow.
-   **Persevere**: Recognize and push through challenging "marathon of the middle" phases.
-   **Think Clearly & Concisely**: Go straight to the point, avoiding jargon unless defined.
-   **Proper Formatting**: Utilize lists, headings, bold, and italics for readability and engagement.
-   **Sequential Writing**: For processes, ensure steps are written in a consecutive, easy-to-follow manner.
-   **Include Images**: Normalize the inclusion of diagrams, screenshots, and visual aids to reinforce concepts.
-   **Define Acronyms**: Define all acronyms on their first use.
-   **Avoid Excessive Abbreviations**: Use abbreviations sparingly.
-   **Break Ideas into Paragraphs**: Ensure paragraphs are well-structured and focus on a single idea.
-   **Relatability**: Anticipate reader challenges and make the content relatable to their experience level.

### C. Editing & Publishing

-   **Ferocious Self-Editing**: Engage in rigorous self-editing, switching roles to read as a beginner.
-   **Grammar Checker**: Utilize grammar checkers to ensure error-free writing.
-   **Seek Mentorship/Critique**: Obtain constructive criticism from peers or mentors.
-   **Avoid Haste**: Do not rush the editing or information gathering process.
-   **Don't Pressure Yourself**: Avoid unhealthy self-comparison; focus on continuous improvement.
-   **Stop, Ship, and Celebrate**: Recognize that perfection is elusive; aim to ship a high-quality product and celebrate the accomplishment.
