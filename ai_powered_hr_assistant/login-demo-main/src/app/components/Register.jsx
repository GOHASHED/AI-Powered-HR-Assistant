'use client';

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "",
    hr_profile: {
      Name: "",
      OrganizationName: "",
    },
    employee_profile: {
      Department: "",
      Position: "",
      OrganizationName: "",
    },
    candidate_profile: {
      uploadCV: null,
      Name: "",
    },
  });

  const [error, setError] = useState("");
  const router = useRouter();

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value, type, files } = e.target;

    if (name.startsWith("hr_")) {
      const field = name.split("hr_")[1];
      setFormData((prev) => ({
        ...prev,
        hr_profile: { ...prev.hr_profile, [field]: value },
      }));
    } else if (name.startsWith("employee_")) {
      const field = name.split("employee_")[1];
      setFormData((prev) => ({
        ...prev,
        employee_profile: { ...prev.employee_profile, [field]: value },
      }));
    } else if (name.startsWith("candidate_")) {
      const field = name.split("candidate_")[1];
      setFormData((prev) => ({
        ...prev,
        candidate_profile: { ...prev.candidate_profile, [field]: type === "file" ? files[0] : value },
      }));
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
    setError(""); // Clear error message on input
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    const payload = {
      username: "testuser", // Replace with actual form values
      email: "testuser@example.com",
      password: "password",
      role: "candidate",
    };
  
    console.log("Payload being sent:", payload);
  
    try {
      const response = axios.post("http://127.0.0.1:8000/register/", payload, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log("API Response:", response.data);
    } catch (error) {
      if (error.response) {
        console.error("API Error Response:", error.response.data);
        console.error("Status Code:", error.response.status);
      } else if (error.request) {
        console.error("No Response Received:", error.request);
      } else {
        console.error("Error during setup:", error.message);
      }
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-6">Registration Page</h1>
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded shadow-md w-96"
      >
        {error && <p className="text-red-500 mb-4">{error}</p>}

        <div className="mb-4">
          <label className="block text-sm font-medium">User Name</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
            className="w-full mt-1 p-2 border rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full mt-1 p-2 border rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full mt-1 p-2 border rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Confirm Password</label>
          <input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
            className="w-full mt-1 p-2 border rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Role</label>
          <div className="mt-2">
            <label className="inline-flex items-center">
              <input
                type="radio"
                name="role"
                value="hr"
                onChange={handleChange}
                checked={formData.role === "hr"}
                className="mr-2"
              />
              HR
            </label>
            <label className="inline-flex items-center ml-4">
              <input
                type="radio"
                name="role"
                value="employee"
                onChange={handleChange}
                checked={formData.role === "employee"}
                className="mr-2"
              />
              Employee
            </label>
            <label className="inline-flex items-center ml-4">
              <input
                type="radio"
                name="role"
                value="candidate"
                onChange={handleChange}
                checked={formData.role === "candidate"}
                className="mr-2"
              />
              Candidate
            </label>
          </div>
        </div>

        {/* Conditional Role Fields */}
        {formData.role === "hr" && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium">Name</label>
              <input
                type="text"
                name="hr_Name"
                value={formData.hr_profile.Name}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium">Organization Name</label>
              <input
                type="text"
                name="hr_OrganizationName"
                value={formData.hr_profile.OrganizationName}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
          </>
        )}

        {formData.role === "employee" && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium">Department</label>
              <input
                type="text"
                name="employee_Department"
                value={formData.employee_profile.Department}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium">Position</label>
              <input
                type="text"
                name="employee_Position"
                value={formData.employee_profile.Position}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium">Organization Name</label>
              <input
                type="text"
                name="employee_OrganizationName"
                value={formData.employee_profile.OrganizationName}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
          </>
        )}

        {formData.role === "candidate" && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium">Upload CV</label>
              <input
                type="file"
                name="candidate_uploadCV"
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium">Name</label>
              <input
                type="text"
                name="candidate_Name"
                value={formData.candidate_profile.Name}
                onChange={handleChange}
                required
                className="w-full mt-1 p-2 border rounded"
              />
            </div>
          </>
        )}

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Register
        </button>
      </form>
    </div>
  );
}

