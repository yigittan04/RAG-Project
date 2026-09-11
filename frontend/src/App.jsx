import { useState } from "react";
import { useAuth } from "./context/AuthContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import Documents from "./pages/Documents";
import Settings from "./pages/Settings";
import "./App.css";

function App() {
    const { loading, isAuthenticated } = useAuth();
    const [showRegister, setShowRegister] = useState(false);
    const [page, setPage] = useState("chat");

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (!isAuthenticated) {
        if (showRegister) {
            return (
                <>
                    <Register />

                    <div className="auth-switch">
                        <p>
                            Already have an account?{" "}
                            <button onClick={() => setShowRegister(false)}>
                                Sign in
                            </button>
                        </p>
                    </div>
                </>
            );
        }

        return (
            <>
                <Login />

                <div className="auth-switch">
                    <p>
                        Don't have an account?{" "}
                        <button onClick={() => setShowRegister(true)}>
                            Create one
                        </button>
                    </p>
                </div>
            </>
        );
    }

    if (page === "documents") {
        return <Documents onNavigate={setPage} />;
    }

    if (page === "settings") {
        return <Settings onNavigate={setPage} />;
    }

    return <Chat onNavigate={setPage} />;

}

export default App;