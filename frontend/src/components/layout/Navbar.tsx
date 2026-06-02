import { useEffect, useState } from "react";
import { MdOutlineDarkMode } from "react-icons/md";

import { type NavbarProps } from "../../types/navbar";
import { Container } from "./Container";

import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate, useLocation } from "react-router-dom";

import { isAuthenticated, logout } from "../../lib/auth";

import { Menu, X } from "lucide-react";

export const Navbar = ({
    mainTitle,
    links,
    theme,
    toggleTheme,
}: NavbarProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const [authenticated, setAuthenticated] = useState(false);

    const navigate = useNavigate();
    const location = useLocation();

    // Re-check auth whenever route changes
    useEffect(() => {
        setAuthenticated(isAuthenticated());
    }, [location]);

    const handleLogout = () => {
        logout();
        setAuthenticated(false);
        navigate("/login");
    };

    return (
        <nav role="navigation" className="fixed top-6 inset-x-0 z-50">
            <Container>
                <div
                    className="
                        flex items-center justify-between
                        px-6 py-4
                        rounded-full
                        text-white
                        bg-black
                        backdrop-blur-lg
                        border border-white
                        shadow-xl
                        relative
                    "
                >
                    {/* Logo */}
                    <motion.div
                        className="text-2xl font-bold"
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <Link to="/" className="text-2xl font-bold">
                            {mainTitle}
                        </Link>
                    </motion.div>

                    {/* Desktop Links */}
                    <div className="hidden md:flex items-center gap-8">
                        <ul className="flex items-center gap-8">
                            {authenticated ? (
                                <>
                                    {links.map((link) => (
                                        <motion.li
                                            key={link.href}
                                            className="list-none"
                                        >
                                            <Link
                                                to={link.href}
                                                className="
                                                    relative text-lg
                                                    transition-all duration-300
                                                    after:absolute
                                                    after:left-0
                                                    after:-bottom-1
                                                    after:h-0.5
                                                    after:w-0
                                                    after:bg-white
                                                    after:transition-all
                                                    after:duration-300
                                                    hover:after:w-full
                                                "
                                            >
                                                {link.label}
                                            </Link>
                                        </motion.li>
                                    ))}

                                    <li className="list-none">
                                        <button
                                            onClick={handleLogout}
                                            className="text-lg hover:text-red-400 transition"
                                        >
                                            Logout
                                        </button>
                                    </li>
                                </>
                            ) : (
                                <>
                                    <li className="list-none">
                                        <Link to="/summarize">Summarize</Link>
                                    </li>

                                    <li className="list-none">
                                        <Link to="/login">Login</Link>
                                    </li>

                                    <li className="list-none">
                                        <Link to="/register">Register</Link>
                                    </li>
                                </>
                            )}
                        </ul>

                        <button
                            onClick={toggleTheme}
                            className={`
                                ${theme} hover:bg-blue-500/80
                                backdrop-blur-lg
                                p-3
                                rounded-2xl
                                transition-all duration-300
                                border border-white/20
                                shadow-lg
                            `}
                        >
                            <MdOutlineDarkMode size={22} />
                        </button>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        className="md:hidden z-50"
                        onClick={() => setIsOpen(!isOpen)}
                        aria-label="Toggle Menu"
                    >
                        {isOpen ? <X size={28} /> : <Menu size={28} />}
                    </button>

                    {/* Mobile Dropdown */}
                    <AnimatePresence>
                        {isOpen && (
                            <motion.div
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                transition={{ duration: 0.3 }}
                                className="
                                    absolute
                                    top-20
                                    left-0
                                    w-full
                                    rounded-3xl
                                    bg-black/80
                                    backdrop-blur-xl
                                    border border-white/10
                                    shadow-2xl
                                    p-6
                                    md:hidden
                                "
                            >
                                {/* Theme Toggle */}
                                <button
                                    onClick={toggleTheme}
                                    className={`
                                        mb-6
                                        ${theme} hover:bg-blue-500/80
                                        backdrop-blur-lg
                                        p-3
                                        rounded-2xl
                                        transition-all duration-300
                                        border border-white/20
                                        shadow-lg
                                    `}
                                >
                                    <MdOutlineDarkMode size={22} />
                                </button>

                                <ul className="flex flex-col gap-6">
                                    {authenticated ? (
                                        <>
                                            {links.map((link, index) => (
                                                <motion.li
                                                    key={link.href}
                                                    initial={{
                                                        opacity: 0,
                                                        x: -20,
                                                    }}
                                                    animate={{
                                                        opacity: 1,
                                                        x: 0,
                                                    }}
                                                    transition={{
                                                        delay: index * 0.1,
                                                        duration: 0.4,
                                                    }}
                                                    whileHover={{ x: 6 }}
                                                    className="list-none"
                                                >
                                                    <Link
                                                        to={link.href}
                                                        onClick={() =>
                                                            setIsOpen(false)
                                                        }
                                                        className="text-2xl"
                                                    >
                                                        {link.label}
                                                    </Link>
                                                </motion.li>
                                            ))}

                                            <li className="list-none">
                                                <button
                                                    onClick={() => {
                                                        handleLogout();
                                                        setIsOpen(false);
                                                    }}
                                                    className="
                                                        text-left
                                                        text-2xl
                                                        hover:text-red-400
                                                        transition
                                                    "
                                                >
                                                    Logout
                                                </button>
                                            </li>
                                        </>
                                    ) : (
                                        <>
                                            <li className="list-none">
                                                <Link
                                                    to="/summarize"
                                                    onClick={() =>
                                                        setIsOpen(false)
                                                    }
                                                    className="text-2xl"
                                                >
                                                    Summarize
                                                </Link>
                                            </li>

                                            <li className="list-none">
                                                <Link
                                                    to="/login"
                                                    onClick={() =>
                                                        setIsOpen(false)
                                                    }
                                                    className="text-2xl"
                                                >
                                                    Login
                                                </Link>
                                            </li>

                                            <li className="list-none">
                                                <Link
                                                    to="/register"
                                                    onClick={() =>
                                                        setIsOpen(false)
                                                    }
                                                    className="text-2xl"
                                                >
                                                    Register
                                                </Link>
                                            </li>
                                        </>
                                    )}
                                </ul>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </Container>
        </nav>
    );
};
