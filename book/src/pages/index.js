import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import UserDashboard from '../components/UserDashboard';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
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
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        {/* Placeholder for Book Categories */}
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--6">
                <h2>Introduction to Physical AI</h2>
                <p>Explore the foundational concepts of physical AI.</p>
              </div>
              <div className="col col--6">
                <h2>Humanoid Robotics Fundamentals</h2>
                <p>Dive into the mechanics and control of humanoid robots.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Placeholder for My Progress Dashboard */}
        <section className={styles.dashboard}>
          <div className="container">
            <h2>My Progress Dashboard</h2>
            <UserDashboard />
          </div>
        </section>

      </main>
    </Layout>
  );
}
