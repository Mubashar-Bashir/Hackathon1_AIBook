#!/usr/bin/env python3
"""
UI/UX Components Generator Script

This script generates UI components for the Physical AI & Humanoid Robotics textbook interface.
"""

import argparse
import json
import os
from typing import Dict, List, Any, Optional

def load_design_tokens():
    """Load design tokens from assets/design_tokens.json"""
    tokens_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'design_tokens.json')
    if os.path.exists(tokens_path):
        with open(tokens_path, 'r') as f:
            return json.load(f)
    else:
        # Default design tokens
        return {
            "colors": {
                "primary": "#1976D2",
                "primary_variant": "#1565C0",
                "secondary": "#FF5722",
                "background": "#FFFFFF",
                "surface": "#F5F5F5",
                "error": "#D32F2F",
                "on_primary": "#FFFFFF",
                "on_secondary": "#000000",
                "on_background": "#000000",
                "on_surface": "#000000"
            },
            "typography": {
                "font_family": "Roboto, sans-serif",
                "sizes": {
                    "h1": "96px",
                    "h2": "60px",
                    "h3": "48px",
                    "h4": "34px",
                    "h5": "24px",
                    "h6": "20px",
                    "subtitle1": "16px",
                    "subtitle2": "14px",
                    "body1": "16px",
                    "body2": "14px",
                    "button": "14px",
                    "caption": "12px",
                    "overline": "10px"
                }
            },
            "spacing": {
                "unit": "8px",
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px"
            },
            "breakpoints": {
                "xs": "0",
                "sm": "600px",
                "md": "960px",
                "lg": "1280px",
                "xl": "1920px"
            }
        }

def generate_component_code(component_type: str, props: List[str], design_system: str = "material") -> Dict[str, str]:
    """Generate component code based on type and properties."""

    design_tokens = load_design_tokens()

    if component_type.lower() == "button":
        return generate_button_component(props, design_tokens)
    elif component_type.lower() == "card":
        return generate_card_component(props, design_tokens)
    elif component_type.lower() == "input":
        return generate_input_component(props, design_tokens)
    elif component_type.lower() == "modal":
        return generate_modal_component(props, design_tokens)
    else:
        return generate_generic_component(component_type, props, design_tokens)

