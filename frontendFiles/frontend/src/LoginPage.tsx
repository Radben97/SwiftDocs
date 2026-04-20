import type { homePageProp } from "./Homepage"
import { useState } from "react"
const LoginPage = ({ setLoginPageOpen }: homePageProp) => {
  async function handleLoginSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    try {
      const refreshResponse = await fetch("http://localhost:8000/refresh", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({})
      })
      console.log(refreshResponse)
      if (refreshResponse.status == 200) {
        console.log("Login successfull")
      }
      else if (refreshResponse.status == 403) {
        const loginResponse = await fetch("http://localhost:8000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(loginFormData)
        })
        console.log(refreshResponse)
        if (loginResponse.status == 200) {
          console.log("logged in succesfully")
        }

      }
      else {
        setAuthNotExists(true)
      }
    }
    catch (err) {
      console.log(err)
    }
  }
  function handleChange(event: React.ChangeEvent<HTMLInputElement, HTMLInputElement>) {
    const e = event?.target as HTMLInputElement
    const name: string = e.name
    const value: string = e.value
    setLoginFormData({...loginFormData,[name] : value})
  }
  const authErr = "Email id or Password is incorrect"
  const [authNotExists,setAuthNotExists] = useState(false)
  const [loginFormData, setLoginFormData] = useState({
    org_name: "",
    email_id: "",
    password: ""
  })
  return (
    <div className="LoginModal">
          <div className="LoginCard">
            <h1>Login Page</h1>
            <form onSubmit={handleLoginSubmit}>
                <label htmlFor="Email_id">Email_id:</label>
                <input type="text" id="Email_id" name="email_id" placeholder="Enter email id" value={loginFormData.email_id} onChange={handleChange} />
                <label htmlFor="Org_name">Org_name:</label>
          <input type="text" id="Org_name" name="org_name" placeholder="Enter Org. name:" value={loginFormData.org_name} onChange={handleChange} />
                <label htmlFor="Password">Password</label>
                <input type="password" id="Password" name="password" minLength={6} placeholder="Enter password: " value={loginFormData.password} onChange={handleChange} />
          <p id="authChecker">{authNotExists ? authErr : ""}</p>
                <button type="submit">Submit</button>
                <button onClick={() => setLoginPageOpen(false)}>Close</button>  
                </form>
            </div>
        </div>
  )
}

export default LoginPage