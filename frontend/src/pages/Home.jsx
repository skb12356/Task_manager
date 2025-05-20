import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
    const [userDetails, setUserDetails] = useState({});
    const [members, setMembers] = useState([]);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProtectedData = async () => {
            try {
                // Fetch authenticated user details
                const res = await fetch("http://localhost:8000/api/protected/", {
                    credentials: "include", // Send cookies
                });

                if (res.ok) {
                    const data = await res.json();
                    setUserDetails(data);
                } else {
                    throw new Error("Unauthorized");
                }
            } catch (err) {
                setError("You must be logged in as a member to view this page.");
                setTimeout(() => navigate("/login"), 2000);
            }
        };

        const fetchMembers = async () => {
            try {
                const res = await fetch("http://localhost:8000/members/", {
                    credentials: "include",
                });

                if (res.ok) {
                    const data = await res.json();
                    setMembers(data);
                }
            } catch (err) {
                console.error("Error fetching members:", err);
            }
        };

        fetchProtectedData();
        fetchMembers();
    }, [navigate]);

    if (error) return <div className="error-message">{error}</div>;

    return (
        <div className="home-container">
            <div className="sidebar">
                <h2>Cubical</h2>
                <button className="new-project">+ New Project</button>
                <div className="project-list">
                    <div className="project">1️⃣ My First Project</div>
                    <div className="project">2️⃣ My Second Project</div>
                </div>
            </div>

            <div className="main">
                <h2>My First Project</h2>
                <div className="project-body">
                    <div className="warehouse">
                        <div className="warehouse-header">
                            <span>Warehouse</span>
                            <button className="add-file">+</button>
                        </div>
                        <ul className="file-list">
                            <li>Floor plan.csv</li>
                            <li>Random notes.txt</li>
                            <li>Top view.png</li>
                        </ul>
                    </div>

                    <div className="updates">
                        <div className="update-message">
                            <strong>{userDetails.username || "Loading..."}:</strong> Hello everyone...
                        </div>
                        <div className="update-message">
                            <strong>{userDetails.username || "Loading..."}:</strong> Let's collaborate well!
                        </div>
                        <div className="update-input">
                            <input placeholder="What's your update?..." />
                        </div>
                    </div>

                    <div className="user-details">
                        <h3>Your Details</h3>
                        <label>User ID:</label>
                        <input value={userDetails.id || ""} readOnly />
                        <label>Name:</label>
                        <input value={userDetails.username || ""} readOnly />
                        <label>DOB:</label>
                        <input value={userDetails.dob || ""} readOnly />
                        <label>Email:</label>
                        <input value={userDetails.email || ""} readOnly />
                        <label>Mobile:</label>
                        <input value={userDetails.mobile_no || ""} readOnly />
                        <button className="add-member">+ Add Member</button>

                        <div className="member-list">
                            {members.map((member, index) => (
                                <div className="member" key={index}>
                                    <span>{member.user.username[0]}</span>
                                    {member.user.username} <br />
                                    <small>{member.user.email}</small>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;
