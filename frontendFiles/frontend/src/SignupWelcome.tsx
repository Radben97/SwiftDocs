type signupProps = {
    setSignupWelcome: React.Dispatch<React.SetStateAction<boolean>>
    setLoginPageOpen: React.Dispatch<React.SetStateAction<boolean>>
}
const SignupWelcome = ({setSignupWelcome,setLoginPageOpen}: signupProps) => {
  return (
    <div className="WelcomeModal">
      <div className="WelcomeCard">

        <button className="CloseBtn" onClick={() => setSignupWelcome(false)}>×</button>

        <div className="WelcomeIcon">✓</div>

        <h1>Registration Successful</h1>

        <p>
          Your account has been created successfully. Please log in to continue.
        </p>

              <button className="PrimaryBtn" onClick={() => {
                  setSignupWelcome(false)
                  setTimeout(() => {
                    setLoginPageOpen(true)
                  }, 500);
        }}>Go to Login</button>

      </div>
    </div>
  )
}

export default SignupWelcome