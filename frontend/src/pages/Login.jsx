import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Form from "../components/Form";

function Login() {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            // ✅ No extra login call needed — handled inside Form
            navigate("/home");
        } catch (err) {
            console.error("Login error:", err);
            setError(err.message || "Login failed");
        }
    };

    return (
        <div className="login-container">
            <h1>Login</h1>
            {error && <div className="error-message">{error}</div>}
            <Form method="login" onSuccess={handleLogin} />
        </div>
    );
}

export default Login;
