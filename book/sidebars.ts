import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Sidebar for the Physical AI & Humanoid Robotics textbook
  textbookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-robotic-nervous-system/chapter1',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/chapter1',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3-ai-robot-brain/chapter1',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vision-language-action/chapter1',
      ],
    },
    {
      type: 'category',
      label: 'Physical AI',
      items: [
        'physical-ai/chapter1',
        'physical-ai/chapter2',
        'physical-ai/chapter3',
        'physical-ai/chapter4',
      ],
    },
    {
      type: 'category',
      label: 'Humanoid Robotics',
      items: [
        'humanoid-robotics/chapter1',
        'humanoid-robotics/chapter2',
        'humanoid-robotics/chapter3',
        'humanoid-robotics/chapter4',
      ],
    },
  ],
};

export default sidebars;
