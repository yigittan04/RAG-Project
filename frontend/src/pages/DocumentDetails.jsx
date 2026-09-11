import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
    getDocument,
    deleteDocument,
} from "../services/api";

function DocumentDetails({
    documentId,
    onNavigate,
}) {
    const { token } = useAuth();

    const [document, setDocument] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadDocument() {
            try {
                const data = await getDocument(
                    token,
                    documentId
                );

                setDocument(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadDocument();
    }, [token, documentId]);

    function formatFileSize(bytes) {
        if (!bytes) {
            return "0 Bytes";
        }

        const units = [
            "Bytes",
            "KB",
            "MB",
            "GB",
        ];

        const index = Math.floor(
            Math.log(bytes) / Math.log(1024)
        );

        return `${(
            bytes / Math.pow(1024, index)
        ).toFixed(2)} ${units[index]}`;
    }

    async function handleDelete() {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${document.filename}"?`
        );

        if (!confirmed) {
            return;
        }

        try {
            await deleteDocument(
                token,
                document.id
            );

            onNavigate("documents");
        } catch (err) {
            setError(err.message);
        }
    }

    if (loading) {
        return (
            <div className="document-details-page">
                <main className="document-details-main">
                    <p>Loading document...</p>
                </main>
            </div>
        );
    }

    if (error) {
        return (
            <div className="document-details-page">
                <main className="document-details-main">
                    <button
                        className="back-to-documents-button"
                        onClick={() =>
                            onNavigate("documents")
                        }
                    >
                        ← Back to Documents
                    </button>

                    <div className="document-details-error">
                        {error}
                    </div>
                </main>
            </div>
        );
    }

    if (!document) {
        return null;
    }

    return (
        <div className="document-details-page">
            <main className="document-details-main">
                <button
                    className="back-to-documents-button"
                    onClick={() =>
                        onNavigate("documents")
                    }
                >
                    ← Back to Documents
                </button>

                <div className="document-details-header">
                    <div>
                        <div className="document-details-icon">
                            📄
                        </div>

                        <h1>{document.filename}</h1>

                        <p>
                            Detailed information about this
                            document.
                        </p>
                    </div>

                    <button
                        className="ask-document-large-button"
                        onClick={() =>
                            onNavigate(
                                "chat",
                                document.id
                            )
                        }
                    >
                        Ask about this document
                    </button>
                </div>

                <section className="document-details-section">
                    <h2>Document Information</h2>

                    <div className="document-details-card">
                        <div className="document-detail-row">
                            <span>Filename</span>
                            <strong>
                                {document.filename}
                            </strong>
                        </div>

                        <div className="document-detail-row">
                            <span>File type</span>
                            <strong>
                                {document.mime_type ||
                                    "Unknown"}
                            </strong>
                        </div>

                        <div className="document-detail-row">
                            <span>File size</span>
                            <strong>
                                {formatFileSize(
                                    document.file_size
                                )}
                            </strong>
                        </div>

                        <div className="document-detail-row">
                            <span>Chunks</span>
                            <strong>
                                {document.total_chunks ?? 0}
                            </strong>
                        </div>

                        <div className="document-detail-row">
                            <span>Status</span>
                            <strong
                                className={`document-status ${document.status}`}
                            >
                                {document.status}
                            </strong>
                        </div>
                    </div>
                </section>

                <section className="document-details-section">
                    <h2>Actions</h2>

                    <div className="document-details-actions">
                        <button
                            className="ask-document-large-button"
                            onClick={() =>
                                onNavigate(
                                    "chat",
                                    document.id
                                )
                            }
                        >
                            Ask questions
                        </button>

                        <button
                            className="delete-document-large-button"
                            onClick={handleDelete}
                        >
                            Delete document
                        </button>
                    </div>
                </section>
            </main>
        </div>
    );
}

export default DocumentDetails;