def generate_button_component(props: List[str], tokens: Dict) -> Dict[str, str]:
    """Generate a button component."""

    # Determine which props to include
    has_variant = "variant" in props
    has_size = "size" in props
    has_disabled = "disabled" in props

    component_code = f'''import React, {{ useState }} from 'react';
import './Button.css';

interface ButtonProps {{
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outlined' | 'text';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  className?: string;
}}

const Button: React.FC<ButtonProps> = ({{
  children,
  onClick,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  className = ''
}}) => {{
  const [isFocused, setIsFocused] = useState(false);

  const handleClick = () => {{
    if (!disabled && onClick) {{
      onClick();
    }}
  }};

  const handleKeyDown = (e: React.KeyboardEvent) => {{
    if ((e.key === 'Enter' || e.key === ' ') && !disabled) {{
      e.preventDefault();
      handleClick();
    }}
  }};

  const buttonClasses = [
    'ai-book-button',
    `ai-book-button--variant-${{variant}}`,
    `ai-book-button--size-${{size}}`,
    disabled ? 'ai-book-button--disabled' : '',
    isFocused ? 'ai-book-button--focused' : '',
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      className={{buttonClasses}}
      onClick={{handleClick}}
      onKeyDown={{handleKeyDown}}
      disabled={{disabled}}
      aria-disabled={{disabled}}
      tabIndex={{disabled ? -1 : 0}}
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
    >
      {{children}}
    </button>
  );
}};

export default Button;
'''

    css_styles = f'''/* Button Component Styles */
.ai-book-button {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 4px;
  font-family: {tokens['typography']['font_family']};
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}}

/* Primary variant */
.ai-book-button--variant-primary {{
  background-color: {tokens['colors']['primary']};
  color: {tokens['colors']['on_primary']};
}}

.ai-book-button--variant-primary:not(.ai-book-button--disabled):hover {{
  background-color: {tokens['colors']['primary_variant']};
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Secondary variant */
.ai-book-button--variant-secondary {{
  background-color: {tokens['colors']['secondary']};
  color: {tokens['colors']['on_secondary']};
}}

.ai-book-button--variant-secondary:not(.ai-book-button--disabled):hover {{
  background-color: #E64A19;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Outlined variant */
.ai-book-button--variant-outlined {{
  background-color: transparent;
  color: {tokens['colors']['primary']};
  border: 1px solid {tokens['colors']['primary']};
}}

.ai-book-button--variant-outlined:not(.ai-book-button--disabled):hover {{
  background-color: rgba({int(tokens['colors']['primary'][1:3], 16)}, {int(tokens['colors']['primary'][3:5], 16)}, {int(tokens['colors']['primary'][5:7], 16)}, 0.04);
}}

/* Text variant */
.ai-book-button--variant-text {{
  background-color: transparent;
  color: {tokens['colors']['primary']};
  padding: 6px 8px;
}}

.ai-book-button--variant-text:not(.ai-book-button--disabled):hover {{
  background-color: rgba({int(tokens['colors']['primary'][1:3], 16)}, {int(tokens['colors']['primary'][3:5], 16)}, {int(tokens['colors']['primary'][5:7], 16)}, 0.04);
}}

/* Size variants */
.ai-book-button--size-small {{
  padding: 4px 8px;
  font-size: {tokens['typography']['sizes']['button']};
  min-height: 32px;
}}

.ai-book-button--size-medium {{
  padding: 6px 16px;
  font-size: {tokens['typography']['sizes']['button']};
  min-height: 40px;
}}

.ai-book-button--size-large {{
  padding: 8px 24px;
  font-size: calc({tokens['typography']['sizes']['button']} * 1.2);
  min-height: 48px;
}}

/* Disabled state */
.ai-book-button--disabled {{
  opacity: 0.6;
  cursor: not-allowed;
}}

/* Focused state for accessibility */
.ai-book-button--focused {{
  outline: 2px solid {tokens['colors']['secondary']};
  outline-offset: 2px;
}}

/* Focus visible polyfill for better accessibility */
.ai-book-button:focus-visible {{
  outline: 2px solid {tokens['colors']['secondary']};
  outline-offset: 2px;
}}

/* Remove default focus for mouse users */
.ai-book-button:focus:not(:focus-visible) {{
  outline: none;
}}
'''

    documentation = f"""
# Button Component

A versatile button component for the AI & Humanoid Robotics textbook interface.

## Props

- `children`: The content to display inside the button
- `onClick`: Function to call when button is clicked
- `variant`: Style variant ('primary', 'secondary', 'outlined', 'text') - default: 'primary'
- `size`: Size variant ('small', 'medium', 'large') - default: 'medium'
- `disabled`: Whether the button is disabled - default: false
- `className`: Additional CSS classes to apply

## Usage

```tsx
import Button from './Button';

// Primary button
<Button variant="primary" size="medium" onClick={() => console.log('Clicked')}>
  Primary Button
</Button>

// Secondary button
<Button variant="secondary" size="large">
  Secondary Button
</Button>

// Disabled button
<Button disabled>
  Disabled Button
</Button>
```

## Accessibility

- Proper ARIA attributes for disabled state
- Keyboard navigation support (Enter/Space)
- Focus management with visible focus indicators
- Color contrast meets WCAG 2.1 AA standards
"""

    return {
        "component_code": component_code,
        "css_styles": css_styles,
        "documentation": documentation,
        "test_hooks": ["button-click", "button-disabled", "keyboard-navigation"]
    }

