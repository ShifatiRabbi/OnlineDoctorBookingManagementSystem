"use client";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function TestApi() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    console.log("👉 Calling API:", "http://localhost:8000/api/v1/accounts/test/");
    
    api.get("/accounts/test/")
        .then((res) => {
        console.log("✅ API Response:", res.data);
        setMessage(res.data.message || JSON.stringify(res.data));
        })
        .catch((err) => {
        console.error("❌ API Error:", err);
        setMessage("Error: " + (err.response?.data?.detail || err.message));
        });
    }, []);

  return <div>Hello - {message}</div>;
}
