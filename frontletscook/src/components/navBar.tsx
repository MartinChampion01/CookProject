import React from 'react';
import NavButton from './navButton';

const navItem = [
  { label: 'Home', to: '/' },
  { label: 'About', to: '/about' },
];

const NavBar: React.FC = () => {
  return (
    <nav>
      <div className="flex flex-row">
        <h1>LETK</h1>
        <ul>
          {navItem.map((item) => (
            <li key={item.to}>
              <NavButton label={item.label} to={item.to} />
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default NavBar