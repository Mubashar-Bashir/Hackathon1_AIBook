import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import { ChatServiceProvider } from '../components/Chat/ChatContext';
import LessonAssistant from '../components/Chat/LessonAssistant';

export default function Layout(props) {
  return (
    <OriginalLayout {...props}>
      {props.children}
      <ChatServiceProvider>
        <LessonAssistant />
      </ChatServiceProvider>
    </OriginalLayout>
  );
}