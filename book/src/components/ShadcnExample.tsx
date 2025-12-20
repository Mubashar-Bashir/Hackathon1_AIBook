import React from 'react';
import { Button } from '../components/ui/button';

const ShadcnExample = () => {
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">ShadCN UI Example</h2>
      <div className="flex gap-2">
        <Button variant="default">Default Button</Button>
        <Button variant="destructive">Destructive</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link</Button>
      </div>
    </div>
  );
};

export default ShadcnExample;