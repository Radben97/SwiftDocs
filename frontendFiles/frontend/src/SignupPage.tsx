import { useEffect,useState } from "react";
export interface signupPageToggle {
  setSignupPageOpen: React.Dispatch<React.SetStateAction<boolean>>
  setSignupWelcome: React.Dispatch<React.SetStateAction<boolean>>
  setErrorPage: React.Dispatch<React.SetStateAction<boolean>>
}

 interface formDataStruct {
    Firstname: string
    Lastname: string
    Org_name: string
    Email_id: string
    Password: string
} 

const SignupPage = ({ setSignupPageOpen,setSignupWelcome,setErrorPage }: signupPageToggle) => {
  const [formData, setFormData] = useState({
    Firstname: "",
    Lastname: "",
    Org_name: "",
    Email_id: "",
    Password: ""
  } as formDataStruct)
  const passwordErr = "your password must contain at least one uppercase letter, one numerical digit, and one special character (such as @, #, $, or !)"
  const confPasswordErr = "Password doesn't match"
  const orgExistErr = "The organisation already exists"

  function passwordValidation(pwd: string | null): boolean {
        if (!pwd) {return false}
        const regex: RegExp = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};':"\\|,.<>\/?]).{8,}$/;
        return regex.test(pwd)
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement, HTMLInputElement>) {
    const e = event?.target as HTMLInputElement
    const name: string = e.name
    const value: string = e.value
    setFormData({...formData,[name] : value})
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    let closeTabFlag: boolean = false
    try {
      setFormData({ ...formData, Password: password })
      const response = await fetch("http://localhost:8000/signup/org", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });
      if (response.status == 400 || response.status == 422) {
        setOrgExists(true)
      } else {
        closeTabFlag = true
        setSignupWelcome(true)
      }

    }
    catch (error) {
      setSignupPageOpen(false)
      setErrorPage(true)
    }
    finally {
      if (closeTabFlag) {
        setSignupPageOpen(false)
      }
    }
  }
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [passErr, setPassErr] = useState(false)
  const [confPassErr, setConfPassErr] = useState(false)
  const [orgExists, setOrgExists] = useState(false)

  useEffect(() => {
    setPassErr(password.length > 0 && !passwordValidation(password))
    setConfPassErr(
      confirmPassword.length > 0 && password.length > 0 && password !== confirmPassword
    )
  }, [password, confirmPassword])
  return (
    <div className="LoginModal">
          <div className="LoginCard">
            <h1>Signup Page</h1>
              <form onSubmit={handleSubmit}>
                <label htmlFor="Firstname">Firstname:</label>
                <input type="text" id="Firstname" name="Firstname" placeholder="Enter Firstname " required  value={formData.Firstname} onChange={handleChange}/>
                <label htmlFor="Lastname">Lastname:</label>
                <input type="text" id="Lastname" name="Lastname" placeholder="Enter Lastname " required  value={formData.Lastname} onChange={handleChange}/>
                <label htmlFor="Org_name">Org_name:</label>
                <input type="text" id="Org_name" name="Org_name" placeholder="Enter org name " required value={formData.Org_name} onChange={handleChange} />
                <label htmlFor="Email_id" >Email_id:</label>
                <input type="text" id="Email_id" name="Email_id" placeholder="Enter email id" required value={formData.Email_id} onChange={handleChange} />
                <label htmlFor="Password">Password</label>
                  <input
                    type="password"
                    id="Password"
                    minLength={8}
                    required
                    placeholder="Enter password "
                    value={password}
            onChange={(e) => {
                    setPassword(e.target.value)
                    handleChange  
                     }}
                  />
                <p id="passPara" style={{"paddingBottom":"10px"}}>{passErr ? passwordErr : ""}</p>
                <label htmlFor="ConfirmPassword">Confirm password</label>
                <input
                  type="password"
                  id="ConfirmPassword"
                  minLength={6}
                  placeholder="Enter password again "
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value)
             }}
                />
          <p id="confPassPara">{confPassErr ? confPasswordErr : ""}</p>
          <p id="OrgCheck">{orgExists ? orgExistErr: ""}</p>
          <button type="submit" disabled={(passErr || confPassErr)}>Submit</button>
                <button onClick={() => setSignupPageOpen(false)}>Close</button>  
                </form>
            </div>
        </div>
  )
}

export default SignupPage