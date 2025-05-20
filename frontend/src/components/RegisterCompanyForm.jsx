import React, { useState } from "react";
import axios from "axios";

function RegisterCompanyForm() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    company_name: "",
    company_id: ""
  });
  const [message, setMessage] = useState({ text: "", type: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: "", type: "" });

    try {
      const response = await axios.post(
        "http://localhost:8000/api/register-company/",
        formData,
        { withCredentials: true }
      );
      setMessage({ text: response.data.message, type: "success" });
      setFormData({
        username: "",
        password: "",
        company_name: "",
        company_id: ""
      });
    } catch (error) {
      const err = error.response?.data;
      const msg =
        typeof err === "object"
          ? Object.entries(err).map(([k, v]) => `${k}: ${v}`).join("\n")
          : "Registration failed.";
      setMessage({ text: msg, type: "error" });
    }
  };

  return (
    <div>
      <h2>Register New Company</h2>
      {message.text && (
        <div
          style={{
            padding: "1rem",
            backgroundColor: message.type === "success" ? "#d4edda" : "#f8d7da",
            color: message.type === "success" ? "#155724" : "#721c24",
            marginBottom: "1rem"
          }}
        >
          {message.text}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        {["username", "password", "company_name", "company_id"].map((field) => (
          <div key={field}>
            <label>{field.replace("_", " ").toUpperCase()}:</label>
            <input
              type={field === "password" ? "password" : "text"}
              name={field}
              value={formData[field]}
              onChange={handleChange}
              required
            />
          </div>
        ))}
        <button type="submit">Register Company</button>
      </form>
    </div>
  );
}

export default RegisterCompanyForm;
