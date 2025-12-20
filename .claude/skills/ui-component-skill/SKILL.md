---
name: ui-component-skill
description: Create and manage UI components using Tailwind CSS, ShadCN UI, and DaisyUI with proper integration patterns to avoid conflicts. Use this skill when creating UI components that need to leverage the best of all three systems without causing rendering issues.
---

# UI Component Skill

This skill provides guidance for creating UI components that properly integrate Tailwind CSS, ShadCN UI, and DaisyUI without conflicts.

## When to Use This Skill

Use this skill when you need to create UI components that:
1. Leverage Tailwind CSS for utility-based styling
2. Use ShadCN UI for accessible, well-designed components
3. Integrate DaisyUI for theme support and pre-styled components
4. Avoid conflicts between styling systems
5. Maintain consistent rendering across different contexts

## Core Principles

### 1. Layered Integration Approach
- **Foundation Layer**: Tailwind CSS for base utilities and responsive design
- **Component Layer**: ShadCN UI for complex, accessible components
- **Theme Layer**: DaisyUI for consistent theming and visual styles

### 2. Conflict Prevention
- Never apply DaisyUI classes directly to ShadCN UI components
- Use Tailwind classes for custom styling on ShadCN components
- Apply DaisyUI themes at the container/wrapper level
- Use CSS variable overrides for theme consistency when needed

### 3. Proper Class Order
- Base styles first (Tailwind utilities)
- Component styles second (ShadCN UI generated classes)
- Theme styles last (DaisyUI theme classes)

## Component Creation Workflow

### Step 1: Analyze Requirements
Determine which system(s) to use:
- **Pure Tailwind**: For simple layouts and utility styling
- **ShadCN UI**: For complex, accessible components (buttons, dialogs, etc.)
- **DaisyUI**: For themed components and rapid prototyping
- **Hybrid**: For advanced components requiring all systems

### Step 2: Create Component Structure
```
// For ShadCN + Tailwind + DaisyUI hybrid:
- Use ShadCN UI base component
- Extend with Tailwind utilities for customizations
- Wrap with DaisyUI theme containers if needed
```

### Step 3: Implement with Best Practices
1. Create the component with proper TypeScript interfaces
2. Apply ShadCN UI classes for base functionality
3. Add Tailwind utilities for custom styling
4. Apply DaisyUI themes at appropriate wrapper levels
5. Test for conflicts and rendering issues

## Example Component Pattern

```tsx
import React from 'react';
// Import ShadCN UI components
import { Button } from '@/components/ui/button';
// Import DaisyUI for themes
import { cn } from '@/utils/cn'; // ShadCN utility

interface CardProps {
  title: string;
  description: string;
  theme?: 'light' | 'dark' | 'corporate'; // DaisyUI themes
  className?: string;
}

const CardWithMultipleSystems = ({
  title,
  description,
  theme = 'light',
  className
}: CardProps) => {
  return (
    // DaisyUI theme wrapper
    <div className={`card bg-base-100 text-base-content ${theme}`}>
      {/* Tailwind layout */}
      <div className="p-6 max-w-md mx-auto">
        {/* ShadCN UI component with Tailwind extensions */}
        <div className="space-y-4">
          <h3 className="text-xl font-bold">{title}</h3>
          <p className="text-gray-600">{description}</p>
          {/* ShadCN button with Tailwind customizations */}
          <Button className="mt-4 w-full">
            Click Me
          </Button>
        </div>
      </div>
    </div>
  );
};
```

## Common Integration Patterns

### Pattern 1: ShadCN UI with DaisyUI Themes
- Use ShadCN UI components for functionality
- Apply DaisyUI theme classes to parent containers
- Avoid applying DaisyUI classes directly to ShadCN components

### Pattern 2: Tailwind + DaisyUI for Layout
- Use Tailwind for responsive layouts
- Use DaisyUI for themed containers/cards
- Avoid conflicting utility classes

### Pattern 3: ShadCN UI Extensions
- Extend ShadCN components with Tailwind utilities
- Use `cn()` function to merge classes properly
- Maintain accessibility features from ShadCN

## Troubleshooting Common Issues

### Issue: Component not rendering properly
**Solution**: Check class order and ensure no conflicting DaisyUI classes on ShadCN components

### Issue: Themes not applying correctly
**Solution**: Apply DaisyUI theme classes to wrapper elements, not individual components

### Issue: Responsive design conflicts
**Solution**: Use Tailwind for responsive utilities, DaisyUI for themes, ShadCN for component behavior

## File Structure
```
src/
├── components/
│   ├── ui/           # ShadCN UI components
│   ├── themed/       # Components with DaisyUI themes
│   └── layout/       # Layout components with Tailwind
└── utils/
    └── cn.ts         # Class merging utility
```