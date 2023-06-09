// Navbar.js or Navbar.tsx
import { AuthContext } from "../contexts/AuthContext";
import { useContext } from "react";
import React from "react";
import { Link } from "react-router-dom";
import "./style.css"; // Import the Languages CSS file
import LoginComponent from "./LoginComponent";

function Navbar() {
  const {
    isAuthenticated,
    isLibrarian,
  }: { isAuthenticated: boolean; isLibrarian: boolean } =
    useContext(AuthContext);
  function loggedin() {
    return (
      <div style={{ flexDirection: "row", display: "flex" }}>
        {isAuthenticated ? (
          <li>
            <Link to="/update_profile">My Profile</Link>
          </li>
        ) : (
          <li style={{ justifyContent: "flex-end" }}>
            <Link to="/signup">Signup</Link>
          </li>
        )}
        {isLibrarian && (
          <li style={{ justifyContent: "flex-end" }}>
            <Link to="/librarian/signup">Librarian Signup</Link>
          </li>
        )}
        <li>
          <LoginComponent />
        </li>
      </div>
    );
  }

  return (
    <nav className="navbar">
      <ul style={{ justifyContent: "space-between" }}>
        <div style={{ flexDirection: "row", display: "flex" }}>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/authors">Authors</Link>
          </li>
          <li>
            <Link to="/books">Books</Link>
          </li>
          <li>
            <Link to="/genre">Genres</Link>
          </li>
          <li style={{ justifyContent: "flex-end" }}>
            <Link to="/Language">Languages</Link>
          </li>
          {isLibrarian && (
            <li style={{ justifyContent: "flex-end" }}>
              <Link to="/users">Users</Link>
            </li>
          )}
          {isAuthenticated && (
            <li>
              <Link to="/my_borrowed">My Borrowed</Link>
            </li>
          )}
        </div>

        {loggedin()}
      </ul>
    </nav>
  );
}

export default Navbar;
