import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
    getDocuments,
    uploadDocument,
    deleteDocument,
} from "../services/api";

function Documents({ onNavigate }) {
    const { token } = useAuth();

    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    async function loadDocuments() {
        setError("");

        try {
            const data = await getDocuments(token);
            setDocuments(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadDocuments();
    }, [token]);

    async function handleUpload(event) {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        setError("");
        setSuccess("");
        setUploading(true);

        try {
            const data = await uploadDocument(token, file);

            setSuccess(`${data.filename} uploaded successfully.`);

            await loadDocuments();
        } catch (err) {
            setError(err.message);
        } finally {
            setUploading(false);
            event.target.value = "";
        }
    }

    async function handleDelete(documentId, filename) {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${filename}"?`
        );

        if (!confirmed) {
            return;
        }

        setError("");
        setSuccess("");

        try {
            await deleteDocument(token, documentId);

            setDocuments((previous) =>
                previous.filter((document) => document.id !== documentId)
            );

            setSuccess(`${filename} deleted successfully.`);
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <div className="documents-page">
            <header className="documents-header">
                <div>
                    <button
                        className="back-to-chat-button"
                        onClick={() => onNavigate("chat")}
                    >
                        ← Back to Chat
                    </button>

                    <h1>Documents</h1>

                    <p>
                        Manage the documents used by your RAG assistant.
                    </p>
                </div>

                <label className="upload-button">
                    {uploading ? "Uploading..." : "+ Upload document"}

                    <input
                        type="file"
                        accept=".pdf,.txt,.docx"
                        onChange={handleUpload}
                        disabled={uploading}
                        hidden
                    />
                </label>
            </header>

            {error && (
                <div className="document-message error">
                    {error}
                </div>
            )}

            {success && (
                <div className="document-message success">
                    {success}
                </div>
            )}

            <main className="documents-content">
                {loading ? (
                    <p className="document-empty">
                        Loading documents...
                    </p>
                ) : documents.length === 0 ? (
                    <div className="document-empty">
                        <h2>No documents yet</h2>
                        <p>
                            Upload a PDF, DOCX, or TXT file to start asking
                            questions about it.
                        </p>
                    </div>
                ) : (
                    <div className="document-list">
                        {documents.map((document) => (
                            <div
                                key={document.id}
                                className="document-card"
                            >
                                <div className="document-info">
                                    <div className="document-icon">
                                        📄
                                    </div>

                                    <div>
                                        <h3
                                            className="document-name-link"
                                            onClick={() =>
                                                onNavigate(
                                                    "document-details",
                                                    document.id
                                                )
                                            }
                                        >
                                            {document.filename}
                                        </h3>

                                        <p>
                                            {document.mime_type || "Unknown type"}
                                        </p>

                                        <p>
                                            {document.total_chunks ?? 0} chunks
                                        </p>
                                    </div>
                                </div>

                                <div className="document-actions">
                                    <button
                                        className="ask-document-button"
                                        onClick={() =>
                                            onNavigate("chat", document.id)
                                        }
                                    >
                                        Ask about this
                                    </button>

                                    <button
                                        className="delete-document-button"
                                        onClick={() =>
                                            handleDelete(
                                                document.id,
                                                document.filename
                                            )
                                        }
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

export default Documents;