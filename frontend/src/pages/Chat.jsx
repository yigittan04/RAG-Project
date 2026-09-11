import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
    askQuestion,
    getConversations,
    getConversationMessages,
    getDocuments,
} from "../services/api";

function Chat({ onNavigate }) {
    const { token, user, logout } = useAuth();

    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);
    const [conversationId, setConversationId] = useState(null);

    const [conversations, setConversations] = useState([]);
    const [loadingConversations, setLoadingConversations] = useState(true);

    const [documents, setDocuments] = useState([]);
    const [selectedDocumentId, setSelectedDocumentId] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadConversations() {
            try {
                const data = await getConversations(token);
                setConversations(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoadingConversations(false);
            }
        }

        loadConversations();
    }, [token]);

    useEffect(() => {
        async function loadDocuments() {
            try {
                const data = await getDocuments(token);
                setDocuments(data);
            } catch (err) {
                setError(err.message);
            }
        }

        loadDocuments();
    }, [token]);

    async function handleSelectConversation(id) {
        setError("");
        setLoading(true);

        try {
            const data = await getConversationMessages(token, id);

            setConversationId(id);

            const formattedMessages = data.map((message) => ({
                role: message.role,
                content: message.content,
            }));

            setMessages(formattedMessages);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();

        const trimmedQuestion = question.trim();

        if (!trimmedQuestion || loading) {
            return;
        }

        setError("");

        const userMessage = {
            role: "user",
            content: trimmedQuestion,
        };

        setMessages((previous) => [...previous, userMessage]);
        setQuestion("");
        setLoading(true);

        try {
            const data = await askQuestion(
                token,
                trimmedQuestion,
                conversationId,
                selectedDocumentId || null
            );

            setConversationId(data.conversation_id);

            if (!conversationId) {
                const newConversation = {
                    id: data.conversation_id,
                    title: trimmedQuestion.slice(0, 50),
                };

                setConversations((previous) => [
                    newConversation,
                    ...previous,
                ]);
            }

            const assistantMessage = {
                role: "assistant",
                content: data.answer,
                sources: data.sources || [],
            };

            setMessages((previous) => [
                ...previous,
                assistantMessage,
            ]);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    function handleNewChat() {
        setMessages([]);
        setConversationId(null);
        setQuestion("");
        setError("");
    }

    return (
        <div className="chat-page">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h2>RAG Assistant</h2>

                    <button onClick={handleNewChat}>
                        + New Chat
                    </button>
                </div>

                <div className="conversation-list">
                    {loadingConversations ? (
                        <p className="empty-state">
                            Loading conversations...
                        </p>
                    ) : conversations.length === 0 ? (
                        <p className="empty-state">
                            No conversations yet.
                        </p>
                    ) : (
                        conversations.map((conversation) => (
                            <button
                                key={conversation.id}
                                className={`conversation-item ${
                                    conversation.id === conversationId
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    handleSelectConversation(
                                        conversation.id
                                    )
                                }
                            >
                                {conversation.title ||
                                    "Untitled conversation"}
                            </button>
                        ))
                    )}
                </div>

                <div className="sidebar-footer">
                    <button onClick={() => onNavigate("documents")}>
                        Documents
                    </button>

                    <button onClick={() => onNavigate("settings")}>
                        Settings
                    </button>

                    <button onClick={logout}>
                        Log out
                    </button>
                </div>
            </aside>

            <main className="chat-main">
                <header className="chat-header">
                    <div>
                        <h1>
                            {conversationId
                                ? "Conversation"
                                : "New conversation"}
                        </h1>

                        <p>
                            Welcome, {user.username}. Ask questions
                            about your documents.
                        </p>
                    </div>

                    <div className="document-selector">
                        <label htmlFor="document-select">
                            Search in:
                        </label>

                        <select
                            id="document-select"
                            value={selectedDocumentId}
                            onChange={(event) =>
                                setSelectedDocumentId(
                                    event.target.value
                                )
                            }
                        >
                            <option value="">
                                All Documents
                            </option>

                            {documents.map((document) => (
                                <option
                                    key={document.id}
                                    value={document.id}
                                >
                                    {document.filename}
                                </option>
                            ))}
                        </select>
                    </div>
                </header>

                <div className="messages">
                    {messages.length === 0 ? (
                        <div className="welcome-message">
                            <h2>How can I help?</h2>

                            <p>
                                Ask a question and I'll search your
                                documents for the information you need.
                            </p>
                        </div>
                    ) : (
                        <div className="message-list">
                            {messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`message ${
                                        message.role === "user"
                                            ? "user-message"
                                            : "assistant-message"
                                    }`}
                                >
                                    <div className="message-role">
                                        {message.role === "user"
                                            ? "You"
                                            : "RAG Assistant"}
                                    </div>

                                    <div className="message-content">
                                        {message.content}
                                    </div>

                                    {message.sources &&
                                        message.sources.length > 0 && (
                                            <div className="sources">
                                                <strong>Sources</strong>

                                                {message.sources.map(
                                                    (
                                                        source,
                                                        sourceIndex
                                                    ) => (
                                                        <div
                                                            key={
                                                                sourceIndex
                                                            }
                                                            className="source"
                                                        >
                                                            {source}
                                                        </div>
                                                    )
                                                )}
                                            </div>
                                        )}
                                </div>
                            ))}

                            {loading && (
                                <div className="message assistant-message">
                                    <div className="message-role">
                                        RAG Assistant
                                    </div>

                                    <div className="message-content">
                                        Thinking...
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                <form
                    className="chat-input-area"
                    onSubmit={handleSubmit}
                >
                    <input
                        type="text"
                        value={question}
                        onChange={(event) =>
                            setQuestion(event.target.value)
                        }
                        placeholder="Ask something..."
                        disabled={loading}
                    />

                    <button
                        type="submit"
                        disabled={
                            loading || !question.trim()
                        }
                    >
                        {loading ? "..." : "Send"}
                    </button>
                </form>

                {error && (
                    <div className="chat-error">
                        {error}
                    </div>
                )}
            </main>
        </div>
    );
}

export default Chat;