import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
    getDocuments,
    getConversations,
} from "../services/api";

function Settings({ onNavigate }) {
    const { token, user, logout } = useAuth();

    const [documentCount, setDocumentCount] = useState(0);
    const [conversationCount, setConversationCount] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadStatistics() {
            try {
                const [documents, conversations] = await Promise.all([
                    getDocuments(token),
                    getConversations(token),
                ]);

                setDocumentCount(documents.length);
                setConversationCount(conversations.length);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadStatistics();
    }, [token]);

    return (
        <div className="settings-page">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h2>RAG Assistant</h2>

                    <button onClick={() => onNavigate("chat")}>
                        ← Back to Chat
                    </button>
                </div>

                <div className="sidebar-footer">
                    <button onClick={() => onNavigate("documents")}>
                        Documents
                    </button>

                    <button className="active-nav">
                        Settings
                    </button>

                    <button onClick={logout}>
                        Log out
                    </button>
                </div>
            </aside>

            <main className="settings-main">
                <div className="settings-header">
                    <h1>Settings</h1>
                    <p>
                        Manage your account and view your RAG Assistant
                        information.
                    </p>
                </div>

                {error && (
                    <div className="settings-error">
                        {error}
                    </div>
                )}

                <section className="settings-section">
                    <h2>Account</h2>

                    <div className="settings-card">
                        <div className="setting-row">
                            <span className="setting-label">
                                Username
                            </span>

                            <span className="setting-value">
                                {user.username}
                            </span>
                        </div>

                        <div className="setting-row">
                            <span className="setting-label">
                                Email
                            </span>

                            <span className="setting-value">
                                {user.email}
                            </span>
                        </div>
                    </div>
                </section>

                <section className="settings-section">
                    <h2>Usage</h2>

                    <div className="settings-stats">
                        <div className="stat-card">
                            <span className="stat-number">
                                {loading ? "..." : documentCount}
                            </span>

                            <span className="stat-label">
                                Documents
                            </span>
                        </div>

                        <div className="stat-card">
                            <span className="stat-number">
                                {loading ? "..." : conversationCount}
                            </span>

                            <span className="stat-label">
                                Conversations
                            </span>
                        </div>
                    </div>
                </section>

                <section className="settings-section">
                    <h2>Session</h2>

                    <div className="settings-card">
                        <div className="session-row">
                            <div>
                                <strong>Sign out</strong>
                                <p>
                                    Sign out of your RAG Assistant account
                                    on this device.
                                </p>
                            </div>

                            <button
                                className="logout-button"
                                onClick={logout}
                            >
                                Log out
                            </button>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}

export default Settings;