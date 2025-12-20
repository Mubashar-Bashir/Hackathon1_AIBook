# UI Integration Patterns Reference

## 1. Tailwind + ShadCN UI + DaisyUI Integration Patterns

### Pattern A: Component-First Approach
When you need a complex, accessible component with theming:

```tsx
// Card with ShadCN structure, Tailwind layout, DaisyUI theme
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ThemedCardProps {
  title: string;
  children: React.ReactNode;
  theme?: string; // DaisyUI theme class
  className?: string;
}

const ThemedCard = ({ title, children, theme = "", className = "" }: ThemedCardProps) => {
  return (
    // Apply DaisyUI theme to wrapper
    <div className={`card ${theme}`}>
      {/* ShadCN UI component with Tailwind extensions */}
      <Card className={cn("w-full", className)}>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
        <CardContent>
          {children}
        </CardContent>
      </Card>
    </div>
  );
};
```

### Pattern B: Layout-First Approach
When you need responsive layouts with themed containers:

```tsx
// Responsive grid with DaisyUI themes and Tailwind utilities
const ResponsiveGrid = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {/* Each card uses DaisyUI theme with Tailwind layout */}
      <div className="card bg-primary text-primary-content">
        <div className="card-body">
          <h2 className="card-title">Card Title</h2>
          <p>Card content with Tailwind utilities</p>
        </div>
      </div>
    </div>
  );
};
```

### Pattern C: Interactive Component with Theming
When you need ShadCN interactive components with DaisyUI themes:

```tsx
// Button with ShadCN functionality and DaisyUI themes
import { Button } from "@/components/ui/button";

const ThemedButton = ({
  children,
  variant = "default",
  theme = "normal"
}: {
  children: React.ReactNode;
  variant?: "default" | "destructive" | "outline";
  theme?: string;
}) => {
  // Apply DaisyUI theme to parent, ShadCN variant to button
  return (
    <div className={`btn-group ${theme}`}>
      <Button variant={variant}>
        {children}
      </Button>
    </div>
  );
};
```

## 2. Class Order Best Practices

### Correct Order:
1. DaisyUI theme classes (on wrappers/containers)
2. ShadCN UI generated classes (component base)
3. Tailwind utility classes (customizations)

### Example:
```tsx
// ✅ CORRECT
<div className="card bg-base-100"> {/* DaisyUI theme */}
  <Card className="w-full max-w-sm"> {/* ShadCN base */}
    <CardContent className="p-6 space-y-4"> {/* Tailwind utilities */}
      <Button className="w-full">Click me</Button>
    </CardContent>
  </Card>
</div>

// ❌ INCORRECT - DaisyUI classes on ShadCN component
<Card className="card bg-primary text-primary-content w-full"> {/* Mixed systems on same element */}
```

## 3. Conflict Prevention Strategies

### Strategy 1: Wrapper Pattern
```tsx
// Apply DaisyUI themes to wrapper elements, not components
const SafeThemedComponent = () => (
  <div className="theme-forest"> {/* DaisyUI theme */}
    <Card> {/* ShadCN component */}
      <CardContent className="p-4"> {/* Tailwind utilities */}
        Content here
      </CardContent>
    </Card>
  </div>
);
```

### Strategy 2: Conditional Class Application
```tsx
// Use conditional classes to avoid conflicts
const ConditionalComponent = ({ useDaisyTheme }: { useDaisyTheme: boolean }) => (
  <div className={useDaisyTheme ? "card bg-base-100" : "bg-white rounded-lg"}>
    <Card className="border-0">
      <CardContent className="p-6">
        Content
      </CardContent>
    </Card>
  </div>
);
```

## 4. Theme Consistency Patterns

### CSS Variable Override Pattern
```tsx
// Override ShadCN themes with DaisyUI variables
const CustomThemedComponent = () => (
  <div className="theme-forest">
    <Card className="border-0" style={{
      // Use CSS variables that match DaisyUI theme
      '--border-color': 'hsl(var(--b2))',
      '--background-color': 'hsl(var(--b1))'
    } as React.CSSProperties}>
      <CardContent>
        Content matching DaisyUI theme
      </CardContent>
    </Card>
  </div>
);
```

## 5. Testing for Conflicts

### Visual Testing Checklist:
- [ ] Components render without visual distortion
- [ ] Hover/focus states work correctly
- [ ] Responsive behavior functions properly
- [ ] Theme colors apply consistently
- [ ] Accessibility features remain intact
- [ ] No unexpected layout shifts

### Class Conflict Detection:
1. Check for duplicate property definitions
2. Verify that DaisyUI classes don't override ShadCN functionality
3. Ensure Tailwind utilities don't break component structure
4. Test all interactive states (hover, focus, active)