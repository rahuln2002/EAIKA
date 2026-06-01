type NavLink = {
    label: string;
    href: string;
};

export type NavbarProps = {
    mainTitle: string;
    theme: string;
    toggleTheme: () => void;
    links: NavLink[];
};
