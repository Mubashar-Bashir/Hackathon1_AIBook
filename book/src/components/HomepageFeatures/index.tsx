import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
  icon?: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Physical AI Fundamentals',
    icon: '🤖',
    description: (
      <>
        Explore the core principles of Physical AI - the intersection of artificial intelligence and physical systems.
        Learn how machines can perceive, reason, and interact with the real world.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    icon: '🦾',
    description: (
      <>
        Dive deep into humanoid robot design, kinematics, and control systems.
        Understand how to create robots that mimic human movement and interaction.
      </>
    ),
  },
  {
    title: 'Advanced Applications',
    icon: '🚀',
    description: (
      <>
        Discover cutting-edge applications of Physical AI and Humanoid Robotics in industry,
        healthcare, and research. Learn about real-world implementations and future possibilities.
      </>
    ),
  },
];

function Feature({title, Svg, description, icon}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <div className="cyber-feature-card cyber-card cyber-glow cyber-glow--violet">
          <div className="cyber-feature-icon">
            {icon ? <span className="feature-icon">{icon}</span> : Svg && <Svg className={styles.featureSvg} role="img" />}
          </div>
          <Heading as="h3" className="cyber-feature-title">{title}</Heading>
          <p className="cyber-feature-description">{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={clsx(styles.features, 'cyber-feature-grid-section')}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
