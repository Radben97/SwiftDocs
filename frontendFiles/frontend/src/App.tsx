import Homepage from './Homepage'
import './App.css'
import { useState } from 'react'
import LoginPage from './LoginPage'
import SignupPage from './SignupPage'
import SignupWelcome from './SignupWelcome'
import ErrorPage from './ErrorPage'

function App() {
  const [loginPageOpen,setLoginPageOpen] = useState(false)
  const [SignupPageOpen, setSignupPageOpen] = useState(false)
  const [signupWelcome, setSignupWelcome] = useState(false)
  const [errorPage,setErrorPage] = useState(false)
  return (
    <>
      <Homepage setLoginPageOpen={setLoginPageOpen} setSignupPageOpen={setSignupPageOpen} />
      {loginPageOpen && <LoginPage setLoginPageOpen={setLoginPageOpen} />}
      {SignupPageOpen && <SignupPage setSignupPageOpen={setSignupPageOpen} setSignupWelcome={setSignupWelcome} setErrorPage={setErrorPage} />}
      {signupWelcome && <SignupWelcome setSignupWelcome={setSignupWelcome} setLoginPageOpen={setLoginPageOpen} />}
      {errorPage && <ErrorPage setErrorPage={setErrorPage} /> }
    </>
  )
}

export default App
