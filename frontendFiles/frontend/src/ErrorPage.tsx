
type errorPageSetter = {
    setErrorPage: React.Dispatch<React.SetStateAction<boolean>>
}
const ErrorPage = ({setErrorPage}: errorPageSetter) => {
  return (
    <div className="ErrorModal">
      <div className="ErrorCard">

        <button className="CloseBtn" onClick={() => setErrorPage(false)}>×</button>

        <div className="ErrorIcon">!</div>

        <h1>Something went wrong</h1>

        <p>
          We couldn’t complete your request at the moment. Please try again.
        </p>

        <div className="ErrorActions">
          <button className="SecondaryBtn" onClick={() => setErrorPage(false)}>Go to Home</button>
        </div>

      </div>
    </div>
  )
}

export default ErrorPage