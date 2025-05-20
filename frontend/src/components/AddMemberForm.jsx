import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AddMemberForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    mobile_no: "",
    dob: "",
    address: ""
  });
  const [message, setMessage] = useState({ text: "", type: "" });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

 const handleSubmit = async (e) => {
  e.preventDefault();
  setIsLoading(true);
  setMessage({ text: "", type: "" });
  
  try {
    const response = await axios.post(
      "http://localhost:8000/api/members/", 
      formData,
      {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': await getCsrfToken() // Add this if you're using CSRF
        }
      }
    );
    
    // Handle both possible success response structures
    const successMsg = response.data.message || "Member registered successfully!";
    
    setMessage({
      text: `${successMsg} Redirecting to login...`,
      type: "success"
    });

    // Reset form
    setFormData({
      username: "",
      password: "",
      email: "",
      mobile_no: "",
      dob: "",
      address: ""
    });

    // Redirect to login after 2 seconds
    setTimeout(() => navigate("/login"), 2000);
    
  } catch (error) {
    console.error("Registration error:", error);
    
    let errorMsg = "Failed to register member";
    if (error.response) {
      // Handle Django error responses
      if (error.response.data) {
        if (typeof error.response.data === 'object') {
          errorMsg = Object.entries(error.response.data)
            .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(' ') : value}`)
            .join('\n');
        } else {
          errorMsg = error.response.data;
        }
      }
    } else if (error.request) {
      errorMsg = "No response from server";
    }

    setMessage({
      text: errorMsg,
      type: "error"
    });
  } finally {
    setIsLoading(false);
  }
};

// Add this function if you need CSRF token
async function getCsrfToken() {
  const response = await axios.get('http://localhost:8000/api/csrf_token/');
  return response.data.csrfToken;
}

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Register New Company Member</h2>
      
      {message.text && (
        <div style={{
          ...styles.message,
          backgroundColor: message.type === "success" ? "#d4edda" : "#f8d7da",
          color: message.type === "success" ? "#155724" : "#721c24"
        }}>
          {message.text}
        </div>
      )}
      
      <form onSubmit={handleSubmit} style={styles.form}>
        {["username", "password", "email", "mobile_no", "dob", "address"].map((field) => (
          <div key={field} style={styles.inputGroup}>
            <label style={styles.label}>
              {field.replace("_", " ").toUpperCase()}:
            </label>
            <input
              type={
                field === "dob" ? "date" : 
                field === "password" ? "password" : 
                field === "email" ? "email" : "text"
              }
              name={field}
              value={formData[field]}
              onChange={handleChange}
              required
              style={styles.input}
            />
          </div>
        ))}
        <button 
          type="submit" 
          style={styles.button}
          disabled={isLoading}
        >
          {isLoading ? "Registering..." : "Add Member"}
        </button>
      </form>
    </div>
  );
};

const styles = {
  container: { 
    maxWidth: "500px",
    margin: "2rem auto",
    padding: "2rem",
    backgroundColor: "#f8f9fa",
    borderRadius: "8px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
  },
  heading: { 
    textAlign: "center",
    color: "#2c3e50",
    marginBottom: "1.5rem"
  },
  form: { 
    display: "flex",
    flexDirection: "column",
    gap: "1rem"
  },
  inputGroup: { 
    marginBottom: "1rem" 
  },
  label: {
    display: "block",
    marginBottom: "0.5rem",
    fontWeight: "600",
    color: "#495057"
  },
  input: {
    width: "100%",
    padding: "0.75rem",
    borderRadius: "4px",
    border: "1px solid #ced4da",
    fontSize: "1rem"
  },
  button: { 
    backgroundColor: "#28a745",
    color: "white",
    padding: "0.75rem",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
    fontWeight: "600",
    marginTop: "1rem",
    transition: "background-color 0.2s",
    ":hover": {
      backgroundColor: "#218838"
    }
  },
  message: {
    padding: "1rem",
    borderRadius: "4px",
    marginBottom: "1rem",
    textAlign: "center"
  }
};

export default AddMemberForm;