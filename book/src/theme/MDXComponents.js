import React from 'react';
import DefaultLayout from '@theme-original/Layout';

// Wrapper layout that simply extends the default layout
export default function Layout(props) {
  return (
    <DefaultLayout {...props}>
      {props.children}
    </DefaultLayout>
  );
}