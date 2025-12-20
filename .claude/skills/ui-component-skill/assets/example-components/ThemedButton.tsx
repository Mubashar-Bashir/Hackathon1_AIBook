import React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/utils/cn';

interface ThemedButtonProps {
  children: React.ReactNode;
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  theme?: string; // DaisyUI theme class like 'btn-primary', 'btn-accent', etc.
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

const ThemedButton = ({
  children,
  variant = 'default',
  size = 'default',
  theme = '',
  className = '',
  onClick,
  disabled = false,
  type = 'button'
}: ThemedButtonProps) => {
  // Combine DaisyUI theme classes with ShadCN UI component
  // Apply DaisyUI classes to a wrapper to avoid conflicts
  return (
    <div className={theme}>
      <Button
        variant={variant}
        size={size}
        className={cn(className)}
        onClick={onClick}
        disabled={disabled}
        type={type}
      >
        {children}
      </Button>
    </div>
  );
};

export default ThemedButton;