export interface TooltipState {
  isVisible: boolean;
  position: {
    x: number;
    y: number;
  };
  selectedText: string;
  targetElement: Element | null;
}