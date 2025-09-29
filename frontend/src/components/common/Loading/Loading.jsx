import React from "react";

const Loading = () => {
  return (
    <div style={styles.container}>
      <div style={styles.spinner}></div>
      <p style={styles.text}>Loading...</p>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    background: "#f9f9f9",
  },
  spinner: {
    border: "6px solid #f3f3f3",      // light gray
    borderTop: "6px solid #3498db",   // blue
    borderRadius: "50%",
    width: "50px",
    height: "50px",
    animation: "spin 1s linear infinite",
  },
  text: {
    marginTop: "15px",
    fontSize: "16px",
    color: "#333",
    fontFamily: "Arial, sans-serif",
  },
};

// Add CSS keyframes manually (inline keyframes don’t work in React)
const styleSheet = document.styleSheets[0];
const keyframes =
  `@keyframes spin {
     0% { transform: rotate(0deg); }
     100% { transform: rotate(360deg); }
   }`;
styleSheet.insertRule(keyframes, styleSheet.cssRules.length);

export default Loading;
