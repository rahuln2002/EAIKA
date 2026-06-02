import { colors } from "../constants/colors";

type DashboardPageProps = {
    theme?: string;
};

export default function DashboardPage({
    theme = `${colors.primaryBg} ${colors.primaryText}`,
}: DashboardPageProps) {
    const isDark = theme === `${colors.secondaryBg} ${colors.secondaryText}`;

    const cardClasses = isDark
        ? "bg-zinc-900 border border-white/10 text-white"
        : "bg-gray-100 border border-black/10 text-black";

    const workflowClasses = isDark
        ? "bg-blue-500/10 border border-blue-500/20"
        : "bg-blue-100 border border-blue-300/40";

    const pillClasses = isDark
        ? "bg-white/10 border border-white/10"
        : "bg-white border border-black/10";

    return (
        <div className="min-h-screen transition-all duration-300">
            <div className="max-w-5xl mx-auto">
                <div className="space-y-6">
                    <div>
                        <h1 className="text-4xl font-bold tracking-tight">
                            EAIKA
                        </h1>

                        <p className="mt-3 text-lg max-w-3xl opacity-80">
                            Enterprise AI Knowledge Assistant powered by RAG,
                            LLMs, summarization, and intelligent document
                            conversations.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-5 mt-10">
                        <div
                            className={`
                                ${cardClasses}
                                rounded-2xl p-6 transition-all duration-300
                            `}
                        >
                            <h2 className="text-xl font-semibold">
                                AI Summarization
                            </h2>

                            <p className="mt-3 text-sm leading-6 opacity-80">
                                Instantly summarize PDFs, research papers,
                                reports, and documents without creating an
                                account.
                            </p>

                            <span className="inline-block mt-4 text-green-500 text-sm font-medium">
                                Available without login
                            </span>
                        </div>

                        <div
                            className={`
                                ${cardClasses}
                                rounded-2xl p-6 transition-all duration-300
                            `}
                        >
                            <h2 className="text-xl font-semibold">
                                Chat with Documents
                            </h2>

                            <p className="mt-3 text-sm leading-6 opacity-80">
                                Upload your documents and interact with them
                                using contextual AI conversations powered by RAG
                                pipelines.
                            </p>

                            <span className="inline-block mt-4 text-blue-500 text-sm font-medium">
                                Login required
                            </span>
                        </div>

                        <div
                            className={`
                                ${cardClasses}
                                rounded-2xl p-6 transition-all duration-300
                            `}
                        >
                            <h2 className="text-xl font-semibold">
                                Secure Workspace
                            </h2>

                            <p className="mt-3 text-sm leading-6 opacity-80">
                                Create your workspace, manage uploaded files,
                                and access personalized AI-powered knowledge
                                retrieval.
                            </p>

                            <span className="inline-block mt-4 text-purple-500 text-sm font-medium">
                                Register → Login → Upload → Chat
                            </span>
                        </div>
                    </div>

                    <div
                        className={`
                            ${workflowClasses}
                            mt-12 rounded-2xl p-6 transition-all duration-300
                        `}
                    >
                        <h3 className="text-2xl font-semibold">Workflow</h3>

                        <div className="flex flex-wrap items-center gap-3 mt-5 text-sm">
                            {[
                                "Register",
                                "Login",
                                "Upload Documents",
                                "Chat with AI",
                            ].map((step, index) => (
                                <div
                                    key={step}
                                    className="flex items-center gap-3"
                                >
                                    <span
                                        className={`
                                            ${pillClasses}
                                            px-4 py-2 rounded-full
                                        `}
                                    >
                                        {step}
                                    </span>

                                    {index !== 3 && (
                                        <span className="opacity-50">→</span>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
