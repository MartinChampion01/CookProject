import React from "react";
import { NavLink } from 'react-router-dom';

interface NavButtonProps {
    label: string;
    to: string
}

const NavButton: React.FC<NavButtonProps> = ({label, to}) => {
    return (
        <NavLink
            to={to}
        >
            {label}    
        </NavLink>
    );
};

export default NavButton