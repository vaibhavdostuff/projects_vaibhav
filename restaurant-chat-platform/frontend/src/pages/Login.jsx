import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { signInWithGoogle } from "../services/auth";

function Login() {
  const { user } = useContext(AuthContext);

  if (user) {
    return <h2>Logged in as {user.displayName}</h2>;
  }

  return (
    
    <div>
      <h1>Restaurant Chat</h1>
      <button onClick={signInWithGoogle}>Sign in with Google</button>
    </div>
  );
  
}

export default Login;

