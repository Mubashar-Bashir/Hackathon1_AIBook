import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header style={{
      padding: '4rem 0',
      textAlign: 'center',
      backgroundColor: '#17199eff',
    }}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div style={{marginTop: '2rem'}}>
          <a href="/docs/intro" className="button button--secondary button--lg">
            Start Reading
          </a>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics Textbook">
      <HomepageHeader />
      <main>
        <section style={{padding: '4rem 0', textAlign: 'center'}}>
          <div className="container">
            <h2>Physical AI & Humanoid Robotics Textbook</h2>
            <p>Your comprehensive guide to understanding and implementing physical AI and humanoid robotics.</p>

            <div style={{display: 'flex', justifyContent: 'center', gap: '2rem', marginTop: '2rem', flexWrap: 'wrap'}}>
              <div style={{flex: '1', minWidth: '250px', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px'}}>
                <h3>Module 1: Robotic Nervous System</h3>
                <p>Learn about ROS 2 and how it acts as the nervous system for robots.</p>
              </div>

              <div style={{flex: '1', minWidth: '250px', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px'}}>
                <h3>Module 2: Digital Twins</h3>
                <p>Understand Gazebo and Unity simulation environments.</p>
              </div>

              <div style={{flex: '1', minWidth: '250px', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px'}}>
                <h3>Module 3: AI Robot Brains</h3>
                <p>Explore NVIDIA Isaac™ platform for AI-powered robotics.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}