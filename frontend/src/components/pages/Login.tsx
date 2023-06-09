import React, { useState, useContext, useEffect } from "react";
import { client } from "../../axios";
import { useHistory } from "react-router-dom";
import jwt_decode from "jwt-decode";
import { AuthContext, DecodedToken } from "../../contexts/AuthContext";

function Login() {
  /**
   * When the users credentials are authenticated, the refresh token and access token are stored in localstorage.
   * The details of the user are stored in state with the help of the useContext hook
   */
  const { LoginFunction }: { LoginFunction: (arg0: DecodedToken) => void } =
    useContext(AuthContext);
  const { LogoutFunction }: { LogoutFunction: () => void } =
    useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } =
    useContext(AuthContext);

  const history = useHistory();
  const [userName, setUserName]: [
    string,
    React.Dispatch<React.SetStateAction<string>>
  ] = useState("");
  const [password, setPassword]: [
    string,
    React.Dispatch<React.SetStateAction<string>>
  ] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (isAuthenticated) {
      LogoutFunction();
    }
    //The comment below disables the warning that is generated for not including isAuthenticated and LogoutFunction()
    //in the parameter list

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data: FormData = new FormData();
    data.append("username", userName);
    data.append("password", password);
    client
      .Login(data)
      .then((Token) => {
        const decoded_token: DecodedToken = jwt_decode(Token.access_token);
        //passing the decoded access token to the AuthContext to get the state variables needed to render for the
        //current user
        console.log(decoded_token);
        LoginFunction(decoded_token);
        history.push("/");
      })
      .catch((error) => {
        // Handle error and show an error message
        console.log(error.response);
        if (error.response.status === 422) {
          const errorMessage = error.response.data.detail[0].msg;
          // Show the error message to the user (e.g., set it to a state variable to display in the UI)
          setError(errorMessage);
        } else {
          const errorMessage = error.response.data.detail;
          // Show the error message to the user (e.g., set it to a state variable to display in the UI)
          setError(errorMessage);
        }
      });
  }

  return (
    <div className="background-image">
      <div className="signup-container">
        <form className="signup-form" onSubmit={handleSubmit}>
          <h1>Login</h1>
          <label className="form-group">
            User Name
            <input
              className="form-group"
              type="text"
              value={userName}
              placeholder="Username"
              onChange={(e) => setUserName(e.target.value.trim())}
            />
          </label>
          <br />
          <label className="form-group">
            Password
            <input
              className="form-group"
              type="password"
              value={password}
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <br />
          <div className="error-message">{error}</div>
          <div className="form-group">
            <button>Login</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
