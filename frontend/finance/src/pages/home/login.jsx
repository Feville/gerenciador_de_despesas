import { useState } from "react";
import { FaUser, FaRegAddressCard } from "react-icons/fa";
import axios from "axios";
import { API_BASE_URL } from "../../api/api";

const Login = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post(`${API_BASE_URL}/register`, { username, email });
      console.log("Resposta do servidor:", response.data);
    } catch (error) {
      console.error("Erro ao enviar dados:", error);
    }
  };

  return (
    <div className='container'>
      <form onSubmit={handleSubmit}>
        <h1>Login</h1>

        <div className="form">
          <FaUser className="icon"/>
          <input
            type="text"
            placeholder='Nome de usuário'
            id='txtBar'
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="form">
          <FaRegAddressCard className="icon"/>
          <input
            type="email"
            placeholder='Email'
            id='txtBar'
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="recall_forget">
          <label htmlFor="">
            <input type="checkbox" /> Remember me?
            <a href="#"> Register </a>
          </label>
        </div>

        <button type="submit">Entrar</button>
      </form>
    </div>
  );
};

export default Login;