def generate_card_component(props: List[str], tokens: Dict) -> Dict[str, str]:
    """Generate a card component."""

    component_code = f'''import React from 'react';
import './Card.css';

interface CardProps {{
  children: React.ReactNode;
  elevation?: number;
  className?: string;
}}

const Card: React.FC<CardProps> = ({{
  children,
  elevation = 1,
  className = ''
}}) => {{
  const cardClasses = [
    'ai-book-card',
    `ai-book-card--elevation-${{elevation}}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={{cardClasses}}>
      {{children}}
    </div>
  );
}};

export default Card;
'''

    css_styles = f'''/* Card Component Styles */
.ai-book-card {{
  background-color: {tokens['colors']['surface']};
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  transition: all 0.2s ease-in-out;
  overflow: hidden;
  box-sizing: border-box;
}}

/* Elevation variants */
.ai-book-card--elevation-0 {{
  box-shadow: none;
}}

.ai-book-card--elevation-1 {{
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}}

.ai-book-card--elevation-2 {{
  box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
}}

.ai-book-card--elevation-3 {{
  box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
}}

.ai-book-card--elevation-4 {{
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
}}

.ai-book-card--elevation-5 {{
  box-shadow: 0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22);
}}

/* Responsive design */
@media (max-width: {tokens['breakpoints']['sm']}) {{
  .ai-book-card {{
    margin: {tokens['spacing']['sm']};
  }}
}}
'''

    documentation = """
# Card Component

A container component for grouping related content with a subtle shadow effect.

## Props

- `children`: The content to display inside the card
- `elevation`: Shadow depth (0-5) - default: 1
- `className`: Additional CSS classes to apply

## Usage

```tsx
import Card from './Card';

<Card elevation={2}>
  <h3>Card Title</h3>
  <p>Card content goes here...</p>
</Card>
```

## Accessibility

- Proper semantic structure
- Sufficient color contrast
- Responsive design for all screen sizes
"""

    return {
        "component_code": component_code,
        "css_styles": css_styles,
        "documentation": documentation,
        "test_hooks": ["card-content", "card-elevation"]
    }

def generate_generic_component(component_type: str, props: List[str], tokens: Dict) -> Dict[str, str]:
    """Generate a generic component as fallback."""

    component_code = f'''import React from 'react';
import './{component_type}.css';

interface {component_type[0].upper() + component_type[1:]}Props {{
  children?: React.ReactNode;
  className?: string;
  [key: string]: any;
}}

const {component_type[0].upper() + component_type[1:]}: React.FC<{component_type[0].upper() + component_type[1:]}Props> = (props) => {{
  const {{ children, className = '', ...otherProps }} = props;

  const componentClasses = [
    'ai-book-{component_type}',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={{componentClasses}} {{...otherProps}}>
      {{children}}
    </div>
  );
}};

export default {component_type[0].upper() + component_type[1:]};
'''

    css_styles = f'''/* {component_type[0].upper() + component_type[1:]} Component Styles */
.ai-book-{component_type} {{
  /* Add your styles here */
  box-sizing: border-box;
}}
'''

    documentation = f"""
# {component_type[0].upper() + component_type[1:]} Component

A generic {component_type} component for the AI & Humanoid Robotics textbook interface.

## Props

- `children`: The content to display inside the component
- `className`: Additional CSS classes to apply
- Additional props are spread to the root element

## Usage

```tsx
import {component_type[0].upper() + component_type[1:]} from './{component_type[0].upper() + component_type[1:]}.tsx';

<{component_type[0].upper() + component_type[1:]} className="custom-class">
  Content goes here
</{component_type[0].upper() + component_type[1:]} >
```
"""

    return {
        "component_code": component_code,
        "css_styles": css_styles,
        "documentation": documentation,
        "test_hooks": [f"{component_type}-render"]
    }

def main():
    parser = argparse.ArgumentParser(description='UI/UX Components Generator')
    parser.add_argument('--type', type=str, required=True, help='Type of component to generate')
    parser.add_argument('--props', type=str, help='Comma-separated list of properties')
    parser.add_argument('--design-system', type=str, default='material', help='Design system to follow')

    args = parser.parse_args()

    # Parse properties
    props = []
    if args.props:
        props = [p.strip() for p in args.props.split(',')]

    # Generate component
    result = generate_component_code(args.type, props, args.design_system)

    # Prepare output
    output = {
        "component_type": args.type,
        "props": props,
        "design_system": args.design_system,
        "component_code": result["component_code"],
        "css_styles": result["css_styles"],
        "documentation": result["documentation"],
        "test_hooks": result["test_hooks"]
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()