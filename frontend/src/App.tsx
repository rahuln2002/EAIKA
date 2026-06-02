import "./App.css";
import { useState, useEffect } from "react";

import { Toaster } from "react-hot-toast";

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

    useEffect(() => {
        const isDark =
            useTheme === `${colors.secondaryBg} ${colors.secondaryText}`;

        if (isDark) {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
    }, [useTheme]);

    return (
        <div
            className={`
                ${useTheme}
                ${useTheme === `${colors.secondaryBg} ${colors.secondaryText}` ? "dark" : ""}
                min-h-screen flex flex-col pt-35
            `}
        >
            <Toaster position="top-right" />
            <Navbar
                mainTitle={mainTitle}
                links={links}
                theme={useTheme}
                toggleTheme={toggleTheme}
            />
            <main className="flex-1">
                <Routes>
                    <Route
                        path="/"
                        element={<DashboardPage theme={useTheme} />}
                    />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route
                        path="/dashboard"
                        element={<DashboardPage theme={useTheme} />}
                    />
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
