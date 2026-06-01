import "./App.css";
import { useState } from "react";
import { motion, useScroll } from "framer-motion";

import { Footer } from "./components/layout/Footer";
import { Navbar } from "./components/layout/Navbar";

import { colors } from "./constants/colors";
import { mainTitle, links } from "./constants/navbar";

import { Routes, Route } from "react-router-dom";

import LoginPage from "./pages/login";
import RegisterPage from "./pages/register";
import DashboardPage from "./pages/dashboard";
import ChatPage from "./pages/chat";
import UploadPage from "./pages/upload";
import SummarizePage from "./pages/summarize";

function App() {
    const { scrollYProgress } = useScroll();

    const [useTheme, setUseTheme] = useState(
        `${colors.primaryBg} ${colors.primaryText}`,
    );

    const toggleTheme = () => {
        setUseTheme(() =>
            useTheme === `${colors.primaryBg} ${colors.primaryText}`
                ? `${colors.secondaryBg} ${colors.secondaryText}`
                : `${colors.primaryBg} ${colors.primaryText}`,
        );
    };

    return (
        <div className={`${useTheme} min-h-screen flex flex-col pt-28`}>
            <motion.div
                className={`fixed top-0 left-0 right-0 h-1 origin-left z-50 bg-blue-500`}
                style={{ scaleX: scrollYProgress }}
            />
            <Navbar
                mainTitle={mainTitle}
                links={links}
                theme={useTheme}
                toggleTheme={toggleTheme}
            />
            <main className="flex-1">
                <Routes>
                    <Route path="/" element={<DashboardPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/chat" element={<ChatPage />} />
                    <Route path="/upload" element={<UploadPage />} />
                    <Route path="/summarize" element={<SummarizePage />} />
                </Routes>
            </main>

            <Footer />
        </div>
    );
}

export default App;
