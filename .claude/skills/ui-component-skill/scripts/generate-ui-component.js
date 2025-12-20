#!/usr/bin/env node
/**
 * UI Component Generator
 * Creates UI components following Tailwind + ShadCN + DaisyUI integration patterns
 */

const fs = require('fs');
const path = require('path');

// Component templates
const componentTemplates = {
  card: {
    name: 'Card Component',
    description: 'Card with ShadCN structure, Tailwind layout, and DaisyUI theming',
    template: `import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/utils/cn';

interface {{PascalCaseName}}Props {
  title: string;
  description?: string;
  children?: React.ReactNode;
  theme?: string;
  className?: string;
}

const {{PascalCaseName}} = ({
  title,
  description,
  children,
  theme = '',
  className = ''
}: {{PascalCaseName}}Props) => {
  return (
    {/* Apply DaisyUI theme to wrapper element */}
    <div className={\`card bg-base-100 text-base-content \${theme}\`}>
      {/* ShadCN component with Tailwind extensions */}
      <Card className={cn("w-full", className)}>
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
        <CardContent>
          {children}
        </CardContent>
      </Card>
    </div>
  );
};

export default {{PascalCaseName}};
`
  },

  button: {
    name: 'Button Component',
    description: 'Button with ShadCN functionality and DaisyUI theming options',
    template: `import React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/utils/cn';

interface {{PascalCaseName}}Props {
  children: React.ReactNode;
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  theme?: string; // DaisyUI theme class
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
}

const {{PascalCaseName}} = ({
  children,
  variant = 'default',
  size = 'default',
  theme = '',
  className = '',
  onClick,
  disabled = false
}: {{PascalCaseName}}Props) => {
  return (
    <div className={theme}>
      <Button
        variant={variant}
        size={size}
        className={cn(className)}
        onClick={onClick}
        disabled={disabled}
      >
        {children}
      </Button>
    </div>
  );
};

export default {{PascalCaseName}};
`
  },

  modal: {
    name: 'Modal Component',
    description: 'Modal dialog with ShadCN accessibility and DaisyUI themes',
    template: `import React from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { cn } from '@/utils/cn';

interface {{PascalCaseName}}Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  theme?: string;
  className?: string;
}

const {{PascalCaseName}} = ({
  open,
  onOpenChange,
  title,
  description,
  children,
  theme = '',
  className = ''
}: {{PascalCaseName}}Props) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={cn("max-w-md", theme, className)}>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <div className="py-4">
          {children}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default {{PascalCaseName}};
`
  }
};

function generateComponent(componentType, componentName) {
  const template = componentTemplates[componentType];
  if (!template) {
    console.error(\`Unknown component type: \${componentType}\`);
    console.log('Available types:', Object.keys(componentTemplates).join(', '));
    return null;
  }

  // Convert to PascalCase
  const pascalCaseName = componentName.charAt(0).toUpperCase() + componentName.slice(1);

  // Replace placeholders
  let componentCode = template.template;
  componentCode = componentCode.replace(/\{\{PascalCaseName\}\}/g, pascalCaseName);

  return componentCode;
}

function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log('Usage: node generate-ui-component.js <component-type> <component-name> [output-dir]');
    console.log('');
    console.log('Component types:');
    Object.keys(componentTemplates).forEach(type => {
      console.log(\`  \${type}: \${componentTemplates[type].description}\`);
    });
    return;
  }

  const [componentType, componentName, outputDir = './src/components'] = args;

  const componentCode = generateComponent(componentType, componentName);

  if (!componentCode) {
    return;
  }

  // Create output directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Write component file
  const outputPath = path.join(outputDir, \`\${componentName}.tsx\`);
  fs.writeFileSync(outputPath, componentCode);

  console.log(\`✅ Created \${componentName}.tsx in \${outputDir}\`);
  console.log(\`📋 Component type: \${componentType}\`);
  console.log(\`📋 Follows Tailwind + ShadCN + DaisyUI integration patterns\`);
}

if (require.main === module) {
  main();
}