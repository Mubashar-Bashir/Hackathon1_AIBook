import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/utils/cn';

interface ThemedCardProps {
  title: string;
  description?: string;
  children?: React.ReactNode;
  theme?: string; // DaisyUI theme class like 'theme-forest', 'theme-dark', etc.
  className?: string;
  footer?: React.ReactNode;
}

const ThemedCard = ({
  title,
  description,
  children,
  theme = '',
  className = '',
  footer
}: ThemedCardProps) => {
  return (
    {/* DaisyUI theme applied to wrapper element to avoid conflicts with ShadCN component */}
    <div className={`card bg-base-100 text-base-content ${theme}`}>
      {/* ShadCN UI component with Tailwind extensions */}
      <Card className={cn("w-full shadow-lg", className)}>
        <CardHeader className="pb-3">
          <CardTitle className="text-xl">{title}</CardTitle>
          {description && (
            <CardDescription className="text-sm text-muted-foreground">
              {description}
            </CardDescription>
          )}
        </CardHeader>
        <CardContent className="pb-3">
          {children}
        </CardContent>
        {footer && (
          <CardFooter className="flex justify-between pt-0">
            {footer}
          </CardFooter>
        )}
      </Card>
    </div>
  );
};

export default ThemedCard;