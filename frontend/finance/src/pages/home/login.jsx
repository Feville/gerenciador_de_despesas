import { useState } from "react"
import { FaUser, FaRegAddressCard } from "react-icons/fa"
import "./login.css"

const Login = () => {
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  
  const handleSubmit = (event) => {
    event.preventDefault()

    console.log("Envio", username, email)
  }
  
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
          <FaRegAddressCard className = "icon"/>
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
            <a href="#"> Resgister </a>
          </label>
        </div>

        <button>Entrar</button>

        </form>
    
    </div>
  )
}

export default Login
